---
title: Best Time To Buy And Sell Stock
date: 2019-08-01 12:00:00
tags: ["leetcode", "algorithm", "code"]
categories: leetcode
description: 121. Best Time to Buy and Sell Stock   python class Solution: def maxProfitself, prices: Listint - int: length  lenprices minprices  floatinf maxprofit  0 for i in rangelength: if
---
# 121. Best Time to Buy and Sell Stock
 
```python
class Solution:
def maxProfit(self, prices: List[int]) -> int:
length = len(prices)
minprices = float("inf")
maxprofit = 0
for i in range(length):
if prices[i] < minprices:
# 找到最低的点，如果不是最低点，就有可能产生maxprofit的点
minprices = prices[i]
elif (prices[i] - minprices) > maxprofit:
maxprofit = prices[i] -minprices
return maxprofit
```