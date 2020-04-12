# coding=gbk
import numpy as np
import akshare as ak
from pyecharts.charts import Map, Line, Grid, WordCloud
from pyecharts import options as opts


date_span_1 = ['2020-01-0' + str(i) for i in range(1, 10)]
date_span_2 = ['2020-01-' + str(i) for i in range(10, 31)]
date_span_3 = ['2020-02-0' + str(i) for i in range(1, 10)]
date_span_4 = ['2020-02-' + str(i) for i in range(10, 30)]
date_span_5 = ['2020-03-0' + str(i) for i in range(1, 10)]
date_span = date_span_1 + date_span_2 + date_span_3 + date_span_4 + date_span_5
time_list = [item[-5:] for item in date_span]

hubei_out_data = []
migration_out_baidu_df = ak.migration_scale_baidu(area="湖北省", indicator="move_out", start_date="20190101",
                                                    end_date="20200130")
for date in date_span:
    hubei_out_data.append(float(migration_out_baidu_df.loc[date]))

hubei_in_data = []
migration_in_baidu_df = ak.migration_scale_baidu(area="湖北省", indicator="move_in", start_date="20190101",
                                                    end_date="20200130")
for date in date_span:
    hubei_in_data.append(float(migration_in_baidu_df.loc[date]))


# 获取前50个迁出城市
def get_out_cities():
    migration_area_baidu_df = ak.migration_area_baidu(area="湖北省", indicator="move_out", date="20200121")
    migration_out_city = migration_area_baidu_df.loc[:50]
    cities = np.array(migration_out_city['city_name'])
    ratio = np.array(migration_out_city['value'])
    city_data = [x for x in zip(cities, ratio)]

    return city_data


def get_line_charts():
    line_chart_1 = (
        Line(init_opts=opts.InitOpts(width='500px', height='250px'))
            .add_xaxis(time_list)
            .add_yaxis(series_name="迁出指数",
                       y_axis=hubei_out_data,
                       # symbol="emptyCircle",
                       is_symbol_show=True,
                       is_smooth=True, )
            .add_yaxis(series_name="迁入指数",
                       y_axis=hubei_in_data,
                       # symbol="emptyCircle",
                       is_symbol_show=True,
                       is_smooth=True, )
            .set_global_opts(
            title_opts=opts.TitleOpts(title='01-01至03-10湖北省迁徙指数',
                                      pos_left='72%', pos_top='15%'),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type='shadow'),
            legend_opts=opts.LegendOpts(is_show=True ,orient='horizontal', pos_left='75%', pos_top='20%'),
            yaxis_opts=opts.AxisOpts(
                name='迁徙指数',
                type_='value',
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            )
        )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False), splitline_opts=opts.SplitLineOpts(is_show=True))

    )

    wordcloud = (
        WordCloud()
        .add(series_name="城市", data_pair=get_out_cities(), word_size_range=[10, 66],
             pos_left='-8%', pos_top='10%', shape='triangle-forward')
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="1-21湖北省迁出热门城市", pos_left='20%', pos_top='15%'
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )

    grid_chart = (
        Grid(init_opts=opts.InitOpts(width='1500px', height='700px'))
            .add(
            line_chart_1,
            grid_opts=opts.GridOpts(
                pos_left='65%', pos_right='80', pos_top='30%', pos_bottom='30%'
            )
    )
            .add(wordcloud, grid_opts=opts.GridOpts(pos_left="20%", pos_top="10%"))
    )
    return grid_chart


if __name__ == '__main__':
    g = get_line_charts()
    g.render("hubei_migrate.html")
