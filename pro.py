# 将deepL Pro翻译除中文html文档（book_name_zh.html）
# 与英文原文档（book_name_en.html）合并
# 做成左右中英对照格式的文档（book_name_bi_en_zh.html）/Users/tangqiang/books/e33_identity

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

# Python基础路径设置及待复制：
python_path = r"/Users/tangqiang/jiqimao/"
# Windows用户可更换为：python_path = r"C:\\Users\\Administrator\\jiqimao\\"
# 并调整文件路径

book_no = "001"
book_name = "go_pro"

# 第一步：读取英文和中文文档，设置输出双语文件名
path = r"/Users/tangqiang/books/{}_{}/".format(book_no,book_name)
# Windows用户可更换为：path = r"D:\\books\\{}_{}\\".format(book_no, book_name)
# 并调整文件路径

css_file = r"style.css"
file_en = r"{}_en.html".format(book_name)
file_zh = r"{}_zh.html".format(book_name)
file_bi = r"{}_bi_en_zh.html".format(book_name)

# ===查看是否存在image文件夹：若有则忽略，若不存在则创建 2022-11-21 17:20:39
image_dir = path + r"images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# ===2022-10-25 调试代码：复制广告图片文件和style.css文件
libmind.copy_allfiles(python_path+"ad_img", path+"images")      # 复制广告图片
shutil.copyfile(python_path+"style.css", path+"style.css")      # 复制css文件

# ===读取中英文文件

html_en = open(path + file_en, 'r', encoding='utf-8').read()    # 读取英文文件
html_zh = open(path + file_zh, 'r', encoding='utf-8').read()    # 读取中文文件

# 第二步：将英文和中文文件按段落排列好，
soup_en = BeautifulSoup(html_en, features='html.parser')
# 删除所有span标签
for span in soup_en("span"):
    span.unwrap()
raw_en = soup_en.get_text(separator=" ")
lst_en = raw_en.split("\n")
len_en = len(lst_en)
len_en_new = 0
while len_en_new < len_en:
    len_en = len(lst_en)
    for el in lst_en:
        if len(el.strip())==0:
            lst_en.remove(el)
    len_en_new = len(lst_en)

# 取图片——取所有英文文档中的<img />标签，删除alt和class属性  2022-11-22
lst_img = soup_en("img")

# 分别计算每张图片的前一个和后一个要素，做成列表集：
# [图片,前一个非空元素的最后20个字符（若不满20个则以本身计）,后一个非空元素的前20个字符（若不满20个则以本身计）]
idx_img = []
try:
    for img_tag in lst_img:
        # 计算当前img_tag前一个非空元素的最后20个字符（若不满20个则以本身计）
        crt_img_prv_txt = img_tag.previous_element
        while len(crt_img_prv_txt.get_text().strip()) == 0:
            crt_img_prv_txt = crt_img_prv_txt.previous_element
        prv_img_txt = crt_img_prv_txt.get_text().replace("\n","")[-30:]

        # 计算当前img_tag后一个非空元素的前20个字符（若不满20个则以本身计）
        crt_img_nxt_txt = img_tag.next_element
        while len(crt_img_nxt_txt.get_text().strip()) == 0:
            crt_img_nxt_txt = crt_img_nxt_txt.next_element
        nxt_img_txt = crt_img_nxt_txt.get_text().replace("\n","")[:30]

        img_tag_wrap = img_tag
        # 将计算结果放入idx_img列表
        idx_img.append([img_tag, prv_img_txt, nxt_img_txt])
except:
    pass

soup_zh = BeautifulSoup(html_zh, features='html.parser')  # 'lxml'
# 删除所有span标签
for span in soup_zh("span"):
    span.unwrap()
raw_zh = soup_zh.get_text(separator=" ")
lst_zh = raw_zh.split("\n")

# 过滤中文格式
lst_zh_format = []
for el in lst_zh:
    new_el = libmind.zh_format(el)
    lst_zh_format.append(new_el)
lst_zh = lst_zh_format

len_zh = len(lst_zh)
len_zh_new = 0
while len_zh_new < len_zh:
    len_zh = len(lst_zh)
    for el in lst_zh:
        if len(el.strip())==0:
            lst_zh.remove(el)
    len_zh_new = len(lst_zh)

# 判断中英文两个数组的数量是否一致
if len(lst_en) == len(lst_zh):
    print(f"中英文数组长度一致，均为{len(lst_zh)}")
else:
    print(f"中英文数组长度不一致：英文{len(lst_en)}行，中文{len(lst_zh)}行")
    print(f"请检查！")

# 创建双语一一对应切按序的列表，吧lst_en和lst_zh中的元素逐一列入：
lst_bi = []
try:
    for i, el_en in enumerate(lst_en):
        if len(el_en.strip()) != 0 and len(lst_zh[i]) != 0:
            lst_bi.append((el_en, lst_zh[i]))
        else:
            print("中英文行数不一样，请确认")
            print(f"英文行数：{i}:{el_en}")
            print(f"中文行数：{i}:{lst_zh[i]}")
