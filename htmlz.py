# Htmlz类
# 用于解压缩HTMLz文件到指定目录。
# 一般加入了calibre的图书，会被自动命名。使用该类可以直接将htmlz文件解压到同名文件夹中。
#
# Author：Tecson
# Date: 2022-11-25

import os
import zipfile

class Htmlz():
    def __init__(self,htmlz_file,out_dir="") -> None:
        # 带解压的HTMLZ文件
        self.htmlz_file = htmlz_file
        # 解压目录。如果为空，则解压到和htmlz同名的文件夹中
        self.out_dir = out_dir

    '''
    解压文件。
    如果指定目录不存在，就解压到文件名对应的文件夹中。
    '''    
    def extract(self):
        # 判断待解压文件存在
        if not os.path.exists(self.htmlz_file):
            raise Exception(f'待解压文件{self.htmlz_file}不存在。')
        # 若解压目录为空，则用文件名作为目录
        if self.out_dir == "":
            fname = os.path.basename(self.htmlz_file).split('.')[0]
            self.out_dir = os.path.join(os.path.curdir,fname)
        # 若目录不存在，则建立目录
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
            print("已创建新目录")
        # 确保目录存在，并且是目录而非文件
        if not (os.path.isdir(self.out_dir) & os.path.exists(self.out_dir) ):
            raise Exception(f"{self.out_dir} 解压缩路径不正确或不存在。")

        # 解压缩文件
        zFile = zipfile.ZipFile(self.htmlz_file, "r")
        for fileM in zFile.namelist(): 
            zFile.extract(fileM, self.out_dir)
        zFile.close()        
        


# if __name__ == '__main__':
#     z = Htmlz("xxxxxx.htmlz")
#     z.extract() 
#     print(f"文件被解压到{z.out_dir}")

# 用法如下
# from htmlz import Htmlz

# z = Htmlz("C:\DataRoot\git\jiqimao\How to Attract Money - Murphy, Joseph,.htmlz",out_dir='aaa')
# z.extract()
# print(z.out_dir)
    