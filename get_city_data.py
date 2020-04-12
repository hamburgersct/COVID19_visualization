# coding=gbk
import json
import akshare as ak
import numpy as np

date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2

city_names = ['�人��', '��ʯ��', 'ʮ����', '�˲���', '������', '������', '������',
                  'Т����', '������', '�Ƹ���', '������', '������', '��ʩ����������������',
                  '������', 'Ǳ����', '������', '��ũ������']

# # ��ȡ�����ں���ʡ��������
selected_cols = ['date','city', 'confirmed', 'suspected','cured','dead']
hubei_data = []
covid_19_province_df = ak.covid_19_hist_province(province="����ʡ")

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
