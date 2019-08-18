# encoding: utf-8
'''
@Author: 刘琛
@Time: 2019/2/15 12:18
@Contact: victordefoe88@gmail.com

@File: temp.py
@Statement: 这是一个为了筛选和处理特定信息的脚本文件

故事是这样的：有一天老板让更新他的学术论文主页

'''
import os
import os.path as osp
from pprint import pprint
import re
import Levenshtein
import difflib


home_dir = 'D:/办公事务/论文主页更新/home/'


def pre_do_home():
    with open(home_dir + 'items.txt', encoding='utf-8') as f:
        core_cont = f.readlines()
        core_cont = [re.search(r'(?<=\“)(.*)(?=\,\”)', item).group().lower() for item in core_cont]  #全部小写字母
        print('home_items: ', len(core_cont))
    with open(home_dir + 'items_titles.txt', 'w', encoding='utf-8') as f:
        f.writelines([each + '\n' for each in core_cont])
    return core_cont

# print(core_cont[0])
def pre_do_goo(home_directory=None, file_name=None):
    home = home_dir if home_directory == None else home_directory
    file_name = 'goo.txt' if file_name == None else file_name

    #classify
    authors, titles, journals, others = [], [], [], []
    journal_sign = ['(', 'IEEE', 'AAAI', 'Conference', 'Transactions']
    journame = ['Neurocomputing', 'Remote Sensing']
    def check_sign(L, string):
        for sign in L:
            if sign in string:
                return True
        return False

    def check_name(L, string):
        for name in L:
            if name == string:
                return True
        return False

    with open(osp.join(home, file_name), encoding='utf-8') as fid:
        goo_item = fid.readlines()

    for idx in range(len(goo_item)):
        each = goo_item[idx].strip()
        if 'Q Wang' in each or 'yuan' in each:
            authors.append(each)
        elif '\t' in each or len(each) < 7:
            others.append(each)
        # elif '(' in each or ',' in each or 'IEEE' in each or 'AAAI' in each or 'Neurocomputing' in each or 'remote sensing' in each:
        elif check_sign(journal_sign, each) != False:
            journals.append(each)
        elif check_name(journame, each) == True:
            journals.append(each)

        elif re.search(r'\d\d', each) is not None:
            others.append(each)
        elif re.search(r'\*' ,each) is not None:
            others.append(each)
        else:
            titles.append(each.lower())    # 全部小写字母

    print('titles', len(titles))
    # for aa in titles:
    #     print(aa)
    # print(others)
    # print(journals)
    with open (osp.join(home, file_name.split('.')[0] + '_titles.txt'), 'w', encoding='utf-8') as f:
        f.writelines([title + '\n' for title in titles])
    # print(titles)
    return titles

def compare(L1, L2):
    # 忽略大小写
    L1 = [each.lower() for each in L1]
    L2 = [each.lower() for each in L2]

    unique_of_L1 = []
    unique_of_L2 = []
    # print('-------------------\n unique of L1 \n------------------- \n')
    for each_1 in L1:
        for each_2 in L2:
            if Levenshtein.distance(each_1, each_2) < 5:
                break
        else:
            unique_of_L1.append(each_1)
            # print(each_1)
    print('unique of L1 -- total: ', len(unique_of_L1))

    # print('-------------------\n unique of L2 \n------------------- \n')
    for each_2 in L2:
        for each_1 in L1:
            if Levenshtein.distance(each_1, each_2) < 10:
                break
        else:
            unique_of_L2.append(each_2)
            # print(each_2)
    print('unique of L2 -- total: ', len(unique_of_L2),  '\n')

    return unique_of_L1, unique_of_L2


def Orcid():
    with open(home_dir + 'works.bib', 'r', encoding='utf-8') as f:
        mix = f.readlines()
        exist_orc = []
        for each in mix:
            if 'title' in each:
                # print(each)
                item = re.search(r'(?<=title\s=\s{)(.*?)(?=},)', each).group()
                item = re.sub(r'({|})','', item)
                item = re.sub(r'(\\textendash)', '-', item)
                exist_orc.append(item.lower())
                # print(item)
    print('orc: ', len(exist_orc))
    return exist_orc

def self_repeat(L):
    del_list = []
    for i in range(len(L)):
        for j in range(i+1, len(L)):
            if Levenshtein.distance(L[i], L[j]) < 10:
                print(L[i], i, j)
                del_list.append(L[j])

    for each in del_list:
        L.remove(each)
    return L

def extract_title_from_bibtext():
    dir = home_dir + 'scopus.bib'
    with open(dir, 'r') as f:
        lines = f.readlines()
    titles = []
    for each in lines:
        if 'title' in each:
            title = re.search(r'(?<={).*(?=})', each).group()
            titles.append(title)
            # print(title)
    # print(len(titles))
    return titles


def task_01():
    goo = pre_do_goo()
    items = pre_do_home()
    orc = Orcid()

    _, ad1 = compare(goo, items)

    extract_title_from_bibtext()
    scopus = extract_title_from_bibtext()
    a, _ = compare(scopus, items)
    b, ad2 = compare(scopus, goo)
    ad = ad1 + ad2

    print('delete', b)
    with open(home_dir + 'scopus_delete.txt', 'w', encoding='utf-8') as f:
        f.writelines([de + '\n' for de in b])

    with open(home_dir + 'scopus_add.txt', 'w', encoding='utf-8') as f:
        f.writelines([de + '\n' for de in ad])

def WOS_SearchFiles(sourcefile, dir):
    with open(sourcefile, 'r') as f:
        titles = f.readlines()
    with open(os.path.join(dir, 'goo_wos_search.txt'), 'w') as f:
        for i in titles:
            i = i.strip()
            i = '\"' + i + '\"' + ' OR '
            f.write(i)


if __name__ == '__main__':
    # pre_do_goo('D:\办公事务\高被引集热点论文查询', 'goo.txt')
    WOS_SearchFiles('D:/办公事务/高被引集热点论文查询/goo_titles.txt', 'D:/办公事务/高被引集热点论文查询/')





