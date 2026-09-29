# 演算法分析機測
# 學號: 11227203 / 11227236 / 11227246
# 姓名: 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

import cv2
import numpy as np


# 每一塊拼圖大小為 120 × 120 像素
PIECE = 120

# 原圖共有 9 列、16 行
ROWS = 9
COLS = 16


# 將整張打亂的圖片切成 144 塊
def split_puzzles(img):
    pieces = []

    for r in range(ROWS):
        for c in range(COLS):
            y1 = r * PIECE
            y2 = y1 + PIECE
            x1 = c * PIECE
            x2 = x1 + PIECE

            # 切出一塊 120 × 120 的拼圖
            pieces.append(img[y1:y2, x1:x2].copy())

    return pieces


# 計算兩條邊的平均平方差
# 數值越小，代表兩條邊越相似
def average_diff(edge1, edge2):
    diff = (
        edge1.astype(np.int32)
        - edge2.astype(np.int32)
    )

    return float(np.mean(diff * diff))


# 取得一塊拼圖的上、下、左、右四條邊
def get_edges(puzzle):
    top = puzzle[0, :, :].astype(np.int32)
    bottom = puzzle[-1, :, :].astype(np.int32)
    left = puzzle[:, 0, :].astype(np.int32)
    right = puzzle[:, -1, :].astype(np.int32)

    return top, bottom, left, right


# 計算每兩塊拼圖在四個方向的邊緣差異
def THE_diff(puzzles):
    n = len(puzzles)
    edges = []

    # 先取得每塊拼圖的四條邊
    for puzzle in puzzles:
        edge = get_edges(puzzle)
        edges.append(edge)

    # 建立四個 144 × 144 的差異矩陣
    right = np.full((n, n), np.inf)
    left = np.full((n, n), np.inf)
    down = np.full((n, n), np.inf)
    up = np.full((n, n), np.inf)

    for i in range(n):
        top_i, bottom_i, left_i, right_i = edges[i]

        for j in range(n):
            # 同一塊不能和自己連接
            if i == j:
                continue

            top_j, bottom_j, left_j, right_j = edges[j]

            # j 放在 i 的右邊
            right[i, j] = average_diff(right_i, left_j)

            # j 放在 i 的左邊
            left[i, j] = average_diff(left_i, right_j)

            # j 放在 i 的下方
            down[i, j] = average_diff(bottom_i, top_j)

            # j 放在 i 的上方
            up[i, j] = average_diff(top_i, bottom_j)

    return right, left, down, up


# 找出互相認為最適合的左右鄰居
def best_one(right, left, up):
    n = ROWS * COLS

    # 每一塊最適合接在右邊的拼圖
    best_right_index = np.argmin(right, axis=1)

    # 每一塊最適合接在左邊的拼圖
    best_left_index = np.argmin(left, axis=1)

    right_connect = {}

    for i in range(n):
        # i 覺得 j 最適合放右邊
        j = int(best_right_index[i])

        # j 覺得哪一塊最適合放左邊
        left_of_j = int(best_left_index[j])

        # 若兩邊互相認為是最佳鄰居，才建立連接
        if left_of_j == i:
            right_connect[i] = j

    # 每一塊最小的上方與左方差異
    best_up = np.min(up, axis=1)
    best_left = np.min(left, axis=1)

    return right_connect, best_up, best_left


# 將一個段落補成長度 16
# 沒有拼圖的位置使用 -1
def replace(segment):
    row = [-1] * COLS

    for pos, piece_index in enumerate(segment):
        if pos >= COLS:
            break

        row[pos] = piece_index

    return row


# 根據左右連接關係形成多個橫向段落
def row_order(right, right_connect):
    n = ROWS * COLS
    segments = []
    used = set()

    for i in range(n):
        # 沒有右鄰居，無法當成段落起點
        if i not in right_connect:
            continue

        # 如果 i 是其他拼圖的右鄰居，
        # 代表它不是整個段落的起點
        if any(
            right_connect.get(j) == i
            for j in right_connect
        ):
            continue

        cur = i
        chain = []

        # 一直沿著右邊鄰居走
        while cur not in used:
            chain.append(cur)
            used.add(cur)

            if cur not in right_connect:
                break

            cur = right_connect[cur]

        # 一列最多只能放 16 塊
        if chain:
            for start in range(0, len(chain), COLS):
                segments.append(
                    chain[start:start + COLS]
                )

    # 記錄尚未出現在任何段落中的拼圖
    NO_found_index = []

    for i in range(n):
        if i not in used:
            NO_found_index.append(i)

    return segments, NO_found_index


