# -*- coding: utf-8 -*-
import mesh_ops
import image_ops
import numpy as np


def perform_saturation(x, tau):#饱和度
    x = x - np.mean(x)
    mad = np.mean(np.absolute(x - np.mean(x)))
    x = mesh_ops.clamp(x / (2 * mad), -tau, tau)
    return x