---
title: Leetcode Summary
date: 2019-08-01 12:00:00
tags: ["leetcode", "algorithm", "code"]
categories: leetcode
description: wp:table backgroundColor:subtle-pale-green,align:center,className:is-style-stripes Lhttps:leetcode.com eetCode - The Worlds Leading Online Programming Learning Platformhttps:
---
wp:table {"backgroundColor":"subtle-pale-green","align":"center","className":"is-style-stripes"} [L](https://leetcode.com/) [eetCode - The World’s Leading Online Programming Learning Platform](https://leetcode.com/problemset/all/) list[::]注意切割时候会生成新的list，所以新的list会有新的index Add Two Numbers 
 1.没想到只要检测到为None可使用数值0去取代， `x = l1.val if l1 else 0` 妙呀 2.carry进位使用的顺序问题，其实一开始我想用，但是不知道如何下手 滑动窗口题目：比较经典的流程和二分法有点相似 
 `cache = {} while l<length and r <length: if s[r] not in cache: cache[s[r]] = r r += 1 else: longest = max(longest , r-l) cache.pop(s[l]) l += 1 ` 想法1：在使用配对的时候，可以尝试使用从中间两边去扩充，但是需要考虑长度是奇偶的问题 想法2：寻找最大的回文串，指针一前一后去寻找的话，第一次找到就是最长的 实现数字的反转，需要好好记住 
 `# 实现反转 result = 0 while x: temp = result 10 + x % 10 if temp//10 != result: return 0 result = temp x //= 10 ` 解决思路：先升序排列（和为0只能从两头取一正一负）后使用双指针即可 》》 
 要是倒序删除某个值，可以使用一快一慢指针，让快指针先跑n个长度，在启用慢指针，这样快指针到达终点时，与慢指针刚好相差n个长度>> 
 **判断linklist长度是偶数还是奇数：主要看fast，如果fast是None的话，链表的长度是偶数，所以判断的时候用if not fast : (linklist length example#123456)** 使用stack的方式–整理思路可以想象成配对：一对人，在前面的是公头，后面的是母头，可以看出对公头进行存储是value，对母头存储是key，进行查询 
 `stack = []store = {‘)’:’(‘,’]’:’[‘,’}’:’{‘} # 为什么需要这样设计？for char in s: if char in store.values(): # 将正向的符号使用stack存储起来 stack.append(char) elif char in store.keys(): # 查找key进行配对 if stack == [] or store[char] != stack.pop(): return Falsereturn stack == [] ` 创造dummy节点用来串接两个链表较大的值/交换头节点 矩阵旋转技巧 clockwise rotate *first zip(* a)使用 
 >>> a = [[1,2,3],[4,5,6],[7,8,9]] 
 >>> d = zip( *a) >>> next(d) (1, 4, 7)* 使用的collections.defaultdict函数/sorted()接受迭代对象返回list/对字符出现频率进行统计 
 `def groupAnagrams(strs): ans = collections.defaultdict(list) for s in strs: count = [0] 26 for c in s: count[ord(c) - ord(‘a’)] += 1 ans[tuple(count)].append(s) return ans.values() ` DP动态规划：典型动态规划模板 
 `for i in range(1, len(nums)): if nums[i-1] > 0: # 对前面的每一项之和进行判断，妙呀 nums[i] += nums[i-1] return max(nums) ` 想法：思想，就是在第一行和第一列设置flag（就是将首先将他们置为0，后来第一行和第一列的值就好了） 
 使用迭代只能对一个list进行置零，要是想给一列置零还需要遍历下标 从list后面开始比较，这样的好处是前面排过序的部分不用反复排序 其实使用recursion遍历，没有办法中间停止，但是使用iteration可以中间暂停 
 `def inorderTraversal(self, root): res = [] if root: res += self.inorderTraversal(root.left) res.append(root.val) res += self.inorderTraversal(root.right) return res # iteratively def inorderTraversal(self, root): res, stack = [], [] while True: while root: stack.append(root) root = root.left if not stack: return res node = stack.pop() res.append(node.val) root = node.right ` **queue使用/BFS>>** **需要总结：** 初始化定义ans的方式def **init** (self):>> 105. Construct Binary Tree from Preorder and Inorder Traversal 
 ` def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode: if not preorder or not inorder: return None root = TreeNode(preorder.pop(0)) index = inorder.index(root.val) root.left = self.buildTree(preorder,inorder[: index]) root.right = self.buildTree(preorder , inorder[index+1:]) return root ` 116/117：node添加和检验方式 
 `while queue: cur_level , size = [] ,len(queue) for i in range(size): node = queue.popleft() if node: queue.append(node.left) queue.append(node.right) cur_level.append(node) # 将每层的node值添加进cur_level for index,node in enumerate(cur_level[:-1]): node.next = cur_level[index+1] cur_level[-1].next = None ` 一个点要么是最低点要么是差值最大点, 异或使用So we can XOR all bits together to find the unique number. 
 a⊕b⊕a=(a⊕a)⊕b=0⊕b=b `a = 1 if 0 else 2` 使用结构>> 逻辑解读： 
 `if 0 : a = 1 else: a =21` [189. Rotate Array](https://leetcode.com/problems/rotate-array/) 
 让数字在一定范围内循环递增常常使用 % 操作 
 注意点：当循环在一个list中，比如list=[1,2,3,4]，当寻找index=5时，希望循环list里面的元素，使用index = index % len(list) 
 来自 < [https://github.com/cy69855522/Shortest-LeetCode-Python-Solutions/blob/master/README.md#-%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE](https://github.com/cy69855522/Shortest-LeetCode-Python-Solutions/blob/master/README.md#-%E4%BA%8C%E5%88%86%E6%9F%A5%E6%89%BE) > 创造dummy节点以满足整体性dummy_head= ListNode(-1) [217. Contains Duplicate](https://leetcode.com/problems/contains-duplicate/) 
 像这一类的重复问题的查找，基本上是有两种思路：–使用hash性质的set/dict，–或者使用异或的数学解决 做法和参考做法其实比较关键的还是reversed first half 部分不一样，但是微妙之处我还是没有能体会到，但是收获是链表反转 dict统计序列中重复出现频次/使用list统计有限个数出现频次 
 ` for item in s: dic1[item] = dic1.get(item, 0) + 1` 
 说明dict.get(item , default =0) 表示如果在字典中查找到item（dic1中的key）返回value，要是没有找到返回default值（为0），实现统计意义 [283.Move Zeroes](https://leetcode.com/problems/move-zeroes/) 
 交换两个值的时候a，b = b，a 
 while循环的中断点需要加break [349. Intersection of Two Arrays](https://leetcode.com/problems/intersection-of-two-arrays/) 
 set操作时间空间都是O(1) 
 来自 < [https://leetcode.com/problems/intersection-of-two-arrays/solution/](https://leetcode.com/problems/intersection-of-two-arrays/solution/) > 
 ` To solve the problem in linear time, let’s use the structure set, which provides in/contains operation in O(1) time in average case. list(set2 & set1)查找出公共元素 list转化为set都需要O(n)的空间 Complexity Analysis Time complexity : O(n+m), where n and m are arrays’ lengths.O(n) time is used to convert nums1into set,O(m) time is used to convert nums2, and contains/in operations are O(1) in the average case. Space complexity : O(m+n) in the worst case when all elements in the arrays are different. ` 灵活使用collections.Counter进行对数组的统计 dict统计字频使用的是：count = collections.Counter(s) [412. Fizz Buzz](https://leetcode.com/problems/fizz-buzz/) 
 >>>来自 < [https://leetcode.com/problems/fizz-buzz/](https://leetcode.com/problems/fizz-buzz/) > 
 利用字典存储对应的值，但是要想两个字典进行融合输出 fizz_buzz_dict = {3 : “Fizz”, 5 : “Buzz”} >>>想要输出3/5的组合即15 = 3 *5使用对字典循环 fizz_buzz_dict = {3 : “Fizz”, 5 : “Buzz”} >>>想要输出3/5的组合即15 = 3* 5使用对字典循环 
 num_ans_str = “” 
 for key in fizz_buzz_dict.keys(): 
 # If the num is divisible by key, 
 # then add the corresponding string mapping to current num_ans_str 
 if num % key == 0: 
 num_ans_str += fizz_buzz_dict[key] # 其实这个地方3/5分两部分进行添加 判断单词的大小写 
 520. Detect Capital 
 对所有单词判断大写all(‘A’ <= ch <= ‘Z’ for ch in word) 
 对每个单词进行标记 
 ` c = 0 for i in word: if i == i.upper(): c += 1 return c == len(word) or (c == 1 and word[0] == word[0].upper()) or c == 0 ` **使用and去掉root = None的情况** **stack = root and [root]>>** 
 **>>** /wp:table