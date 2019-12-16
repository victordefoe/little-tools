# encoding: utf-8
'''
@Author: 刘琛
@Time: 2019/12/12 16:58
@Contact: victordefoe88@gmail.com

@File: magics.py
@Statement: All kinds of functions

'''

import cv2, os
import numpy as np

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def cv_imwrite(file_path, img):

    cv2.imencode('.png', img)[1].tofile(file_path)
    return


def white2alpha(img_file, save=True):
    """
    This is for change the image into vector style
    :param img_file: path
    :param save: if true output the file into org directory
    :return:
    """
    dir, fname = os.path.split(img_file)
    fname[0:fname.find('.')]
    new_fname = fname[0:fname.find('.')]+ '_a' +fname[fname.find('.'):]
    img = cv_imread(img_file)

    sp = img.shape
    width = sp[0]
    height = sp[1]
    # b_channel, g_channel, r_channel, alpha_channel = cv2.split(img)
    #
    # # alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # # 最小值为0
    # alpha_channel[:] = 0
    #
    # img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
    for i in range(width):
        for j in range(height):
            if img[i,j][0] > 100:
                img[i,j][3] = 0
            # else:  # make the dark theme into bright
            #     img[i,j][:3] = [255,255,255]

            if img[i,j][1] < 100 :
                img[i, j][:3] = [255, 255, 255]

    img_BGRA = img
    if save:
        print('%s is generated' % (new_fname))
        cv_imwrite(os.path.join(dir, new_fname), img_BGRA)
    return img_BGRA



def alpha2white(img_file, save=True):
    dir, fname = os.path.split(img_file)
    fname[0:fname.find('.')]
    new_fname = fname[0:fname.find('.')] + '_a' + fname[fname.find('.'):]
    img = cv_imread(img_file)

    sp = img.shape
    width = sp[0]
    height = sp[1]

    for i in range(width):
        for j in range(height):
            if img[i,j][0] >= 200:
                img[i,j][:3] = [255,255,255]



    img_BGRA = img
    if save:
        print('%s is generated' % (new_fname))
        cv_imwrite(os.path.join(dir, new_fname), img_BGRA)
    return img_BGRA

def rotate(img_file, angle=45, save=True):
    def img_rotate(image, angle, center=None, scale=1.0, borad_value=(255,255,255)):
        # 获取图像尺寸
        (h, w) = image.shape[:2]

        # 若未指定旋转中心，则将图像中心设为旋转中心
        if center is None:
            center = (w / 2, h / 2)

        # 执行旋转
        M = cv2.getRotationMatrix2D(center, angle, scale)
        rotated = cv2.warpAffine(image, M, (w, h), borderValue=borad_value)

        # 返回旋转后的图像
        return rotated


    dir, fname = os.path.split(img_file)
    fname[0:fname.find('.')]
    new_fname = fname[0:fname.find('.')] + '_a' + fname[fname.find('.'):]
    img = cv_imread(img_file)

    sp = img.shape
    width = sp[0]
    height = sp[1]

    img = img_rotate(img, 30)

    img_BGRA = img
    if save:
        print('%s is generated' % (new_fname))
        cv_imwrite(os.path.join(dir, new_fname), img_BGRA)
    return img_BGRA



