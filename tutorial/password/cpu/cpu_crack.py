import itertools
import os
import pyzipper
from tqdm import tqdm


def format_number(num):
    """将数字格式化为带单位的字符串（K, M, B）"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)


def crack_zip_optimized(zip_path, charset, min_len=1, max_len=4):
    """
    暴力破解ZIP压缩包的密码（支持 ZipCrypto 和 AES 加密，附进度条）

    :param zip_path: ZIP文件路径（字符串）
    :param charset: 密码可能包含的字符集（字符串），例如 '0123456789'
    :param min_len: 密码最小长度（整数），默认1
    :param max_len: 密码最大长度（整数），默认4
    :return: 成功时返回密码字符串，失败时返回 None
    """
    # 检查文件是否存在
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP文件不存在: {zip_path}")

    # 使用 pyzipper 打开（同时支持传统加密和 AES）
    with pyzipper.AESZipFile(zip_path) as zf:
        # 检查ZIP是否加密
        # 注意：pyzipper 没有直接提供 flag_bits，但可以通过 infolist 的 flag_bits 属性判断
        if not any(f.flag_bits & 0x1 for f in zf.infolist()):
            print("ZIP文件未加密，无需破解")
            return ''

        # 选择第一个文件作为测试目标（通常较小，提高速度）
        test_file = zf.infolist()[0]

        # 计算总尝试次数（从 min_len 到 max_len）
        total = sum(len(charset) ** l for l in range(min_len, max_len + 1))
        # ✅ 修改点：使用自适应单位输出总尝试次数
        print(f"总尝试次数: {format_number(total)}")

        with tqdm(total=total, unit="pwd", desc="暴力破解") as pbar:
            try:
                # 外层循环：从 min_len 到 max_len
                for length in range(min_len, max_len + 1):
                    # 内层循环：生成长度为 length 的所有组合
                    for combo in itertools.product(charset, repeat=length):
                        pwd = ''.join(combo)
                        try:
                            # 尝试读取文件，密码需转为字节串
                            zf.read(test_file, pwd=pwd.encode())
                            print(f"\n✅ 成功！密码是：{pwd}")
                            return pwd
                        except RuntimeError:
                            # 密码错误（pyzipper 和 zipfile 都抛出 RuntimeError）
                            pbar.update(1)
                        except Exception as e:
                            # 其他异常（如文件损坏、不支持的加密类型等）
                            pbar.update(1)
                            print(f"\n⚠️ 错误: {e}")
            except KeyboardInterrupt:
                print("\n⚠️ 用户中断，已停止破解")
                return None

        print("\n❌ 未找到密码，请尝试更大的max_len或更丰富的charset")
        return None


if __name__ == '__main__':
    # 示例1：密码长度在 1~4 位纯数字（你的密码 9347 位于此范围）
    # pwd = crack_zip_optimized('9347.zip', charset='0123456789', min_len=1, max_len=4)

    # 示例2：密码长度在 1~6 位纯数字（你的密码 136758 位于此范围）
    # pwd = crack_zip_optimized('../136758.zip', charset='0123456789', min_len=1, max_len=6)
    # if pwd is not None:
    #     print(f"找到密码: {pwd}")

    # 示例3：密码长度在 1~6 位 数字+小写字母组合

    # 总尝试次数: 2.2B，大约花费500小时时间。 字符集包含 95 个字符
    pwd = crack_zip_optimized('../es68z4.zip', charset='0123456789abcdefghijklmnopqrstuvwxyz', min_len=6, max_len=6)
    if pwd is not None:
        print(f"找到密码: {pwd}")

    # 示例2：密码长度在 3~6 位小写字母
    # pwd = crack_zip_optimized('secret.zip', charset='abcdefghijklmnopqrstuvwxyz', min_len=3, max_len=6)