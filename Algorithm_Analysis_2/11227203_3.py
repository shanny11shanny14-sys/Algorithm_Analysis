# 演算法分析機測
# 學號: 11227203 / 11227236 / 11227246
# 姓名: 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

# deque 適合用來實作 BFS 的佇列
from collections import deque


# 西洋棋騎士一次可以移動的 8 種方向
# 每個 tuple 代表座標的變化量 (dx, dy)
moves = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]


# 將西洋棋座標，例如 b2，轉成程式使用的數字座標
def convert(pos):
    # pos[0] 是英文字母，例如 b
    # ord('b') - ord('a') = 1
    x = ord(pos[0]) - ord('a')

    # pos[1] 是數字字元，例如 '2'
    # 棋盤編號是 1～8，但陣列編號是 0～7，所以減 1
    y = int(pos[1]) - 1

    return x, y


# 使用 BFS 尋找騎士從 start 到 end 的最少步數
def bfs(start, end):
    # 起點和終點相同，不需要移動
    if start == end:
        return 0

    # 將起點與終點轉成數字座標
    sx, sy = convert(start)
    ex, ey = convert(end)

    # 佇列中的資料格式：(x 座標, y 座標, 已走步數)
    q = deque([(sx, sy, 0)])

    # 記錄棋盤上的位置是否已經走過
    visited = [[False] * 8 for _ in range(8)]

    # 起點先標記為已走過
    visited[sx][sy] = True

    # 只要佇列還有資料，就繼續搜尋
    while q:
        # 從佇列前端取出目前位置
        x, y, step = q.popleft()

        # 嘗試騎士的 8 種移動方式
        for dx, dy in moves:
            nx = x + dx
            ny = y + dy

            # 判斷新位置是否在棋盤內，且尚未走過
            if (
                0 <= nx < 8
                and 0 <= ny < 8
                and not visited[nx][ny]
            ):
                # 第一次找到終點時，就是最少步數
                if nx == ex and ny == ey:
                    return step + 1

                # 標記成已走過，避免重複搜尋
                visited[nx][ny] = True

                # 將新位置及新的步數放進佇列
                q.append((nx, ny, step + 1))


def main():
    while True:
        # 讀取起點與終點，例如 b2 c3
        s, t = input().split()

        # 輸入 0 0 代表結束
        if s == "0" and t == "0":
            break

        # 使用 BFS 計算最少步數
        ans = bfs(s, t)

        # 按照題目指定格式輸出
        print(f"From {s} to {t}, Knight Moves = {ans}")


# 執行主程式
main()