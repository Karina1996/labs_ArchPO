from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
import pyodbc
import json

#  uvicorn main:app --reload 

cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=LAPTOP-L1R8HGF9;"
                      "Database=aero_myfastAPI;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()

ls_type_comp = cursor.execute('''select type_, ID id from Type_aviacompany''').fetchall()
ls_comp = cursor.execute('''select name, ID_comp id, id_type from Aviacompany''').fetchall()
ls_passeng = cursor.execute('''select name_, ID_psg id from Passenger''').fetchall()
ls_trip = cursor.execute('''select trip_no id, plane, town_from, town_to, time_out, time_in, ID_comp from Trip''').fetchall()
ls_PassTrip = cursor.execute('''select * from Pass_in_trip''').fetchall()

def all_elements(ls_data):
    data = []
    for row in ls_data:
        data.append(dict(zip([t[0] for t in row.cursor_description], row)))
    return data

def find_element(id, db):
    print('id = ' + str(id))
    print(db)
    for row in db:
        if str(row[1]) == str(id):
            return dict(zip([t[0] for t in row.cursor_description], row))
    return None
 
def check_is_None(x): # если данные не найдены, отправляем статусный код и сообщение об ошибке
    if x is None: 
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, 
            content={ "message": "Данные не найдены" }
        )

app = FastAPI()

#----------------------------------------------------------
@app.get("/TYPEaviacomp") 
async def main():
    return FileResponse("public/index_1.html")

@app.get("/api/TYPEaviacomp") # список типов авиакомпаний
def get_TYPEaviacomp():
    return all_elements(ls_type_comp)

@app.get("/api/TYPEaviacomp/{id}")
def get_TYPEaviacomp(id):
    x = find_element(id, ls_type_comp) 
    check_is_None(x)
    return x
 
@app.post("/api/TYPEaviacomp")
def create_TYPEaviacomp(data = Body()):
    cursor.execute(f'''insert into Type_aviacompany values('{data["type_"]}')''') 
    cursor.commit()
    return data
 
@app.put("/api/TYPEaviacomp")
def edit_TYPEaviacomp(data = Body()):
    cursor.execute(f'''update Type_aviacompany set type_ = '{data["type_"]}' where ID = {data["id"]}''')
    cursor.commit()
    return data
 
@app.delete("/api/TYPEaviacomp/{id}") 
def delete_aviacomp(id):
    x = find_element(id, ls_type_comp)
    cursor.execute(f'''delete from Type_aviacompany where ID = {id}''')
    cursor.commit()
    check_is_None(x)
    return x
# #----------------------------------------------------------

@app.get("/aviacomp") # root
async def main():
    return FileResponse("public/index.html")

@app.get("/api/aviacomp") # список авиакомпаний
def get_aviacomp():
    return all_elements(ls_comp)
 
@app.get("/api/aviacomp/{id}")
def get_aviacomp(id):
    x = find_element(id, ls_comp) # получаем по id
    check_is_None(x)  # если найдена, отправляем 
    return x
 
@app.post("/api/aviacomp")
def create_aviacomp(data = Body()):
    cursor.execute(f'''insert into Aviacompany values('{data["name"]}', {data["id_type"]})''') 
    cursor.commit()
    return data
 
@app.put("/api/aviacomp")
def edit_aviacomp(data = Body()):
    # если найден, изменяем данные и отправляем обратно клиенту
    cursor.execute(f'''update Aviacompany set name = '{data["name"]}', id_type = {data["id_type"]} where ID_comp = {data["id"]}''')
    cursor.commit()
    return data
 
@app.delete("/api/aviacomp/{id}") # ВАЖНО: ON DELETE CASCADE - не реализован! (не удаляет дочерние строки при удалении родительского ключа)
def delete_aviacomp(id):
    comp = find_element(id, ls_comp)
    check_is_None(comp)
    cursor.execute(f'''delete from Aviacompany where ID_comp = {id}''')
    cursor.commit()
    return comp

