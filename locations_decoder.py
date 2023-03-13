import requests
for page in range(1, 100):

    url = f"https://api.ejobs.ro/jobs?page={page}&sort=suitability&pageSize=100"


    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = response.json()
    try:
        if data['jobs']:
            data_raw = data['jobs']
            for x in data_raw:
                loc = x['locations']
                for i in loc:
                    print(i)

    except KeyError:
        break