# 將較短的段落合併，直到段落數不超過 9
def merge_together(segments, right):
    segments = [
        list(segment)
        for segment in segments
    ]

    while len(segments) > ROWS:
        best_merge = None

        for i, seg_a in enumerate(segments):
            for j, seg_b in enumerate(segments):
                if i == j:
                    continue

                # 合併後不能超過一列的 16 塊
                if len(seg_a) + len(seg_b) > COLS:
                    continue

                # 比較 A 最後一塊和 B 第一塊的邊緣差異
                cost = right[seg_a[-1], seg_b[0]]

                if (
                    best_merge is None
                    or cost < best_merge[0]
                ):
                    best_merge = (cost, i, j)

        if best_merge is None:
            break

        _, i, j = best_merge

        # 將選中的兩個段落取出
        if i > j:
            seg_a = segments.pop(i)
            seg_b = segments.pop(j)
        else:
            seg_b = segments.pop(j)
            seg_a = segments.pop(i)

        # 合併成一個較長段落
        segments.append(seg_a + seg_b)

    return segments


# 決定各個橫向段落的上下順序
def decide_order(segments, down, up):
    n = len(segments)

    if n == 0:
        return []

    # 將每個段落補成固定 16 格
    partial_rows = [
        replace(segment)
        for segment in segments
    ]

    # 根據上邊緣差異，估計哪一列適合放最上面
    best_up = np.min(up, axis=1)
    max_up = float(np.max(best_up))

    start_penalty = [
        0.05 * (
            max_up - best_up[segment[0]]
        )
        for segment in segments
    ]

    # cost_matrix[i][j]：
    # 第 j 個段落放在第 i 個段落下方的差異
    cost_matrix = np.full((n, n), np.inf)

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            total = 0.0
            count = 0

            for c in range(COLS):
                a = partial_rows[i][c]
                b = partial_rows[j][c]

                # 兩列同一欄都有拼圖時，
                # 才計算上下邊緣差異
                if a != -1 and b != -1:
                    total += down[a, b]
                    count += 1

            if count > 0:
                cost_matrix[i, j] = total

    # 使用位元遮罩動態規劃，
    # 找出所有列的最佳上下排列順序
    full_mask = (1 << n) - 1

    best = [
        [float("inf")] * n
        for _ in range(1 << n)
    ]

    parent = [
        [-1] * n
        for _ in range(1 << n)
    ]

    # 每個段落都可能是第一列
    for i in range(n):
        best[1 << i][i] = start_penalty[i]

    # 枚舉已經使用過哪些列
    for mask in range(1 << n):
        for last in range(n):
            if not (mask >> last) & 1:
                continue

            if best[mask][last] == float("inf"):
                continue

            # 嘗試將下一列接在下面
            for nxt in range(n):
                if (mask >> nxt) & 1:
                    continue

                next_mask = mask | (1 << nxt)

                new_cost = (
                    best[mask][last]
                    + cost_matrix[last, nxt]
                )

                if new_cost < best[next_mask][nxt]:
                    best[next_mask][nxt] = new_cost
                    parent[next_mask][nxt] = last

    # 找出完整排列中成本最小的最後一列
    best_last = 0
    best_cost = best[full_mask][0]

    for last in range(1, n):
        if best[full_mask][last] < best_cost:
            best_cost = best[full_mask][last]
            best_last = last

    # 利用 parent 反向還原列的順序
    order = []
    mask = full_mask
    cur = best_last

    while cur != -1:
        order.append(cur)

        prev = parent[mask][cur]
        mask ^= 1 << cur
        cur = prev

    order.reverse()

    return [
        segments[i]
        for i in order
    ]


# 將尚未放入的拼圖補到空格中
def missing(grid, right, down, used):
    n = ROWS * COLS

    for r in range(ROWS):
        for c in range(COLS):
            # 不是空格就跳過
            if grid[r][c] != -1:
                continue

            # 找出尚未使用的拼圖
            chance_puzzle = [
                x
                for x in range(n)
                if x not in used
            ]

            if not chance_puzzle:
                continue

            best_piece = None
            best_score = float("inf")

            for x in chance_puzzle:
                score = 0

                # 比較左邊拼圖的右邊緣
                if c > 0:
                    left_piece = grid[r][c - 1]
                    score += right[left_piece, x]

                # 比較上方拼圖的下邊緣
                if r > 0:
                    above_piece = grid[r - 1][c]
                    score += down[above_piece, x]

                # 選擇差異最小的拼圖
                if score < best_score:
                    best_score = score
                    best_piece = x

            grid[r][c] = best_piece
            used.add(best_piece)

    return grid


