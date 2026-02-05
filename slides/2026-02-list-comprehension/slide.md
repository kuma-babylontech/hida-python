---
title: "リスト内包表記とジェネレータ"
date: 2026-02-12
description: "Pythonの強力な機能であるリスト内包表記とジェネレータについて解説します。"
tags:
  - 中級
  - パフォーマンス
author: "hida-python"
---

# リスト内包表記と
# ジェネレータ

飛騨高山Pythonの会 2026年2月

---

## リスト内包表記とは

従来のforループ:

```python
squares = []
for x in range(10):
    squares.append(x ** 2)
```

リスト内包表記:

```python
squares = [x ** 2 for x in range(10)]
```

---

## 条件付きリスト内包表記

```python
# 偶数のみを抽出
evens = [x for x in range(20) if x % 2 == 0]

# 条件分岐
labels = ["偶数" if x % 2 == 0 else "奇数"
          for x in range(5)]
```

---

## 辞書・集合内包表記

```python
# 辞書内包表記
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 集合内包表記
unique_lengths = {len(word) for word in words}
```

---

## ジェネレータ式

```python
# リスト内包表記（メモリに全要素を保持）
nums_list = [x ** 2 for x in range(1000000)]

# ジェネレータ式（遅延評価）
nums_gen = (x ** 2 for x in range(1000000))
```

メモリ効率が大幅に向上!

---

## ジェネレータ関数

```python
def fibonacci(n):
    """フィボナッチ数列のジェネレータ"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# 使用例
for num in fibonacci(10):
    print(num)
```

---

## パフォーマンス比較

| 方式 | メモリ使用量 | 処理速度 |
|------|-------------|---------|
| forループ | 中 | 遅い |
| リスト内包表記 | 高 | 速い |
| ジェネレータ | 低 | 中程度 |

---

## まとめ

- リスト内包表記は簡潔で高速
- ジェネレータはメモリ効率が良い
- 用途に応じて使い分けよう

---

# ありがとうございました

質問があればどうぞ!
