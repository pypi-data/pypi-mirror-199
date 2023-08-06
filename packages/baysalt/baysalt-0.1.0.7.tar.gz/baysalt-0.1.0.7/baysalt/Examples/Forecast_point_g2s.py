#!/home/ocean/.Software/Python-env/base/bin/python
# -*- coding: utf-8 -*-
#  日期 : 2023/3/1 20:22
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import os
import sys
from christmas.read_conf import read_conf
from baysalt.Single_Forecast_with_g2s import Grid2Sca, get_parser, print_args


def print_conf(_Conf_Grid2scatter):
    print('-----------------conf default-----------------')
    for key, value in _Conf_Grid2scatter.items():
        print(f'{key} : {value}')
    print('-----------------conf default-----------------')



if __name__ == '__main__':
    args, Conf_Grid2scatter_file = get_parser()
    if not args.conf:
        if os.path.basename(__file__) in sys.argv[-1]:
            print_args(args)
        X = Grid2Sca(args.lon,
                     args.lat,
                     _input='./output/',
                     value_list=args.iv,
                     title_list=args.ov,
                     _output=args.o,
                     _name=args.n,
                     _method=args.m
                     )
        X.makefore(_date=args.d, _json=False, _txt=True)
    else:
    
        if args.conf == '1':
            args.conf = Conf_Grid2scatter_file
    
        Conf_Grid2scatter = read_conf(args.conf)
        print_conf(Conf_Grid2scatter)
    #s_lon, s_lat, _input, _output, _name, value_list, title_list, m_hours=216, time_zone=8, search_point=4, _location=None, _method=None
        X = Grid2Sca(Conf_Grid2scatter['Lon_Scatter'],
                     Conf_Grid2scatter['Lat_Scatter'],
                     _input=Conf_Grid2scatter['InputDir'],
                     _output=Conf_Grid2scatter['OutputDir'],
                     _name=Conf_Grid2scatter['NamePrefix'],
                     value_list=Conf_Grid2scatter['ValueList'],
                     title_list=Conf_Grid2scatter['TitleList'],
                     m_hours=int(Conf_Grid2scatter['DurHours']),
                     time_zone=int(Conf_Grid2scatter['TimeZone']),
                     search_point=int(Conf_Grid2scatter['SearchPoint']),
                     _location=Conf_Grid2scatter['Location'],
                     _method=Conf_Grid2scatter['Method_griddata'])
        X.makefore(_date=int(Conf_Grid2scatter['Date_Scatter']), _json=False, _txt=True)
    
