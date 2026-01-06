---
title: Decrease Elements To Make Array Zigzag
date: 2019-08-01 12:00:00
tags: ["leetcode", "algorithm", "code"]
categories: leetcode
description: 1144.Decrease Elements To Make Array Zigzag   Given an array nums of integers, a move consists of choosing any element and decreasing it by 1.   An array A is a zigzag array if either:  - Every even
---
# 1144.Decrease Elements To Make Array Zigzag
 
Given an array nums of integers, a move consists of choosing any element and decreasing it by 1.
 
An array A is a zigzag array if either:
 - Every even-indexed element is greater than adjacent elements, ie. A[0] > A[1] < A[2] > A[3] < A[4] > ... - OR, every odd-indexed element is greater than adjacent elements, ie. A[0] < A[1] > A[2] < A[3] > A[4] < ... 
Return the minimum number of moves to transform the given array nums into a zigzag array.
 
Example 1:
 
```python
Input: nums = [1,2,3]
Output: 2
Explanation: We can decrease 2 to 0 or 3 to 1.
```
 
Example 2:
 
```python
Input: nums = [9,6,1,6,2]
Output: 4
```
 
```python
class Solution(object):
def movesToMakeZigzag(self, nums):
"""
:type nums: List[int]
:rtype: int
"""
'''题意理解错误
我一开始的理解是以为理解一次操作（就是比如2 to 0）代表两次的moves
这样的话我的思路就变成一个寻找'''
# def peak(a,b,c):
# if a < b and b > c and a!=c:
# return 0
# else:
# return
# def valley(a,b,c):
# if a > b and b < c and a!= c:
# return 0
# else:
# return 2
# length = len(nums)
# i = 0
# '''even'''
# while i < length -2:
# p = peak(nums[i-1],nums[i],nums[i+1])
# i += 1
# v = valley(nums[i-1],nums[i],nums[i+1])
# i += 1
# print(p,v,1111)
# return (p+v)
```
 
# APPROACH ONE
 
```python
'''copy lee215'''
def movesToMakeZigzag(self, nums):
A = [float("inf")] + nums + [float("inf")]
res = [0,0]
for i in xrange(1,len(A)-1):
res[i%2] += max(0,A[i]-min(A[i-1],A[i+1])+1)
return min(res)
```
 
## 自己分析
 
from your python code , i learn that
 - the comparison among adjacent element and the pivot in elements - how to count even and odd in a array respectively