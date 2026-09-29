# Algorithm Analysis - Programming Tests

這個 repository 收錄我在「演算法分析」課程兩次機測中完成的程式。

兩次機測各有 5 題，主要練習不同類型的演算法問題，包含樹、圖形、搜尋、動態規劃、編碼、迷宮與影像處理等。  
我把程式整理放在這裡，方便之後複習，也可以直接查看每一題的實作內容。

---

## 使用語言

- Python

部分題目另外使用：

- OpenCV
- NumPy

---

# 第一次機測

## 1. Binary Search Tree

給定 Binary Search Tree 的 Preorder Traversal，輸出對應的 Postorder Traversal。

### 主要內容

- Binary Search Tree
- Preorder Traversal
- Postorder Traversal
- Tree Traversal

---

## 2. Hamiltonian Cycle

給定一張圖，從 Vertex 1 出發，找出一條走訪所有頂點一次後再回到 Vertex 1 的 Hamiltonian Cycle。

### 主要內容

- Graph
- Vertex / Edge
- Hamiltonian Cycle
- 路徑搜尋

---

## 3. Poker 24-Point Game

輸入 4 張撲克牌的數值，使用 `+ - * /` 以及括號組合出結果為 24 的算式。

每張牌只能使用一次，如果無法得到 24，則輸出：

```text
No Solutions
```

### 主要內容

- 四則運算
- 排列組合
- Expression Search
- Case Enumeration

---

## 4. Water Jug Puzzle

給定兩個不同容量的水桶與目標水量，找出可以讓水桶 B 得到指定水量的操作順序。

允許的操作包含：

```text
Fill
Empty
Pour
```

最後輸出完整的操作流程直到：

```text
Success
```

### 主要內容

- State Search
- 狀態轉移
- 路徑搜尋

---

## 5. Pushing Box Game

在二維迷宮中將 Box 推到指定 Target。

除了需要成功把箱子推到終點之外，也需要讓推動箱子的次數盡量少；如果有多組相同推箱次數的解，再比較總移動次數。

### 主要內容

- Maze
- State Search
- Path Finding
- Box Pushing
- 最短路徑問題

---

# 第二次機測

## 1. Twin Towers

給定兩座塔的石塊排列，在維持原本順序的情況下，找出兩座塔可以保留下來的最大相同高度。

### 主要內容

- Sequence
- Dynamic Programming
- Longest Common Subsequence

---

## 2. Huffman Codes

根據每個字元的出現頻率建立 Huffman Code。

除了輸出每個字元對應的編碼之外，也需要利用建立好的 Huffman Code 對指定的二進位字串進行解碼。

### 主要內容

- Huffman Coding
- Binary Tree
- Encoding
- Decoding
- Data Compression

---

## 3. Chess Knight

給定西洋棋棋盤上的兩個座標，計算 Knight 從起點移動到終點最少需要幾步。

棋盤大小固定為：

```text
8 x 8
```

### 主要內容

- Graph Search
- Shortest Path
- Chessboard State

---

## 4. Maze Problem

輸入一張 500 x 500 的迷宮影像，將影像轉換成可以搜尋的迷宮資料後，找出從左上角到右下角的最短路徑。

最後將找到的路徑畫回原始影像中，並輸出結果影像。

### 影像規格

- 24-bit RGB
- 500 x 500 pixels
- 每個 cell 為 20 x 20 pixels
- 總共 25 x 25 個格子
- 最短路徑以藍線表示

### 主要內容

- Maze
- Shortest Path
- Image Processing
- OpenCV
- NumPy

---

## 5. Puzzle

輸入一張被打亂的拼圖影像，將每一塊拼圖視為節點，分析拼圖邊緣之間的相似程度，再找出拼圖之間最可能的相鄰關係。

題目中的拼圖規格：

```text
原始影像：1920 x 1080
拼圖大小：120 x 120
拼圖數量：16 x 9
```

最後重新組合並輸出完整影像。

### 主要內容

- Graph
- Image Processing
- Edge Similarity
- Minimum Spanning Tree
- Kruskal / Prim
- OpenCV

---

# 題目整理

| 機測 | 題目 | 主要內容 |
|---|---|---|
| 第一次 | Binary Search Tree | Tree Traversal |
| 第一次 | Hamiltonian Cycle | Graph / Path Search |
| 第一次 | Poker 24-Point Game | Expression Search |
| 第一次 | Water Jug Puzzle | State Search |
| 第一次 | Pushing Box Game | Maze / Path Finding |
| 第二次 | Twin Towers | Dynamic Programming / LCS |
| 第二次 | Huffman Codes | Huffman Tree / Coding |
| 第二次 | Chess Knight | Shortest Path |
| 第二次 | Maze Problem | Maze / Image Processing |
| 第二次 | Puzzle | Graph / MST / Image Processing |

---

# 我做完這些題目後

這兩次機測讓我把很多原本只在課堂上看到的演算法實際寫成程式。

從一開始的 Tree、Graph、搜尋問題，到後面的 Dynamic Programming、Huffman Coding、Maze、Image Processing 和 Puzzle，都需要先把題目轉成適合程式處理的資料，再決定要怎麼搜尋或計算。

我覺得最大的差別是，真的自己寫過之後，會比較清楚每一種演算法到底是在什麼情況下使用，而不只是記住它的名稱。

---

## Notes

此 repository 主要作為課程實作紀錄與個人複習使用。
