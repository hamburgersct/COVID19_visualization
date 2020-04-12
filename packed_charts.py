# coding=gbk
import json
from operator import itemgetter

import numpy as np
import akshare as ak
from pyecharts.charts import Map, Line, Grid, Timeline, Bar, Pie
from pyecharts import options as opts

date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2
time_list = [item[-5:] for item in date_span]

# 截取所选的两周全国数据
df_covid_total = ak.covid_19_163(indicator="中国历史时点数据")
df_covid_total = df_covid_total.loc[date_span, :]
# 处理为pyecharts接受的格式
confirmed = [int(x) for x in np.array(df_covid_total['confirm'])]
suspected = [int(x) for x in np.array(df_covid_total['suspect'])]
healed = [int(x) for x in np.array(df_covid_total['heal'])]
death = [int(x) for x in np.array(df_covid_total['dead'])]

# get每日的分省份详细信息
with open('epidata.json', 'r') as f:
    prov_data = json.loads(f.read())


def get_processed_data(date: str):
    processed_data = []
    for d in prov_data:
        if d['time'] == date:
            for x in d['data']:
                if x['name'] in ['内蒙古自治区', '黑龙江省']:
                    processed_data.append([x["name"][:3], x["value"]])
                else:
                    processed_data.append([x["name"][:2], x["value"]])
    processed_data = sorted(processed_data, key=(lambda x: x[1][0]), reverse=True)

    return processed_data


def get_packed_charts(date: str):
    map_data = [get_processed_data(date)][0]
    data_mark = []
    i = 0
    for x in time_list:
        if x == date[-5:]:
            data_mark.append(confirmed[i])
        else:
            data_mark.append('')
        i += 1

    line_chart = (
        Line()
            .add_xaxis(time_list)
            .add_yaxis('新增确诊', confirmed, color='#ff6361')
            .add_yaxis('新增疑似', suspected, color='#ffa600')
            .add_yaxis('新增治愈', healed, color='#bc5090')
            .add_yaxis('新增死亡', death, color='#003f5c')
            .add_yaxis('', data_mark,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),
                       tooltip_opts=opts.TooltipOpts(is_show=False),
                       color='#ff6361')
            .set_global_opts(
            title_opts=opts.TitleOpts(title='2-8至2-22之间国内疫情变化趋势',
                                      pos_left='72%', pos_top='15%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='shadow'),
            legend_opts=opts.LegendOpts(orient='horizontal', pos_left='70%', pos_top='20%'),
            yaxis_opts=opts.AxisOpts(
                name='人数',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), splitline_opts=opts.SplitLineOpts(is_show=True))

    )
    pie_data_1 = [[x[0], x[1][0]] for x in map_data]
    pie_1 = (
        Pie()
            .add(
            series_name='',
            data_pair=pie_data_1,
            radius=["15%", "35%"],
            center=["15%", "50%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=date[5:] + '确诊人数', pos_top='20%', pos_left='0%')
        )
    )

    pie_data_2 = [[x[0], x[1][1]] for x in map_data]
    pie_2 = (
        Pie()
            .add(
            series_name='',
            data_pair=pie_data_2,
            radius=["15%", "35%"],
            center=["45%", "50%"],
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=1, border_color="rgba(0,0,0,0.3)"
            ),
        )
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title=date[5:] + '治愈人数', pos_top='20%', pos_left='30%')
        )
    )

    grid_chart = (
        Grid()
            .add(
            line_chart,
            grid_opts=opts.GridOpts(
                pos_left='65%', pos_right='80', pos_top='30%', pos_bottom='30%'
            )
        )
            .add(pie_1, grid_opts=opts.GridOpts(pos_left="20%", pos_top="10%"))
            .add(pie_2, grid_opts=opts.GridOpts(pos_left="20%", pos_top="10%"))
    )
    return grid_chart


if __name__ == '__main__':
    timeline = Timeline(
        init_opts=opts.InitOpts(width='1500px', height='700px')
    )
    for item in date_span:
        g = get_packed_charts(date=item)
        timeline.add(g, time_point=str(item))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=2000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    timeline.render("china_packed_epidemic.html")
