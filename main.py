import requests

for page in range(1, 100):
    url = f"https://api.ejobs.ro/jobs?page={page}&pageSize=100&filters.departments=57&sort=suitability"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    try:
        if data['jobs']:
            print(data)  # TODO: extract columns to csv, trim columns then export to xlsx
    except KeyError:
        break
