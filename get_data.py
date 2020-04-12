# coding=gbk
import json
import numpy as np
import akshare as ak


date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2

province_names = ['北京市', '天津市', '河北省', '山西省', '内蒙古自治区', '辽宁省', '吉林省',
                  '黑龙江省', '上海市', '江苏省', '浙江省', '安徽省', '福建省', '江西省',
                  '山东省', '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省',
                  '重庆市', '四川省', '贵州省', '云南省', '西藏自治区', '陕西省', '甘肃省',
                  '青海省', '宁夏回族自治区', '新疆维吾尔自治区', '香港特别行政区', '澳门特别行政区', '台湾省']

# # 截取两周内全国各省数据
selected_cols = ['date','city', 'confirmed', 'suspected','cured','dead']
prov_data = []
covid_19_history_df = ak.covid_19_history()
covid_19_history_df = covid_19_history_df.loc[covid_19_history_df['country']=='中国']

for date in date_span:
    data = []
    for province in province_names:
        df_epidemic = covid_19_history_df.loc[covid_19_history_df['province']==province]
        df_dt_epidemic = df_epidemic.loc[df_epidemic['date']==date]
        confirm = int(np.array(df_dt_epidemic['confirmed'])[0])
        cure = int(np.array(df_dt_epidemic['cured'])[0])
        dead = int(np.array(df_dt_epidemic['dead'])[0])
        prov_dict = {'name':province, 'value':[confirm, cure, dead, province]}
        data.append(prov_dict)
    date_dict = {'time':date, 'data':data}
    prov_data.append(date_dict)

json_str = json.dumps(prov_data, indent=4)
with open('test.json','w') as json_file:
    json_file.write(json_str)

time_list = [item[-5:] for item in date_span]

# print(prov_data)

maxNum = 5000
minNum = 0

# def get_map_data(date:str):
with open('epidata.json', 'r') as f:
    prov_data = json.loads(f.read())