import subprocess
import os
import re
import sys
import tempfile
import threading
import time
from typing import Optional
from tqdm import tqdm

# ==================== 配置区域（请根据实际路径修改） ====================
CONFIG = {
    "hashcat_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\hashcat-6.2.6\hashcat.exe",
    "zip2john_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\john-1.9.0-jumbo-1-win64\run\zip2john.exe",
    "gpu_ids": None,
    "optimize": True,
    "workload": 3,
    "extra_args": ["--force"],
    "fallback_to_cpu": False,
}
# =====================================================

def format_number(n: int) -> str:
    if n < 1_000:
        return str(n)
    if n < 1_000_000:
        return f"{n/1_000:.2f}K"
    if n < 1_000_000_000:
        return f"{n/1_000_000:.2f}M"
    if n < 1_000_000_000_000:
        return f"{n/1_000_000_000:.2f}B"
    return f"{n/1_000_000_000_000:.2f}T"

def run_command(cmd, description="", cwd=None):
    print(f"[*] {description}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                encoding='utf-8', errors='replace',
                                timeout=3600, cwd=cwd)
        if result.returncode != 0:
            print(f"[!] 命令失败，返回码 {result.returncode}")
            if result.stderr:
                print(f"错误: {result.stderr[:500]}")
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        print(f"[!] 异常: {e}")
        return False, "", str(e)

def extract_clean_hash(zip_path: str) -> Optional[str]:
    if not os.path.exists(CONFIG["zip2john_path"]):
        print("[!] zip2john 不存在")
        return None
    cmd = [CONFIG["zip2john_path"], zip_path]
    ok, stdout, stderr = run_command(cmd, "提取ZIP哈希")
    if not ok or not stdout:
        return None

    pattern = r'(\$zip2\$[^\$]+\$/zip2\$|\$pkzip\$[^\$]+\$/pkzip\$)'
    for line in stdout.splitlines():
        match = re.search(pattern, line)
        if match:
            raw = match.group(1)
            if ':' in raw:
                raw = raw.split(':', 1)[0]
            clean = raw.strip()
            hash_file = os.path.join(os.path.dirname(zip_path), "zip_hash_clean.txt")
            with open(hash_file, 'w', encoding='ascii') as f:
                f.write(clean + '\n')
            print(f"[+] 清理后的哈希已保存到 {hash_file}")
            return hash_file
    print("[!] 未能提取哈希")
    return None

