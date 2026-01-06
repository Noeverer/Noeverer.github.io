---
title: Sort An Array
date: 2019-08-01 12:00:00
tags: ["leetcode", "algorithm", "code"]
categories: leetcode
description: 912_Sort an Array    排序算法的讲解菜鸟教程   Given an array of integers nums, sort the array in ascending order.   Example 1:   python Input: 5,2,3,1 Output: 1,2,3,5    Example 2:   python Inpu
---
# 912_Sort an Array
 
## 排序算法的讲解菜鸟教程
 
Given an array of integers nums, sort the array in ascending order.
 
Example 1:
 
```python
Input: [5,2,3,1]
Output: [1,2,3,5]
```
 
Example 2:
 
```python
Input: [5,1,1,2,0,0]
Output: [0,0,1,1,2,5]
```
 
Note:
 1. 1 <= A.length <= 10000 2. -50000 <= A[i] <= 50000 
## 冒泡排序
 
```python
def sortArray(self, nums: List[int]) -> List[int]:
'''Bubble Sort'''
for i in range(1,len(nums)):
issort = True
for j in range(0,len(nums)-i):
if nums[j] > nums[j+1]:
nums[j], nums[j+1] = nums[j+1],nums[j]
issort = False
if issort:
break
return nums
```
 
## 选择排序
 
```python
'''Picking Sort'''
def sortArray(self, nums: List[int]) -> List[int]:
length = len(nums)
for i in range(length -1):
min_index = i
for j in range((i+1), length):
if nums[j] < nums[min_index]:
min_index = j
if i != min_index:
nums[i] , nums[min_index] = nums[min_index] ,nums[i]
return nums
```
 
## 插入排序
 
```python
def sortArray(self, nums: List[int]) -> List[int]:
for i in range(len(nums)):
preindex = i -1
current = nums[i]
while preindex >= 0 and nums[preindex] > current:
nums[preindex + 1] = nums[preindex]
preindex -= 1
nums[preindex +1] = current
return nums
```
 
## 希尔排序
 
```python
def sortArray(self, nums: List[int]) -> List[int]:
import math
gap=1
while(gap < len(nums)/3):
gap = gap*3+1
while gap > 0:
for i in range(gap,len(nums)):
temp = nums[i]
j = i-gap
while j >=0 and nums[j] > temp:
nums[j+gap]=nums[j]
j-=gap
nums[j+gap] = temp
gap = math.floor(gap/3)
return nums
```
 
## 归并排序(Merge Sort)
 
```python
def merge_sort(nums):
if len(nums) < 2:
return nums
pivot = len(nums) // 2
left = merge_sort(nums[:pivot])
right = merge_sort(nums[pivot:])
return merge(left,right)
def merge(left,right):
left_cursor = right_cursor = 0
ret = []
while left_cursor < len(left) and right_cursor < len(right):
# print(left[left_cursor],right[right_cursor],1111)
if left[left_cursor] < right[right_cursor]:
ret.append(left[left_cursor])
left_cursor += 1
else:
ret.append(right[right_cursor])
right_cursor += 1
ret.extend(left[left_cursor:])
ret.extend(right[right_cursor:])
return ret
return merge_sort(nums)
```
 
## 快速排序(Quicksort)
 
```python
def sortArray(self, nums):
'''quick sort'''
def quicksort(lst):
"""
Sorts an array in the ascending order in O(n log n) time
:param nums: a list of numbers
:return: the sorted list
"""
n = len(lst)
qsort(lst, 0, n - 1)
return lst
def qsort(lst, lo, hi):
"""
Helper
:param lst: the list to sort
:param lo: the index of the first element in the list
:param hi: the index of the last element in the list
:return: the sorted list
"""
if lo < hi:
p = partition(lst, lo, hi)
qsort(lst, lo, p - 1)
qsort(lst, p + 1, hi)
def partition(lst, lo, hi):
"""
Picks the last element hi as a pivot
and returns the index of pivot value in the sorted array
"""
pivot = lst[hi]
i = lo
for j in range(lo, hi):
if lst[j] < pivot:
lst[i], lst[j] = lst[j], lst[i]
i += 1
lst[i], lst[hi] = lst[hi], lst[i]
return i
return quicksort(nums)
```