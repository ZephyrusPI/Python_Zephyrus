import time
import psutil
import pandas
from datetime import datetime
dados={
   "timestamp":[],
   "pid":[],
   "name":[],
   "username":[],
   "cpu":[],
   "ram":[]

}
usuario="Isabella"



while True:
    time.sleep(60)
    timestamp=datetime.now()

    dataframe=pandas.DataFrame(dados)
    dataframe.to_csv("dados_processos.csv", index=False)
    for proc in psutil.process_iter(['pid', 'name', 'username','cpu_percent','memory_percent']):
        if proc.info["username"]=="ISABELLA\isafa":
            dados["username"].append(proc.info["username"])  
            dados["timestamp"].append(timestamp)
            dados["pid"].append(proc.info["pid"])
            dados["name"].append(proc.info["name"])
            dados["cpu"].append(proc.info["cpu_percent"])
            dados["ram"].append(proc.info["memory_percent"])



        
        
