# 演算法分析機測
# 學號 : 11227203 / 11227236 / 11227246
# 姓名 : 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

from collections import deque
import heapq
import sys

# 四個方向：
# (列變化, 行變化, 小寫方向, 大寫方向)
# 小寫：人自己走路
# 大寫：推箱子
DIRS = [
  (0, 1, 'e', 'E'),   # 向東
  (0, -1, 'w', 'W'),  # 向西
  (1, 0, 's', 'S'),   # 向南
  (-1, 0, 'n', 'N')   # 向北
]


def shortest_walk(start, goal, box, neighbors, cell_count):
  """
  找人從 start 走到 goal 的最短路徑。
  這裡要把箱子目前的位置 box 當成障礙物，不能穿過。
  如果走得到，回傳小寫路徑字串；否則回傳 None。
  """

  # 如果起點就是目標位置，代表不用走
  if start == goal:
    return ""

  # prev[i] 紀錄走到格子 i 的前一個格子是誰
  prev = [-1] * cell_count

  # move[i] 紀錄走到格子 i 時，最後一步用的是哪個方向字元
  move = [''] * cell_count

  # BFS 佇列
  q = deque([start])

  # 用自己指向自己，表示 start 已拜訪
  prev[start] = start

  while q:
    cur = q.popleft()

    # 嘗試四個方向
    for d in range(4):
      nxt = neighbors[cur][d]

      # nxt == -1：不能走（牆或越界）
      # nxt == box：箱子那格不能穿過
      # prev[nxt] != -1：已拜訪過
      if nxt == -1 or nxt == box or prev[nxt] != -1:
        continue

      # 紀錄前驅格子
      prev[nxt] = cur

      # 紀錄走到 nxt 這一步用的小寫方向字元
      move[nxt] = DIRS[d][2]

      # 如果已到達目標，回推出完整路徑
      if nxt == goal:
        path_chars = []
        x = nxt

        # 沿著 prev 往回走到 start
        while x != start:
          path_chars.append(move[x])
          x = prev[x]

        # 因為是反向回推，所以要反轉
        path_chars.reverse()
        return ''.join(path_chars)

      # 還沒到終點，加入 BFS 佇列
      q.append(nxt)

  # 走不到 goal
  return None