# 計算交換兩個位置後，邊緣總差異會改變多少
def swap(grid, r1, c1, r2, c2, right, down):

    # 找出一個位置右邊與下方的相鄰邊
    def edges_for_position(r, c):
        result = []

        if c + 1 < COLS:
            result.append(
                (r, c, r, c + 1)
            )

        if r + 1 < ROWS:
            result.append(
                (r, c, r + 1, c)
            )

        return result

    # 只需要檢查兩個交換位置附近的邊
    positions = {
        (r1, c1),
        (r2, c2)
    }

    for dr, dc in (
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ):
        positions.add((r1 + dr, c1 + dc))
        positions.add((r2 + dr, c2 + dc))

    edges = set()

    for r, c in positions:
        if 0 <= r < ROWS and 0 <= c < COLS:
            for edge in edges_for_position(r, c):
                edges.add(edge)

    piece1 = grid[r1][c1]
    piece2 = grid[r2][c2]

    original_cost = 0.0
    new_cost = 0.0

    for a_r, a_c, b_r, b_c in edges:
        original_a = grid[a_r][a_c]
        original_b = grid[b_r][b_c]

        new_a = original_a
        new_b = original_b

        # 模擬交換後的拼圖
        if (a_r, a_c) == (r1, c1):
            new_a = piece2
        elif (a_r, a_c) == (r2, c2):
            new_a = piece1

        if (b_r, b_c) == (r1, c1):
            new_b = piece2
        elif (b_r, b_c) == (r2, c2):
            new_b = piece1

        # 水平方向
        if b_c == a_c + 1:
            original_cost += right[
                original_a,
                original_b
            ]

            new_cost += right[
                new_a,
                new_b
            ]

        # 垂直方向
        else:
            original_cost += down[
                original_a,
                original_b
            ]

            new_cost += down[
                new_a,
                new_b
            ]

    # 小於 0 代表交換後變得更好
    return new_cost - original_cost


# 透過交換拼圖，降低整體邊緣差異
def maximize(grid, right, down):
    current = [
        row.copy()
        for row in grid
    ]

    # 最多進行 10 次最佳交換
    for _ in range(10):
        best_delta = 0.0
        best_swap = None

        # 嘗試所有兩兩交換
        for r1 in range(ROWS):
            for c1 in range(COLS):
                for r2 in range(r1, ROWS):
                    for c2 in range(COLS):
                        # 避免同一組重複比較
                        if (
                            r1 == r2
                            and c2 <= c1
                        ):
                            continue

                        change = swap(
                            current,
                            r1,
                            c1,
                            r2,
                            c2,
                            right,
                            down
                        )

                        # 找出能讓差異下降最多的交換
                        if change < best_delta:
                            best_delta = change
                            best_swap = (
                                r1,
                                c1,
                                r2,
                                c2
                            )

        # 沒有更好的交換就停止
        if best_swap is None:
            break

        r1, c1, r2, c2 = best_swap

        current[r1][c1], current[r2][c2] = (
            current[r2][c2],
            current[r1][c1]
        )

    return current


# 整合所有步驟，取得拼圖排列結果
def solve_puzzle(right, left, down, up):
    right_connect, best_up, best_left = best_one(
        right,
        left,
        up
    )

    # 形成橫向段落
    segments, not_found = row_order(
        right,
        right_connect
    )

    # 將小段落合併
    segments = merge_together(
        segments,
        right
    )

    # 若不足 9 列，從尚未使用的拼圖補成新段落
    while len(segments) < ROWS and not_found:
        one = min(
            not_found,
            key=lambda x: (
                best_left[x]
                + best_up[x]
            )
        )

        segments.append([one])
        not_found.remove(one)

    # 決定各列的上下順序
    ordered_segments = decide_order(
        segments,
        down,
        up
    )

    # 建立 9 × 16 的拼圖排列
    grid = [
        [-1] * COLS
        for _ in range(ROWS)
    ]

    used = set()

    # 先把已經確定的段落放入 grid
    for row_index, segment in enumerate(
        ordered_segments[:ROWS]
    ):
        row = replace(segment)

        for column_index, index in enumerate(row):
            if index == -1:
                continue

            grid[row_index][column_index] = index
            used.add(index)

    # 將剩餘拼圖補進空格
    grid = missing(
        grid,
        right,
        down,
        used
    )

    # 使用交換方式進一步改善排列
    return maximize(
        grid,
        right,
        down
    )


# 根據 grid 將 144 塊拼圖重新組成完整圖片
def compose_to_image(pieces, grid):
    result = np.zeros(
        (
            ROWS * PIECE,
            COLS * PIECE,
            3
        ),
        dtype=np.uint8
    )

    for r in range(ROWS):
        for c in range(COLS):
            idx = grid[r][c]

            if idx < 0:
                continue

            y1 = r * PIECE
            y2 = y1 + PIECE
            x1 = c * PIECE
            x2 = x1 + PIECE

            result[y1:y2, x1:x2] = pieces[idx]

    return result


def main():
    # 讀取輸入圖片檔名
    filename = input("請輸入影像檔: ")

    # 使用 OpenCV 讀取彩色圖片
    img = cv2.imread(
        filename,
        cv2.IMREAD_COLOR
    )

    if img is None:
        print("讀取影像失敗")
        return

    # 將圖片切成 144 塊
    puzzles = split_puzzles(img)

    # 計算所有拼圖的邊緣差異
    right, left, down, up = THE_diff(puzzles)

    # 求出拼圖排列
    grid = solve_puzzle(
        right,
        left,
        down,
        up
    )

    # 根據排列重建完整圖片
    result = compose_to_image(
        puzzles,
        grid
    )

    # 產生輸出檔名
    name = filename.rsplit(".", 1)[0]
    output = name + "_result.bmp"

    # 儲存結果
    cv2.imwrite(output, result)

    print("輸出影像檔:", output)


if __name__ == "__main__":
    main()