import random
import time
import requests
import pandas as pd
from functions import get_keys_from_dict, process_data
from Dicts import region_dict, departments_dict, type_dict, edu_dict, level_dict, industry_dict
# Initial request
data_list = []

user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'
]
for i in range(1, 5):
    user_agent = random.choice(user_agent_list)


def init_req():
    print("Begin init request")
    for page in range(1, 12):
        url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100"

        payload = {}
        headers = {"User-Agent": user_agent}
        response = requests.request("GET", url, headers=headers, data=payload)
        try:
            data = response.json()
            time.sleep(1)
            if data['totalCount'] > 999:
                print(f"---TOO MUCH---")
                break
            for i in data['jobs']:
                data_list.append(process_data(i))

        except KeyError:
            break


# Direct department request
def department_req():
    print("Begin departments req")
    department_list_plus = []
    department_list = departments_dict.values()
    for val_department in department_list:
        for page in range(1, 12):
            url = f"https://api.ejobs.ro/jobs?pageSize=100&sort=suitability&page={page}&" \
                  f"filters.departments={val_department}"

            payload = {}
            headers = {"User-Agent": user_agent}
            response = requests.request("GET", url, headers=headers, data=payload)
            try:
                data = response.json()
                time.sleep(1)

                if 'jobs' in data:
                    for i in data['jobs']:

                        data_list.append(process_data(i))
                elif 'error' in data and page == 11:
                    print(f"---TOO MANY---{get_keys_from_dict(departments_dict, val_department)}")
                    department_list_plus.append(val_department)
                    break
                elif 'error' in data:
                    print(f"---OK---{get_keys_from_dict(departments_dict, val_department)}")
                    break
            except KeyError:
                break
    return department_list_plus, data_list


# Regional request
def region_req(data_list):
    print("Begin region request")

    region_id_list = list(region_dict.values())
    region_list_plus = []

    for val_region in region_id_list:
        for page in range(1, 12):

            url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.cities={val_region}"

            payload = {}
            headers = {"User-Agent": user_agent}
            response = requests.request("GET", url, headers=headers, data=payload)
            try:
                data = response.json()
                time.sleep(1)

                if 'jobs' in data:
                    for i in data['jobs']:
                        data_list.append(process_data(i))

                elif 'error' in data and page == 11:
                    print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}")
                    region_list_plus.append(val_region)
                    break
                elif 'error' in data:
                    print(f"---OK---{get_keys_from_dict(region_dict, val_region)}")
                    break
            except KeyError:
                break
    return region_list_plus, data_list


def region_department_req(region_list_updated, department_list_updated, data_list):
    print("Begin reg-dep req")
    region_dep_list_plus = []
    dep_region_list_plus = []
    for val_region in region_list_updated:
        for val_department in department_list_updated:
            for page in range(1, 12):
                url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.cities={val_region}&" \
                      f"filters.departments={val_department}&sort=suitability"

                payload = {}
                headers = {"User-Agent": user_agent}
                response = requests.request("GET", url, headers=headers, data=payload)
                try:
                    data = response.json()
                    time.sleep(1)

                    if 'jobs' in data:
                        for i in data['jobs']:

                            data_list.append(process_data(i))
                    elif 'error' in data and page == 11:
                        print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}---"
                              f"{get_keys_from_dict(departments_dict, val_department)}")
                        if val_region not in region_dep_list_plus:
                            region_dep_list_plus.append(val_region)
                        if val_department not in dep_region_list_plus:
                            dep_region_list_plus.append(val_department)
                        break
                    elif 'error' in data:
                        print(f"---OK---{get_keys_from_dict(region_dict, val_region)}---"
                              f"{get_keys_from_dict(departments_dict, val_department)}")

                        break
                except KeyError:
                    break
    return region_dep_list_plus, dep_region_list_plus, data_list


