# -*- coding: utf-8 -*-

# @File    : new_single.py
# @Date    : 2022-12-30
# @Author  : Dovelet
import netCDF4
import numpy as np
import os
import datetime
import baysalt.strDateTime as strDateTime
from scipy.interpolate import interp2d
from scipy.interpolate import interpn
import scipy.integrate
import json
import math

m_hours = list(range(216))


class Cangnan_Single:
    def __init__(self, _lon, _lat, _input, _output_txt, _output_json, _name, **_new_dict):
        self._lon = _lon
        self._lat = _lat
        self._input = _input
        self._output_txt = _output_txt
        self._output_json = _output_json
        self._name = _name
        self._new_dict = _new_dict
    
    def getnum(self, _date, _idx):
        """
        获取ww3_djk数据
        :param _date: 任务日期
        :param _idx: 小时
        :return: 有效波高，平均周期，谱峰周期，平均波向
        """
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H')
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
            '%Y%m%d') + '.nc'  # ww3 nc文件名

        w = netCDF4.Dataset(filename)  # 读取ww3_Wp的nc文件，传入w中
        lons = w.variables['longitude'][:]
        lats = w.variables['latitude'][:]
        ww3hs = w.variables['hs'][idx, :, :]  # 有效波高
        ww3t02 = w.variables['t02'][idx, :, :]  # 平均周期
        ww3fp = w.variables['fp'][idx, :, :]  # 谱峰频率
        ww3dir = w.variables['dir'][idx, :, :]  # 波向
        ww3swellhs = w.variables['phs1'][idx, :, :]  # 涌浪有效波高
        ww3swelltm = w.variables['ptp1'][idx, :, :]  # 涌浪谱峰周期
        ww3lm = w.variables['lm'][idx, :, :]  # 波长

        fhs = interp2d(lons, lats, ww3hs, kind='linear')
        ft02 = interp2d(lons, lats, ww3t02, kind='linear')
        ffp = interp2d(lons, lats, ww3fp, kind='linear')
        fdir = interp2d(lons, lats, ww3dir, kind='linear')
        fswellhs = interp2d(lons, lats, ww3swellhs, kind='linear')
        fswelltm = interp2d(lons, lats, ww3swelltm, kind='linear')
        flm = interp2d(lons, lats, ww3lm, kind='linear')

        hs = fhs(self._lon, self._lat)
        # H4
        t02 = ft02(self._lon, self._lat)
        # H10
        mwd = fdir(self._lon, self._lat)
        # pp
        PP = 1 / ffp(self._lon, self._lat)
        # phs1
        phs1 = fswellhs(self._lon, self._lat)
        # ptp1
        ptp1 = fswelltm(self._lon, self._lat)
        # LM
        lm = flm(self._lon, self._lat)

        if phs1[0] >= 1e+10 or ptp1[0] >= 1e+10:  # 涌浪波高或谱峰周期为空时用一维谱计算
            ef_filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
                '%Y%m%d') + '_ef.nc'  # ww3_ef nc文件名
            ww3_ef = netCDF4.Dataset(ef_filename)
            ww3ef = ww3_ef.variables['ef'][idx, :, :, :]
            f = ww3_ef.variables['f'][:]

            Z, Y, X = np.meshgrid(f, self._lat, self._lon, indexing='ij')
            ef = interpn((f, lats, lons), ww3ef, (Z, Y, X), method='linear')  # 维度和值的维度是正的

            # 涌浪要素
            # 新的涌浪计算公式
            sf1 = ef[:18, 0, 0]
            fs1 = f[:18]
            phs1[0] = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
            ptp1[0] = math.sqrt(
                scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1), fs1))  # 计算涌浪有效周期

        hs_rtn = np.round(hs[0], 2)
        t02_rtn = np.round(t02[0], 2)
        dir_rtn = np.round(mwd[0], 2)
        PP_rtn = np.round(PP[0], 2)
        phs1_rtn = np.round(phs1[0], 2)
        ptp1_rtn = np.round(ptp1[0], 2)
        lm_rtn = np.round(lm[0], 2)

        return hs_rtn, t02_rtn, dir_rtn, PP_rtn, phs1_rtn, ptp1_rtn, lm_rtn
    
    def getfore(self, _date, _idx):
        """
        获取ww3_djk数据
        :param _date: 任务日期
        :param _idx: 小时
        :return: 有效波高，平均周期，谱峰周期，平均波向
        """
        hs_rtn, t02_rtn, dir_rtn, PP_rtn, phs1_rtn, ptp1_rtn, lm_rtn = self.getnum(_date, _idx)
        return str(format(hs_rtn, '.2f')).rjust(10, " "), \
            str(format(t02_rtn, '.2f')).rjust(10, " "), \
            str(format(dir_rtn, '.2f')).rjust(10, " "), \
            str(format(PP_rtn, '.2f')).rjust(10, " "), \
            str(format(phs1_rtn, '.2f')).rjust(10, " "),\
            str(format(ptp1_rtn, '.2f')).rjust(10, " "),\
            str(format(lm_rtn, '.2f')).rjust(10, " ")
    
    @staticmethod
    def getTime(_date, _hour):
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
    
    @staticmethod
    def getJsonData(date, fc_hs, fc_dir, fc_t01, fc_PP, fc_phs1, fc_ptp1, fc_lm):
        # sourcery skip: dict-literal, inline-immediately-returned-variable, merge-dict-assign
        postData = dict()
        postData['date'] = date
        postData['swh'] = fc_hs
        postData['mwd'] = fc_dir
        postData['mwp'] = fc_t01
        postData['pp1d'] = fc_PP
        postData['shts'] = fc_phs1
        postData['mpts'] = fc_ptp1
        postData['mwl'] = fc_lm
        return postData

    def grttxt(self, _date):
        """
        构建预报单信息
        :param _date: 预报单日期
        :return: 0-生成预报数据成功  大于等于1-生成预报数据失败
        """
        isTemp = False  # 是否未来日期的扩展任务
        today = strDateTime.getToday()
        isTemp = _date <= today
        file_path = self._output_txt
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # 写入文件内容----------------------------------begin
        _date0 = _date
        list_hours = [m_hours]
        # 写入文件头----------------------------------begin
        fh_time = "time".rjust(10, " ")  # 第一列日期留空白
        fh_hs = "swh".rjust(10, " ")  # 有效波高
        fh_dir = "mwd".rjust(10, " ")  # 波向
        fh_t01 = "mwp".rjust(10, " ")  # 平均周期
        fh_lm = 'mwl'.rjust(10, " ")  # 波长
        fh_PP = "pp1d".rjust(10, " ")  # 谱峰周期
        fh_phs1 = 'shts'.rjust(10, " ")  # 涌浪有效波高
        fh_ptp1 = 'mpts'.rjust(10, " ")  # 涌浪谱峰周期

        for k in range(1):
            tmp = list_hours[k]
            file_name = self._name + strDateTime.addDays(_date, k) + ".txt"
            file = os.path.join(file_path, file_name)

            with open(file, "w") as fl:
                fl.writelines([fh_time, fh_hs, fh_dir, fh_t01, fh_lm, fh_PP, fh_phs1, fh_ptp1, "\n"])
            # 写入文件头----------------------------------end

                for i in range(max(tmp) + 1):  # +72

                    fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                    fc_hs, fc_t01, fc_dir, fc_PP, fc_phs1, fc_ptp1, fc_lm = self.getfore(_date0, i)  # 获得数据

                    if fc_PP.strip() == "--":  # 谱峰周期为空时，采用2.99代替
                        fc_PP = str(2.99).rjust(10, " ")
                    if i in m_hours:
                        fl.writelines([fc_time, fc_hs, fc_dir, fc_t01, fc_lm, fc_PP, fc_phs1, fc_ptp1, "\n"])
                        print(f"hour in={str(i)}")
                    else:
                        print(f"hour={str(i)}")

    def grtjson(self, _date):
        
        file_path = self._output_json
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        _date0 = _date
        list_hours = [m_hours]
        # 创建json数据----------------------------------begin
        for k in range(1):
            tmp = list_hours[k]
            list = []
            for i in range(max(tmp) + 1):

                fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                fc_hs, fc_t01, fc_dir, fc_PP, fc_phs1, fc_ptp1, fc_lm = self.getnum(_date0, i)  # 获取数据

                if np.isnan(fc_PP):  # 谱峰周期为空时，采用2.99代替
                    fc_PP = 2.99

                JsonData = self.getJsonData(fc_time, fc_hs, fc_dir, fc_t01, fc_lm, fc_PP, fc_phs1, fc_ptp1)  # dict()
                list.append(JsonData)
                # 创建json数据----------------------------------end
                # 创建json文件----------------------------------begin
                file_name = self._name + strDateTime.addDays(_date, k) + ".json"
                file = os.path.join(file_path, file_name)
                # new_dict = {"location": {"No": "rzlssh01", "name": "日照岚山港区原油码头", "lon": lon_g, "lat": lat_g}, "data": list}
                new_dict = {"location": self._new_dict, "data": list}
                with open(file, "w") as f:
                    json.dump(new_dict, f, ensure_ascii=False, indent=10)
                # 写入文件内容----------------------------------end