def read_password_from_potfile(hash_file: str) -> Optional[str]:
    potfile_path = os.path.join(os.path.dirname(CONFIG["hashcat_path"]), "hashcat.potfile")
    if not os.path.exists(potfile_path):
        return None

    with open(hash_file, 'r', encoding='ascii') as f:
        target_hash = f.read().strip()
    print(f"[DEBUG] 在 potfile 中查找哈希: {target_hash}")

    with open(potfile_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if ':' not in line:
                continue
            h, pwd = line.split(':', 1)
            h = h.strip()
            pwd = pwd.strip()
            if h == target_hash:
                print(f"[DEBUG] 找到精确匹配: {pwd}")
                return pwd
    print("[DEBUG] 未找到精确匹配")
    return None

def test_hash_load(hash_file: str, mode: int) -> bool:
    cmd = [CONFIG["hashcat_path"], "-m", str(mode), hash_file, "--stdout", "--force"]
    ok, stdout, stderr = run_command(cmd, f"测试模式 {mode}", cwd=os.path.dirname(CONFIG["hashcat_path"]))
    if "No hashes loaded" in stderr or "No such file" in stderr:
        return False
    return ok and "No hashes" not in stderr and "No such file" not in stderr

def detect_working_mode(hash_file: str) -> Optional[int]:
    for mode in [13600, 17200, 17210, 17220, 17225]:
        print(f"[*] 尝试模式 {mode}...")
        if test_hash_load(hash_file, mode):
            print(f"[+] 模式 {mode} 可以加载哈希")
            return mode
    return None

def build_base_cmd(hash_file: str, mode: int, output_file: str) -> list:
    cmd = [CONFIG["hashcat_path"], "-m", str(mode), "-a", "3", hash_file,
           "-o", output_file, "--status", "--status-timer=1"]
    if CONFIG["gpu_ids"]:
        cmd.extend(["-d", CONFIG["gpu_ids"]])
    if CONFIG["optimize"]:
        cmd.append("-O")
    cmd.extend(["-w", str(CONFIG["workload"])])
    cmd.extend(CONFIG["extra_args"])
    if CONFIG["fallback_to_cpu"] and not CONFIG["gpu_ids"]:
        cmd.extend(["-D", "1"])
    return cmd

def run_hashcat_cmd(cmd, total: int, description: str, hash_file: str):
    """
    执行 hashcat 命令，实时解析进度并显示 tqdm 进度条。
    """
    print(f"[*] {description}: {' '.join(cmd)}")
    formatted_total = format_number(total)
    print(f"[*] 总尝试次数: {total:,} ({formatted_total})")
    if total > 50_000_000:
        print(f"[*] 尝试次数较多，请耐心等待...")

    # 删除旧的输出文件
    output_file = None
    for i, arg in enumerate(cmd):
        if arg == "-o" and i+1 < len(cmd):
            output_file = cmd[i+1]
            break
    if output_file and os.path.exists(output_file):
        os.remove(output_file)

    # 启动子进程
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=os.path.dirname(CONFIG["hashcat_path"]),
        bufsize=1,
        universal_newlines=True
    )

    # 准备进度条
    pbar = tqdm(total=total, unit='pwd', unit_scale=True, desc=description, dynamic_ncols=True)
    # 增强的正则表达式，匹配常见的进度格式
    progress_re = re.compile(r'Progress[:\s]*(\d+)/(\d+)\s+\((\d+\.?\d*)%\)', re.IGNORECASE)
    success_re = re.compile(r'^(\$pkzip\$[^:]+|\$zip2\$[^:]+):(.+)$')
    found_password = None
    stderr_lines = []
    last_progress_time = time.time()
    progress_received = False

    def read_stderr():
        nonlocal found_password, progress_received, last_progress_time
        for line in process.stderr:
            stderr_lines.append(line)
            # 实时打印 stderr（可选，便于调试）
            sys.stderr.write(f"[STDERR] {line}")
            sys.stderr.flush()
            # 检查是否已找到密码
            sm = success_re.match(line.strip())
            if sm:
                found_password = sm.group(2)
                break
            # 匹配进度
            match = progress_re.search(line)
            if match:
                current = int(match.group(1))
                total_attempts = int(match.group(2))
                # 更新 tqdm 的 total（以防万一）
                if pbar.total != total_attempts:
                    pbar.total = total_attempts
                pbar.n = current
                pbar.refresh()
                progress_received = True
                last_progress_time = time.time()
                # 可选：打印调试信息
                # print(f"\n[DEBUG] 进度更新: {current}/{total_attempts}")

    def read_stdout():
        for _ in process.stdout:
            pass

    t_err = threading.Thread(target=read_stderr)
    t_out = threading.Thread(target=read_stdout)
    t_err.daemon = True
    t_out.daemon = True
    t_err.start()
    t_out.start()

    # 监控进度更新，如果长时间无进展则输出诊断信息
    start_time = time.time()
    while process.poll() is None:
        time.sleep(1)
        if not progress_received and time.time() - start_time > 10:
            print("\n[!] 警告: 10秒内未收到任何进度更新，可能 Hashcat 启动失败或输出格式不匹配。")
            print("[!] 已捕获的 stderr 内容（最后10行）:")
            for line in stderr_lines[-10:]:
                print(f"    {line.rstrip()}")
            print("[!] 请检查上述输出，常见原因：设备不支持、权限问题、哈希格式错误。")
            # 可以选择终止进程，或者继续等待
            break
        if progress_received and time.time() - last_progress_time > 30:
            print("\n[!] 警告: 30秒内无进度更新，可能 Hashcat 卡住。")
            break

    returncode = process.wait()
    t_out.join(timeout=2)
    t_err.join(timeout=2)
    pbar.close()

    # 检查是否因为 potfile 中已有哈希而跳过
    stderr_text = ''.join(stderr_lines)
    if "All hashes found as potfile" in stderr_text:
        print("[*] 哈希已在 potfile 中，尝试读取密码...")
        pwd = read_password_from_potfile(hash_file)
        if pwd:
            print(f"\n[+] 从 potfile 中找到密码: {pwd}")
            return True, pwd
        else:
            print("[!] potfile 中存在该哈希？但读取失败")
            return False, None

    if returncode != 0:
        print(f"\n[!] Hashcat 进程异常退出，返回码: {returncode}")
        pwd = read_password_from_potfile(hash_file)
        if pwd:
            print(f"\n[+] 从 potfile 中找到密码: {pwd}")
            return True, pwd
        return False, None

    if found_password:
        print(f"\n[+] 破解成功！密码: {found_password}")
        return True, found_password

    # 从输出文件读取
    if output_file and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.read().strip().splitlines()
            for line in lines:
                if ':' in line:
                    pwd = line.split(':', 1)[1].strip()
                    if pwd:
                        print(f"\n[+] 破解成功！密码: {pwd}")
                        return True, pwd
            if lines:
                pwd = lines[-1].strip()
                if pwd:
                    print(f"\n[+] 破解成功！密码: {pwd}")
                    return True, pwd

    # 最后尝试 potfile
    pwd = read_password_from_potfile(hash_file)
    if pwd:
        print(f"\n[+] 从 potfile 中找到密码: {pwd}")
        return True, pwd

    print("[*] 未找到密码")
    return False, None

