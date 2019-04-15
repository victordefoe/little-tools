# encoding: utf-8
'''
@Author: 刘琛
@Time: 2019/4/13 23:43
@Contact: victordefoe88@gmail.com

@File: test_core.py
@Statement:

'''


#coding:utf8
import win32clipboard as wc
import win32con
from tkinter import *
root = Tk(className = 'Bib2Pami_V2')
#root.iconbitmap('logo48.ico')

#sss
import base64
from icon import img
import os
import re



pamidic = {}


# test
#import chardet
#print chardet.detect(getCopyText())   # 找到包含中文内容的字符串编码


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

inform = '''@inproceedings{lin2017focal,
  title={Focal loss for dense object detection},
  author={Lin, Tsung-Yi and Goyal, Priya and Girshick, Ross and He, Kaiming and Doll{\'a}r, Piotr},
  booktitle={Proceedings of the IEEE international conference on computer vision},
  pages={2980--2988},
  year={2017}
}
'''


def Change():
    try:

        #print getCopyText().decode('GB2312')  # 转码
        bib = inform.split('\n')
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
            except:
                continue
        if len(author) >= 3:
            author[-1] = 'and ' + author[-1]

        if 'pages' in pamidic:
            pamidic['pages'] = pamidic['pages'].replace('--','-')
        if 'author' in pamidic:
            pamidic['author'] = ' '.join(author)
        if 'title' in pamidic:
            pamidic['title'] = '\"' + pamidic['title'] + ','+ '\"'
        if 'journal' in pamidic:
            is_conference = False
            pamidic['journal'] = pamidic['journal'] + ','
        if 'volume' in pamidic:
            pamidic['volume'] = 'vol. ' + pamidic['volume'] + ','
        if 'number' in pamidic:
            pamidic['number'] = 'no. ' + pamidic['number'] + ','
        if 'booktitle' in pamidic:
            is_conference = True
            pamidic['booktitle'] = transform_booktitle(pamidic['booktitle']) + ','
        if 'pages' in pamidic:
            pamidic['pages'] = 'pp. ' + pamidic['pages'] + (',', '.')[is_conference]
        if 'year' in pamidic:
            pamidic['year'] = pamidic['year'] + ('.', ',')[is_conference]


        if is_conference is True:
            pamilist = ['author', 'title', 'booktitle',  'year', 'pages' ]
        else:
            pamilist = ['author', 'title', 'journal', 'booktitle', 'volume', 'number', 'pages', 'year']

        pami = []
        for each in pamilist:
            if each in pamidic:
                pami.append(pamidic[each])
        pami = ' '.join(pami)

        #print author
        #print pamidic
    except Exception as e:
        print(e)
    print(pami)
    return pami


# Change()

#input('aaa')


def test_win():
    import clipboard
    text = clipboard.paste()
    print(text)
    clipboard.copy('asafddsaa')


test_win()




