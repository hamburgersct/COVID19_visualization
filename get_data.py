# coding=gbk
import json
import numpy as np
import akshare as ak


date_span_1 = ['2020-02-0' + str(i) for i in range(8, 10)]
date_span_2 = ['2020-02-' + str(i) for i in range(10, 22)]
date_span = date_span_1 + date_span_2

province_names = ['������', '�����', '�ӱ�ʡ', 'ɽ��ʡ', '���ɹ�������', '����ʡ', '����ʡ',
                  '������ʡ', '�Ϻ���', '����ʡ', '�㽭ʡ', '����ʡ', '����ʡ', '����ʡ',
                  'ɽ��ʡ', '����ʡ', '����ʡ', '����ʡ', '�㶫ʡ', '����׳��������', '����ʡ',
                  '������', '�Ĵ�ʡ', '����ʡ', '����ʡ', '����������', '����ʡ', '����ʡ',
                  '�ຣʡ', '���Ļ���������', '�½�ά���������', '����ر�������', '�����ر�������', '̨��ʡ']

# # ��ȡ������ȫ����ʡ����
selected_cols = ['date','city', 'confirmed', 'suspected','cured','dead']
prov_data = []
covid_19_history_df = ak.covid_19_history()
covid_19_history_df = covid_19_history_df.loc[covid_19_history_df['country']=='�й�']

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