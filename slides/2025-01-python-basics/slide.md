---
title: "Pythonの基礎"
date: 2025-01-15
description: "Python入門者向けの基礎文法解説。変数、データ型、制御構文について学びます。"
tags:
  - 基礎
  - 入門
author: "hida-python"
---

# Pythonの基礎

Python勉強会 2025年1月

---

## 今日の内容

- 変数とデータ型
- 演算子
- 制御構文
- 関数の基本

---

## 変数とデータ型

```python
# 変数の定義
name = "Python"
version = 3.12
is_awesome = True

# 型の確認
print(type(name))     # <class 'str'>
print(type(version))  # <class 'float'>
```

---

## リストと辞書

```python
# リスト
fruits = ["apple", "banana", "orange"]
fruits.append("grape")

# 辞書
person = {
    "name": "Alice",
    "age": 30
}
```

---

## 制御構文

```python
# if文
if x > 0:
    print("正の数")
elif x < 0:
    print("負の数")
else:
    print("ゼロ")

# forループ
for i in range(5):
    print(i)
```

---

## 関数の定義

```python
def greet(name: str) -> str:
    """挨拶を返す関数"""
    return f"Hello, {name}!"

# 使用例
message = greet("Python")
print(message)  # Hello, Python!
```

---

## まとめ

- Pythonは動的型付け言語
- シンプルで読みやすい文法
- 豊富な標準ライブラリ

---

# ありがとうございました

次回: リスト内包表記とジェネレータ
