# 演算法分析機測
# 學號: 11227203 / 11227236 / 11227246
# 姓名: 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

import cv2
from collections import deque
import os


# 每一個迷宮格子是 20 × 20 像素
CELL = 20

# 500 ÷ 20 = 25，所以迷宮是 25 × 25 格
SIZE = 25


# 判斷兩個相鄰格子之間是否可以通過
def can_move(img, r1, c1, r2, c2):
    # 將格子座標轉成格子中心的像素座標
    # 每格 20 像素，所以加 10 會到格子中心
    y1 = r1 * CELL + 10
    x1 = c1 * CELL + 10
    y2 = r2 * CELL + 10
    x2 = c2 * CELL + 10

    # 如果兩格在同一列，表示向左或向右移動
    if y1 == y2:
        xs = min(x1, x2)
        xe = max(x1, x2)

        # 檢查兩格中心之間是否有白色牆壁
        for x in range(xs, xe + 1):
            if img[y1][x][0] > 200:
                return False

    # 否則是向上或向下移動
    else:
        ys = min(y1, y2)
        ye = max(y1, y2)

        # 檢查兩格中心之間是否有白色牆壁
        for y in range(ys, ye + 1):
            if img[y][x1][0] > 200:
                return False

    # 沒有遇到白色牆壁，代表可以通過
    return True


# 使用 BFS 找出左上角到右下角的最短路徑
def shortest_path(img):
    # 左上角格子
    start = (0, 0)

    # 右下角格子
    end = (24, 24)

    # BFS 佇列，先放入起點
    q = deque([start])

    # parent 記錄每一格是從哪一格走過來的
    # 之後可以用來還原完整路徑
    parent = {}

    # 記錄已經走過的格子
    visited = {start}

    # 上、下、左、右四個方向
    dirs = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    while q:
        # 從佇列前面取出目前格子
        r, c = q.popleft()

        # 到達終點就停止搜尋
        if (r, c) == end:
            break

        # 嘗試四個方向
        for dr, dc in dirs:
            nr = r + dr
            nc = c + dc

            # 確認新格子仍在 25 × 25 的迷宮內
            if 0 <= nr < SIZE and 0 <= nc < SIZE:

                # 確認新格子還沒走過
                if (nr, nc) not in visited:

                    # 確認兩格之間沒有牆壁
                    if can_move(img, r, c, nr, nc):
                        visited.add((nr, nc))

                        # 記錄新格子是從目前格子走過來的
                        parent[(nr, nc)] = (r, c)

                        # 放進佇列繼續搜尋
                        q.append((nr, nc))

    # 從終點開始反向找回起點
    path = []
    cur = end

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    # 加入起點
    path.append(start)

    # 原本是終點到起點，所以反轉成起點到終點
    path.reverse()

    return path


# 讀取使用者輸入的圖片檔名
filename = input("Enter file name: ")

# 使用 OpenCV 讀取圖片
img = cv2.imread(filename)

# 找出最短路徑
path = shortest_path(img)


# 將路徑中相鄰的格子中心連成藍線
for i in range(len(path) - 1):
    r1, c1 = path[i]
    r2, c2 = path[i + 1]

    # OpenCV 座標順序是 (x, y)
    p1 = (
        c1 * CELL + 10,
        r1 * CELL + 10
    )

    p2 = (
        c2 * CELL + 10,
        r2 * CELL + 10
    )

    # OpenCV 使用 BGR
    # (255, 0, 0) 代表藍色，線寬為 2 像素
    cv2.line(img, p1, p2, (255, 0, 0), 2)


# 移除原本的副檔名
name = os.path.splitext(filename)[0]

# 產生輸出檔名
output = name + "_result.bmp"

# 儲存結果圖片
cv2.imwrite(output, img)

print("Output file:", output)