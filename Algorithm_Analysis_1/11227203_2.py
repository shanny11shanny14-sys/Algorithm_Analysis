# 演算法分析機測
# 學號: 11227203 11227236/11227246
# 姓名: 謝采凌/曹湘婷/徐雨瑄
# 中原大學資訊工程系

def find_ans(total_dot, edges):

    the_dot = [] # 這裡會存每個點連到哪些點
    for i in range(total_dot + 1):
        the_dot.append([])

    # 無向圖，所以兩邊都要加
    for dot, attach in edges:
        the_dot[dot].append(attach)
        the_dot[attach].append(dot)

    # 排序一下，這樣會先走編號小的點
    for i in range(1, total_dot + 1):
        the_dot[i].sort()

    used = [False] * (total_dot + 1)
    ans = [1] # 從1開始走
    used[1] = True

    #=======================================================================

    def dfs(now):
        # 如果已經把所有點都走過了
        if len(ans) == total_dot:
            # 看最後能不能回到1
            if 1 in the_dot[now]:
                ans.append(1)
                return True
            return False

        # 一個一個試下一個點
        for dot in the_dot[now]:  # the_dot[now]會存每個點連到哪些點
            if used[dot] == False:
                used[dot] = True
                ans.append(dot)

                if dfs(dot): #遞迴
                    return True
                
                ans.pop()
                used[dot] = False

        return False

    dfs(1)
    return ans


out = []

while True:
    line = input() # 讀一行  total dot and total edge

    if line == "":
        continue
    parts = line.split()

    nums = []
    for p in parts:
        nums.append(int(p))

    total_dot = nums[0]
    total_edge = nums[1]

    if total_dot == 0 and total_edge == 0:
        break
#======================================================================
    edges = []
    for i in range(total_edge):
        line = input()
        parts = line.split()

        nums = []
        for p in parts:
            nums.append(int(p))

        edges.append((nums[0], nums[1]))
        

    res = find_ans(total_dot, edges)

    text_list = []
    for uu in res:
        text_list.append(str(uu))

    out.append(" ".join(text_list))

print("\n".join(out))