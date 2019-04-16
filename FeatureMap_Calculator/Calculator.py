# encoding: utf-8
'''
@Author: 刘琛
@Time: 2019/4/12 12:13
@Contact: victordefoe88@gmail.com

@File: FeatureMap_Calculator.py
@Statement:

'''

import torch
import torch.nn as nn
import numpy as np



class Size_Calculator(object):

    def __init__(self):

        # Flags for counting the layers number
        self.conv_idx = 0
        self.pool_idx = 0
        self.total_layer_num = 0
        self.extra_idx = 0

    def cal_BNconv(
            self,
            in_ch,
            in_channels,
            out_channels,
            kernel=7,
            padding=3,
            stride=2):
        # BNconv = Batch_Normalization + Convolution
        # BN did not change any shaoe of feture map
        out_shape = (in_ch - kernel + 2 * padding) / stride + 1
        self.conv_idx += 1
        print(
            'BNConv_%d: %dx%dx%d' %
            (self.conv_idx,
             out_channels,
             out_shape,
             out_shape))

        self.total_layer_num += 3
        return (int(out_shape), out_channels)

    def cal_pool(self, in_ch, in_channels, out_channels, kernel, stride):
        out_shape = (in_ch - kernel) / stride + 1
        self.pool_idx += 1
        print(
            'Pool_%d: %dx%dx%d' %
            (self.pool_idx,
             out_channels,
             out_shape,
             out_shape))

        self.total_layer_num += 1
        return out_shape

    def res(self, in_ch, in_channels, out_channels, stride, num_conv=0, exp=1):
        """

        :param in_ch: input size (int)
        :param in_channels: input channels num (int)
        :param out_channels: output channels (int)
        :param stride:
        :param num_conv:
            3*3 stide=1 conv for factorizing Convolutions with Large Filter Size,
            larger convolution kernels brings lager receitive fleid
        :param exp: for calculating the middle channels number
        :return:
        """
        oci = out_channels // exp
        (out_shape, channels) = self.cal_BNconv(
            in_ch, in_channels, oci, kernel=3, padding=1, stride=stride)
        for _ in range(num_conv):
            (out_shape, channels) = self.cal_BNconv(
                out_shape, channels, oci, kernel=3, padding=1, stride=1)
        (out_shape, channels) = self.cal_BNconv(out_shape,
                                                channels, out_channels, kernel=3, padding=1, stride=1)
        return (out_shape, out_channels)

    def cal_resblock(
            self,
            in_ch,
            in_channels,
            out_channels,
            stride=1,
            num_layers=1):
        (out_shape, channels) = self.res(
            in_ch, in_channels, out_channels, stride=stride)
        for _ in range(num_layers - 1):
            (out_shape, channels) = self.res(
                out_shape, channels, channels, stride=2)
        return (int(out_shape), channels)

    def cal_fc(self):
        pass

    def cal_extra(self, in_ch, channels, stride=1):
        """

        :param in_ch: input size (shape)
        :param in_channels: a list of layers' channels, channels[0] = in_channels
        :param out_channels:
        :param stride:
        :return:
        """
        flag = False

        self.extra_idx += 1
        kernel = (1, 3)
        outc = channels[0]
        out_shape = in_ch
        for k, each in enumerate(channels[1:]):
            if each == 'S':
                (out_shape, outc) = self.cal_BNconv(out_shape, outc,
                                                    channels[1:][k + 1], kernel=kernel[flag], padding=1, stride=2)
            else:
                (out_shape, outc) = self.cal_BNconv(out_shape, outc,
                                                    each, kernel=kernel[flag], padding=0, stride=1)

        print('\033[0;36m  Extra_%d:  %dx%dx%d  \033[0m' %
              (self.extra_idx, outc, out_shape, out_shape))
        return (out_shape, outc)

    def seq_cal(self, x, input_channels=3, enlarge=1):
        # 备忘-带颜色输出： \033[0;36m ----- \033[0m：  30-36
        print('\033[0;32mInput: %dx%dx%d\033[0m' % (input_channels, x, x))

        x, ch = self.cal_BNconv(
            x, input_channels, 64, kernel=7, padding=3, stride=2)
        # print('BNConv_0: %dx%dx%d' % (ch, x, x))
        x = self.cal_pool(x, ch, ch, kernel=3, stride=2)
        # print('MaxPool_0: %dx%dx%d' % (ch, x, x))

        s_s = [1, 2, 2, 2]
        num_layers = [0, 0, 0, 0]
        ch_s = [
            ch,
            ch * enlarge,
            ch * enlarge * 2,
            ch * enlarge * 4,
            ch * enlarge * 8]

        for i in range(len(s_s)):
            x, outc = self.cal_resblock(
                x, ch_s[i], out_channels=ch_s[i + 1], stride=s_s[i], num_layers=num_layers[i])
            print(
                '\033[0;36m  ResBlock_%d:  %dx%dx%d  \033[0m' %
                (i, outc, x, x))

        x = self.cal_pool(x, outc, outc, kernel=7, stride=1)

        print(
            '\033[0;35m  Total layers\' number: %d \033[0m' %
            self.total_layer_num)


# Cal.seq_cal(28, enlarge=1)
def FashionNetCal(x, input_channels=3, enlarge=1):
    Cal = Size_Calculator()
    print('\033[0;32mInput: %dx%dx%d\033[0m' % (input_channels, x, x))
    x, ch = Cal.cal_BNconv(x, input_channels, 64,
                           kernel=7, padding=3, stride=2)
    x = Cal.cal_pool(x, ch, ch, kernel=3, stride=2)

    x, outc = Cal.cal_resblock(x, ch, out_channels=ch, stride=1, num_layers=1)
    print('\033[0;36m  ResBlock_%d:  %dx%dx%d  \033[0m' % (1, outc, x, x))

# FashionNetCal(700, 1)


def FusingNetBase(x, input_channels=3, enlarge=1):
    Cal = Size_Calculator()
    print('\033[0;32mInput: %dx%dx%d\033[0m' % (input_channels, x, x))

    x, ch = Cal.cal_BNconv(x, input_channels, 64,
                           kernel=7, padding=3, stride=2)
    x = Cal.cal_pool(x, ch, ch, kernel=3, stride=2)

    s_s = [1, 2, 2, 2]
    num_layers = [2, 2, 2, 2]
    ch_s = [
        ch,
        ch * enlarge,
        ch * enlarge * 2,
        ch * enlarge * 4,
        ch * enlarge * 8]

    for i in range(len(s_s)):
        x, outc = Cal.cal_resblock(
            x, ch_s[i], out_channels=ch_s[i + 1], stride=s_s[i], num_layers=num_layers[i])
        print('\033[0;36m  ResBlock_%d:  %dx%dx%d  \033[0m' % (i, outc, x, x))

    x = Cal.cal_pool(x, outc, outc, kernel=2, stride=1)

    x = Cal.cal_extra(x, [256, 'S', 512, 128, 'S', 256, 128, 256, 128, 256], )

    print(
        '\033[0;35m  Total layers\' number: %d \033[0m' %
        Cal.total_layer_num)


FusingNetBase(700)



