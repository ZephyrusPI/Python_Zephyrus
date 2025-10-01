import psutil as ps
import pandas as pd
import time
from datetime import datetime


dados = {
    "timestamp": [],
    "usuario": [],
    "CPU": [],
    "RAM": [],
    "Disco": [],
    "Processos": [],
    "Bateria":[]
}


def obter_uso():
    usuario = ps.users()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user = usuario[0].name
    cpuPercent = ps.cpu_percent(interval=1)
    RAM = ps.virtual_memory()
    disco = ps.disk_usage('/')
    processos = len({p.pid: p.info for p in ps.process_iter(['name', 'username'])})
    bateria = ps.sensors_battery()

    dados["timestamp"].append(timestamp)
    dados["usuario"].append(user)
    dados["CPU"].append(cpuPercent)
    dados["RAM"].append(round(RAM.used / 1024 ** 3))
    dados["Disco"].append(round(disco.used / 1024 ** 3))
    dados["Processos"].append(processos)
    dados["Bateria"].append(round(bateria.percent,1))
    


def salvar_csv():
    df = pd.DataFrame(dados)
    df.to_csv("coletaGeralGrupo2.csv", encoding="utf-8", index=False)



def monitoramento():
    
        while True:
            obter_uso()

            print(f"\nData/Hora: {dados['timestamp'][-1]} \nUsuário: {dados["usuario"][-1]} \nUso da CPU: {dados["CPU"][-1]}% \nUso de RAM: {dados["RAM"][-1]} Gb \nDisco usado: {dados["Disco"][-1]} Gb \nProcessos: {dados["Processos"][-1]}\nBateria: {dados["Bateria"][-1]}%")

            salvar_csv()
            time.sleep(5)

monitoramento()
