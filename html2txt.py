# 自动读取zh.html文件，转为txt，转到Google Drive中去
# 只借取『简介』，或第一章（第1章）之后的文字
# 自动转为

import time
import os
import shutil
from bs4 import BeautifulSoup
import time
import random
import libmind
import htmlz

# 开始计时
time_start=time.time()
translated_date = time.strftime("%Y-%m-%d", time.localtime())   # 电子书制作日期

# 设置Google Drive路径
txt_path = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/"

# 设置书号和书名
book_no = "007"
book_name = "the_lessons_of_history"

# 设置书名和作者的中英文名
book_name_en = "{}".format(book_name.replace("_", " ").title())
book_name_zh = "历史的教训"
author_name_en = "Will Durant"
author_name_zh = "威尔·杜兰特"

# 读取英文和中文文档，设置输出双语文件名
path = r"/Users/tangqiang/books/{}_{}/".format(book_no,book_name)
# Windows用户可更换为：path = r"D:\\books\\{}_{}\\".format(book_no, book_name)
file_zh = r"{}_zh.html".format(book_name)

html_zh = open(path + file_zh, 'r', encoding='utf-8').read()    # 读取中文文件
soup_zh = BeautifulSoup(html_zh, features='html.parser')  # 'lxml'
# 删除所有span标签
for span in soup_zh("span"):
    span.unwrap()
raw_zh = soup_zh.get_text(separator=" ")
lst_zh = raw_zh.split("\n")

if os.path.exists(path + file_zh[:-5] + ".txt"):
    os.rename(path + file_zh[:-5] + ".txt", path + str(random.randint(1000,9999))+" - "+file_zh[:-5] + ".txt")
    for el in lst_zh:
        if el == "":
            continue
        else:
            with open(path + file_zh[:-5] + ".txt", "a", encoding="utf-8") as f:
                el = el.replace(" ", "")
                f.write(f'{el}\n')
else:
    for el in lst_zh:
        if el == "":
            continue
        else:
            with open(path + file_zh[:-5] + ".txt", "a", encoding="utf-8") as f:
                el = el.replace(" ", "")
                f.write(f'{el}\n')

# 复制文件到Google Drive里去

txt_path = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/"
txt_file_name = file_zh[:-5] + ".txt"
full_txt_file_name = book_name_zh + " " + author_name_zh + " " + book_name_en + " By " + author_name_en + ".txt"
try:
   shutil.copy(path + txt_file_name, txt_path)
   os.rename(txt_path + txt_file_name, txt_path + full_txt_file_name)
except TypeError as e:
   print("IO错误报错{}".format(e))


# 计算时间
time_end=time.time()
print(f"本次html2txt流程消耗{time_end-time_start:.2f}秒")