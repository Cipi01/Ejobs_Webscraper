from forex_python.converter import CurrencyRates

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
if __name__ == '__main__':
    print(salary_convertor('1500 USD'))