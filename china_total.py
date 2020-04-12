# coding=gbk
import json

from pyecharts.charts import Map, Grid, Timeline, Bar
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode

date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2
# print(date_span)
province_names = ['������', '�����', '�ӱ�ʡ', 'ɽ��ʡ', '���ɹ�������', '����ʡ', '����ʡ',
                  '������ʡ', '�Ϻ���', '����ʡ', '�㽭ʡ', '����ʡ', '����ʡ', '����ʡ',
                  'ɽ��ʡ', '����ʡ', '����ʡ', '����ʡ', '�㶫ʡ', '����׳��������', '����ʡ',
                  '������', '�Ĵ�ʡ', '����ʡ', '����ʡ', '����������', '����ʡ', '����ʡ',
                  '�ຣʡ', '���Ļ���������', '�½�ά���������', '����ر�������', '�����ر�������', '̨��ʡ']


time_list = [item[-5:] for item in date_span]

# print(prov_data)

maxNum = 5000
minNum = 0

# def get_map_data(date:str):
with open('epidata.json', 'r') as f:
    prov_data = json.loads(f.read())


# ��������ʡ����������
def get_processed_data(date: str):
    processed_data = []
    for d in prov_data:
        if d['time'] == date:
            for x in d['data']:
                if x['name'] in ['���ɹ�������', '������ʡ']:
                    processed_data.append([x["name"][:3], x["value"]])
                else:
                    processed_data.append([x["name"][:2], x["value"]])
    processed_data = sorted(processed_data, key=(lambda x: x[1][0]), reverse=True)
    return processed_data


def get_epidemic_date_chart(date: str):
    map_data = [
        get_processed_data(date)
    ][0]
    min_data, max_data = (minNum, maxNum)


    map_chart = (
        Map()
            .add(
            series_name='',
            data_pair=map_data,
            zoom=0,
            # center=[119.5, 34.5],
            is_map_symbol_show=False,
            itemstyle_opts={
                'normal': {'areaColor': "#323c48", "borderColor": "#404a59"},
                'emphasis': {
                    "label": {"show": Timeline},
                    "areaColor": "rgba(255,255,255, 0.5)",
                }
            }
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title='' + str(date) + 'ȫ���ֵ���ȷ������ ������Դ��AkShare',
                pos_left='center',
                pos_top='top',
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=25, color="rgba(0,0,0, 0.9)"
                )
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                formatter=JsCode(
                    """
                    function(params){
                    if ('value' in params.data){
                        return params.data.value[3] + ':' + params.data.value[0];
                    }
                    }
                    """
                )
            ),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left='30',
                pos_top='center',
                range_text=['High', 'Low'],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                min_=min_data,
                max_=max_data
            )
        )
    )

    # bar plot
    bar_x_data = [x[0] for x in map_data]
    bar_y_data = [{'name': x[0], 'value': x[1][0]} for x in map_data]
    bar = (
        Bar()
            .add_xaxis(xaxis_data=bar_x_data)
            .add_yaxis(
            series_name='',
            yaxis_data=bar_y_data,
            label_opts=opts.LabelOpts(
                is_show=True, position='right', formatter='{b} : {c}'
            )
        )
            .reversal_axis()
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(
                max_=65000,
                axislabel_opts=opts.LabelOpts(is_show=False),
            ),
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
            tooltip_opts=opts.TooltipOpts(is_show=False),
            visualmap_opts=opts.VisualMapOpts(
                is_calculable=True,
                dimension=0,
                pos_left="10",
                pos_top="top",
                range_text=["High", "Low"],
                range_color=["lightskyblue", "yellow", "orangered"],
                textstyle_opts=opts.TextStyleOpts(color="black"),
                min_=0,
                max_=5000,
            ),
        )
    )
    grid_chart = (
        Grid()
            .add(
            bar,
            grid_opts=opts.GridOpts(
                pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"
            ), )
            .add(map_chart, grid_opts=opts.GridOpts())
    )


    return grid_chart


if __name__ == '__main__':
    timeline = Timeline(
        init_opts=opts.InitOpts(width='1500px', height='700px')
    )
    for item in date_span:
        g = get_epidemic_date_chart(date=item)
        timeline.add(g, time_point=str(item))

    timeline.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=3000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    timeline.render("china_total_epidemic.html")