except:
    pass

# 输出book_name_bi_en_zh.html文档

# .1）输出标题头
html_head = libmind.html_head.format(soup_en.title.string, soup_zh.title.string, translated_date)
# 检查bilingual_html是否存在，若存在，在先改名：原文件名前加『backup=』，再删除源文件
if os.path.exists(path + file_bi):
    os.rename(path + file_bi, path + "backup-{}-".format(random.randint(1000,9999)) + file_bi)

with open(path + file_bi, "a", encoding="utf-8") as f:
    f.write(f"{html_head}\n")

# .2）输出主干部分（仅文字）
# 2022-11-22新增：图片计数器： img_num
img_num = 0
for i,el in enumerate(lst_bi):
    if el[0]=="" and el[1]=="":
        continue
    else:
        with open(path + file_bi, "a", encoding="utf-8") as f:
            f.write(f'<div class ="bottom">\n<div class ="top left">\n')
            f.write(f'<p class ="en">{el[0]}</p>')
            f.write(f'</div>\n<div class="top right">\n')
            f.write(f'<p class ="cn">{el[1]}</p>')
            f.write(f'</div>\n</div>\n')

            # 图片自动检测程序：若en.html文件内的img_tag前后30个非空字符满足，则自动插入图片链接：
            # 检测第一张图片是否符合条件，若符合条件，则插入，开始检测第二张：
            try:
                # 前后均有对应：
                if (idx_img[img_num][1].strip() in el[0] and len(idx_img[img_num][1].strip()) >= 4 or \
                    el[0].strip() in idx_img[img_num][1] and len(el[0].strip()) >= 4) and \
                    ((idx_img[img_num][2].strip() in lst_bi[i+1][0] and len(idx_img[img_num][2].strip()) >= 4) or
                     lst_bi[i+1][0].strip() in idx_img[img_num][2] and len(lst_bi[i+1][0].strip()) >= 4):
                    f.write(f"<div style='text-align: center'>{idx_img[img_num][0]}</div>\n")
                    print(f"========")
                    print(f"第{img_num + 1}张图片{idx_img[img_num][0].get('src')}完美插入")
                    print(f"{idx_img[img_num][1] = }")
                    print(f"前部：{el[0]}")
                    print(f"{idx_img[img_num][2] = }")
                    print(f"后部：{lst_bi[i+1][0]}")
                    print(f"========")
                    print(f"\n\n")
                    img_num += 1

                # 前部对应
                elif (idx_img[img_num][1].strip() in el[0] and len(idx_img[img_num][1]) >= 4) or \
                        (el[0] in idx_img[img_num][1].strip() and len(el[0]) >= 4) :
                    f.write(f"<div style='text-align: center'>{idx_img[img_num][0]}</div>\n")
                    print(f"========")
                    print(f"第{img_num + 1}张图片{idx_img[img_num][0].get('src')}前部对齐，建议人工审核")
                    print(f"{idx_img[img_num][1] = }")
                    print(f"前部：{el[0]}")
                    print(f"{idx_img[img_num][2] = }")
                    print(f"后部：{lst_bi[i+1][0] =}")
                    print(f"{idx_img[img_num][2] in lst_bi[i+1][0] = }")
                    print(f"{lst_bi[i+1][0] in idx_img[img_num][2] = }")
                    print(f"========")
                    print(f"\n\n")
                    img_num += 1

                # 后部对应
                elif idx_img[img_num][2].strip() in lst_bi[i+1][0] or lst_bi[i+1][0].strip() in idx_img[img_num][2]:
                    f.write(f"<div style='text-align: center'>{idx_img[img_num][0]}</div>\n")
                    print(f"========")
                    print(f"第{img_num + 1}张图片{idx_img[img_num][0].get('src')}后部对齐，建议人工审核")
                    print(f"{idx_img[img_num][1] = }")
                    print(f"前部：{el[0]}")
                    print(f"{idx_img[img_num][2] = }")
                    print(f"后部：{lst_bi[i+1][0]}")
                    print(f"========")
                    print(f"\n\n")
                    img_num += 1
            except:
                if img_num == len(idx_img):
                    print(f"图片匹配结束，共匹配{img_num}张")
                    img_num += 1
                elif img_num > len(idx_img):
                    pass
                else:
                    if img_num >= len(idx_img):
                        print(f"完成{img_num}张图片插入")
                    else:
                        print(f"第{img_num}张图片报错，放弃，请检查")

# .3)输出末尾部分
html_end = libmind.html_end
with open(path + file_bi, "a", encoding="utf-8") as f:
    f.write(f"{html_end}")
    f.write(f"</body>\n</html>")

# 判断中英文两个数组的数量是否一致
if len(lst_en) == len(lst_zh):
    print(f"中英文数组长度一致，均为{len(lst_zh)}")
else:
    print(f"中英文数组长度不一致：英文{len(lst_en)}行，中文{len(lst_zh)}行")
    print(f"请检查！")

# 计算时间
time_end=time.time()
print(f"本书合并流程消耗{time_end-time_start:.2f}秒")