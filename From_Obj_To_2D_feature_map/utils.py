# -*- coding: utf-8 -*-

import os
import numpy as np
import mesh_ops
import config
from face3d import mesh_numpy
import utils
import imageio
from PIL import Image

def name_rotation(name,x,y,z):
    return name[0:-4]+"_"+str(x)+"_"+str(y)+"_"+str(z) 
def name(name,x,y,z):
    return name[0:-4]
"""读取并返回指定路径下的所有obj文件的名称"""
def load_names_from_folder(path):
    names=[name for name in os.listdir(path) if name.endswith(".obj")]
    return names;

def mesh_projection(vertices,faces,attribute,c=1):#延Z轴正投影到 x,y平面
    if c==1:
        attribute=np.reshape(attribute, [attribute.shape[0],1]) 

    for i in range(c):
        attribute[:,i]=np.interp(attribute[:,i], (min(attribute[:,i]), max(attribute[:,i])), (0, 255))
    attribute=attribute.reshape([attribute.shape[0],c])
    image_vertices = mesh_numpy.transform.to_image(vertices, config.height_image, config.width_image,config.height_content,uni_height=config.uni_height)
    image = mesh_numpy.render.render_colors(image_vertices, faces, attribute, config.height_image, config.width_image, c=c)
    # 处理无效值
    image = np.nan_to_num(image)
    # 确保数值在 uint8 范围内
    image = np.clip(image, 0, 255)
    image = np.uint8(image)
    if config.conditonal:
        image[0,0]=255
    return image   

def mesh_to_3channel_image(vertices,faces,name):
    """计算曲率、法向仰角信息数组"""
    #Compute Curvatures
    colors_curv=None
    if config.curv :       
        Umin, Umax, Cmin, Cmax, Cmean, Cgauss, Normal = mesh_ops.compute_curvature(vertices, faces)
        colors_curv = utils.perform_saturation(np.abs(Cmin)+np.abs(Cmax), 2)
    #Compute Normals
    elevation=None
    if config.elev :
        normals, normalf = mesh_ops.compute_normals(vertices, faces)
        normals = normals.T
        #Compute Elevation of Normals
        azimuth, elevation, r = mesh_ops.cart2sph(normals[:, 0], normals[:, 1], normals[:, 2])
    depth=None
    if config.depth :
        depth=vertices[:,2].T      
    """渲染构建图片数组"""
    thr_c=None
    final_image=None
    thr_c_list=[depth,colors_curv,elevation]
    if config.final_only:
        for attr in thr_c_list:
            if attr is not None :
                attr=np.reshape(attr, [attr.shape[0],1]) 
                if thr_c is not None:
                    thr_c=np.concatenate((thr_c,attr),axis=-1)
                else:
                    thr_c=attr
        final_image=mesh_projection(vertices,faces,thr_c,c=3)
    # else :
        depth_im=np.zeros([config.height_image,config.width_image], dtype = np.uint8)
        if depth is not None:
            # path_depth_im=config.depth_dir+"/"+"depth_"+name+".png"
            path_depth_im = config.depth_dir + "/"+ name + ".png"
            depth_im=mesh_projection(vertices,faces,depth)
            #imageio.imwrite(path_depth_im, depth_im)

            # print(depth_im.shape)
            #使用Pillow保存图像
            depth_im = np.squeeze(depth_im) #去除通道
            depth_im = Image.fromarray(depth_im)
            depth_im.save(path_depth_im)

        elev_im=np.zeros([config.height_image,config.width_image], dtype = np.uint8)
        if elevation is not None:
            # path_elev_im=config.elev_dir+"/"+"elve_"+name+".png"
            path_elev_im=config.elev_dir+"/"+name+".png"
            elev_im=mesh_projection(vertices,faces,elevation)
            # imageio.imwrite(path_elev_im, elev_im)

            #使用Pillow保存图像
            elev_im = np.squeeze(elev_im) #去除通道
            elev_im = Image.fromarray(elev_im)
            elev_im.save(path_elev_im)

        curv_im=np.zeros([config.height_image,config.width_image], dtype = np.uint8)
        if colors_curv is not None:
            # path_curv_im=config.curv_dir+"/"+"curv_"+name+".png"
            path_curv_im=config.curv_dir+"/"+name+".png"
            curv_im=mesh_projection(vertices,faces,colors_curv)
            # imageio.imwrite(path_curv_im, curv_im)

            # print(curv_im.shape)
            #使用Pillow保存图像
            curv_im = np.squeeze(curv_im) #去除通道
            curv_im = Image.fromarray(curv_im)
            curv_im.save(path_curv_im)

        if config.final:
            final_image = np.concatenate((depth_im, curv_im, elev_im), axis=-1)
 
    
    """将数组写入图片文件"""
    if final_image is not None:       
        path_final_image=config.threeC_dir+"/"+name+".png"
        imageio.imwrite(path_final_image, final_image)


"""获取二维投影，并进行缩放"""
def get_projected_vertices(vertices,img_width,img_height,target_height):
    #平行于y轴投影到x,z平面,直接取x,z坐标
    x = vertices[:,0]
    z = -vertices[:,2] #负号用以调整内容在图片中的上下翻转，同理x也可加符号调整
    y=vertices[:1]
    ratio = (x.max()-x.min())/(z.max()-z.min())#模型的宽(x)和高(z)之比
    content_y=target_height*(y.max()-y.min())/(z.max()-z.min())*2
    x = np.interp(x, (x.min(), x.max()), ((img_width-target_height*ratio)/2, img_width-(img_width-target_height*ratio)/2))#一维线性插值，将原坐标映射到合适的坐标区域
    z=np.interp(z, (z.min(), z.max()),((img_height-target_height)/2, img_height-(img_height-target_height)/2))
   
    vertices_2d = np.asarray(list(zip(x, z)))
    if content_y>255:
        content_y=255
        
    return vertices_2d,int(content_y)

def perform_saturation(x, tau):#饱和度
    x = x - np.mean(x)
    mad = np.mean(np.absolute(x - np.mean(x)))
    x = mesh_ops.clamp(x / (2 * mad), -tau, tau)
    return x

