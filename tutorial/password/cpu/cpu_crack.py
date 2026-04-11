import itertools
import os
import pyzipper
from tqdm import tqdm
from typing import Optional


def format_number(num: int) -> str:
    """将数字格式化为带单位的字符串（K, M, B）"""
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)


def crack_zip_optimized(
    zip_path: str,
    charset: str,
    min_len: int = 1,
    max_len: int = 4,
    must_include: Optional[str] = None,
    exclude: Optional[str] = None,
) -> Optional[str]:
    """
    暴力破解ZIP压缩包的密码（支持 ZipCrypto 和 AES 加密，附进度条）

    :param zip_path: ZIP文件路径
    :param charset: 密码可能包含的字符集（例如 '0123456789'）
    :param min_len: 密码最小长度
    :param max_len: 密码最大长度
    :param must_include: 密码必须包含的字符集合（例如 'abc'），默认None
    :param exclude:   密码中禁止出现的字符集合（例如 '01'），默认None
    :return: 成功时返回密码字符串，失败时返回 None
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"ZIP文件不存在: {zip_path}")

    # 处理 exclude 和 must_include
    exclude = exclude or ''
    must_include = must_include or ''

    # 根据 exclude 过滤字符集
    final_charset = ''.join([c for c in charset if c not in exclude])
    if not final_charset:
        raise ValueError("排除所有字符后，字符集为空，无法破解")

    # 检查必须字符是否都在最终字符集中
    must_set = set(must_include)
    if not must_set.issubset(final_charset):
        missing = must_set - set(final_charset)
        raise ValueError(f"必须包含的字符 {missing} 不在最终字符集中")

    # 输出掩码信息
    print(f"原始字符集 ({len(charset)}): {charset}")
    if exclude:
        print(f"排除字符 ({len(exclude)}): {exclude}")
    if must_include:
        print(f"必须包含的字符 ({len(must_include)}): {must_include}")
    print(f"最终尝试的字符集 ({len(final_charset)}): {final_charset}")

    # 打开ZIP文件
    with pyzipper.AESZipFile(zip_path) as zf:
        # 检查是否加密
        if not any(f.flag_bits & 0x1 for f in zf.infolist()):
            print("ZIP文件未加密，无需破解")
            return ''

        # 选择第一个文件作为测试目标（通常较小，且只读1字节）
        test_file = zf.infolist()[0]

        # 计算总尝试次数
        total = sum(len(final_charset) ** l for l in range(min_len, max_len + 1))
        print(f"总尝试次数: {format_number(total)}")

        # 预绑定局部变量，减少属性查找开销
        zf_open = zf.open
        pbar_update = None

        with tqdm(total=total, unit="pwd", unit_scale=True, desc="暴力破解") as pbar:
            pbar_update = pbar.update
            try:
                # 外层循环：密码长度
                for length in range(min_len, max_len + 1):
                    # 内层循环：生成所有组合
                    for combo in itertools.product(final_charset, repeat=length):
                        pwd = ''.join(combo)

                        # 必须包含字符检查（若指定）
                        if must_include and not must_set.issubset(pwd):
                            pbar_update(1)
                            continue

                        # 验证密码（只读取1字节，极快）
                        try:
                            with zf_open(test_file, pwd=pwd.encode()) as f:
                                f.read(1)  # 只读1字节，足以验证密码正确性
                            print(f"\n✅ 成功！密码是：{pwd}")
                            return pwd
                        except (RuntimeError, ValueError):
                            # 密码错误
                            pbar_update(1)
                        except Exception as e:
                            # 其他异常（理论上不应发生，打印并继续）
                            pbar_update(1)
                            print(f"\n⚠️ 未预期的错误: {e}")
            except KeyboardInterrupt:
                print("\n⚠️ 用户中断，已停止破解")
                return None

        print("\n❌ 未找到密码，请尝试更大的max_len或更丰富的charset")
        return None


if __name__ == '__main__':
    # 示例：破解6位数字+小写字母的密码（密码必须包含数字和字母）
    # pwd = crack_zip_optimized(
    #     '../es68z4.zip',
    #     charset='0123456789abcdefghijklmnopqrstuvwxyz',
    #     min_len=6,
    #     max_len=6,
    #     must_include='0123456789',   # 必须包含至少一个数字（简化写法：包含所有数字字符，实际只需一个）
    #     exclude=''                   # 不排除任何字符
    # )

    # 只尝试6位纯数字密码
    # pwd = crack_zip_optimized('../136758.zip', charset='0123456789', min_len=6, max_len=6,must_include='13',exclude='9')

    # 密码必须包含字母和数字，排除容易混淆的字符（如 0, O, 1, l）
    pwd = crack_zip_optimized('../es68z4.zip', charset='0123456789abcdefghijklmnopqrstuvwxyz',
                        min_len=6, max_len=6, must_include='e6', exclude='01lLpt')

    if pwd is not None:
        print(f"找到密码: {pwd}")