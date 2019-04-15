# coding:utf8
# import win32clipboard as wc
# import win32con
import clipboard
import re
import os
from icon import img
import base64
from tkinter import *
root = Tk(className='Bib2Pami_V2')
# root.iconbitmap('logo48.ico')
root.title('bib2pami_v2.0_beta')
root.config(bg='#8B8B83')
# sss

# 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
tmp = open("tmp.ico", "wb+")
tmp.write(base64.b64decode(img))
tmp.close()

root.iconbitmap('tmp.ico')  # 加图标
os.remove("tmp.ico")
# 以上是为exe制作icon


label = Label(root, text="请复制goole学术(或百度学术）上“引用”的BibTex格式全部内容,然后点击Convert按钮即可",
              bg="#B4CDCD",
              fg="yellow",
              font=("黑体", 10),
              width=60,
              height=4,
              wraplength=300,
              anchor="n",
              justify="right"
              )

T1 = Text(root, height=10, width=60, foreground='blue')
T2 = Text(root, height=10, width=60)

# T1.insert(END, )
T2.insert(END, '(该区域显示转化后的PAMI格式文献）\n')
# 'IEEE T-PAMI标准会议格式进行，'
# '作者名在前，姓在后，不写middle name；文章题目实词首字母大写；'
# '会议名称建议全称（斜体）；会议时间在页码前\n'
# 'IEEE T-PAMI标准期刊格式进行，作者名在前，姓在后，不写middle name；文章题目实词首字母大写；'
# '期刊名称建议全称（斜体）；卷号页码等确保完整')

pamidic = {}

# This function was deprecated
# def getCopyText():
#     wc.OpenClipboard()
#     copy_text = wc.GetClipboardData(win32con.CF_TEXT)
#     wc.CloseClipboard()
#     copy_text = str(copy_text, encoding='utf-8')
#     return copy_text


def getCopyText():
    copy_text = clipboard.paste()
    return copy_text

# test
#import chardet
# print chardet.detect(getCopyText())   # 找到包含中文内容的字符串编码


def transform_booktitle(name, is_conference=True):
    assert isinstance(name, str), 'Booktitle must be string type'
    flags = ['proceedings' in name.lower(), 'conference' in name.lower()]
    prefix = 'in Proc. IEEE Conf.'
    pattern = re.compile(r'(?<=IEEE\s).*')
    if 'IEEE' in name:
        content = re.search(pattern, name).group()
    else:
        content = name
    if True in flags:
        is_conference = True
    standard = prefix + ' ' + content
    return standard


def Change():
    try:

        # print getCopyText().decode('GB2312')  # 转码
        bib = getCopyText().split('\n')
        if bib[-1] != '}':
            del bib[-1]
        for i in range(len(bib)):
            bib[i] = bib[i].strip()

        for each in bib[1:-2]:
            each = each.split('=')
            pamidic[each[0]] = each[1][1:-2]
        each = bib[-2].split('=')
        pamidic[each[0]] = each[1][1:-1]

        print(pamidic)
        if 'year' in pamidic:
            if pamidic['year'][-1] == '}':
                pamidic['year'] = pamidic['year'][:-1]

        if 'journal' not in pamidic and 'booktitle' not in pamidic:
            pamidic['journal'] = 'Eprint Arxiv'

        author = pamidic['author'].split('and')

        for i in range(len(author)):
            try:
                yy = []
                tmp = author[i].split(',')
                tmp[1] = tmp[1].strip()
                tmp[0] = tmp[0].strip()
                tmp[1] = tmp[1].split(' ')
                for each in tmp[1]:
                    yy.append(each[0] + '. ')
                tmp[1] = ''.join(yy)
                author[i] = tmp[1] + tmp[0] + ','
            except BaseException:
                continue
        if len(author) >= 3:
            author[-1] = 'and ' + author[-1]

        if 'pages' in pamidic:
            pamidic['pages'] = pamidic['pages'].replace('--', '-')
        if 'author' in pamidic:
            pamidic['author'] = ' '.join(author)
        if 'title' in pamidic:
            pamidic['title'] = '\"' + pamidic['title'] + ',' + '\"'
        if 'journal' in pamidic:
            is_conference = False
            pamidic['journal'] = pamidic['journal'] + ','
        if 'volume' in pamidic:
            pamidic['volume'] = 'vol. ' + pamidic['volume'] + ','
        if 'number' in pamidic:
            pamidic['number'] = 'no. ' + pamidic['number'] + ','
        if 'booktitle' in pamidic:
            is_conference = True
            pamidic['booktitle'] = transform_booktitle(
                pamidic['booktitle']) + ','
        if 'pages' in pamidic:
            pamidic['pages'] = 'pp. ' + \
                pamidic['pages'] + (',', '.')[is_conference]
        if 'year' in pamidic:
            pamidic['year'] = pamidic['year'] + ('.', ',')[is_conference]

        if is_conference is True:
            pamilist = ['author', 'title', 'booktitle', 'year', 'pages']
        else:
            pamilist = [
                'author',
                'title',
                'journal',
                'booktitle',
                'volume',
                'number',
                'pages',
                'year']

        pami = []
        for each in pamilist:
            if each in pamidic:
                pami.append(pamidic[each])
        pami = ' '.join(pami)

        # print author
        # print pamidic
    except BaseException:
        pass

    T1.delete(0.0, END)
    try:
        T1.insert(END, getCopyText())
    except BaseException:
        #T2.delete(0.0, END)
        T2.insert(END, '\n复制出错')

    # print pami
    # try:
    #     wc.OpenClipboard()
    #     wc.EmptyClipboard()
    #     wc.SetClipboardData(win32con.CF_UNICODETEXT, pami)
    #     wc.CloseClipboard()
    # except Exception as e:
    #     wc.CloseClipboard()
    #     print(e)
    try:
        clipboard.copy(pami)
    except Exception as e:
        print(e)

    try:
        T2.delete(0.0, END)
        T2.insert(END, pami)
        T2.insert(END, '\n\n\n(已经复制到剪切板)')
    except Exception as e:
        T2.tag_configure('r', foreground='red')
        T2.tag_config('color', foreground='black')
        T2.insert(END, '\n%s \nmaybe复制的内容格式不对，请重新复制' % e)
    finally:
        pamidic.clear()


Button(root, text='Convert', command=Change, bg='#FFFACD').pack(side=RIGHT)
label.pack()
T1.pack()
T2.pack()

root.mainloop()

# input('aaa')
