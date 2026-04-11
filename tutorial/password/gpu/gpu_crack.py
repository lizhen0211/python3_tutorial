import subprocess
import os
import re
import threading
import string
from tqdm import tqdm
from typing import Optional

# ==================== 配置区域（请根据实际路径修改） ====================
CONFIG = {
    "hashcat_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\hashcat-6.2.6\hashcat.exe",
    "zip2john_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\john-1.9.0-jumbo-1-win64\run\zip2john.exe",
    "gpu_ids": None,           # 例如 "1,2" 或 None（使用默认设备）
    "optimize": True,          # -O 优化内核
    "workload": 3,             # -w 3 高负载
    "extra_args": ["--force"], # 额外参数
}
# =====================================================

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
    """使用 zip2john 提取哈希并清理为纯哈希格式，返回哈希文件路径"""
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
            # 保存到临时文件
            hash_file = os.path.join(os.path.dirname(zip_path), "zip_hash_clean.txt")
            with open(hash_file, 'w', encoding='ascii') as f:
                f.write(clean + '\n')
            print(f"[+] 清理后的哈希已保存到 {hash_file}")
            return hash_file
    print("[!] 未能提取哈希")
    return None

def test_hash_load(hash_file: str, mode: int) -> bool:
    """测试某个模式是否能加载哈希"""
    cmd = [CONFIG["hashcat_path"], "-m", str(mode), hash_file, "--stdout", "--force"]
    ok, stdout, stderr = run_command(cmd, f"测试模式 {mode}", cwd=os.path.dirname(CONFIG["hashcat_path"]))
    if "No hashes loaded" in stderr or "No such file" in stderr:
        return False
    return ok and "No hashes" not in stderr and "No such file" not in stderr

def detect_working_mode(hash_file: str) -> Optional[int]:
    """自动检测可用的 hashcat 模式"""
    for mode in [13600, 17200, 17210, 17220, 17225]:
        print(f"[*] 尝试模式 {mode}...")
        if test_hash_load(hash_file, mode):
            print(f"[+] 模式 {mode} 可以加载哈希")
            return mode
    return None

def run_hashcat_with_progress(cmd, total: int, description: str):
    """执行 hashcat 并显示进度条，返回 (成功标志, 密码)"""
    print(f"[*] {description}: {' '.join(cmd)}")
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

    found_password = None
    progress_re = re.compile(r'Progress[\.\s]*:\s*(\d+)/(\d+)\s+\((\d+\.?\d*)%\)')
    success_re = re.compile(r'^(\$pkzip\$[^:]+|\$zip2\$[^:]+):(.+)$')

    pbar = tqdm(total=total, unit='pwd', unit_scale=True, desc=description, dynamic_ncols=True)

    def read_output(stream, is_stderr):
        nonlocal found_password
        for line in stream:
            match = progress_re.search(line)
            if match:
                current = int(match.group(1))
                total_attempts = int(match.group(2))
                pbar.total = total_attempts
                pbar.n = current
                pbar.refresh()
            if not is_stderr:
                sm = success_re.match(line.strip())
                if sm:
                    found_password = sm.group(2)
                    break
            if is_stderr:
                sm = success_re.match(line.strip())
                if sm:
                    found_password = sm.group(2)
                    break

    t_out = threading.Thread(target=read_output, args=(process.stdout, False))
    t_err = threading.Thread(target=read_output, args=(process.stderr, True))
    t_out.start()
    t_err.start()

    process.wait()
    t_out.join(timeout=1)
    t_err.join(timeout=1)
    pbar.close()

    if found_password:
        print(f"\n[+] 破解成功！密码: {found_password}")
        return True, found_password

    # 检查输出文件（如果指定了 -o）
    output_file = None
    for i, arg in enumerate(cmd):
        if arg == "-o" and i+1 < len(cmd):
            output_file = cmd[i+1]
            break
    if output_file and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                sm = success_re.match(line.strip())
                if sm:
                    pwd = sm.group(2)
                    print(f"[+] 破解成功！密码: {pwd}")
                    return True, pwd
    return False, None

