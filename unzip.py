# 自动解压calibre文件夹中最新的文件，到指定目录中去，可以省去《自助翻译课程》里的calibre解压后的手工腾挪
# 本代码来源于巴别塔社群Tecson同学的贡献，Tecson同学贡献了思路和htmlz.py文件
import os
import time
import re
from collections import Counter
import htmlz

# 设置calibre路径（用户设置），自动解压calibre转换的htmlz文件
calibre_path = r"/Users/tangqiang/Calibre Library/"
# 解压文件的目标路径
book_path = r"/Users/tangqiang/books/"
# 原书语言，默认英语
origin_lang = "en"

# 数下根目录有几个分隔符
root_sep_num =  calibre_path.count(os.sep)
# 遍历calibre_path里的所有文件夹，取最新修改的文件夹（作者）里最新修改的文件夹（书名），计算出book_no和book_name
calibre_folders = os.walk(calibre_path)
authors = {}
books =  {}

for root, dirs, files in calibre_folders:
    if root == calibre_path:
        print("root: ", root)  # 当前目录路径
        print("dirs: ", dirs)  # 当前路径下所有子目录
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(root).st_mtime)))
        print("======")

        for sub_root, sub_dirs, sub_files in os.walk(root):
            if sub_root.count(os.sep) == root_sep_num:
                author = sub_root.replace(calibre_path, "")
                modified_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(sub_root).st_mtime))
                print("sub_root: ", sub_root)
                print("author: ", author)
                print("sub_dirs: ", sub_dirs)
                print("modify_date: ", modified_date)
                print("======")

                if len(author) > 0:
                    authors[author] = modified_date

# 取根目录下最新文件夹（作者）：
for author, modified_time in authors.items():
    if modified_time == max(authors.values()):
        newest_author = author
print(f"最新作者为：{newest_author}，更新时间为：{max(authors.values())}")

# 查找最新作者的最新书籍
author_path = calibre_path + newest_author
author_path_folders = os.walk(author_path)
for root, dirs, files in author_path_folders:
    if root == author_path:
        print("root: ", root)  # 当前目录路径
        print("dirs: ", dirs)  # 当前路径下所有子目录
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(root).st_mtime)))
        print("======")

        for sub_root, sub_dirs, sub_files in os.walk(root):
            if sub_root.count(os.sep) == root_sep_num + 1:
                book = sub_root.replace(calibre_path + newest_author + os.sep, "")
                modified_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(sub_root).st_mtime))
                print("sub_root: ", sub_root)
                print("book: ", )
                print("sub_dirs: ", sub_dirs)
                print("modify_date: ", modified_date)
                print("======")

                if len(book) > 0:
                    books[book] = modified_date

# 取根目录下最新文件夹（作者）的最新文件夹（书籍）：
for book, modified_time in books.items():
    if modified_time == max(books.values()):
        newest_book = book
print(f"最新作者为：{newest_book}，更新时间为：{max(authors.values())}")



# 计算作者名和书名
author_name = newest_author
book_name = newest_book

# 打印验证
print(f"{author_name = }")
print(f"{book_name = }")

# 全路径名称：calibre_path + author_name  + os.sep +book_name + os.sep
destin_path = calibre_path + author_name  + os.sep + book_name + os.sep
# 查找全路径名下的.htmlz文件
for el in os.listdir(destin_path):
    if el.endswith(".htmlz"):
        htmlz_name = el

# 计算 book_path 下书的文件名 book_path
num_patten = r'(^[-+]?([1-9][0-9]*|0)(\.[0-9]+)?$)'
fore_3rd = ["000"]
for el in os.listdir(book_path):
    try:
        el = "{:03d}".format(int(el[:3]))
        print("成功：{}   type(el) = {}".format(el, type(el)))
        if re.match(num_patten, str(int(el))) != None:
            print(el)
            fore_3rd.append(el)
    except:
        # print("失败：{}".format(el))
        pass
print(fore_3rd)
fore_set = set(fore_3rd)

new_book_num = int(max(fore_set)) + 1                           # 计算新书号
new_book_name = re.sub(r'\([^)]*\)', '', book_name).strip()     # 计算新书名

# 计算书的文件夹名：三位书号 + 全部小写的书名
file_name = new_book_name.replace(" ", "_").lower()
book_file_name = "{:03d}_{}".format(new_book_num, file_name)


# 解压文件去指定目录book_path
zip = htmlz.Htmlz(destin_path + htmlz_name, book_path + book_file_name)
zip.extract()
print(zip.out_dir)

# 将index.html文件改名，方便上传DeepL时的区分
os.rename(book_path + book_file_name + os.sep + "index.html", \
          book_path + book_file_name + os.sep + "{}_{}.html".format(file_name, origin_lang))

# transfer variants
book_no = "{:03d}".format(new_book_num)
book_name= book_name

















