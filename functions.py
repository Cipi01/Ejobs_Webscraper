from forex_python.converter import CurrencyRates
from Dicts import region_dict, departments_dict, type_dict, edu_dict, level_dict, industry_dict

def salary_convertor(salary):
    c = CurrencyRates()

    if isinstance(salary, str) and ('USD' in salary or 'EUR' in salary or 'GBP' in salary):
        salary_range = salary.split(" ")
        std_salary_range = []
        for s in salary_range:
            if 'USD' in salary and s.isdigit():
                std_salary_range.append(round(c.convert('USD', 'RON', float(s)), 2))
            elif 'EUR' in salary and s.isdigit():
                std_salary_range.append(round(c.convert('EUR', 'RON', float(s)), 2))
            elif 'GBP' in salary and s.isdigit():
                std_salary_range.append(round(c.convert('GBP', 'RON', float(s)), 2))
        salary = f"{std_salary_range[0]}-{std_salary_range[-1]} RON"

    return salary


def get_keys_from_dict(d, val):
    lst = [k for k, v in d.items() if v == val]
    return lst[0]


def process_data(item):
    item_id = item.get('id', 'n/a')
    title = item.get('title'.capitalize(), 'n/a')
    company = item.get('company').get('name'.capitalize(), 'n/a')
    locations_raw = item.get('locations', 'n/a')
    locations = [get_keys_from_dict(region_dict, str(location['cityId'])).capitalize() for location in locations_raw if locations_raw != 'n/a']
    positions = item.get('positions', 'n/a')
    c_date = item['creationDate']
    industries_raw = item.get('industriesIds', 'n/a')
    industries = [get_keys_from_dict(industry_dict, str(industryId)).capitalize() for industryId in industries_raw if industries_raw != 'n/a']
    career_raw = item.get('careerLevelsIds', 'n/a')
    career = [get_keys_from_dict(level_dict, str(careerId)).capitalize() for careerId in career_raw if career_raw != 'n/a']
    department_raw = item.get('departmentsIds', 'n/a')
    department = [get_keys_from_dict(departments_dict, str(departmentId)).capitalize() for departmentId in department_raw if department_raw != 'n/a']
    contract_raw = item.get('contractTypesIds', 'n/a')
    contract = [get_keys_from_dict(type_dict, str(contractId)).capitalize() for contractId in contract_raw if contract_raw != 'n/a']
    return [
        item_id,
        title,
        company,
        locations,
        c_date,
        industries,
        positions,
        career,
        department,
        contract

    ]


if __name__ == '__main__':
    print(salary_convertor('1500 USD'))
