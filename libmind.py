import os
import shutil
import re
from bs4 import BeautifulSoup
import time

def copy_allfiles(src, dest):
    """
    复制文件夹内所有文件：src:原文件夹；dest:目标文件夹
    """
    src_files = os.listdir(src)
    for file_name in src_files:
        full_file_name = os.path.join(src, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, dest)

def zh_format(html):
    """
    中文段落处理函数（zh_format）：清理DeepL翻译过的中文段落，相见函数内部

    " 要相应地替换成 “”
    ' 要相应地替换成 ‘’
    无论是单引号还是双引号，都要与相邻的字符之间留有一个空格；标点符号 ，。？！ 除外；
    数字、百分比、英文字母，与汉字之间应该应该留有空格；
    应用在中文字符的 “斜体” 样式，应该改成 “加重” 样式；
    破折号统一使用 ——（前后有空格，除非与标点符号相邻）而非 — 或者 --；
    外国姓名之间的符号为 ·；
    ……
    """
    # 去掉半角方括号
    pttn = r'\[(.*?)\]'
    rpl = r'\1'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 直双引号转换成弯双引号
    pttn = r'\s*"(.*?)\s*"'
    rpl = r'『\1』'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 直单引号转换成弯单引号
    pttn = r"\s*'(.*?)\s*'"
    rpl = r'「\1」'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # html tag 中被误伤的直引号
    pttn = r'=[“”"](.*?)[“”"]'
    rpl = r'="\1"'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # html 弯引号之前的空格
    pttn = r'([\u4e00-\u9fa5])([“‘])'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # html 弯引号之后的空格
    pttn = r'([’”])([\u4e00-\u9fa5])'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # html tag: strong 内部的 “”、‘’、《》、（）
    pttn = r'([《（“‘]+)'
    rpl = r'\1'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    pttn = r'([》）”’。，]+)'
    rpl = r'\1'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 省略号
    pttn = r'\.{2,}\s*。*\s*'
    rpl = r'…… '
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 破折号
    pttn = r'&mdash；|—|--'
    rpl = r' —— '
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 姓名之间的 ·（重复三次）
    pttn = r'([\u4e00-\u9fa5])-([\u4e00-\u9fa5])'
    rpl = r'\1·\2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    pttn = r'([\u4e00-\u9fa5])-([\u4e00-\u9fa5])'
    rpl = r'\1·\2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    pttn = r'([\u4e00-\u9fa5])-([\u4e00-\u9fa5])'
    rpl = r'\1·\2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    pttn = r'([A-Z]{1})\s*\.\s*([A-Z]{1})'
    rpl = r'\1·\2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    pttn = r'([A-Z]{1})\s*\.\s*([\u4e00-\u9fa5])'
    rpl = r'\1·\2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 全角百分号
    pttn = r'％'
    rpl = r'%'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 数字前的空格
    pttn = r'([\u4e00-\u9fa5])(\d)'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 数字后的空格，百分比 % 后的空格
    pttn = r'([\d%])([\u4e00-\u9fa5])'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 英文字母前的空格
    pttn = r'([\u4e00-\u9fa5])([a-zA-Z])'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 英文字母后的空格，百分比 % 后的空格
    pttn = r'([a-zA-Z])([\u4e00-\u9fa5])'
    rpl = r'\1 \2'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # tag 内的英文字母前的空格
    pttn = r'([\u4e00-\u9fa5])<(strong|i|em|span)>(.[a-zA-Z\d ]*?)<\/(strong|i|em|span)>'
    rpl = r'\1 <\2>\3\4>'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # tag 内的英文字母后的空格，百分比 % 后的空格
    pttn = r'<(strong|i|em|span)>(.[a-zA-Z\d ]*?)<\/(strong|i|em|span)>([\u4e00-\u9fa5])'
    rpl = r'<\1>\2\3> \4'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 弯引号前的逗号
    pttn = r'，([”’])'
    rpl = r'\1，'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 中文标点符号之前多余的空格
    pttn = r'([，。！？》〉】]) '
    rpl = r'\1'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 英文句号 . 与汉字之间的空格
    pttn = r'\.([\u4e00-\u9fa5])'
    rpl = r'. \1'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 左半角括号
    pttn = r'\s*\('
    rpl = r'（'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 右半角括号
    pttn = r'\)\s*'
    rpl = r'）'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    # 多余的括号（DeepL 返回文本经常出现的情况）
    pttn = r'）。）'
    rpl = r'。）'
    re.findall(pttn, html)
    html = re.sub(pttn, rpl, html)

    return html