def solve_one_maze(grid, rows, cols):
  """
  解一組迷宮，回傳答案字串：
  - 如果可解，回傳由小寫/大寫方向組成的路徑
  - 如果不可解，回傳 "Impossible"
  """

  # 迷宮總格數
  cell_count = rows * cols

  # walls[i] = True 代表該格是牆
  walls = [True] * cell_count

  # 玩家起點、箱子起點、目標點
  player_start = None
  box_start = None
  target = None

  # 掃描迷宮，找出 S、B、T，並建立牆資訊
  for r in range(rows):
    for c, ch in enumerate(grid[r]):
      idx = r * cols + c  # 把二維座標壓成一維編號

      # 不是牆就可站立
      if ch != '#':
        walls[idx] = False

      # 記錄三個重要位置
      if ch == 'S':
        player_start = idx
      elif ch == 'B':
        box_start = idx
      elif ch == 'T':
        target = idx

  # neighbors[idx][d] 表示：
  # 從 idx 往第 d 個方向走，會到哪個格子
  # 如果不能走，記為 -1
  neighbors = [[-1] * 4 for _ in range(cell_count)]

  for r in range(rows):
    for c in range(cols):
      idx = r * cols + c

      # 牆不用建立鄰居
      if walls[idx]:
        continue

      # 嘗試四個方向
      for d, (dr, dc, _, _) in enumerate(DIRS):
        nr = r + dr
        nc = c + dc

        # 檢查有沒有越界
        if 0 <= nr < rows and 0 <= nc < cols:
          nidx = nr * cols + nc

          # 不是牆才可走
          if not walls[nidx]:
            neighbors[idx][d] = nidx

  def is_dead_corner(cell):
    """
    判斷這格是不是『非目標死角』。
    如果箱子被推到不是目標的牆角，通常就永遠出不來。
    """

    # 如果這格本身就是目標，不能視為死角
    if cell == target:
      return False

    # 看上下左右有沒有被擋住
    up = neighbors[cell][3] == -1
    down = neighbors[cell][2] == -1
    left = neighbors[cell][1] == -1
    right = neighbors[cell][0] == -1

    # 若上下至少一邊堵住，且左右至少一邊堵住，就形成角落
    return (up or down) and (left or right)

  # 預先把每格是否為死角算好
  dead_corner = [False] * cell_count
  for cell in range(cell_count):
    if not walls[cell]:
      dead_corner[cell] = is_dead_corner(cell)

  # 狀態 = (人位置, 箱子位置)
  start_state = (player_start, box_start)

  # dist[state] = (推箱次數, 總移動數)
  # 用來記錄到某狀態的最佳代價
  dist = {start_state: (0, 0)}

  # path_map[state] = 到某狀態的最佳路徑字串
  path_map = {start_state: ""}

  # priority queue 內容：
  # (推箱次數, 總移動數, 路徑字串, 人位置, 箱子位置)
  pq = [(0, 0, "", player_start, box_start)]

  # Dijkstra 主迴圈
  while pq:
    pushes, moves, path, player, box = heapq.heappop(pq)
    state = (player, box)

    # 如果這筆不是目前最佳狀態，跳過
    if dist.get(state) != (pushes, moves) or path_map.get(state) != path:
      continue

    # 箱子到目標，直接回傳答案
    if box == target:
      return path

    # 嘗試往四個方向推箱子
    for d in range(4):
      # 箱子推完後的新位置
      box_next = neighbors[box][d]

      # 推箱前，人必須站在箱子反方向那格
      # d ^ 1 可用來取得反方向：
      # 0<->1, 2<->3
      player_need = neighbors[box][d ^ 1]

      # 箱子不能推進牆/界外
      # 人要站的位置也必須存在
      if box_next == -1 or player_need == -1:
        continue

      # 先檢查人能不能走到推箱位置
      # 注意：人的走路過程中不能穿過箱子目前那格
      walk_path = shortest_walk(player, player_need, box, neighbors, cell_count)
      if walk_path is None:
        continue

      # 若箱子會被推進非目標死角，直接略過
      if dead_corner[box_next]:
        continue

      # 推完之後：
      # 人會站到箱子原本的位置
      # 箱子會移到新位置
      new_player = box
      new_box = box_next

      # 這一步的新增路徑：
      # 先走到推箱位置（小寫）
      # 再推箱一次（大寫）
      segment = walk_path + DIRS[d][3]

      # 新的完整路徑
      new_path = path + segment

      # 新代價：
      # 推箱次數 +1
      # 總移動數 = 原本 moves + 這一段長度
      new_cost = (pushes + 1, moves + len(segment))

      # 新狀態
      new_state = (new_player, new_box)

      # 取出舊資料做比較
      old_cost = dist.get(new_state)
      old_path = path_map.get(new_state)

      # 更新條件：
      # 1. 新狀態沒出現過
      # 2. 新代價更小
      # 3. 代價相同，但路徑字串字典序更小（讓輸出更穩定）
      if (
        old_cost is None
        or new_cost < old_cost
        or (new_cost == old_cost and new_path < old_path)
      ):
        dist[new_state] = new_cost
        path_map[new_state] = new_path

        # 丟進 priority queue
        heapq.heappush(
          pq,
          (new_cost[0], new_cost[1], new_path, new_player, new_box)
        )

  # 所有狀態都找過，仍無法到達目標
  return "Impossible"


def main():
  """
  主程式：
  持續讀入多組迷宮，直到 r c = 0 0 為止。
  """

  maze_id = 1
  outputs = []

  while True:
    try:
      line = input().strip()
    except EOFError:
      break

    # 跳過空白行
    if not line:
      continue

    # 讀取迷宮大小
    r, c = map(int, line.split())

    # 0 0 表示結束
    if r == 0 and c == 0:
      break

    # 讀入迷宮
    grid = []
    for _ in range(r):
      grid.append(input().rstrip('\n'))

    # 儲存這組輸出
    outputs.append(f"Maze #{maze_id}")
    outputs.append(solve_one_maze(grid, r, c))
    outputs.append("")  # 每組之間空一行
    maze_id += 1

  # 一次輸出全部結果，最後多餘空白行去掉
  sys.stdout.write('\n'.join(outputs).rstrip())


if __name__ == "__main__":
  main()
  