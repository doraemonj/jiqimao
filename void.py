# 给定一个字符串s，找出这样一个子串：
# 子串符合两个条件：
# 1）该子串中的任意一个字符串最多出现2次；
# 2）该子串不包含指定某个字符

import re

excluded = input()
s = input()

# 计数字典
dicts = {}

# 最长子串长度
max_len = 0

# 遍历字符串
for i in range(len(s)):
    tmp_str = ""
    tmp_dict = {}
    for j in range(i, len(s)):
        # 条件：
        # 如果字符不是指定排除字符，并且字符数出现次数小于2次
        if s[j] != excluded and tmp_dict.get(s[j], 0)< 2:
            tmp_str += s[j]
            tmp_dict[s[j]] = tmp_dict.get(s[j], 0) + 1
        else:
            break
    # 若子串长度大于最大子串长度，则更新
    if len(tmp_str) > max_len:
        max_len = len(tmp_str)



print(max_len)


