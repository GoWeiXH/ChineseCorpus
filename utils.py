"""
一些工具方法
"""


def get_ips():
    """
    从代理 ip 文件中读取 ip 并返回
    """
    ps, ips = [], []
    with open("ips.txt") as f:
        for ip in f.readlines():
            ps.append(ip.split(":")[0])
            ips.append(ip.split(":")[1][2:])

    return ps, ips
