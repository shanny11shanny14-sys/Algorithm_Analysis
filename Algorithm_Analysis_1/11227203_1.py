# 演算法分析機測
# 學號: 11227203 11227236/11227246
# 姓名: 謝采凌/曹湘婷/徐雨瑄
# 中原大學資訊工程系

import sys

def preorder_to_postorder(arr):
    n = len(arr)
    idx = 0
    result = []

    def build(lower=None, upper=None):
        nonlocal idx

        if idx >= n:
            return

        val = arr[idx]

        if lower is not None and val <= lower:
            return
        if upper is not None and val >= upper:
            return

        idx += 1

        build(lower, val)   # 左子樹
        build(val, upper)   # 右子樹
        result.append(str(val))   # 後序：左、右、根

    build()
    return result


for line in sys.stdin:
    line = line.strip()

    if not line:
        continue

    if line == "0":
        break

    tokens = line.split()

    if all(t.isdigit() for t in tokens):
        arr = list(map(int, tokens))
    else:
        arr = tokens

    ans = preorder_to_postorder(arr)
    print(" ".join(ans))
    