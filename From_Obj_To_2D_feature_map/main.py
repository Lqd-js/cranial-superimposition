# -*- coding: utf-8 -*-
import os
import pywavefront
import numpy as np
import utils
from face3d import mesh_numpy
import config
import random

"""输出不同投影图片,设置config.py文件"""


"""读取并返回指定路径下的所有obj文件的名称"""
obj_names=utils.load_names_from_folder(config.input_dir)

"""检查是否有数据输入"""
if len(obj_names)==0:
    print("None input data")


"""循环读取文件夹下的每个obj模型，并单独进行处理"""        
for i in range(len(obj_names)):
    
    """读取obj并获取点、面信息数组"""
    name=obj_names[i]
    obj_path=os.path.join(config.input_dir, name)#obj完整路径
    #读取并返回obj模型，此方法的返回称为scene不单纯为obj模型
    scene=pywavefront.Wavefront(obj_path, collect_faces=True)
    vertices= np.asarray(scene.vertices)#获取顶点数组
    faces=np.asarray(scene.mesh_list[0].faces)#面数组

    
    """调整模型位置大小旋转到正确的投影位置"""
    R = mesh_numpy.transform.angle2matrix([90, 0, 0]) #rotation 
    t = [0, 0, 0] #tansformation
    s=1 #scale
    if config.uni_height == False: #如果要得到高度不统一的投影，需将模型缩放到合适的大小，s为缩放比例   
        s = 1/0.83
    vertices = mesh_numpy.transform.similarity_transform(vertices, s, R, t)
    
    """不同角度投影"""
    
    if config.data_augmentation:

        for x in range(1):
            for y in range(1):
                for z in range(1):

                    rx=random.uniform(-10, 0) if x==0 else random.uniform(0, 10)
                    ry=random.uniform(-10, 0) if y==0 else random.uniform(0, 10)
                    rz=random.uniform(-10, 0) if z==0 else random.uniform(0, 10)
                    R = mesh_numpy.transform.angle2matrix([rx, ry, rz]) #rotation

                    t = [0, 0, 0] #tansformation
                    s=1
                    vertices_r = mesh_numpy.transform.similarity_transform(vertices, s, R, t)
                    name_r=name[0:-4]+"_"+str(x)+"_"+str(y)+"_"+str(z)+"_0"
                    #print(rx,ry,rz)
                    utils.mesh_to_3channel_image(vertices_r,faces,name_r)
         
    for x in config.rotation_xs:
        for y in config.rotation_ys:
            for z in config.rotation_zs:
                R = mesh_numpy.transform.angle2matrix([x, y, z]) #rotation 

                t = [0, 0, 0] #tansformation
                s=1
                vertices_r = mesh_numpy.transform.similarity_transform(vertices, s, R, t)
                name_r=name[0:-4]+"_0"#+"_"+str(x)+"_"+str(y)+"_"+str(z)
                utils.mesh_to_3channel_image(vertices_r,faces,name_r)
    print("(",i+1,",",name,")")

