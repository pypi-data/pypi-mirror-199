# -*- coding: utf-8 -*-

# @File    : Single_Forecast.py
# @Date    : 2022-09-22
# @Author  : 24672

import netCDF4
import numpy as np
import datetime
import os
import math
import scipy.integrate
import scipy.interpolate

import baysalt.strDateTime as strDateTime

m_hours = [key for key in range(216)]
''' [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
       46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
        68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
       94, 95, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168]'''


class Single_Forecast():

    def __init__(self,_lon,_lat,_input,_output,_name,_area):
        self._lon =_lon
        self._lat =_lat
        self._input=_input
        self._output=_output
        self._name=_name
        self._area=_area

    def getsp(self, _date):
        """
        索引ww3点位,找到最近的ww3散点
        :param _date: 任务日期
        :param _hour: 小时
        :return: 点位No
        """
        _date=str(_date)
        filename =self._input+_date+'/ww3.'+_date+'.nc'

        w = netCDF4.Dataset(filename)  # 读取ww3_rizhao的nc文件，传入w中

        lon = w.variables['longitude'][:]
        lat = w.variables['latitude'][:]
        D = np.zeros((lon.size, 1))
        for i in range(lon.size):
            D[i] = (self._lon - lon[i]) ** 2 + (self._lat - lat[i]) ** 2  # 读取ww3_rizhao的nc文件，传入w中
        p = np.argwhere(D == min(D))

        return p

    def getfvsp(self, _date):
        """
        索引fvcome点位,找到最近的fvcom散点
        :param _date: 任务日期
        :param _hour: 小时
        :return: 点位No
        """
        _date=str(_date)
        filename ='/data/Output_250/fvcom_EAMS/'+_date+'/EAMSforecast_0001.nc'
        w = netCDF4.Dataset(filename)   # 读取ww3_rizhao的nc文件，传入w中

        lon = w.variables['lonc'][:]
        lat = w.variables['latc'][:]
        D = np.zeros((lon.size, 1))
        for i in range(lon.size):
            D[i] = (self._lon - lon[i]) ** 2 + (self._lat - lat[i]) ** 2  # 读取ww3_rizhao的nc文件，传入w中
        fvp = np.argwhere(D == min(D))

        return fvp

    def getMaxHS(self, _hs):
        """
        根据有效波高计算最大波高
        :param _hs: 有效波高
        :return: 最大波高
        """
        hs_max = _hs * 1.46

        return hs_max

    def getWind(self, _date, _idx):
        """
        获取风
        :param _date:
        :param _idx:
        :return:风速，风向
        """
        # 时间处理
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = '/home/ocean/Postprocess/160/Data/NC/wind10/'+self._area+'/'+date1.strftime('%Y%m%d')+'/'+self._area+'_'+date2.strftime(
            '%Y%m%d') + '.nc'   # 插值后的风场nc文件名
        # print(filename)
        nc_ds = netCDF4.Dataset(filename, 'r')

        lon = np.array(nc_ds.variables['longitude'])
        lat = np.array(nc_ds.variables['latitude'])
        latli = np.argmin(np.abs(lat - self._lat))
        lonli = np.argmin(np.abs(lon - self._lon))

        # 根据经纬度索引取值
        v = np.array(nc_ds.variables['v_VM'][idx, latli, lonli])
        dir = np.array(nc_ds.variables['dir_VM'][idx, latli, lonli])

        v_rtn = np.round(v, 2)
        dir_rtn = np.round(dir, 2)

        return str(v_rtn).rjust(14, " "), str(dir_rtn).rjust(14, " ")

    def getfvdata(self, _date, _idx, fvp, dep):
        """
        获取fvcome_eams数据
        :param _date: 任务日期
        :param _idx: 小时
        :param p: 点位
        :return: 流速，流向
        """
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = '/data/Output_250/fvcom_EAMS/' + date2.strftime(
            '%Y%m%d') + '/EAMSforecast_0001.nc'  # fvcom_EAMS nc文件名
        if not os.path.exists(filename):
            date3 = date2 + datetime.timedelta(days=-1)
            if not os.path.exists('/data/Output_250/fvcom_EAMS/' + date2.strftime('%Y%m%d')):
                os.mkdir('/data/Output_250/fvcom_EAMS/' + date2.strftime('%Y%m%d'))
            filename_old = '/data/Output_250/fvcom_EAMS/' + date3.strftime('%Y%m%d') + '/EAMSforecast_0001.nc'
            os.system('cp '+filename_old+' '+'/data/Output_250/fvcom_EAMS/' + date2.strftime('%Y%m%d'))
        w = netCDF4.Dataset(filename)   # 读取fvcom_EAMS的nc文件，传入w中
        fvcomu = w.variables['u'][idx, dep, fvp[0][0]]
        fvcomv = w.variables['v'][idx, dep, fvp[0][0]]

        # 计算流速和流向
        dir = math.atan2(fvcomu, fvcomv)
        dir = int(dir * 180 / math.pi)
        if dir < 0:
            dir = dir + 360
        speed = (fvcomu ** 2 + fvcomv ** 2) ** 0.5

        dir_rtn = np.round(float(dir), 2)
        speed_rtn = np.round(float(speed), 2)
        return str(speed_rtn).rjust(14, " "), str(dir_rtn).rjust(14, " ")

    def gettpxo(self, _date, _idx, dep):
        """
        获取tpxo数据
        :param _date: 任务日期
        :param _idx: 小时
        :return: 流速，流向
        """
        # 时间处理，不需要转cst
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        date2 = date1 + datetime.timedelta(hours=_idx)
        filename='/data/Postprocess/160/Data/input/tpxo/'+_date[0:4]+'_singlepoint_tpxo.nc'
        w = netCDF4.Dataset(filename, 'r', format='NETCDF4')
        lons = w.variables['longitude'][:]
        times = w.variables['TIME_CST'][:]

        row = 0
        for i in range(len(times)):
            if ("".join(times[i].astype(str).tolist())) == date2.strftime('%Y%m%d%H'):
                row = i
                break
        col = np.argmin(np.abs(lons - self._lon))

        # print(row,col)
        u_m = w.variables['u'][row, col]  # 中层流速u
        v_m = w.variables['v'][row, col]  # 中层流速v
        # 计算流速和流向
        dir = math.atan2(u_m, v_m)
        dir = int(dir * 180 / math.pi)
        if dir < 0:
            dir = dir + 360
        speed = (u_m ** 2 + v_m ** 2) ** 0.5

        if dep == 0:
            speed = 1.2 * speed  # 表层流速
        elif dep == 9:
            speed = 1.0 * speed  # 中层流速
        elif dep == 19:
            speed = 0.5 * speed  # 底层流速

        dir_rtn = np.round(float(dir), 2)
        speed_rtn = np.round(float(speed), 2)
        return str(speed_rtn).rjust(14, " "), str(dir_rtn).rjust(14, " ")

    def getDataFromSwan(self, _date, _idx, p):
        """
        获取ww3_djk数据
        :param _date: 任务日期
        :param _idx: 小时
        :param p: 点位
        :return: 有效波高，最大波高，涌浪有效波高，涌浪最大波高，风浪有效波高，风浪最大波高，波向，平均周期，风浪周期，涌浪周期，风浪波向，涌浪波向
        """
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
            '%Y%m%d') + '.nc'  # ww3 nc文件名

        w = netCDF4.Dataset(filename)  # 读取ww3_djk的nc文件，传入w中
        ww3hs = w.variables['hs'][idx, :]  # 有效波高
        ww3t02 = w.variables['t02'][idx, :]   # 平均周期
        ww3max = w.variables['hmaxe'][idx, :]  # 最大波高
        ww3dir = w.variables['dir'][idx, :]   # 波向

        # 依靠最近点进行索引
        out_ww3hs = ww3hs[p[0][0]]  # 有效波高
        out_ww3t02 = ww3t02[p[0][0]]  # 波周期
        out_ww3max = ww3max[p[0][0]]  # 最大波高
        out_ww3dir = ww3dir[p[0][0]]  # 波向

        # print(out_ww3hs)

        # 1.海浪要素
        hs_rtn = np.round(float(out_ww3hs), 2)  # 有效波高
        t02_rtn = np.round(float(out_ww3t02), 2)  # 波周期
        hs_max = np.round(float(out_ww3max), 2)  # 最大波高
        out_ww3dir = np.where(out_ww3dir < 100.0, out_ww3dir + 50.0, out_ww3dir)
        out_ww3dir = np.where(out_ww3dir > 150.0, out_ww3dir - 30.0, out_ww3dir)
        dir_rtn = np.round(float(out_ww3dir), 2)  # 浪向

        # 读取一位谱数据用于下面计算风浪和涌浪
        ef_filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
            '%Y%m%d') + '_ef.nc'  # ww3 nc文件名
        ww3_ef = netCDF4.Dataset(ef_filename)
        ef = ww3_ef.variables['ef'][:, :, p[0][0]]
        f = ww3_ef.variables['f'][:]

        # 2.风浪要素
        # 新的风浪替代公式
        sf2 = ef[idx, 18:30]
        fs2 = f[18:30]
        wndhs = 4 * math.sqrt(scipy.integrate.trapz(sf2, fs2))  # 计算风浪有效波高
        wndtm = math.sqrt(scipy.integrate.trapz(sf2, fs2) / scipy.integrate.trapz(np.multiply(fs2 ** 2, sf2), fs2))  # 计算风浪有效周期
        wndmaxhs = self.getMaxHS(wndhs)  # 计算风浪最大波高

        wndhs_rtn = np.round(wndhs, 2)  # 风浪有效波高
        wndtm_rtn = np.round(wndtm, 2)  # 风浪周期
        wndmaxhs_rtn = np.round(wndmaxhs, 2)  # 风浪最大波高
        wnddir_rtn = dir_rtn  # 风浪波向用dir替代

        # 3.涌浪要素
        # 新的涌浪计算公式
        sf1 = ef[idx, 0:18]
        fs1 = f[0:18]
        shs = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
        swelltm =math.sqrt(scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1), fs1))  # 计算涌浪有效周期
        maxshs = self.getMaxHS(shs)  # 计算涌浪最大波高

        shs_rtn = np.round(shs, 2)  # 涌浪有效波高
        swelltm_rtn = np.round(swelltm, 2)  # 涌浪周期
        maxshs_rtn = np.round(maxshs, 2)  # 涌浪最大波高
        swelldir_rtn = dir_rtn # 涌浪波向dir替代

        if str(hs_max).strip() == "nan":  # 最大波高为nan，用1.46*HS
            hs_max = self.getMaxHS(hs_rtn)
            hs_max = np.round(float(hs_max), 2)  # 最大波高

        return str(hs_rtn).rjust(14, " "), str(hs_max).rjust(14, " "), str(shs_rtn).rjust(14, " "), \
               str(maxshs_rtn).rjust(14, " "), str(wndhs_rtn).rjust(14, " "), str(wndmaxhs_rtn).rjust(14, " "), \
               str(dir_rtn).rjust(14, " "), str(t02_rtn).rjust(14, " "), str(swelltm_rtn).rjust(14, " "), str(
            swelldir_rtn).rjust(14, " "), \
               str(wndtm_rtn).rjust(14, " "), str(wnddir_rtn).rjust(14, " ")

    def getH4H10CGE(self, _date, _idx, p):
        """
        获取ww3_djk数据
        :param _date: 任务日期
        :param _idx: 小时
        :param p: 点位
        :return: H4 H10 CGE PP
        """
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
            '%Y%m%d') + '.nc'  # ww3 nc文件名

        w = netCDF4.Dataset(filename)  # 读取ww3_djk的nc文件，传入w中
        ww3hs = w.variables['hs'][idx, :]
        ww3cge = w.variables['cge'][idx, :]
        ww3fp = w.variables['fp'][idx, :]
        out_ww3hs = ww3hs[p[0][0]]  # 有效波高
        out_ww3cge = ww3cge[p[0][0]]  # 能量流
        out_ww3fp = ww3fp[p[0][0]]  # 谱峰周期

        # # 水深数据读取
        # py_file_path = os.path.dirname(os.path.abspath(__file__))  # 当前python文件所在位置
        # filename = py_file_path + '/depth_djk.nc'  # depth nc文件名
        # w = netCDF4.Dataset(filename)  # 读取水深的nc文件，传入w中
        # depth = w.variables['depth'][:]
        # d = depth[p[0][0]]
        # 平均波高Hp
        Hp = (0.747*out_ww3hs)/1.129
        # Hd = Hp/d

        # H4
        H4 = 2.024*Hp
        # H10
        H10 = 1.712*Hp
        # pp
        PP = 1/out_ww3fp

        H4_rtn = np.round(H4, 2)
        H10_rtn = np.round(H10, 2)
        cge_rtn = np.round(out_ww3cge, 2)
        PP_rtn = np.round(PP, 2)
        return str(H4_rtn).rjust(14, " "), str(H10_rtn).rjust(14, " "), str(cge_rtn).rjust(14, " "), str(PP_rtn).rjust(14, " ")

    def grtfl(self, _date):
        """
        构建预报单信息
        :param _date: 预报单日期
        :return: 0-生成预报数据成功  大于等于1-生成预报数据失败
        """
        isTemp = False  # 是否未来日期的扩展任务
        today = strDateTime.getToday()
        if _date <= today:
            isTemp = True
        else:
            isTemp = False

        lon_g =self._lon
        lat_g =self._lat
        outpath=self._output

        file_path =outpath
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # 写入文件内容----------------------------------begin
        _date0 = _date
        list_hours = []
        list_hours.append(m_hours)

        sp = self.getsp(_date0)  # 索引点位
        # fvp = self.getfvsp(_date0)
        for k in range(0, 1):
            tmp = list_hours[k]
            list = []
            file_name = self._name + strDateTime.addDays(_date, k) + ".txt"
            file = os.path.join(file_path, file_name)

            fl = open(file, "w")
            # 写入文件头----------------------------------begin
            fh_time = " ".rjust(10, " ")  # 第一列日期留空白

            fh_hs = "swh".rjust(14, " ")  # 有效波高
            fh_dir = "mwd".rjust(14, " ")  # 波向
            fh_t01 = "mwp".rjust(14, " ")  # 平均周期
            fh_hmaxe = "hmax".rjust(14, " ")  # 最大波高

            fh_wwhs = "shww".rjust(14, " ")  # 风浪有效波高
            fh_wwdir = "mdww".rjust(14, " ")  # 风浪向
            fh_wwtm = "mpww".rjust(14, " ")  # 风浪平均周期
            fh_wwhmaxe = "hmaxw".rjust(14, " ")  # 风浪最大波高

            fh_swellhs = "shts".rjust(14, " ")  # 涌浪有效波高
            fh_swelldir = "mdts".rjust(14, " ")  # 涌浪向
            fh_swelltm = "mpts".rjust(14, " ")  # 涌浪平均周期
            fh_swellhmaxe = "hmaxs".rjust(14, " ")  # 涌浪最大波高

            fh_wndspeed = "windspeed".rjust(14, " ")  # 风速
            fh_wnddir = "winddir".rjust(14, " ")  # 风向

            fh_cspeeds = "currentspeeds".rjust(14, " ")  # 表层流速
            fh_cdirs = "currentdirs".rjust(14, " ")  # 表层流向
            fh_cspeedm = "currentspeedm".rjust(14, " ")  # 中层流速
            fh_cdirm = "currentdirm".rjust(14, " ")  # 中层流向
            fh_cspeedb = "currentspeedb".rjust(14, " ")  # 底层流速
            fh_cdirb = "currentdirb".rjust(14, " ")  # 底层流向

            fh_h4 = "h4".rjust(14, " ")  # 百分之4大波
            # fh_h10 = "H10".rjust(14, " ")  # 十分之1大波
            fh_CGE = "CGE".rjust(14, " ")  # 能量流
            fh_PP = "pp1d".rjust(14, " ")  # 谱峰周期

            fl.writelines([fh_time, fh_hs, fh_dir, fh_t01, fh_hmaxe, fh_wwhs, fh_wwdir, fh_wwtm, fh_wwhmaxe,
                           fh_swellhs, fh_swelldir, fh_swelltm, fh_swellhmaxe, fh_wndspeed, fh_wnddir,
                           fh_cspeeds, fh_cdirs, fh_cspeedm, fh_cdirm, fh_cspeedb, fh_cdirb,
                           fh_h4, fh_CGE, fh_PP, "\n"])
            # 写入文件头----------------------------------end

            for i in range(0, max(tmp) + 1):  # +72

                fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                fc_hs, fc_hmaxe, fc_swellhs, fc_swellhmaxe, fc_wwhs, fc_wwhmaxe, fc_dir, fc_t01,fc_swelltm, fc_swellDIR, fc_wwtm, fc_wwdir= \
                    self.getDataFromSwan(_date0, i, sp)  # 有效波高/最大波高

                fc_v, fc_wir = self.getWind(_date0, i)  # 风速/风向

                fc_h4, fc_h10, fc_CGE , fc_PP= self.getH4H10CGE(_date0, i, sp)  # H4/H10/CGE/PP

                fc_cspeeds, fh_cdirs = self.gettpxo(_date0, i, 0)
                fc_cspeedm, fh_cdirm = self.gettpxo(_date0, i, 9)
                fc_cspeedb, fh_cdirb = self.gettpxo(_date0, i, 19)
                # fc_cspeeds, fh_cdirs = self.getfvdata(_date0, i, fvp, 0)   #fvcom
                # fc_cspeedm, fh_cdirm = self.getfvdata(_date0, i, fvp, 9)
                # fc_cspeedb, fh_cdirb = self.getfvdata(_date0, i, fvp, 19)

                # if fc_wwdir.strip() == "nan" :  # 风浪方向为空时，采用综合波向代替
                #     fc_wwdir = fc_dir
                #
                # if fc_swellDIR.strip() == "nan":  # 涌浪方向为空时，采用综合波向代替
                #     fc_swellDIR = fc_dir
                #
                # if  fc_wwhs.strip() == "nan":  # 风浪浪高为空时，采用hs*0.7代替
                #     fc_wwhs=str(np.round(float(fc_hs) * 0.7, 2)).rjust(12, " ")
                #     fc_wwhmaxe=str(np.round(float(fc_wwhs) * 1.68, 2)).rjust(12, " ")

                if fc_PP.strip() == "--":  # 谱峰周期为空时，采用2.99代替
                    fc_PP = str(2.99).rjust(14, " ")
                if (i in m_hours):
                    fl.writelines([fc_time, fc_hs, fc_dir, fc_t01, fc_hmaxe, fc_wwhs, fc_wwdir, fc_wwtm, fc_wwhmaxe,
                                   fc_swellhs, fc_swellDIR, fc_swelltm, fc_swellhmaxe, fc_v, fc_wir,
                                   fc_cspeeds, fh_cdirs, fc_cspeedm, fh_cdirm, fc_cspeedb, fh_cdirb,
                                   fc_h4, fc_CGE, fc_PP, "\n"])
                    print("hour in=" + str(i))
                else:
                    print("hour=" + str(i))

            fl.close()

    def getTime(self, _date, _hour):
        """
        获取预报的日期/小时
        :param _date: 任务日期
        :param _hour: 小时
        :return: 日期/小时(10位长度的字符串)
        """
        if _hour == 215:
            _hour = 215

        date = strDateTime.convertToTime(_date)
        date_t = date + datetime.timedelta(hours=int(_hour))

        return date_t.strftime('%Y%m%d%H')





