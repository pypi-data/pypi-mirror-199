# -*- coding: utf-8 -*-

# @File    : Single_Forecast_js.py
# @Date    : 2022-09-22
# @Author  : 24672

# sourcery skip: identity-comprehension
import netCDF4
import numpy as np
import datetime
import os
import math
import scipy.integrate
import scipy.interpolate
import json
import baysalt.strDateTime as strDateTime

m_hours = [key for key in range(216)]
''' [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
       46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67,
        68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93,
       94, 95, 96, 102, 108, 114, 120, 126, 132, 138, 144, 150, 156, 162, 168]'''


class Single_Forecast():

    def __init__(self,_lon,_lat,_input,_output,_name,_area,**_new_dict):
        self._lon =_lon
        self._lat =_lat
        self._input=_input
        self._output=_output
        self._name=_name
        self._area=_area
        self._new_dict=_new_dict

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

        v_rtn = np.round(float(v), 2)
        dir_rtn = np.round(float(dir), 2)

        return v_rtn, dir_rtn

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
        return speed_rtn,dir_rtn

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
        filename='/data/Postprocess/160/Data/input/tpxo/'+date2.strftime('%Y')+'_singlepoint_tpxo.nc'
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
        return speed_rtn,dir_rtn

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
        print('hour in = ' + str(_idx+8) )
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

        wndhs_rtn = np.round(float(wndhs), 2)  # 风浪有效波高
        wndtm_rtn = np.round(float(wndtm), 2)  # 风浪周期
        wndmaxhs_rtn = np.round(float(wndmaxhs), 2)  # 风浪最大波高
        wnddir_rtn = dir_rtn  # 风浪波向用dir替代

        # 3.涌浪要素
        # 新的涌浪计算公式
        sf1 = ef[idx, 0:18]
        fs1 = f[0:18]
        shs = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
        swelltm =math.sqrt(scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1), fs1))  # 计算涌浪有效周期
        maxshs = self.getMaxHS(shs)  # 计算涌浪最大波高

        shs_rtn = np.round(float(shs), 2)  # 涌浪有效波高
        swelltm_rtn = np.round(float(swelltm), 2)  # 涌浪周期
        maxshs_rtn = np.round(float(maxshs), 2)  # 涌浪最大波高
        swelldir_rtn = dir_rtn # 涌浪波向dir替代

        if str(hs_max).strip() == "nan":  # 最大波高为nan，用1.46*HS
            hs_max = self.getMaxHS(hs_rtn)
            hs_max = np.round(float(hs_max), 2)  # 最大波高

        return hs_rtn, hs_max, shs_rtn, \
               maxshs_rtn, wndhs_rtn, wndmaxhs_rtn, \
               dir_rtn,t02_rtn, swelltm_rtn,swelldir_rtn, \
               wndtm_rtn,wnddir_rtn

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

        H4_rtn = np.round(float(H4), 2)
        H10_rtn = np.round(float(H10), 2)
        cge_rtn = np.round(float(out_ww3cge), 2)
        PP_rtn = np.round(float(PP), 2)
        return H4_rtn,H10_rtn, cge_rtn, PP_rtn

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


        _date0 = _date
        list_hours = []
        list_hours.append(m_hours)

        sp = self.getsp(_date0)  # 索引点位
        # fvp = self.getfvsp(_date0)
        # 创建json数据----------------------------------begin
        for k in range(0, 1):
            tmp = list_hours[k]
            list = []
            for i in range(0, max(tmp) + 1):

                fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                fc_hs, fc_hmaxe, fc_swellhs, fc_swellhmaxe, fc_wwhs, fc_wwhmaxe, fc_dir, fc_t01,fc_swelltm, fc_swellDIR, fc_wwtm, fc_wwdir= \
                    self.getDataFromSwan(_date0, i, sp)  # 综合浪、风浪、涌浪有效波高/最大波高/周期/波向

                fc_v, fc_wir = self.getWind(_date0, i)  # 风速/风向

                fc_h4, fc_h10, fc_CGE , fc_PP= self.getH4H10CGE(_date0, i, sp)  # H4/H10/CGE/PP
                if np.isnan(fc_PP):  # 谱峰周期为空时，采用2.99代替
                    fc_PP = 2.99

                fc_cspeeds, fh_cdirs = self.gettpxo(_date0, i, 0)
                fc_cspeedm, fh_cdirm = self.gettpxo(_date0, i, 9)
                fc_cspeedb, fh_cdirb = self.gettpxo(_date0, i, 19)
                # fc_cspeeds, fh_cdirs = self.getfvdata(_date0, i, fvp, 0)  # 表层流速 fvcom
                # fc_cspeedm, fh_cdirm = self.getfvdata(_date0, i, fvp, 9)  # 中层流速
                # fc_cspeedb, fh_cdirb = self.getfvdata(_date0, i, fvp, 19)  # 底层流速
                JsonData = self.getJsonData(fc_time,fc_hs, fc_hmaxe, fc_swellhs, fc_swellhmaxe, fc_wwhs, fc_wwhmaxe,
                                            fc_dir, fc_t01,fc_swelltm, fc_swellDIR, fc_wwtm, fc_wwdir,
                                            fc_v, fc_wir,fc_h4, fc_h10, fc_CGE , fc_PP,
                                            fc_cspeeds,fh_cdirs,fc_cspeedm, fh_cdirm,fc_cspeedb, fh_cdirb)  # dict()
                list.append(JsonData)
                # 创建json数据----------------------------------end
                # 创建json文件----------------------------------begin
                file_name = self._name + strDateTime.addDays(_date, k) + ".json"
                file = os.path.join(file_path, file_name)
                #new_dict = {"location": {"No": "rzlssh01", "name": "日照岚山港区原油码头", "lon": lon_g, "lat": lat_g}, "data": list}
                new_dict={"location": self._new_dict, "data": list}
                with open(file, "w") as f:
                    json.dump(new_dict, f, ensure_ascii=False, indent=10)
                # 写入文件内容----------------------------------end

    def getJsonData(self,date, fc_hs, fc_hmaxe, fc_swellhs, fc_swellhmaxe, fc_wwhs, fc_wwhmaxe,
                    fc_dir, fc_t01,fc_swelltm, fc_swellDIR, fc_wwtm, fc_wwdir,
                    fc_v, fc_wir,fc_h4, fc_h10, fc_CGE , fc_PP,
                    fc_cspeeds,fh_cdirs,fc_cspeedm, fh_cdirm,fc_cspeedb, fh_cdirb):
        postData = dict()
        postData['date'] = date
        postData['swh'] = fc_hs
        postData['mwd'] = fc_dir
        postData['mwp'] = fc_t01
        postData['hmax'] = fc_hmaxe
        postData['shww'] = fc_wwhs
        postData['mdww'] = fc_wwdir
        postData['mpww'] = fc_wwtm
        postData['hmaxw'] = fc_wwhmaxe
        postData['shts'] = fc_swellhs
        postData['mdts'] =fc_swellDIR
        postData['mpts'] = fc_swelltm
        postData['hmaxs'] = fc_swellhmaxe
        postData['windspeed'] = fc_v
        postData['winddir'] = fc_wir
        postData['currentspeeds'] = fc_cspeeds
        postData['currentdirs'] = fh_cdirs
        postData['currentspeedm'] = fc_cspeedm
        postData['currentdirm'] = fh_cdirm
        postData['currentspeedb'] = fc_cspeedb
        postData['currentdirb'] = fh_cdirb
        postData['h4'] = fc_h4
        postData['CGE'] = fc_CGE
        postData['pp1d'] = fc_PP

        return postData

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





