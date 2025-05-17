import numpy as np
from scipy.interpolate import LinearNDInterpolator
from skimage import draw

def hole_filter(img,x,y):
    count=0
    _sum=0
    for i in range(x-1,x+2):
        for j in range(y-1,y+2):
            if img[i][j]!=0:
                count+=1
                _sum+=img[i][j]
    if count>=2:
        return int(_sum/count)
    else:
        return 0
    


def build_image_array(proj_shape, z3d, w, h,interpolating,background_color,depth=255):# 2d shape ;attribute ;w ;h
    

    step = 1
    # Scale data
    z3d = np.interp(z3d, (z3d.min(), z3d.max()), (0, depth))#线性插值，将属性数据映射到0-255
    
    proj_shape=proj_shape.astype(int)
    
    if interpolating!=2:
        img=np.zeros([h,w], dtype = int)
        for i in range (len(proj_shape)):
            if np.isnan(z3d[i]):
                return img;
            img[proj_shape[i,1]][proj_shape[i,0]]=z3d[i]
        if interpolating==0:
            return img
        for i in range(1):
            
            aux_x=[]
            aux_y=[]
            aux_v=[]
            
            for x in range(min(proj_shape[:,1]),max(proj_shape[:,1])):
                for y in range(min(proj_shape[:,0]),max(proj_shape[:,0])):
                    if img[x][y]==0:
                        temp=hole_filter(img, x, y)
                        if temp!=0:
                            aux_x.append(x)
                            aux_y.append(y)
                            aux_v.append(temp)
            for i in range(len(aux_v)):
                img[aux_x[i]][aux_y[i]]=aux_v[i]
        return np.uint8(img)


    # Build grid
    Xsampling = np.arange(0, w, step, dtype='float')#生成按step递进的数组
    Ysampling = np.arange(0, h, step, dtype='float')
    x_grid, y_grid = np.meshgrid(Xsampling, Ysampling)#Return coordinate matrices from coordinate vectors

    Fz = LinearNDInterpolator(proj_shape, z3d,fill_value=0)#通过线性插值将属性值放入指定的坐标
    
    depth_im = Fz(x_grid, y_grid)#

    mask3d = np.isnan(depth_im)#返回数组中值为Nan的index
    
    depth_im[mask3d] = 0#将图片数组中非内容区域全部设为零
    depth_im = np.uint8(depth_im)
    return depth_im


def add_black_border(img):
    dim = img.shape
    offset = int(np.floor(np.abs((dim[0]-dim[1])/2)))

    if dim[0] < dim[1]:
        border = np.zeros((offset, dim[1], img.shape[2]), dtype=np.uint8)
        img = np.vstack((border, img, border))
    else:
        border = np.zeros((dim[0], offset, img.shape[2]), dtype=np.uint8)
        img = np.hstack((border, img, border))
    return np.uint8(img)


def poly2mask(vertex_row_coords, vertex_col_coords, shape):
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask