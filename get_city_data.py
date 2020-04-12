# coding=gbk
import json
import akshare as ak
import numpy as np

date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2

city_names = ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市',
                  '孝感市', '荆州市', '黄冈市', '咸宁市', '随州市', '恩施土家族苗族自治州',
                  '仙桃市', '潜江市', '天门市', '神农架林区']

# # 截取两周内湖北省各市数据
selected_cols = ['date','city', 'confirmed', 'suspected','cured','dead']
hubei_data = []
covid_19_province_df = ak.covid_19_hist_province(province="湖北省")

for date in date_span:
    data = []
    for city in city_names:
        df_epidemic = covid_19_province_df.loc[covid_19_province_df['city']==city]
        df_dt_epidemic = df_epidemic.loc[df_epidemic['date']==date]
        confirm = int(df_dt_epidemic['confirmed'])
        cure = int(df_dt_epidemic['cured'])
        dead = int(df_dt_epidemic['dead'])
        hubei_dict = {'name':city, 'value':[confirm, cure, dead, city]}
        data.append(hubei_dict)
    date_dict = {'time':date, 'data':data}
    hubei_data.append(date_dict)

print(hubei_data)

json_str = json.dumps(hubei_data, indent=4)
with open('hubei_city_data.json','w') as json_file:
    json_file.write(json_str)
