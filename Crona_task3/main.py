import threading 
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse, FileResponse
import pyodbc
import json
import func

#  uvicorn main:app --reload -- сохраняй перед запуском!

func.SyncRates(func.GetParams('date_start'), func.GetParams('date_end'))
t1 = threading.Thread(target = func.SyncCurrentDay, args = (float(func.GetParams('start_thread')), )) 
t1.start() 

app = FastAPI()
@app.get("/report") 
def get_report(): 
    db = func.GetRates(func.GetParams('currency'))
    ls_rep = []
    for row in db:
        ls_rep.append(dict(zip([t[0] for t in row.cursor_description], row)))
    return ls_rep



# синхронизация основного потока и потока-шедуля -- зачем?
# t2 = threading.Thread(target = f, args=(''' 'dollar', 'lira', 'krona' ''', "09.04.2023", "11.04.2023"))
# t2.start() 