# #----------------------------------------------------------
@app.get("/passenger") 
async def main():
    return FileResponse("public/index_2.html")

@app.get("/api/passenger") # список типов авиакомпаний
def get_TYPEaviacomp():
    return all_elements(ls_passeng)

@app.get("/api/passenger/{id}")
def get_TYPEaviacomp(id):
    x = find_element(id, ls_passeng) 
    check_is_None(x) 
    return x
 
@app.post("/api/passenger")
def create_TYPEaviacomp(data = Body()):
    cursor.execute(f'''insert into Passenger values('{data["name_"]}')''') 
    cursor.commit()
    return data
 
@app.put("/api/passenger")
def edit_TYPEaviacomp(data = Body()):
    cursor.execute(f'''update Passenger set name_ = '{data["name_"]}' where ID_psg = {data["id"]}''')
    cursor.commit()
    return data
 
@app.delete("/api/passenger/{id}") 
def delete_TYPEaviacomp(id):
    x = find_element(id, ls_passeng)
    cursor.execute(f'''delete from Passenger where ID_psg = {id}''')
    cursor.commit()
    check_is_None(x)
    return x
# #----------------------------------------------------------

@app.get("/trip") 
async def main():
    return FileResponse("public/index_3.html")

@app.get("/api/trip") # список типов авиакомпаний
def get_TYPEaviacomp():
    return all_elements(ls_trip)

@app.get("/api/trip/{id}")
def get_TYPEaviacomp(id):
    x = find_element(id, ls_trip) 
    check_is_None(x)
    return x
   
 
@app.post("/api/trip")
def create_TYPEaviacomp(data = Body()):
    cursor.execute(f'''insert into Trip values('{data["plane"]}', '{data["town_from"]}', '{data["town_to"]}', '{data["time_out"]}', 
    '{data["time_in"]}', {data["ID_comp"]})''') 
    cursor.commit()
    return data
 
@app.put("/api/trip")
def edit_TYPEaviacomp(data = Body()):
    cursor.execute(f'''update Trip set plane = '{data["plane"]}', town_from = '{data["town_from"]}', town_to = '{data["town_to"]}', 
        time_out = '{data["time_out"]}',  time_in = '{data["time_in"]}',  ID_comp = '{data["ID_comp"]}, 
        where ID_psg = {data["id"]}''')
    cursor.commit()
    return data
 
@app.delete("/api/trip/{id}") 
def delete_aviacomp(id):
    x = find_element(id, ls_passeng)
    check_is_None(x)
    cursor.execute(f'''delete from Trip where trip_no = {id}''')
    cursor.commit()
    return x
# #----------------------------------------------------------

@app.get("/PassTrip") 
async def main():
    return FileResponse("public/index_4.html")

@app.get("/api/PassTrip") 
def get_TYPEaviacomp():
    return all_elements(ls_PassTrip)

@app.get("/api/PassTrip/{id}")
def get_TYPEaviacomp(id):
    x = find_element(id, ls_PassTrip)
    check_is_None(x)
    return x
 
@app.post("/api/PassTrip")
def create_TYPEaviacomp(data = Body()):
    cursor.execute(f'''insert into Pass_in_trip values('{data["date_"]}', '{data["place"]}' )''') 
    cursor.commit()
    return data
 
@app.put("/api/PassTrip")
def edit_TYPEaviacomp(data = Body()):
    cursor.execute(f'''update Pass_in_trip set date_ = '{data["date_"]}', place = '{data["place"]}'
        where ID_psg = {id.split('-')[0]} and trip_no = {id.split('-')[1]}''')
    cursor.commit()
    return data
 
@app.delete("/api/PassTrip/{id}") 
def delete_aviacomp(id):
    x = find_element(id, ls_PassTrip)
    cursor.execute(f'''delete from Pass_in_trip where ID_psg = {id.split('-')[0]} and trip_no = {id.split('-')[1]}''')
    cursor.commit()
    check_is_None(x)
    return x
# #----------------------------------------------------------