html_head = """
<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type"/>
<link href="style.css" rel="stylesheet" type="text/css"/>
<title>{0} | {1}</title>
</head>
<body>

<div class ="bottom">
<div class ="top left">
<p class ="en"><img src="cover.jpg"></p></div>
<div class="top right">
<p class ="cn"><h2>{0}</h2><h2>{1}</h2><br /><h4>English-Chinese Bilingual Translation Course</h4><h4><a href="https://libmind.com/ebooks/translate-any-ebook-in-5-minutes-secret-course/">👉&nbsp; &nbsp; 自助译书手册&nbsp; &nbsp; 👈</a><br />·<br />让你能五分钟翻译外文书<br />·<br />↓&nbsp; &nbsp; &nbsp; 成果展示&nbsp; &nbsp; &nbsp; ↓</h4><br /><h4>libmind.com</h4><h4>{2}</h4></p></div>
</div>

<div class ="bottom" style="text-align: center">
<div class ="top left">
<p class ="en">外文书中译对照5分钟机器翻译<br />基于DeepL<br />支持多语互译：英德法中俄日西等<br />支持多种格式：Epub、Mobi、PDF等<br />支持支付：国际信用卡、PayPal、MixPay<br /><a target="blank" href="https://libmind.com/zh/">上传</a></p></div>
<div class="top right">
<p class ="cn">创建完全属于你的私人图书馆<br /><a target="blank" href="https://libmind.github.io">参观样馆</a><br />藏书千本 · 独立掌控<br />全文搜索 · 多语秒切<br />听书读书 · 掌控自如<br /><a target="blank" href="https://libmind.com/zh/personal-library/">购买</a></p></div>
</div>

<div class ="bottom">
<div class ="top left">
<p><img src="images/libmind.com-1.png"></p></div>
<div class="top right">
<p><img src="images/libmind.com-2.png"></p></div>
</div>

<div class ="bottom">
<div class ="top left">
<p style="text-align: center">Subscribe <b>Telegram(@libmind)</b>, and receive new bilingual books: <a href="https://t.me/libmind">https://t.me/libmind</a></p></div>
<div class="top right">
<p style="text-align: center">关注<b>Telegram(@libmind)</b>，接收最新双语书资讯：<a href="https://t.me/libmind">https://t.me/libmind</a></p></div>
</div>


"""




html_end = """
<h3>本书由libmind.com基于DeepL翻译</h3>
<h3 style="color: red">现在，你终于可以畅快阅读任何语言写的任何文字了</h3>
<h5 style="text-align: left">&nbsp;&nbsp;在互联网高速发展的过程中，英语在知识积累方面的垄断已经彻底无法超越了，巴别塔相当于早就建成了，英语就是世界语。</h5>
<h5 style="text-align: left">&nbsp;&nbsp;不懂英语，在任何一个领域里都直接落后一大截，无论什么东⻄都只能等翻译，还要等人家愿意翻译，而且人家错译、 漏译你也不知道。 </h5>
<h5 style="text-align: left">&nbsp;&nbsp;libmind.com可以让你在第一时间把所有外文资料(含英语、德语、法语等100多种语言)直接翻译成你指定的语言和 电子书格式，还可以制成中英双语对照格式，只要上传你想翻译的电子书即可。现在上传，还送5本经典热⻔的原版书 和译本。 </h5>
<h5 style="text-align: left">&nbsp;&nbsp;libmind.com使用当前公认最好的翻译引擎DeepL，经过无数次研究测试，独家完成了任何语种的电子书都可以在5分钟内完成翻译，信达雅快。还可以把所有你喜欢的书和译本都放进一个完全属于你自己的图书馆里</h5>
<div class ="bottom"  style="text-align: center">
<div class ="top right">
<p class ="cn"><img src="images/libmind.com-4.jpg"><br /><br />机器翻译 + 双语对照版极速定制<br />即刻<a target="blank" href="https://libmind.com/zh/">上传外文书</a>，定制读本</p></div>
<div class="top right">
<p class ="cn"><img src="images/libmind.com-3.png"><br /><br /><a target="blank" href = "https://libmind.github.io">私人图书馆 样馆参观</a><br /><a target="blank" href = "https://doraemonj.github.io/about">说明</a>  ·  <a target="blank" href = "https://libmind.com/zh/personal-library/">购买</a></p></div>
</div>

<div class ="bottom" style="text-align: center">
<div class ="top left">
<p><a target="blank" href="https://doraemonj.github.io/how_to_translate_a_book_in_five_minutes_tutorial/">五分钟自助翻译教程</a><br />Mixin社群每周开讲，双语对照图文并茂</div>
<div class="top right">
<p>五分钟自助翻译完全手册<br /><a target="blank" href="https://doraemonj.github.io/how_to_translate_a_book_in_five_minutes_tutorial/">带你翻阅汉语围栏</a></p></div>
</div>
<h5 style="text-align: left">&nbsp;&nbsp;建议使用端对端加密即时通信工具Mixin Messenger，
官方下载：<a target="_blank" href="https://mixin.one/messenger">https://mixin.one/messenger</a></h5>
<h5 style="text-align: left">&nbsp;&nbsp;Mixin社群：7000104144（机器猫·译站），Mixin客服：29273（机器猫）</h5>
<h5 style="text-align: left">&nbsp;&nbsp;官网：libmind.com</h5>
<h5 style="text-align: left">&nbsp;&nbsp;关注Telegram（@libmind），接收最新双语书资讯：<a target="_blank" href="https://t.me/libmind">https://t.me/libmind</a></h5>
<h5 style="text-align: left">&nbsp;&nbsp;邮箱：libmind-admin@libmind.com</h5>
<h3 style="text-align: left">&nbsp;&nbsp;“No matter where you are or what you are going through always believe that there is a light at the end of your tunnel.”</h3>
<div style="text-align: center"><img src="images/libmind.com-6.jpg"></div>
<h3 style="text-align: center">Libmind AI作品：众人祈书</h3>
"""