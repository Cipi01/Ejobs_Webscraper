import requests
from datetime import datetime
import openpyxl
from Dicts import get_career, get_contract
from forex_python.converter import CurrencyRates

date = datetime.now().strftime("%d_%m_%Y")
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Job Data"

c = CurrencyRates()
usd_to_ron = c.get_rate('USD', 'RON')
eur_to_ron = c.get_rate('EUR', 'RON')
gbp_to_ron = c.get_rate('GBP', 'RON')

ws.append(['Titlu', 'Company', 'City', 'Creation', 'End', 'Salary', 'Job level', 'Contract'])
for page in range(1, 100):

    url = f"https://api.ejobs.ro/jobs?page={page}&sort=suitability&pageSize=100"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    try:
        if data['jobs']:
            data_raw = data['jobs']
            career = get_career()
            contract = get_contract()
            for d in data_raw:
                level = ','.join([career.get(str(id), 'N/A') for id in d['careerLevelsIds']])
                j_contract = ','.join([contract.get(str(id), 'N/A') for id in d['contractTypesIds']])

                salary = d.get('salary', 'N/A')
                if isinstance(salary, str) and ('USD' in salary or 'EUR' in salary or 'GBP' in salary):
                    salary_range = salary.split(" ")
                    std_salary_range = []
                    for s in salary_range:
                        if 'USD' in salary and s.isdigit():
                            std_salary_range.append(round(int(s) * usd_to_ron))
                        elif 'EUR' in salary and s.isdigit():
                            std_salary_range.append(round(int(s) * eur_to_ron))

                        elif 'GBP' in salary and s.isdigit():
                            std_salary_range.append(round(int(s) * gbp_to_ron))
                    salary = f"{std_salary_range[0]}-{std_salary_range[-1]} RON"

                ws.append([d['title'],
                           d['company'].get('name', 'N/A'),
                           d.get('locations', [{}])[0].get('address', 'N/A'),
                           d.get('creationDate', 'N/A'),
                           d.get('expirationDate', 'N/A'),
                           salary,
                           level,
                           j_contract])


    except KeyError:
        break

# wb.save(f'D:/P/Webscrapers/BD/EJobs_{date}.xlsx')
wb.save(f'D:/P/Webscrapers/BD/TEST.xlsx')
