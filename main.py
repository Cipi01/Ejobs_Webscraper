import pandas as pd
from request import init_req, region_req, department_req, region_department_req, reg_dep_type_req, \
    reg_dep_tp_edu_level_industry_req, reg_dep_tp_edu_req, reg_dep_tp_edu_level_req
import random as rd

data_list = []

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
]
for i in range(1, 5):
    user_agent = rd.choice(user_agent_list)

init_req()
department_list_plus1, data_list = department_req()
region_list_plus2, data_list = region_req(data_list)
region_list_plus3, department_list_plus3, data_list = \
    region_department_req(region_list_plus2, department_list_plus1, data_list)
region_list_plus4, department_list_plus4, type_list_plus4, data_list = \
    reg_dep_type_req(region_list_plus3, department_list_plus3, data_list)
region_list_plus5, department_list_plus5, type_list_plus5, educ_list_plus5, data_list = \
    reg_dep_tp_edu_req(region_list_plus4, department_list_plus4, type_list_plus4, data_list)
region_list_plus6, department_list_plus6, type_list_plus6, educ_list_plus6, level_list_plus6, data_list = \
    reg_dep_tp_edu_level_req(region_list_plus5, department_list_plus5, type_list_plus5, educ_list_plus5, data_list)
region_list_plus7, department_list_plus7, type_list_plus7, educ_list_plus7, level_list_plus7, industry_list_plus7, data_list = \
    reg_dep_tp_edu_level_industry_req(region_list_plus6, department_list_plus6, type_list_plus6, educ_list_plus6,
                                      level_list_plus6, data_list)

columns = ['ID', 'Titlu']
df = pd.DataFrame(data_list, columns=columns)
df = df.drop_duplicates()
df.to_csv('test.csv', index=False)

#TODO: Fix all functions with solution for edu req