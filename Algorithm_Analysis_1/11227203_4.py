# 演算法分析機測
# 學號 : 11227203 / 11227236 / 11227246
# 姓名 : 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

def try_a_to_b(a_cap, b_cap, target):
  a = 0
  b = 0
  steps = []

  while True:
    if b == target:
      steps.append("Success")
      return steps

    if a == 0:
      a = a_cap
      steps.append("Fill A")
    elif b == b_cap:
      b = 0
      steps.append("Empty B")
    else:
      move = min(a, b_cap - b) # 計算要倒多少水
      a = a - move
      b = b + move
      steps.append("Pour A B")

    if len(steps) > 1000:
      return None


def try_b_to_a(a_cap, b_cap, target):
  a = 0
  b = 0
  steps = []

  while True:
    if b == target:
      steps.append("Success")
      return steps

    if b == 0:
      b = b_cap
      steps.append("Fill B")
    elif a == a_cap:
      a = 0
      steps.append("Empty A")
    else:
      move = min(b, a_cap - a)
      b = b - move
      a = a + move
      steps.append("Pour B A")

    if len(steps) > 1000:
      return None


def solve(a_cap, b_cap, target):
  if target == 0:
    return ["Success"]

  ans = try_a_to_b(a_cap, b_cap, target)
  if ans is not None:
    return ans

  ans = try_b_to_a(a_cap, b_cap, target)
  return ans


case_num = 1

while True:
  a_cap, b_cap, target = map(int, input().split())

  if a_cap == 0 and b_cap == 0 and target == 0:
    break

  result = solve(a_cap, b_cap, target)

  print("Case #" + str(case_num))
  for step in result:
    print(step)
  print()

  case_num += 1