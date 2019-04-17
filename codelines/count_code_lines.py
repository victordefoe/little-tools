# encoding: utf-8
'''
@Author: 刘琛
@Time: 2018/10/22 2:49
@Contact: victordefoe88@gmail.com

@File: homework01.py
@Statement:

'''



import pprint
import logging
import collections
import base64
import os
import win32con
import win32clipboard as wc
from tkinter import *
from tkinter import filedialog, ttk, PhotoImage



# 你有个目录，里面是程序（假如是C或者是Python），统计一下你写过多少行代码。包括空行和注释，但是要分别列出来。


def check_code_ammount(dir):
    global text
    allfiles = os.listdir(dir)
    multicmtflag = 1 #多行注释标志符号
    num_code, num_comments, num_sapccline, total, error_file_num = 0, 0, 0, 0, 0
    for root, dirs, files in os.walk(dir):
        for each in files:
            if each[-2:] == '.c' or each[-2:] == '.h' or each[-3:] == '.py' or each[-4:] == '.cpp' or each[-4:] == '.hpp':
                # print('处理：', os.path.join(root, each), end=' ')
                record = total
                try:
                    with open(os.path.join(root, each), encoding='utf-8') as fid:
                        while True:

                            line = fid.readline()
                            total += 1
                            if line == '':  # 等价于if line == "":
                                break


                            line = line.strip()
                            if line == '':
                                num_sapccline += 1
                                continue

                            if multicmtflag == -1:
                                num_comments += 1
                                if line[-3:] == '\'\'\'' or line[-3:] == '\"\"\"' or line[-2:] == '*/':
                                    multicmtflag = 1
                                continue

                            try:
                                if line[0] == '#' or line[:2] == '//':
                                    num_comments +=1
                                    continue
                                elif line[:3] == '\'\'\'' or line[:3] == '\"\"\"' or line[:2] == '/*':
                                    multicmtflag = -1
                                    num_comments += 1
                                    continue
                                else:
                                    num_code += 1
                                    #print(num_code)

                            except Exception as e:

                                # print(e, total, line)
                                #continue
                                pass
                         # print(total-record)
                except Exception as e:
                    # print('\n Error: ', e, 'in: \n            ', os.path.join(root, each))
                    error_file_num += 1


    # print('代码行的数量： %d, 注释行的数量： %d, 空白行的数量： %d, 共计： %d' % (num_code, num_comments, num_sapccline, total))
    text.config(text = '代码行： %d, 注释： %d, 空白： %d, 共计： %d\n 出错文件（未统计）共计： %d' % (num_code, num_comments, num_sapccline, total, error_file_num))

    # print('出错文件（未统计）共计： ', error_file_num)


if __name__ == "__main__":

    # check_code_ammount('D:/work-201809-07/ntmreg')

    root = Tk(className='统计代码行工具')
    root.geometry('430x250')
    bg_color = 'white'
    root.config(bg=bg_color)
    import base64
    from icon import img, flash
    import os

    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    root.iconbitmap('tmp.ico')  # 加图标
    os.remove("tmp.ico")

    keys = Frame(root, bg=bg_color)
    keys.pack(side=TOP)

    T0 = Label(keys, width=10, height=2, bg=bg_color, fg='black', font='华文行楷 25 bold',
               wraplength=100, anchor='center', justify='left', padx=10)

    T0.config(text='Lines')

    T1 = Label(keys, width=40, height=2, bg=bg_color, fg='black', font='宋体 10 bold',
               wraplength=600, anchor='center', justify='left', padx=10)

    T1.config(text='请在下面框框里输入路径：')
    text = Label(keys, width=60, height=2)


    v1 = ''
    e1 = Entry(keys, textvariable=v1, width=30)

    key_A = Button(keys, bg='light blue', relief=RAISED, width=10, height=1, text='查询', command=lambda:check_code_ammount(e1.get()) )
    T0.grid(row=2, column=1, padx=0, pady=0)

    key_A.grid(row=3, column=1, padx=0, pady=0)

    T1.grid(row=5, column=1, padx=0, pady=0, ipady=20)
    e1.grid(row=6, column=1, padx=0, pady=0)
    text.grid(row=7, column=1, padx=0, pady=10)


    root.mainloop()
	
	
	
