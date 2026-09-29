# 演算法分析機測
# 學號 : 11227203 / 11227236 / 11227246
# 姓名 : 謝采凌 / 曹湘婷 / 徐雨瑄
# 中原大學資訊工程系

from itertools import permutations
from fractions import Fraction

operators = ['+', '-', '*', '/']
no_answer = "No Solutions"


def calculate(a, op, b):
  if op == '+':
    return a + b
  elif op == '-':
    return a - b
  elif op == '*':
    return a * b
  else:
    if b == 0:
      return None
    return a / b


def get_priority(op):
  if op == '+' or op == '-':
    return 1
  else:
    return 2


def merge_expression(left, op, right):
  left_value, left_text, left_priority = left
  right_value, right_text, right_priority = right

  result_value = calculate(left_value, op, right_value)
  if result_value is None:
    return None

  current_priority = get_priority(op)

  if left_priority < current_priority:
    left_text = '(' + left_text + ')'

  if right_priority < current_priority:
    right_text = '(' + right_text + ')'
  elif (op == '-' or op == '/') and right_priority == current_priority:
    right_text = '(' + right_text + ')'

  result_text = left_text + op + right_text
  return (result_value, result_text, current_priority)


def solve(nums):
  for p in permutations(nums):
    a = (Fraction(p[0]), str(p[0]), 3)
    b = (Fraction(p[1]), str(p[1]), 3)
    c = (Fraction(p[2]), str(p[2]), 3)
    d = (Fraction(p[3]), str(p[3]), 3)

    for op1 in operators:
      for op2 in operators:
        for op3 in operators:

          # 1. ((a op1 b) op2 c) op3 d
          x1 = merge_expression(a, op1, b)
          if x1 is not None:
            x2 = merge_expression(x1, op2, c)
            if x2 is not None:
              x3 = merge_expression(x2, op3, d)
              if x3 is not None and x3[0] == 24:
                return x3[1] + "=24"

          # 2. (a op1 (b op2 c)) op3 d
          x1 = merge_expression(b, op2, c)
          if x1 is not None:
            x2 = merge_expression(a, op1, x1)
            if x2 is not None:
              x3 = merge_expression(x2, op3, d)
              if x3 is not None and x3[0] == 24:
                return x3[1] + "=24"

          # 3. a op1 ((b op2 c) op3 d)
          x1 = merge_expression(b, op2, c)
          if x1 is not None:
            x2 = merge_expression(x1, op3, d)
            if x2 is not None:
              x3 = merge_expression(a, op1, x2)
              if x3 is not None and x3[0] == 24:
                return x3[1] + "=24"

          # 4. a op1 (b op2 (c op3 d))
          x1 = merge_expression(c, op3, d)
          if x1 is not None:
            x2 = merge_expression(b, op2, x1)
            if x2 is not None:
              x3 = merge_expression(a, op1, x2)
              if x3 is not None and x3[0] == 24:
                return x3[1] + "=24"

          # 5. (a op1 b) op2 (c op3 d)
          x1 = merge_expression(a, op1, b)
          x2 = merge_expression(c, op3, d)
          if x1 is not None and x2 is not None:
            x3 = merge_expression(x1, op2, x2)
            if x3 is not None and x3[0] == 24:
              return x3[1] + "=24"

  return no_answer


while True:
  nums = list(map(int, input().split()))

  if nums == [0, 0, 0, 0]:
    break

  if any(x < 1 or x > 13 for x in nums):
        print("No Solutions")
        continue
  
  print(solve(nums))