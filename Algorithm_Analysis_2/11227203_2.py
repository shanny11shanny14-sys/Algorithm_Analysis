# 演算法分析機測
# 學號: 11227203 / 11227236 / 11227246
# 姓名: 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

import heapq


# 霍夫曼樹的節點
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq      # 字元出現頻率
        self.char = char      # 葉節點的字元
        self.left = left      # 左子節點
        self.right = right    # 右子節點


# 走訪霍夫曼樹，建立每個字元的編碼
def build_codes(root, code, codes):
    if root is None:
        return

    # 走到葉節點，儲存該字元的編碼
    if root.char is not None:
        # 如果只有一個字元，編碼設為 0
        codes[root.char] = code if code != "" else "0"
        return

    # 往左加 0，往右加 1
    build_codes(root.left, code + "0", codes)
    build_codes(root.right, code + "1", codes)


# 使用霍夫曼樹解碼二進位字串
def decode_text(binary_code, root):
    # 如果只有一個字元，每個 0 都代表該字元
    if root.char is not None:
        return root.char * len(binary_code)

    result = ""
    current = root

    for bit in binary_code:
        # 0 往左，1 往右
        if bit == "0":
            current = current.left
        else:
            current = current.right

        # 走到葉節點，取得一個字元
        if current.char is not None:
            result += current.char

            # 回到根節點，繼續解下一個字元
            current = root

    return result


case = 1

# 儲存每一組測資的輸出
# 等全部輸入完成後再一次輸出
all_outputs = []


while True:
    # 讀取字元數量
    n = int(input())

    # 讀到 0 代表所有輸入結束
    if n == 0:
        break

    heap = []
    order = 0

    # 記錄字元原本的輸入順序
    chars = []

    # 讀取每個字元及其頻率
    for i in range(n):
        char, freq = input().split()
        freq = int(freq)

        # 建立葉節點
        node = Node(freq, char)

        # 放入最小堆積
        # order 用來處理頻率相同的情況
        heapq.heappush(heap, (freq, order, node))

        chars.append(char)
        order += 1

    # 讀取需要解碼的二進位字串
    binary_code = input().strip()

    # 建立霍夫曼樹
    while len(heap) > 1:
        # 取出頻率最小的兩個節點
        freq1, order1, left = heapq.heappop(heap)
        freq2, order2, right = heapq.heappop(heap)

        # 合併成新的父節點
        parent = Node(
            freq1 + freq2,
            None,
            left,
            right
        )

        # 將父節點放回最小堆積
        heapq.heappush(
            heap,
            (parent.freq, order, parent)
        )

        order += 1

    # 最後剩下的節點就是樹根
    root = heap[0][2]

    # 建立每個字元的霍夫曼碼
    codes = {}
    build_codes(root, "", codes)

    # 解碼
    decoded = decode_text(binary_code, root)

    # 暫存目前這一組的輸出
    lines = []

    lines.append(f"Huffman Codes #{case}")

    for char in chars:
        lines.append(f"{char} {codes[char]}")

    lines.append(f"Decode = {decoded}")

    # 把這一整組輸出存起來
    all_outputs.append("\n".join(lines))

    case += 1


# 所有輸入都讀完後，再一次全部輸出
print("\n".join(all_outputs))