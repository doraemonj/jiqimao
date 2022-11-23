# 用于切中文语音文本文档
import os
import re
import shutil
# 每N字阶段当前段落
per_num = 20000
para_01_num = 500
para_02_num = 9500

# 设置路径和文本名字
txt_path = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/"
out_path = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/001/"
backup_path = r"/Users/tangqiang/Library/CloudStorage/GoogleDrive-chrishowardaka@gmail.com/My Drive/ebook_for_sale/txt_zh/origin/"

txt_lst = []
for el in os.listdir(txt_path):
    if el.endswith(".txt"):
        txt_lst.append(el)

txt_file_name = r"芯片战争 克里斯·米勒 Chip War By Chris Miller"

for txt_file_name in txt_lst:


    # 通过文件名计算书名和作者名
    # 计算中文书名
    book_name_zh = txt_file_name.split(" ")[0]
    print(f"原书中文名：《{book_name_zh}》")
    # 计算中文作者
    author_name_zh = txt_file_name.split(" ")[1]
    print(f"作者中文名：{author_name_zh}")

    # 计算中文书名
    book_name_en = ""
    # 计算中文作者
    author_name_en = ""

    ads_txt_01 = "定制外文书中文译本双语对照读本和音频、五分钟自助翻译课程请登录libmind.com，或点击视频下方链接，libmind帮你直接阅读世界上任何语言的书，创建完全属于你的私人图书馆，欢迎继续收听libmind为您定制的《{0}》中译音频，作者 ：{1}。".format(book_name_zh, author_name_zh)
    print(f"{ads_txt_01 = }\n")

    ads_txt_02 = "您正在收听的是libmind为您定制的《{0}》中译音频，作者：{1}，libmind帮助你读懂世界上任何语言的书，点击视频下方链接可定制音频和图文并茂的双语对照读本、五分钟自助翻译课程，自己阅读、赠送亲友或自助翻译俱佳。".format(book_name_zh, author_name_zh)
    print(f"{ads_txt_02 = }\n")

    ads_txt_03 = "感谢收听libmind为您朗读的《{0}》第一部分，继续收听请登录libmind.com，或点击视频下方链接。libmind帮助你五分钟内翻译所有外文书，可将中译本定制成音频或图文并茂的双语读本，自己阅读、赠送亲友、自助翻译或自建图书馆，请登录libmind.com，或点击视频下方链接，获私人图书馆，五分钟自助翻译课程，定制更多有声书。".format(book_name_zh, author_name_zh)
    print(f"{ads_txt_03 = }\n")


    audio_txt_zh = open(txt_path + txt_file_name, 'r', encoding='utf-8').read()    # 读取英文文件
    # 显示文章的所有字数
    print(f"{len(audio_txt_zh) = }")
    # 预估切的份数N
    article_num = len(audio_txt_zh)/per_num
    print(f"{article_num = }")

    # 以段为单位，放入列表
    lst_txt_zh = audio_txt_zh.split("\n")
    lst_txt_zh = lst_txt_zh[::-1]


    # 以不超过per_num为限，写入新文本，以此循环
    para_01_switch = 1
    para_02_switch = 1

    print(f"开始打印：\n{txt_file_name}")
    txt_file_name = txt_file_name[:-4]
    try:
        for file_no in range(1):
            left_char_num = per_num
            print(f"正在打印第{file_no + 1}篇")
            while left_char_num >= 0:
                current_para = lst_txt_zh.pop()
                with open(out_path + txt_file_name + "-{:03d}".format(file_no + 1) + ".txt", "a") as f:
                    f.write(f"{current_para}\n")
                left_char_num = left_char_num - len(current_para)
                if per_num - left_char_num > para_01_num and para_01_switch == 1:
                    with open(out_path + txt_file_name + "-{:03d}".format(file_no + 1) + ".txt", "a") as f:
                        f.write(f"\n{ads_txt_01}\n")
                        para_01_switch = 0
                        continue
                elif per_num - left_char_num > para_02_num and para_02_switch == 1:
                    with open(out_path + txt_file_name + "-{:03d}".format(file_no + 1) + ".txt", "a") as f:
                        f.write(f"\n{ads_txt_02}\n")
                        para_02_switch = 0
                        continue
        with open(out_path + txt_file_name + "-{:03d}".format(file_no + 1) + ".txt", "a") as f:
            f.write(f"\n{ads_txt_03}\n")
    except IndexError:
        print("索引完毕")

    # 文件归档
    shutil.copyfile(txt_path + txt_file_name, backup_path + txt_file_name)
    os.remove(txt_path + txt_file_name)