import itertools
import os
import pyzipper
from tqdm import tqdm
from multiprocessing import Pool, cpu_count, Manager
from functools import partial
import time

def check_password(pwd, zip_path, test_file_name):
    try:
        with pyzipper.AESZipFile(zip_path) as zf:
            zf.read(test_file_name, pwd=pwd.encode())
        return True
    except:
        return False

def worker(passwords_generator, zip_path, test_file_name, progress_queue, result_queue, chunk_size=10000):
    """处理一批密码，找到后通知主进程"""
    batch = []
    for pwd in passwords_generator:
        batch.append(pwd)
        if len(batch) >= chunk_size:
            for candidate in batch:
                if check_password(candidate, zip_path, test_file_name):
                    result_queue.put(candidate)
                    return
            progress_queue.put(len(batch))
            batch = []
    # 处理最后不足一批的
    for candidate in batch:
        if check_password(candidate, zip_path, test_file_name):
            result_queue.put(candidate)
            return
    progress_queue.put(len(batch))

def generate_passwords(charset, min_len, max_len, must_include_set):
    """生成器：按长度顺序产生所有密码（满足必须包含条件）"""
    for length in range(min_len, max_len + 1):
        for combo in itertools.product(charset, repeat=length):
            pwd = ''.join(combo)
            if must_include_set and not any(ch in pwd for ch in must_include_set):
                continue
            yield pwd

def crack_zip_parallel_generator(zip_path, charset, min_len, max_len,
                                 must_include=None, exclude=None, workers=None):
    if not os.path.exists(zip_path):
        raise FileNotFoundError(zip_path)
    if exclude:
        final_charset = ''.join(c for c in charset if c not in exclude)
    else:
        final_charset = charset
    if not final_charset:
        raise ValueError("字符集为空")
    must_set = set(must_include or '')
    if not must_set.issubset(final_charset):
        raise ValueError("必须字符不在字符集中")

    total = sum(len(final_charset) ** l for l in range(min_len, max_len + 1))
    print(f"总尝试次数: {total:,}")

    with pyzipper.AESZipFile(zip_path) as zf:
        test_file = zf.infolist()[0].filename

    if workers is None:
        workers = cpu_count()
    print(f"使用 {workers} 个进程并行破解")

    # 将生成器拆分为多个独立的生成器（每个进程从头开始，会造成重复尝试）
    # 更好的方法是使用队列分发密码，但这里简化：每个进程独立生成所有密码，导致重复劳动。
    # 为了真正并行且不重复，我们需要一个任务分配器。这里提供一个基于索引分块的方案：

    # 计算总组合数，每个进程负责一段索引范围
    # 由于组合数巨大，动态映射索引到具体密码较为复杂，建议使用简单分块：每个进程独立生成所有密码并检查，会有重复，但可以设置全局共享标志提前终止。
    # 更优方案：使用 multiprocessing.Manager 的队列，主进程负责生成密码并分发到工作队列。这样可以避免重复。
    # 但生成器速度很快，瓶颈在解密，重复工作可以接受。为了简洁，此处提供基于队列的分发方式。

    manager = Manager()
    task_queue = manager.Queue(maxsize=10000)
    result_queue = manager.Queue()
    stop_flag = manager.Value('b', False)

    def producer():
        """主进程生产密码放入队列"""
        for pwd in generate_passwords(final_charset, min_len, max_len, must_set):
            if stop_flag.value:
                break
            task_queue.put(pwd)
        for _ in range(workers):
            task_queue.put(None)  # 结束信号

    def consumer(worker_id):
        """工作进程消费密码并测试"""
        while not stop_flag.value:
            pwd = task_queue.get()
            if pwd is None:
                break
            if check_password(pwd, zip_path, test_file):
                result_queue.put(pwd)
                stop_flag.value = True
                break

    # 启动生产者线程（主进程内）
    import threading
    prod_thread = threading.Thread(target=producer)
    prod_thread.start()

    # 启动工作进程
    pool = Pool(workers)
    pool.map_async(consumer, range(workers))
    pool.close()

    # 进度监控
    pbar = tqdm(total=total, unit="pwd", unit_scale=True, desc="暴力破解")
    found = None
    while pbar.n < total and not stop_flag.value:
        try:
            # 等待结果或超时
            if not result_queue.empty():
                found = result_queue.get_nowait()
                break
            # 模拟进度更新（实际进度无法精确获取，因为不知道已经处理了多少）
            # 这里简单增加一个计数，不精确
            pbar.update(1000)
            time.sleep(0.1)
        except:
            pass
    pbar.close()
    stop_flag.value = True
    pool.terminate()
    pool.join()
    prod_thread.join()

    if found:
        print(f"\n✅ 成功！密码是：{found}")
        return found
    else:
        print("\n❌ 未找到密码")
        return None

if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    crack_zip_parallel_generator(
        zip_path='../es68z4.zip',
        charset='0123456789abcdefghijklmnopqrstuvwxyz',
        min_len=6, max_len=6,
        must_include='e6',
        exclude='01lLpt',
        workers=8
    )