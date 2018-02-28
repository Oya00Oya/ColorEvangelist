import chainer
import chainer.functions as F
import numpy as np
from chainer.links.caffe import CaffeFunction
from .conv import conv_function
from .dilate_conv import dilated_conv_function

NET_PATH = '../webapps/ROOT/func/models/params/'


class _ConvBlock(chainer.Chain):
    def __init__(self, id, in_channels, out_channels, ksize, stride, pad=1, nobias=True):
        super(_ConvBlock, self).__init__()
        with self.init_scope():
            self.conv = conv_function(id)

    def __call__(self, x):
        y = F.leaky_relu(self.conv(x), 0.2)
        return y


class _ResNeXtBottleneck(chainer.Chain):
    def __init__(self, id, in_channels, out_channels, cardinality, ksize=3, stride=1, pad=1, dilate=1, nobias=True):
        super(_ResNeXtBottleneck, self).__init__()
        with self.init_scope():
            self.conv_reduce = conv_function(id + '_reduce')
            self.conv_conv = dilated_conv_function(id + '_conv')
            self.conv_expand = conv_function(id + '_expand')

    def __call__(self, x):
        bottleneck = self.conv_reduce(x)
        bottleneck = F.leaky_relu(bottleneck, 0.2)
        bottleneck = self.conv_conv(bottleneck)
        bottleneck = F.leaky_relu(bottleneck, 0.2)
        bottleneck = self.conv_expand(bottleneck)
        return x + bottleneck


class _ResNeXtTunnel4(chainer.ChainList):
    def __init__(self, ngf=64):
        super(_ResNeXtTunnel4, self).__init__()
        for i in range(20):
            self.add_link(_ResNeXtBottleneck(str(400 + i), ngf * 8, ngf * 8, cardinality=32, dilate=1))

    def __call__(self, x):
        for f in self.children():
            x = f(x)
        return x


class _ResNeXtTunnel3(chainer.ChainList):
    def __init__(self, ngf=64):
        super(_ResNeXtTunnel3, self).__init__()
        self.add_link(_ResNeXtBottleneck(str(300), ngf * 4, ngf * 4, cardinality=32, dilate=1))
        self.add_link(_ResNeXtBottleneck(str(301), ngf * 4, ngf * 4, cardinality=32, dilate=1))

        self.add_link(_ResNeXtBottleneck(str(302), ngf * 4, ngf * 4, cardinality=32, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(303), ngf * 4, ngf * 4, cardinality=32, dilate=2))

        self.add_link(_ResNeXtBottleneck(str(304), ngf * 4, ngf * 4, cardinality=32, dilate=4))
        self.add_link(_ResNeXtBottleneck(str(305), ngf * 4, ngf * 4, cardinality=32, dilate=4))

        self.add_link(_ResNeXtBottleneck(str(306), ngf * 4, ngf * 4, cardinality=32, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(307), ngf * 4, ngf * 4, cardinality=32, dilate=1))

    def __call__(self, x):
        for f in self.children():
            x = f(x)
        return x


class _ResNeXtTunnel2(chainer.ChainList):
    def __init__(self, ngf=64):
        super(_ResNeXtTunnel2, self).__init__()
        self.add_link(_ResNeXtBottleneck(str(200), ngf * 2, ngf * 2, cardinality=32, dilate=1))
        self.add_link(_ResNeXtBottleneck(str(201), ngf * 2, ngf * 2, cardinality=32, dilate=1))

        self.add_link(_ResNeXtBottleneck(str(202), ngf * 2, ngf * 2, cardinality=32, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(203), ngf * 2, ngf * 2, cardinality=32, dilate=2))

        self.add_link(_ResNeXtBottleneck(str(204), ngf * 2, ngf * 2, cardinality=32, dilate=4))
        self.add_link(_ResNeXtBottleneck(str(205), ngf * 2, ngf * 2, cardinality=32, dilate=4))

        self.add_link(_ResNeXtBottleneck(str(206), ngf * 2, ngf * 2, cardinality=32, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(207), ngf * 2, ngf * 2, cardinality=32, dilate=1))

    def __call__(self, x):
        for f in self.children():
            x = f(x)
        return x


class _ResNeXtTunnel1(chainer.ChainList):
    def __init__(self, ngf=64):
        super(_ResNeXtTunnel1, self).__init__()
        self.add_link(_ResNeXtBottleneck(str(100), ngf, ngf, cardinality=16, dilate=1))
        self.add_link(_ResNeXtBottleneck(str(101), ngf, ngf, cardinality=16, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(102), ngf, ngf, cardinality=16, dilate=4))
        self.add_link(_ResNeXtBottleneck(str(103), ngf, ngf, cardinality=16, dilate=2))
        self.add_link(_ResNeXtBottleneck(str(104), ngf, ngf, cardinality=16, dilate=1))

    def __call__(self, x):
        for f in self.children():
            x = f(x)
        return x