def reg_dep_type_req(region_list_updated, department_list_updated, data_list):
    print("Begin reg-dep-type req")
    region_dep_type_list_plus = []
    dep_region_type_list_plus = []
    type_region_dep_list_plus = []
    type_list = list(type_dict.values())
    for val_region in region_list_updated:
        for val_department in department_list_updated:
            for val_type in type_list:
                for page in range(1, 12):

                    url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&" \
                          f"filters.cities={val_region}&filters.departments={val_department}&" \
                          f"filters.contractTypes={val_type}&sort=suitability"

                    payload = {}
                    headers = {"User-Agent": user_agent}
                    response = requests.request("GET", url, headers=headers, data=payload)
                    data = response.json()
                    time.sleep(1)

                    try:
                        if 'jobs' in data:
                            for i in data['jobs']:

                                data_list.append(process_data(i))
                        elif 'error' in data and page == 11:
                            print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}---"
                                  f"{get_keys_from_dict(departments_dict, val_department)}---"
                                  f"{get_keys_from_dict(type_dict, val_type)}")
                            if val_region not in region_dep_type_list_plus:
                                region_dep_type_list_plus.append(val_region)
                            if val_department not in dep_region_type_list_plus:
                                dep_region_type_list_plus.append(val_department)
                            if val_type not in type_region_dep_list_plus:
                                type_region_dep_list_plus.append(val_type)
                            break
                        elif 'error' in data:
                            print(f"---OK---{get_keys_from_dict(region_dict, val_region)}---"
                                  f"{get_keys_from_dict(departments_dict, val_department)}---"
                                  f"{get_keys_from_dict(type_dict, val_type)}")
                            break
                    except KeyError:
                        break
    return region_dep_type_list_plus, dep_region_type_list_plus, type_region_dep_list_plus, data_list


def reg_dep_tp_edu_req(region_list_updated, department_list_updated, type_list_updated, data_list):
    print("Begin reg-dep-tp-edu req")
    rg_plus_list = []
    dp_plus_list = []
    tp_plus_list = []
    ed_plus_list = []
    edu_list = list(edu_dict.values())
    for val_region in region_list_updated:
        for val_department in department_list_updated:
            for val_type in type_list_updated:
                for val_edu in edu_list:

                    for page in range(1, 12):

                        url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.cities={val_region}" \
                              f"&filters.departments={val_department}&filters.contractTypes={val_type}&" \
                              f"filters.educationLevels={val_edu}&sort=suitability"

                        payload = {}
                        headers = {"User-Agent": user_agent}
                        response = requests.request("GET", url, headers=headers, data=payload)
                        data = response.json()
                        time.sleep(1)

                        try:
                            if 'jobs' in data:
                                for i in data['jobs']:
                                    data_list.append(process_data(i))

                            elif 'error' in data and page == 11:
                                print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}---"
                                      f"{get_keys_from_dict(departments_dict, val_department)}---"
                                      f"{get_keys_from_dict(type_dict, val_type)}---"
                                      f"{get_keys_from_dict(edu_dict, val_edu)}")
                                if val_region not in rg_plus_list:
                                    rg_plus_list.append(val_region)
                                if val_department not in dp_plus_list:
                                    dp_plus_list.append(val_department)
                                if val_type not in tp_plus_list:
                                    tp_plus_list.append(val_type)
                                if val_edu not in ed_plus_list:
                                    ed_plus_list.append(val_edu)
                                break
                            elif 'error' in data:
                                print(f"---OK---{get_keys_from_dict(region_dict, val_region)}---"
                                      f"{get_keys_from_dict(departments_dict, val_department)}---"
                                      f"{get_keys_from_dict(type_dict, val_type)}---"
                                      f"{get_keys_from_dict(edu_dict, val_edu)}")
                                break
                        except KeyError:
                            break
    return rg_plus_list, dp_plus_list, tp_plus_list, ed_plus_list, data_list


