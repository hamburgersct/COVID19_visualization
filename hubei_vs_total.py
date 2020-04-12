# coding=gbk
import json

import pandas as pd
import numpy as np
import akshare as ak
from pyecharts.charts import Map, Line, Grid, Timeline, Bar, Tab
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2

time_list = [item[-5:] for item in date_span]

# print(prov_data)

maxNum = 5000
minNum = 0

# def get_map_data(date:str):
with open('epidata.json', 'r') as f:
    prov_data = json.loads(f.read())


def get_hubei_data():
    hubei_data = []
    for d in prov_data:
        for x in d['data']:
            if x['name'] == '湖北省':
                hubei_data.append(x["value"][:-1])
    return hubei_data


def get_chongqin_data():
    chong_data = []
    for d in prov_data:
        for x in d['data']:
            if x['name'] == '重庆市':
                chong_data.append(x["value"][:-1])
    return chong_data


def get_total_data():
    total_data = []
    for d in prov_data:
        confirm, cure, dead = 0, 0, 0
        for x in d['data']:
            confirm += x['value'][0]
            cure += x['value'][1]
            dead += x['value'][2]
        total_data.append([confirm, cure, dead])
    return total_data


# print(np.array(get_total_data())[:,0])

def get_line_charts():
    hb_confirmed = [int(x) for x in np.array(get_hubei_data())[:, 0]]
    cq_confirmed = [int(x) for x in np.array(get_chongqin_data())[:, 0]]
    tot_confirmed = [int(x) for x in np.array(get_total_data())[:, 0]]
    hb_cured = [int(x) for x in np.array(get_hubei_data())[:, 1]]
    cq_cured = [int(x) for x in np.array(get_chongqin_data())[:, 1]]
    tot_cured = [int(x) for x in np.array(get_total_data())[:, 1]]
    hb_dead = [int(x) for x in np.array(get_hubei_data())[:, 2]]
    cq_dead = [int(x) for x in np.array(get_chongqin_data())[:, 2]]
    tot_dead = [int(x) for x in np.array(get_total_data())[:, 2]]
    line_chart_1 = (
        Line(init_opts=opts.InitOpts())

            .add_xaxis(time_list)
            .add_yaxis('湖北',hb_confirmed, color='#ff6361')
            .add_yaxis('重庆', cq_confirmed, color='#ffa600')
            .add_yaxis('全国', tot_confirmed, color='#bc5090')

            .set_global_opts(
            title_opts=opts.TitleOpts(title='2-8至2-22之间累计确诊病例变化趋势',
                                      pos_left='20%', pos_top='5%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='shadow'),
            legend_opts=opts.LegendOpts(orient='horizontal', pos_left='60%', pos_top='5%'),
            yaxis_opts=opts.AxisOpts(
                name='人数',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), splitline_opts=opts.SplitLineOpts(is_show=True))

    )

    line_chart_2 = (
        Line()

            .add_xaxis(time_list)
            .add_yaxis('湖北', hb_cured, color='#ff6361')
            .add_yaxis('重庆', cq_cured, color='#ffa600')
            .add_yaxis('全国', tot_cured, color='#bc5090')

            .set_global_opts(
            title_opts=opts.TitleOpts(title='2-8至2-22之间累计治愈病例变化趋势',
                                      pos_left='20%', pos_top='5%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='shadow'),
            legend_opts=opts.LegendOpts(orient='horizontal', pos_left='60%', pos_top='5%'),
            yaxis_opts=opts.AxisOpts(
                name='人数',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), splitline_opts=opts.SplitLineOpts(is_show=True))

    )

    line_chart_3 = (
        Line()

            .add_xaxis(time_list)
            .add_yaxis('湖北', hb_dead, color='#ff6361')
            .add_yaxis('重庆', cq_dead, color='#ffa600')
            .add_yaxis('全国', tot_dead, color='#bc5090')

            .set_global_opts(
            title_opts=opts.TitleOpts(title='2-8至2-22之间累计死亡病例变化趋势',
                                      pos_left='20%', pos_top='5%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='shadow'),
            legend_opts=opts.LegendOpts(orient='horizontal', pos_left='60%', pos_top='5%'),
            yaxis_opts=opts.AxisOpts(
                name='人数',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), splitline_opts=opts.SplitLineOpts(is_show=True))

    )
    tab = Tab(page_title='湖北、重庆、全国病例变化趋势')
    tab.add(line_chart_1, '累计确诊人数')
    tab.add(line_chart_2, '累计治愈人数')
    tab.add(line_chart_3, '累计死亡人数')
    return tab


if __name__ == '__main__':
    g = get_line_charts()
    g.render("hubei_vs_total.html")