class _PixelShuffle(chainer.Chain):
    def __init__(self, id, r):
        super(_PixelShuffle, self).__init__()
        with self.init_scope():
            self.conv = conv_function(id)
            self.r = r

    def __call__(self, x):
        r = self.r
        out = self.conv(x)  # 畳み込み
        batchsize = out.shape[0]
        in_channels = out.shape[1]
        out_channels = in_channels // (r ** 2)
        in_height = out.shape[2]
        in_width = out.shape[3]
        out_height = in_height * r
        out_width = in_width * r
        out = F.reshape(out, (batchsize, r, r, out_channels, in_height, in_width))
        out = F.transpose(out, (0, 3, 4, 1, 5, 2))
        out = F.reshape(out, (batchsize, out_channels, out_height, out_width))
        out = F.leaky_relu(out, 0.2)
        return out


class NetI(chainer.Chain):
    def __init__(self):
        super(NetI, self).__init__()
        with self.init_scope():
            i2v_model = CaffeFunction(
                '/home/orashi/Documents/illust2vec_tag_ver200.caffemodel')
            self.model = i2v_model
            self.mean = np.array([164.76139251, 167.47864617, 181.13838569])

    def __call__(self, images):
        images = F.average_pooling_2d(images, 2, 2)
        images = images / 2 + 0.5 * 255
        images = (
            F.broadcast_to(images, (1, 3, images.shape[2], images.shape[3])).transpose(
                (0, 2, 3, 1)) - self.mean).transpose(
            (0, 3, 1, 2))
        return self.model({'data': images}, outputs=['conv4_2'])[0]


class NetG(chainer.Chain):
    def __init__(self, ngf=64):
        super(NetG, self).__init__()
        with self.init_scope():
            self.toH = _ConvBlock('toH', 4, ngf, ksize=7, stride=1, pad=3)
            self.to0 = _ConvBlock('to0', 1, ngf // 2, ksize=3, stride=1, pad=1)
            self.to1 = _ConvBlock('to1', ngf // 2, ngf, ksize=4, stride=2, pad=1)
            self.to2 = _ConvBlock('to2', ngf, ngf * 2, ksize=4, stride=2, pad=1)
            self.to3 = _ConvBlock('to3', ngf * 3, ngf * 4, ksize=4, stride=2, pad=1)
            self.to4 = _ConvBlock('to4', ngf * 4, ngf * 8, ksize=4, stride=2, pad=1)

            self.m4 = _ConvBlock('m4', ngf * 8 + 512, ngf * 8, ksize=3, stride=1, pad=1)
            self.tunnel4 = _ResNeXtTunnel4()
            self.shuffle4 = _PixelShuffle('p4', 2)

            self.m3 = _ConvBlock('m3', ngf * 8, ngf * 4, ksize=3, stride=1, pad=1)
            self.tunnel3 = _ResNeXtTunnel3()
            self.shuffle3 = _PixelShuffle('p3', 2)

            self.m2 = _ConvBlock('m2', ngf * 4, ngf * 2, ksize=3, stride=1, pad=1)
            self.tunnel2 = _ResNeXtTunnel2()
            self.shuffle2 = _PixelShuffle('p2', 2)

            self.m1 = _ConvBlock('m1', ngf * 2, ngf, ksize=3, stride=1, pad=1)
            self.tunnel1 = _ResNeXtTunnel1()
            self.shuffle1 = _PixelShuffle('p1', 2)

            self.exit = conv_function('exit')

            self.netI = NetI()

    def __call__(self, sketch, hint):
        hint = self.toH(hint)
        sketch_feat = self.netI(sketch)

        x0 = self.to0(sketch)
        x1 = self.to1(x0)
        x2 = self.to2(x1)
        x3 = self.to3(F.concat((x2, hint), 1))  # !
        x4 = self.to4(x3)

        x = self.tunnel4(self.m4(F.concat((x4, sketch_feat), 1)))
        x = self.shuffle4(x)
        x = self.tunnel3(self.m3(F.concat((x, x3), 1)))
        x = self.shuffle3(x)
        x = self.tunnel2(self.m2(F.concat((x, x2), 1)))
        x = self.shuffle2(x)
        x = self.tunnel1(self.m1(F.concat((x, x1), 1)))
        x = self.shuffle1(x)
        x = F.tanh(self.exit(F.concat((x, x0), 1)))

        return x
