# 演算法分析機測
# 學號: 11227203 11227236/11227246
# 姓名: 謝采凌/曹湘婷/徐雨瑄
# 中原大學資訊工程系


# 計算兩個數列的最長共同子序列長度
def lcs_length(a, b):

    # 第一座塔有幾塊石頭
    n = len(a)

    # 第二座塔有幾塊石頭
    m = len(b)

    # 準備建立動態規劃表格
    dp = []

    # 建立 n+1 列
    for i in range(n + 1):

        # 先建立一個空的橫列
        row = []

        # 每一列建立 m+1 個 0
        for j in range(m + 1):
            row.append(0)

        # 把這一列放進 dp 表格
        dp.append(row)

    # 開始比較兩座塔的石頭
    for i in range(1, n + 1):
        for j in range(1, m + 1):

            # 如果目前兩塊石頭的半徑相同
            if a[i - 1] == b[j - 1]:

                # 左上角的答案加 1
                dp[i][j] = dp[i - 1][j - 1] + 1

            # 如果目前兩塊石頭不同
            else:

                # 比較上方和左方，保留較大的答案
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 表格右下角就是完整問題的答案
    return dp[n][m]


# 記錄目前是第幾組測試資料
case = 1

# 不斷讀取測試資料
while True:

    # 讀取兩座塔的高度
    n1, n2 = map(int, input().split())

    # 輸入 0 0 代表結束
    if n1 == 0 and n2 == 0:
        break

    # 讀取第一座塔的石頭半徑
    tower1 = list(map(int, input().split()))

    # 讀取第二座塔的石頭半徑
    tower2 = list(map(int, input().split()))

    # 呼叫函式，計算最高的共同高度
    ans = lcs_length(tower1, tower2)

    # 按照題目要求輸出
    print(f"Twin Towers #{case}")
    print(f"Number of Tiles : {ans}")

    # 輸出空白行
    print()

    # 下一組測資
    case += 1