# -*- coding: utf-8 -*-

# @File    : pic_draw.py
# @Date    : 2023-01-17
# @Author  : Dovelet
import sys
import os
import re
import math
from ftplib import FTP
import netCDF4
import numpy as np
from netCDF4 import Dataset
from scipy.interpolate import griddata
from itertools import chain
import datetime
from scipy.interpolate import interp2d

py_file_path = os.path.dirname(__file__)

class Chazhi():
    def __init__(self,area):
        self.area=area
        self.svdir = '/data/Postprocess/160/Data/NC'

    def setting(self,area):
        """
        设置参数
        sv 为保存路径和文件中的区域和分辨率的表达式
        lonmin,lonmax 为目标区域经度范围
        latmin,latmax 为目标区域纬度范围
        re_ra 为resolution ratio即网格分辨率
        """
        if area=='dl':
            self.sv = '121.7E_122.0E_38.8N_39.1N_400'

            self.directory = '/data/ForecastSystem/WW3_6.07/Output/ww3_dalian'  # 大连港数据路径
            self.id='id_dlg_400.nc'
            self.water='water_dlg_400.nc'

            self.lonmin = 121.87
            self.lonmax = 121.96
            self.latmin = 38.92
            self.latmax = 39.01
            self.re_ra = 400

        elif area=='ls':
            self.sv = '119.21E_119.52E_34.95N_35.26N_120'

            self.directory = '/data/Output_160/ww3_lanshan'  # 岚山港数据路径
            self.id = 'id_lsg_120.nc'
            self.water = 'water_lsg_120.nc'

            self.lonmin = 119.21
            self.lonmax = 119.52
            self.latmin = 34.95
            self.latmax = 35.26
            self.re_ra = 120

        elif area=='yt':
            self.sv = '121.03E_121.16E_37.70N_37.83N_120'

            self.directory = '/data/ForecastSystem/WW3_6.07/Output/ww3_yantai'  # 烟台港数据路径
            self.id = 'id_ytg_120.nc'
            self.water = 'water_ytg_120.nc'

            self.lonmin = 121.03
            self.lonmax = 121.16
            self.latmin = 37.70
            self.latmax = 37.83
            self.re_ra = 120

        elif area=='rz':
            self.sv = '119.42E_119.60E_35.23N_35.41N_120'

            self.directory = '/home/ocean/haibotai/model_dlg'  # 日照港数据路径
            self.id = 'id_rzg_120.nc'
            self.water = 'water_rzg_120.nc'

            self.lonmin = 119.42
            self.lonmax = 119.60
            self.latmin = 35.23
            self.latmax = 35.41
            self.re_ra = 120

    def bianjie(self,n):
        if n == 0:
            waters = Dataset(f'/home/ocean/Oceanmax/Data/input/Interpolation/{self.water}')
        if n == 1:
            waters = Dataset(f'/home/ocean/Oceanmax/Data/input/Interpolation/{self.water}')
        water_id = waters['id'][:]
        water_id = water_id.reshape(1, len(water_id) * 4)
        id = water_id.tolist()
        id_fin = id[0]
        a = list(dict.fromkeys(id_fin))
        return a

    def near_inter(self,x_new, y_new, values, switchs):
        """
        x_new建立的插值格点的纬度，y_new建立的插值格点的经度
        values散点数据
        switchs控制是小区还是大区，0为大区，1为小区
        """
        if switchs == 0:
            m = Dataset(f'/home/ocean/Oceanmax/Data/input/Interpolation/{self.id}')
            index = m.variables['id'][:]
            index = list(index)
        if switchs == 1:
            m = Dataset(f'/home/ocean/Oceanmax/Data/input/Interpolation/{self.id}')
            index = m.variables['id'][:]
            index = list(index)

        grid_i, grib_j = x_new.shape
        result = np.zeros([grid_i, grib_j], np.float64)
        lat_number = len(x_new)
        lon_number = len(y_new)
        # 边界识别
        a = self.bianjie(switchs)
        for ilat in range(lat_number):
            for ilon in range(lon_number):
                if ilat * lat_number + ilon not in a:  # 水深大于0是陆地
                    result[ilat, ilon] = np.nan
                    continue
                else:

                    result[ilat, ilon] = values[index[ilat * lat_number + ilon]]

        return result

    def mkdir(self,path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path)
            return True
        else:
            return False

    def select_folder(self,filelist, nowday):
        #### 筛选出存放数据的文件夹并排序
        fd = datetime.datetime.strptime(nowday, "%Y%m%d")
        eta = (fd - datetime.timedelta(days=1)).strftime("%Y%m%d")

        delnum = 0
        for i in range(len(filelist)):
            if filelist[delnum][0] != '2' or filelist[delnum] < eta:
                del filelist[delnum]
            else:
                delnum = delnum + 1
        filelist.sort(key=lambda x: int(x[:]))

        mylist = filelist

        print(mylist)
        return mylist

    def folder_filename(self,dir, nowday):
        directory = dir
        filelist = os.listdir(directory)
        file_list = self.select_folder(filelist, nowday)
        return file_list

    def hourNums(self,eta_temp):

        fd = datetime.datetime.strptime(eta_temp, "%Y%m%d%H")
        eta = (fd + datetime.timedelta(hours=8)).strftime("%Y%m%d%H")

        return eta


    def hour(self,eta_temp):

        fd = datetime.datetime.strptime(eta_temp, "%H")
        eta = (fd + datetime.timedelta(hours=8)).strftime("%H")

        return eta


    def ncrename(self,outpath):
        filelist=os.listdir(outpath)
        filelist = sorted(filelist, key=lambda x: os.path.getmtime(os.path.join(outpath, x)))
        for i in range(0,16):
            filepath=os.path.join(outpath,filelist[i])
            os.system('rm -rf '+filepath)

        for i in range(-8,0):
            filepath = os.path.join(outpath, filelist[i])
            os.system('rm -rf ' + filepath)

        filelist = os.listdir(outpath)
        filelist = sorted(filelist, key=lambda x: os.path.getmtime(os.path.join(outpath, x)))

        for f in filelist:
            oriname=os.path.join(outpath, f)
            oritime=f[-13:-3]
            newtime=self.hourNums(oritime)
            f1=f.replace(oritime,newtime+'@')
            newname=os.path.join(outpath, f1)
            os.rename(oriname,newname)

        filelist = os.listdir(outpath)
        filelist = sorted(filelist, key=lambda x: os.path.getmtime(os.path.join(outpath, x)))

        for f in filelist:
            oriname = os.path.join(outpath, f)
            f1 = f.replace('@','')
            newname = os.path.join(outpath, f1)
            os.rename(oriname, newname)
        print('Rename is done.')


    def jion_strs(self,strs):
        return ' '.join(strs)

    def grid(self,_date):

        nowday = ''
        if len(_date) != 8:
            nowday = str(int(datetime.datetime.now().strftime("%Y%m%d")))  # 运行日期，从运行当天开始
        elif len(_date) == 8:
            nowday = str(_date)
        print(nowday)

        py_file_path = os.path.dirname(os.path.abspath(__file__))
        self.setting(self.area) # 初始化输入输出文件位置，文件保存名

        num_grid = int(round(self.latmax - self.latmin, 2) * self.re_ra)
        lon_new = np.linspace(self.lonmin, self.lonmax, num_grid)  # 创建插值格点
        lat_new = np.linspace(self.latmin, self.latmax, num_grid)
        lat_num_grid = int(round(self.latmax - self.latmin, 2) *self.re_ra)
        lon_num_grid = int(round(self.lonmax - self.lonmin, 2) * self.re_ra)
        y_new, x_new = np.meshgrid(lon_new, lat_new)

        filelist_need = self.folder_filename(self.directory, nowday)
        for item in filelist_need:
            print(f'{self.area}正在读取数据')
            filename = self.directory + '/' + item + '/' + 'ww3.' + item + '.nc'

            nc_obj = Dataset(filename)  # 读取数据

            lon = nc_obj['longitude']
            lat = nc_obj['latitude']
            time = nc_obj['time']
            t02 = nc_obj['t02']  # N*24
            hs = nc_obj['hs']  # N*24
            dir = nc_obj['dir']  # N*24
            for i in range(len(time)):
                t = str(i)  # 参数小时
                print('运行：', item + '-' + t)
                H = t.zfill(2)

                t02_new = np.ones((lat_num_grid, lon_num_grid))
                hs_new = np.ones((lat_num_grid, lon_num_grid))
                u_new = np.ones((lat_num_grid, lon_num_grid))
                v_new = np.ones((lat_num_grid, lon_num_grid))
                dir_new = np.ones((lat_num_grid, lon_num_grid))


                # 插值
                # SWH要素插值
                hs_new[:, :] = self.near_inter(x_new, y_new, hs[i, :], 1)
                dir_new[:, :] =self.near_inter(x_new, y_new, dir[i, :], 1)
                u_new[:, :] = -1 * np.sin(np.deg2rad(dir_new))
                v_new[:, :] = -1 * np.cos(np.deg2rad(dir_new))



                t02_new[:, :] = self.near_inter(x_new, y_new, t02[i, :], 1)

                # 保存
                t = str(i)
                H = t.zfill(2)  # 参数小时

                ## 6.awp ##
                svpath = self.svdir + '/mwp/mwp_' + self.sv + '/' \
                         + nowday + '/' + nowday  # 保存路径
                self.mkdir(svpath)
                ncfile = netCDF4.Dataset(svpath + '/mwp_' + self.sv + '_' + item + H + '.nc', 'w',
                                         format='NETCDF3_64BIT')
                ncfile.createDimension('lon', lon_num_grid)
                ncfile.createDimension('lat', lat_num_grid)
                ncfile.createVariable('lon', np.float64, ('lon'))
                ncfile.createVariable('lat', np.float64, ('lat'))
                ncfile.createVariable('awp', np.float64, ('lat', 'lon'))
                ncfile.variables['lon'][:] = lon_new[:]
                ncfile.variables['lat'][:] = lat_new[:]
                ncfile.variables['awp'][:, :] = t02_new[:, :]
                ncfile.close()
                ## 7.swh ##
                svpath = self.svdir + '/swh/swh_' + self.sv + '/' \
                         + nowday + '/' + nowday  # 保存路径
                self.mkdir(svpath)
                ncfile = netCDF4.Dataset(svpath + '/swh_' + self.sv + '_' + item + H + '.nc', 'w',
                                         format='NETCDF3_64BIT')
                ncfile.createDimension('lon', lon_num_grid)
                ncfile.createDimension('lat', lat_num_grid)
                ncfile.createVariable('lon', np.float64, ('lon'))
                ncfile.createVariable('lat', np.float64, ('lat'))
                ncfile.createVariable('dir', np.float64, ('lat', 'lon'))
                ncfile.createVariable('hs', np.float64, ('lat', 'lon'))
                ncfile.createVariable('u', np.float64, ('lat', 'lon'))
                ncfile.createVariable('v', np.float64, ('lat', 'lon'))
                ncfile.variables['lon'][:] = lon_new[:]
                ncfile.variables['lat'][:] = lat_new[:]
                ncfile.variables['hs'][:, :] = hs_new[:, :]
                ncfile.variables['u'][:, :] = u_new[:, :]
                ncfile.variables['v'][:, :] = v_new[:, :]
                ncfile.variables['dir'][:, :] = dir_new[:, :]
                ncfile.close()

        self.ncrename(self.svdir + '/mwp/mwp_' + self.sv + '/' \
                         + nowday + '/' + nowday)
        self.ncrename(self.svdir + '/swh/swh_' + self.sv + '/' \
                         + nowday + '/' + nowday)

if __name__ == '__main__':
    _date = sys.argv[-1]
    dl=Chazhi('dl')
    dl.grid(_date)

    ls=Chazhi('ls')
    ls.grid(_date)
    yt=Chazhi('yt')
    yt.grid(_date)
