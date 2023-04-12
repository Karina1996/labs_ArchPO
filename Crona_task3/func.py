import requests
import json
from datetime import datetime, timedelta
import pyodbc
import schedule


URL = "https://www.cnb.cz/en/financial_markets/foreign_exchange_market/exchange_rate_fixing/daily.txt?"

cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=LAPTOP-L1R8HGF9;"
                      "Database=Crona_task1;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
data_db = cursor.execute('''select * from daily''').fetchall()

def GetParams(key_):
    with open('config.json', 'r', encoding='utf-8') as f: 
        return json.load(f)[0][key_]

def day_add(x):
    dt = datetime.strptime(x, '%d.%m.%Y') 
    result = dt + timedelta(days = 1)
    x = result
    return x # вычисленная дата

def add_toDB(api, sd_obj):
    response = requests.get(api).text.split('\n')
    del response[0] 
    response.remove('Country|Currency|Amount|Code|Rate') # обрезаю лишнее 
    # добавляю сразу в БД
    for row in response:
        item = row.split('|')
        print(item)
        if '' not in item: 
            sql_query = f'''insert into daily values(
                '{datetime.strftime(sd_obj, "%Y-%m-%d")}', '{item[0]}', '{item[1]}', {int(item[2])}, '{item[3]}', {float(item[4])})'''
            cursor.execute(sql_query)
            cursor.commit()
            
            if api == URL:
                sql_query = f''' delete from daily where date_ = '{datetime.strftime(sd_obj, "%Y-%m-%d")}' ''' # удаление данных за тек дату
                cursor.execute(sql_query)
                cursor.commit()

def SyncRates(start_date, end_date): # допом можно отбирать список избранных валют
    print('-'*100)
    print(f'({datetime.now()})\n1. Возможность заполнить БД данными валютных курсов за определенный период (колонка Rate в отчётах CNB:\n')
    d1 = datetime.strptime(start_date, "%d.%m.%Y")
    d2 = datetime.strptime(end_date, "%d.%m.%Y")
    diff_day = (d2 - d1).days # разница в днях между датами 
    if data_db != []: 
        cursor.execute('''delete from daily''')
        cursor.commit()
    i = 1
    while i <= int(diff_day)+1:
        sd_obj = datetime.strptime(start_date, '%d.%m.%Y')  # в объект для записи корректного формата в БД
        add_toDB(URL + f"date={start_date}", sd_obj) 
        x = day_add(start_date) # + денёк
        start_date = x.strftime('%d.%m.%Y')
        i+=1

def addCurrentDay():
    print('-'*100)
    print(f'({datetime.now()})\n2. Возможность запуска задачи по расписанию, которая будет обновлять текущий курс в БД):\n')
    add_toDB(URL, datetime.now().date()) # в стороннем АПИ по умолчанию вовзращаются данные за тек. дату
    return datetime.now().date()

def SyncCurrentDay(x):
    print(x)
    schedule.every(x).minutes.do(addCurrentDay) # запуск задачи
    while True: schedule.run_pending()

# получение отчета на сервере
def GetRates(ls_rates): 
    # при желании можно выбрать за период, а не только избранные валюты
    # sd = datetime.strptime(start_date, '%d.%m.%Y')  
    # ed = datetime.strptime(end_date, '%d.%m.%Y')
    print(str(ls_rates)[1:-1])
    # print(', '.join(ls_rates))
    get_dataDB = f''' select currency, min(rate) Мин, max(rate) Макс, avg(rate) Среднее
        from daily where Amount = 1 
        group by currency having currency in({str(ls_rates)[1:-1]}) 
        '''
    return cursor.execute(get_dataDB).fetchall()
   