def build_base_cmd(hash_file: str, mode: int, output_file: str) -> list:
    """构建 hashcat 基础命令（不含掩码部分）"""
    cmd = [CONFIG["hashcat_path"], "-m", str(mode), "-a", "3", hash_file,
           "-o", output_file, "--status", "--status-timer=1"]
    if CONFIG["gpu_ids"]:
        cmd.extend(["-d", CONFIG["gpu_ids"]])
    if CONFIG["optimize"]:
        cmd.append("-O")
    cmd.extend(["-w", str(CONFIG["workload"])])
    cmd.extend(CONFIG["extra_args"])
    return cmd

def run_hashcat_mask_with_charset(hash_file: str, charset: str, length: int, mode: int, output_file: str):
    """单字符集掩码攻击（无必须包含要求）"""
    total = len(charset) ** length
    cmd = build_base_cmd(hash_file, mode, output_file)
    cmd.extend(["-1", charset, "?1" * length])
    return run_hashcat_with_progress(cmd, total, f"暴力 {length}位 ({len(charset)}字符)")

def run_hashcat_multi_charset_mask(hash_file: str, must_set: str, other_set: str, length: int,
                                   mode: int, output_file: str, positions: list):
    """多字符集掩码：positions 指定位置必须来自 must_set，其余来自 other_set"""
    mask_chars = ['?2'] * length
    for pos in positions:
        mask_chars[pos] = '?1'
    mask = ''.join(mask_chars)
    total = (len(must_set) ** len(positions)) * (len(other_set) ** (length - len(positions)))
    cmd = build_base_cmd(hash_file, mode, output_file)
    cmd.extend(["-1", must_set, "-2", other_set, mask])
    desc = f"必须包含 {len(positions)}个位置 (总组合 {total:.2e})"
    return run_hashcat_with_progress(cmd, total, desc)

def crack_zip_hashcat(zip_path: str, charset: str, min_len: int, max_len: int,
                      must_include: str = '', exclude: str = '') -> Optional[str]:
    """
    破解 ZIP 密码（GPU 加速）
    :param zip_path:      ZIP 文件路径
    :param charset:       完整字符集（字符串）
    :param min_len:       最小密码长度
    :param max_len:       最大密码长度
    :param must_include:  必须包含的字符集（密码中至少出现其中一个字符）
    :param exclude:       排除的字符（从 charset 中移除）
    :return:              密码字符串，未找到返回 None
    """
    zip_path = os.path.abspath(zip_path)
    if not os.path.exists(zip_path):
        print(f"[!] ZIP 文件不存在: {zip_path}")
        return None

    # 1. 提取哈希
    print("\n[步骤1] 提取哈希")
    hash_file = extract_clean_hash(zip_path)
    if not hash_file:
        print("[!] 哈希提取失败")
        return None

    # 2. 检测工作模式
    print("\n[步骤2] 检测可用的 Hashcat 模式")
    working_mode = detect_working_mode(hash_file)
    if working_mode is None:
        print("[!] 无法加载哈希")
        return None
    print(f"[*] 使用模式 {working_mode}")

    # 3. 处理字符集
    effective_charset = ''.join(ch for ch in charset if ch not in exclude)
    if not effective_charset:
        print("[!] 排除后字符集为空")
        return None
    print(f"[*] 有效字符集: {effective_charset} (共{len(effective_charset)}字符)")

    must_set = ''.join(ch for ch in must_include if ch in effective_charset)
    if must_include and not must_set:
        print("[!] 必须包含的字符都不在有效字符集中，无法满足条件")
        return None
    if must_set:
        print(f"[*] 必须包含字符集: {must_set} (共{len(must_set)}字符)")

    # 4. 依次尝试每个长度
    for length in range(min_len, max_len + 1):
        print(f"\n========== 尝试长度 {length} ==========")
        output_file = os.path.join(os.path.dirname(hash_file), f"hashcat_out_{length}.txt")

        if not must_set:
            ok, pwd = run_hashcat_mask_with_charset(hash_file, effective_charset,
                                                    length, working_mode, output_file)
            if ok and pwd:
                return pwd
        else:
            # 有必须包含要求：生成所有非空位置子集
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
        zip_path='../es68z4.zip',
        charset='0123456789abcdefghijklmnopqrstuvwxyz',
        min_len=6, max_len=6,
        must_include='',
        exclude=''
    )
    if pwd:
        print(f"找到密码: {pwd}")