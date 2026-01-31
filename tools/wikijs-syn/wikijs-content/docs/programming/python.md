# Python

Python 编程相关笔记和技巧。

## 基础

### 数据结构

Python 提供了丰富的内置数据结构：

- **列表 (List)**: 有序、可变
- **元组 (Tuple)**: 有序、不可变
- **字典 (Dict)**: 键值对
- **集合 (Set)**: 无序、唯一

### 常用操作

```python
# 列表推导式
squares = [x**2 for x in range(10)]

# 字典推导式
word_counts = {word: text.count(word) for word in set(text.split())}
```

## 高级特性

### 装饰器

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before function call")
        result = func(*args, **kwargs)
        print("After function call")
        return result
    return wrapper

@decorator
def hello():
    print("Hello, World!")
```

### 生成器

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

for num in fibonacci():
    if num > 100:
        break
    print(num)
```

## 资源

- [Python 官方文档](https://docs.python.org/)
- [Python 之禅](https://peps.python.org/pep-0020/)
