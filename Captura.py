import psutil as ps
import pandas as pd
import time
from datetime import datetime


dados = {
    "timestamp": [],
    "nSerie": [],
    "CPU": [],
    "RAM": [],
    "Disco": [],
    "Processos": [],
    "Bateria":[]
}

user = ps.users()
nSerie = user[-1].name
nSerie = "SN123456789" #No final, deve ser uma coleta de usuário da psutil, pois cada ventilador terá seu identificador no sistema, e no banco SQL


def obter_uso():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cpuPercent = ps.cpu_percent(interval=1)
    RAM = ps.virtual_memory()
    disco = ps.disk_usage('/')
    processos = len({p.pid: p.info for p in ps.process_iter(['name', 'username'])})

    
    bateria = ps.sensors_battery()
    bateria = round(bateria.percent,1)
    

    dados["timestamp"].append(timestamp)
    dados["nSerie"].append(nSerie)
    dados["CPU"].append(cpuPercent)
    dados["RAM"].append(RAM.percent)
    dados["Disco"].append(round(disco.used / 1024 ** 3))
    dados["Processos"].append(processos)
    dados["Bateria"].append(bateria)
    


def salvar_csv():
    df = pd.DataFrame(dados)
    df.to_csv(f"coleta-{nSerie}.csv", encoding="utf-8", index=False)



def monitoramento():
    
        while True:
            obter_uso()

            print(f"\nData/Hora: {dados['timestamp'][-1]}\nNúmero de série: {dados["nSerie"][-1]}\nUso da CPU: {dados["CPU"][-1]}% \nUso de RAM: {dados["RAM"][-1]}% \nDisco usado: {dados["Disco"][-1]} Gb \nProcessos: {dados["Processos"][-1]}\nBateria: {dados["Bateria"][-1]}%")

            salvar_csv()
            time.sleep(5)

monitoramento()
