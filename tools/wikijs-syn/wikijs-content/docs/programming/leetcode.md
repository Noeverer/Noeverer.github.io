# LeetCode

LeetCode 刷题笔记和解题思路。

## 数据结构

### 数组和字符串

#### 两数之和 (Two Sum)

给定一个整数数组 `nums` 和一个整数目标值 `target`，找出和为目标值的那两个整数。

```python
def twoSum(nums, target):
    hashmap = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in hashmap:
            return [hashmap[complement], i]
        hashmap[num] = i
    return []
```

### 链表

#### 反转链表

```python
def reverseList(head):
    prev = None
    current = head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    return prev
```

### 树

#### 二叉树的中序遍历

```python
def inorderTraversal(root):
    result = []
    def traverse(node):
        if node:
            traverse(node.left)
            result.append(node.val)
            traverse(node.right)
    traverse(root)
    return result
```

## 算法

### 排序

#### 快速排序

```python
def quickSort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quickSort(left) + middle + quickSort(right)
```

### 搜索

#### 二分查找

```python
def binarySearch(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 解题技巧

1. **暴力法**: 先用最简单的方法解决，确保正确
2. **优化空间复杂度**: 从 O(n) 优化到 O(1)
3. **优化时间复杂度**: 从 O(n²) 优化到 O(n)
4. **使用数据结构**: 合理使用哈希表、栈、队列等

## 资源

- [LeetCode 官网](https://leetcode.com/)
- [算法可视化](https://visualgo.net/)