def run_hashcat_mask_with_charset(hash_file: str, charset: str, length: int, mode: int, output_file: str):
    total = len(charset) ** length
    cmd = build_base_cmd(hash_file, mode, output_file)
    cmd.extend(["-1", charset, "?1" * length])
    return run_hashcat_cmd(cmd, total, f"暴力 {length}位 ({len(charset)}字符)", hash_file)

def run_hashcat_multi_charset_mask(hash_file: str, must_set: str, other_set: str, length: int,
                                   mode: int, output_file: str, positions: list):
    mask_chars = ['?2'] * length
    for pos in positions:
        mask_chars[pos] = '?1'
    mask = ''.join(mask_chars)
    total = (len(must_set) ** len(positions)) * (len(other_set) ** (length - len(positions)))
    cmd = build_base_cmd(hash_file, mode, output_file)
    cmd.extend(["-1", must_set, "-2", other_set, mask])
    desc = f"必须包含 {len(positions)}个位置 (总组合 {total:.2e})"
    return run_hashcat_cmd(cmd, total, desc, hash_file)

def crack_zip_hashcat(zip_path: str, charset: str, min_len: int, max_len: int,
                      must_include: Optional[str] = None, exclude: Optional[str] = None) -> Optional[str]:
    if must_include is None:
        must_include = ''
    if exclude is None:
        exclude = ''

    print("\n[参数配置]")
    print(f"  ZIP文件: {zip_path}")
    print(f"  原始字符集 (charset): {charset} (长度 {len(charset)})")
    print(f"  必须包含字符 (must_include): {must_include if must_include else '(无)'}")
    print(f"  排除字符 (exclude): {exclude if exclude else '(无)'}")
    print(f"  密码长度范围: {min_len} ~ {max_len}")

    effective_charset = ''.join(ch for ch in charset if ch not in exclude)
    must_set = ''.join(ch for ch in must_include if ch in effective_charset)
    print(f"\n[最终字符集]")
    print(f"  有效字符集: {effective_charset} (长度 {len(effective_charset)})")
    if must_set:
        print(f"  必须包含字符集: {must_set} (长度 {len(must_set)})")
    else:
        print(f"  必须包含字符集: (无)")

    zip_path = os.path.abspath(zip_path)
    if not os.path.exists(zip_path):
        print(f"[!] ZIP 文件不存在: {zip_path}")
        return None

    print("\n[步骤1] 提取哈希")
    hash_file = extract_clean_hash(zip_path)
    if not hash_file:
        print("[!] 哈希提取失败")
        return None

    with open(hash_file, 'r') as f:
        hash_content = f.read().strip()
        print(f"[DEBUG] 哈希内容: {hash_content}")

    print("\n[步骤1.5] 检查 potfile 中是否已有密码")
    existing_pwd = read_password_from_potfile(hash_file)
    if existing_pwd:
        print(f"[+] 密码已存在于 potfile 中: {existing_pwd}")
        return existing_pwd

    print("\n[步骤2] 检测可用的 Hashcat 模式")
    working_mode = detect_working_mode(hash_file)
    if working_mode is None:
        print("[!] 无法加载哈希")
        return None
    print(f"[*] 使用模式 {working_mode}")

    if not effective_charset:
        print("[!] 有效字符集为空")
        return None
    if must_include and not must_set:
        print("[!] 必须包含的字符都不在有效字符集中，无法满足条件")
        return None

    base_dir = os.path.dirname(hash_file)
    test_file = os.path.join(base_dir, ".write_test")
    try:
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        output_dir = base_dir
    except PermissionError:
        print(f"[!] 目录 {base_dir} 不可写，将使用系统临时目录存放输出文件")
        output_dir = tempfile.gettempdir()

    for length in range(min_len, max_len + 1):
        print(f"\n========== 尝试长度 {length} ==========")
        output_file = os.path.join(output_dir, f"hashcat_out_{length}.txt")

        if not must_set:
            ok, pwd = run_hashcat_mask_with_charset(hash_file, effective_charset,
                                                    length, working_mode, output_file)
            if ok and pwd:
                return pwd
        else:
            total_subsets = (1 << length) - 1
            print(f"[*] 需要测试 {total_subsets} 种位置组合")
            for mask_bits in range(1, 1 << length):
                positions = [i for i in range(length) if (mask_bits >> i) & 1]
                ok, pwd = run_hashcat_multi_charset_mask(
                    hash_file, must_set, effective_charset, length,
                    working_mode, output_file, positions
                )
                if ok and pwd:
                    return pwd

    return None

if __name__ == '__main__':
    pwd = crack_zip_hashcat(
        zip_path='../6fvw42.zip',
        charset='0123456789abcdefghijklmnopqrstuvwxyz',
        min_len=6, max_len=6,
        must_include='', exclude=''
    )
    if pwd:
        print(f"找到密码: {pwd}")