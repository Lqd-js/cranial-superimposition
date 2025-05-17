# -*- coding: utf-8 -*-

width_image=512#图片的宽
height_image=512#图片的高
ratio=0.85
height_content=height_image*ratio#obj模型在图片中的宽，高通过模型的宽和高之比自动计算，确保其小于图片的宽
input_dir="input"#输入数据所在文件夹
output_dir="output"
# background_color=0#图片的背景颜色
uni_height=True
depth_dir=output_dir+"/depth"
elev_dir=output_dir+"/elev"
curv_dir=output_dir+"/curv"
threeC_dir=output_dir+ "/3c"
data_augmentation=False
rotation_xs=[0]#[i*5 for i in range(-1,2)]
rotation_ys=[0]#[i*5 for i in range(-1,2)]
rotation_zs=[0]#[i*5 for i in range(-1,2)]
depth=True
elev=True
curv=True
# final=(depth and elev) or (depth and curv) or (elev and curv)
final=False
final_only=True
conditonal=False

