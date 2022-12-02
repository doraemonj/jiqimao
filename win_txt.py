# 将deepL Pro翻译除中文txt文档（book_name_zh.html）
# 与英文原文档（book_name_en.html）合并
# 做成左右中英对照格式的文档（book_name_bi_en_zh.html）/Users/tangqiang/books/j22_other_peoples_money
import os
import shutil
from bs4 import BeautifulSoup
import time
from pathlib import Path
import libmind

translated_date = time.strftime("%Y-%m-%d", time.localtime())

book_no = "003"
book_name = "the_art_of_loving"

title_en = "The Art Of Loving"
title_zh = "爱的艺术"

# 增加清除DeepL文本的函数工具（参考李笑来github代码库）

# 复制所有广告图片
def copy_allfiles(src, dest):
    '''
    复制文件夹内所有文件：src:原文件夹；dest:目标文件夹
    '''
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)

# Python基础路径设置及待复制：
python_path = Path(r"F:\jiqimao")
css_file = r"style.css"

# 第一步：读取英文和中文文档，设置输出双语文件名
path = Path(r"F:\books\{}_{}".format(book_no,book_name))

# ===2022-10-25 调试代码：复制广告图片文件和style.css文件
copy_allfiles(python_path / r"ad_img", path / r"images")              # 复制广告图片
shutil.copyfile(python_path / r"style.css", path / r"style.css")      # 复制css文件


# 第一步：读取英文和中文文档，设置输出双语文件名
path = Path(r"F:\books\{}_{}".format(book_no,book_name))
file_en = "{}_en.txt".format(book_name)
file_zh = "{}_zh.txt".format(book_name)
file_bi = "{}_bi_txt_img_en_zh.html".format(book_name)
txt_en = open(path / file_en, "r", encoding="utf-8").read()    # 读取英文文件
txt_zh = open(path / file_zh, "r", encoding="utf-8").read()    # 读取中文文件

# 第二步：将英文和中文文件按段落排列好，
lst_en=[]
lst_en=txt_en.split("\n")

# 清除列表中的空格
for el in lst_en:
    if len(el.strip()) == 0:
        lst_en.remove(el)
# # 将列表写入txt文件
# with open('{}{}_en_edt_x.txt'.format(path, book_name), 'w') as f:
#     for el in lst_en:
#         f.write(el)
#         f.write("\n\n")

lst_zh=[]
lst_zh=txt_zh.split("\n")
for el in lst_zh:
    if len(el.strip()) == 0:
        lst_zh.remove(el)
# 过滤中文格式
lst_zh_format = []
for el in lst_zh:
    new_el = libmind.zh_format(el)
    lst_zh_format.append(new_el)
lst_zh = lst_zh_format


# 判断中英文两个数组的数量是否一致
if len(lst_en) == len(lst_zh):
    print(f"中英文数组长度一致，均为{len(lst_zh)}")
else:
    print(f"中英文数组长度不一致：英文{len(lst_en)}行，中文{len(lst_zh)}行")
    print(f"请检查！")

# 创建双语一一对应切按序的列表，吧lst_en和lst_zh中的元素逐一列入：
lst_bi = []
for i, el_en in enumerate(lst_zh):
    lst_bi.append((lst_en[i], lst_zh[i]))


# 输出book_name_bi_en_zh.html文档

# .1）输出标题头
html_head = libmind.html_head.format(title_en, title_zh, translated_date)

with open(path / file_bi, "a", encoding="utf-8") as f:
    f.write(f"{html_head}\n")

# .2）输出主干部分（仅文字）
for el in (lst_bi):
    if lst_bi[0]=="" and lst_bi[1]=="":
        continue
    else:
        with open(path / file_bi, "a", encoding ="utf-8") as f:
            f.write(f'<div class ="bottom">\n<div class ="top left">\n')
            f.write(f'<p class ="en">{el[0]}</p>')
            f.write(f'</div>\n<div class="top right">\n')
            f.write(f'<p class ="cn">{el[1]}</p>')
            f.write(f'</div>\n</div>\n')

# .3)输出末尾部分
html_end = libmind.html_end
with open(path / file_bi, "a", encoding="utf-8") as f:
    f.write(f"{html_end}")
    f.write(f"</body>\n</html>")