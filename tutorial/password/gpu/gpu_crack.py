import subprocess
import os
import re
import sys
import tempfile
from typing import Optional

# ==================== 配置区域（请根据实际路径修改） ====================
CONFIG = {
    "hashcat_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\hashcat-6.2.6\hashcat.exe",
    "zip2john_path": r"D:\dev_code\python3_tutorial\tutorial\password\gpu\john-1.9.0-jumbo-1-win64\run\zip2john.exe",
    "gpu_ids": None,           # 例如 "1,2" 或 None（使用默认设备）
    "optimize": True,          # -O 优化内核
    "workload": 3,             # -w 3 高负载
    "extra_args": ["--force"], # 额外参数
    "fallback_to_cpu": False,  # 如果 GPU 设备出错，自动回退到 CPU（添加 -D 1）
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
            hash_file = os.path.join(os.path.dirname(zip_path), "zip_hash_clean.txt")
            with open(hash_file, 'w', encoding='ascii') as f:
                f.write(clean + '\n')
            print(f"[+] 清理后的哈希已保存到 {hash_file}")
            return hash_file
    print("[!] 未能提取哈希")
    return None

def read_password_from_potfile(hash_file: str) -> Optional[str]:
    """
    从 hashcat.potfile 中读取给定哈希对应的密码。
    potfile 默认位于 hashcat.exe 所在目录，文件名为 hashcat.potfile。
    格式：hash:password
    """
    potfile_path = os.path.join(os.path.dirname(CONFIG["hashcat_path"]), "hashcat.potfile")
    if not os.path.exists(potfile_path):
        return None

    # 读取原始哈希内容（用于匹配）
    with open(hash_file, 'r', encoding='ascii') as f:
        target_hash = f.read().strip()

    with open(potfile_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if ':' not in line:
                continue
            h, pwd = line.split(':', 1)
            # 如果 potfile 中的哈希包含目标哈希（或相等）
            if target_hash in h or h == target_hash:
                return pwd
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

    # 如果开启了 CPU 回退且没有指定 GPU ID，添加 -D 1 强制使用 CPU
    if CONFIG["fallback_to_cpu"] and not CONFIG["gpu_ids"]:
        cmd.extend(["-D", "1"])
    return cmd

def run_hashcat_cmd(cmd, total: int, description: str, hash_file: str):
    """
    执行 hashcat 命令，捕获输出，并从输出文件或 potfile 中读取密码。
    """
    print(f"[*] {description}: {' '.join(cmd)}")
    print(f"[*] 总尝试次数: {total:,}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            cwd=os.path.dirname(CONFIG["hashcat_path"]),
            timeout=3600
        )
    except subprocess.TimeoutExpired:
        print("[!] 命令执行超时（3600秒）")
        return False, None
    except Exception as e:
        print(f"[!] 执行异常: {e}")
        return False, None

    # 打印 stdout 和 stderr 以便调试
    if result.stdout:
        print("\n[STDOUT]")
        print(result.stdout)
    if result.stderr:
        print("\n[STDERR]")
        print(result.stderr)

    if result.returncode != 0:
        print(f"\n[!] Hashcat 返回非零状态码: {result.returncode}")
        # 即使返回非零，也可能 potfile 中已有密码？通常不会，但为保险也检查一下
        pwd = read_password_from_potfile(hash_file)
        if pwd:
            print(f"\n[+] 从 potfile 中找到密码: {pwd}")
            return True, pwd
        return False, None

    # 检查输出文件（-o 指定的文件）
    output_file = None
    for i, arg in enumerate(cmd):
        if arg == "-o" and i+1 < len(cmd):
            output_file = cmd[i+1]
            break
    if output_file and os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().strip()
            if content:
                if ':' in content:
                    pwd = content.split(':', 1)[1]
                else:
                    pwd = content
                print(f"\n[+] 破解成功！密码: {pwd}")
                return True, pwd

    # 从 stdout 中尝试匹配（某些模式直接输出）
    success_re = re.compile(r'^(\$pkzip\$[^:]+|\$zip2\$[^:]+):(.+)$')
    for line in result.stdout.splitlines():
        sm = success_re.match(line.strip())
        if sm:
            pwd = sm.group(2)
            print(f"\n[+] 破解成功！密码: {pwd}")
            return True, pwd

    # 最后检查 potfile
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
    """
    破解 ZIP 密码（GPU 加速）
    :param zip_path:      ZIP 文件路径
    :param charset:       完整字符集（字符串）
    :param min_len:       最小密码长度
    :param max_len:       最大密码长度
    :param must_include:  必须包含的字符集（密码中至少出现其中一个字符），None 表示无要求
    :param exclude:       排除的字符（从 charset 中移除），None 表示无排除
    :return:              密码字符串，未找到返回 None
    """
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
        print(f"[DEBUG] 哈希内容: {f.read().strip()}")

    # 提前检查 potfile 中是否已有密码
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

    # 检查输出目录权限，若不可写则回退到临时目录
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
        zip_path='../es68z4.zip',
        charset='0123456789abcdefghijklmnopqrstuvwxyz',
        min_len=6, max_len=6,
        must_include='e6', exclude='01lLpt'
    )
    if pwd:
        print(f"找到密码: {pwd}")