def reg_dep_tp_edu_level_req(region_list_updated, department_list_updated, type_list_updated, educ_list_updated,
                             data_list):
    print("Begin reg-dep-tp-edu-level req")
    rg_plus_list = []
    dep_plus_list = []
    type_plus_list = []
    edu_plus_list = []
    level_plus_list = []
    level_list = list(level_dict.values())
    for val_region in region_list_updated:
        for val_department in department_list_updated:
            for val_type in type_list_updated:
                for val_edu in educ_list_updated:
                    for val_level in level_list:
                        for page in range(1, 12):

                            url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.cities={val_region}" \
                                  f"&filters.departments={val_department}&filters.contractTypes={val_type}&" \
                                  f"filters.educationLevels={val_edu}&filters.careerLevels={val_level}&sort=suitability"

                            payload = {}
                            headers = {"User-Agent": user_agent}
                            response = requests.request("GET", url, headers=headers, data=payload)
                            data = response.json()
                            time.sleep(1)

                            try:
                                if 'jobs' in data:
                                    for i in data['jobs']:
                                        data_list.append(process_data(i))

                                elif 'error' in data and page == 11:
                                    print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}---"
                                          f"{get_keys_from_dict(departments_dict, val_department)}---"
                                          f"{get_keys_from_dict(type_dict, val_type)}---"
                                          f"{get_keys_from_dict(edu_dict, val_edu)}---"
                                          f"{get_keys_from_dict(level_dict, val_level)}")
                                    if val_region not in rg_plus_list:
                                        rg_plus_list.append(val_region)
                                    if val_department not in dep_plus_list:
                                        dep_plus_list.append(val_department)
                                    if val_type not in type_plus_list:
                                        type_plus_list.append(val_type)
                                    if val_edu not in edu_plus_list:
                                        edu_plus_list.append(val_edu)
                                    if val_level not in level_plus_list:
                                        level_plus_list.append(val_level)
                                    break
                                elif 'error' in data:
                                    print(f"---OK---{get_keys_from_dict(region_dict, val_region)}---"
                                          f"{get_keys_from_dict(departments_dict, val_department)}---"
                                          f"{get_keys_from_dict(type_dict, val_type)}---"
                                          f"{get_keys_from_dict(edu_dict, val_edu)}---"
                                          f"{get_keys_from_dict(level_dict, val_level)}")

                                    break
                            except KeyError:
                                break
    return rg_plus_list, dep_plus_list, type_plus_list, edu_plus_list, level_plus_list, data_list


def reg_dep_tp_edu_level_industry_req(region_list_updated, department_list_updated, type_list_updated,
                                      educ_list_updated, level_list_updated, data_list):
    print("Begin reg-dep-tp-edu-level-industry req")
    rg_plus_list = []
    dep_plus_list = []
    type_plus_list = []
    edu_plus_list = []
    level_plus_list = []
    industry_plus_list = []
    industry_list = list(industry_dict.values())
    for val_region in region_list_updated:
        for val_department in department_list_updated:
            for val_type in type_list_updated:
                for val_edu in educ_list_updated:
                    for val_level in level_list_updated:
                        for val_industry in industry_list:
                            for page in range(1, 12):

                                url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.cities={val_region}" \
                                      f"&filters.departments={val_department}&filters.contractTypes={val_type}&" \
                                      f"filters.educationLevels={val_edu}&filters.careerLevels={val_level}" \
                                      f"&filters.industries={val_industry}&sort=suitability"

                                payload = {}
                                headers = {"User-Agent": user_agent}
                                response = requests.request("GET", url, headers=headers, data=payload)
                                data = response.json()
                                time.sleep(1)

                                try:
                                    if 'jobs' in data:
                                        for i in data['jobs']:

                                            data_list.append(process_data(i))
                                    elif 'error' in data and page == 11:
                                        print(f"---TOO MANY---{get_keys_from_dict(region_dict, val_region)}---"
                                              f"{get_keys_from_dict(departments_dict, val_department)}---"
                                              f"{get_keys_from_dict(type_dict, val_type)}---"
                                              f"{get_keys_from_dict(edu_dict, val_edu)}---"
                                              f"{get_keys_from_dict(level_dict, val_level)}---"
                                              f"{get_keys_from_dict(industry_dict, val_industry)}")
                                        rg_plus_list.append(val_region)
                                        dep_plus_list.append(val_department)
                                        type_plus_list.append(val_type)
                                        edu_plus_list.append(val_edu)
                                        level_plus_list.append(val_level)
                                        industry_plus_list.append(val_industry)
                                        break
                                    elif 'error' in data:
                                        print(f"---OK---{get_keys_from_dict(region_dict, val_region)}---"
                                              f"{get_keys_from_dict(departments_dict, val_department)}---"
                                              f"{get_keys_from_dict(type_dict, val_type)}---"
                                              f"{get_keys_from_dict(edu_dict, val_edu)}---"
                                              f"{get_keys_from_dict(level_dict, val_level)}---"
                                              f"{get_keys_from_dict(industry_dict, val_industry)}")

                                        break
                                except KeyError:
                                    break
    return rg_plus_list, dep_plus_list, type_plus_list, edu_plus_list, level_plus_list, industry_plus_list, data_list


if __name__ == '__main__':
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

