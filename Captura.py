import psutil as ps
import pandas as pd
import time
from datetime import datetime


dados = {
    "timestamp": [],
    "ID": [],
    "Modelo": [],
    "Area": [],
    "CPU": [],
    "RAM": [],
    "Disco": [],
    "Processos": [],
    "Bateria":[]
}


def obter_uso():
    # usuario = ps.users()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = 4 #ID 
    modelo = "Dx3010" #modelo do ventilador
    area = "Cirurgia" #Digite a área
    possuiBateria = False #digite se o modelo tem bateria
    cpuPercent = ps.cpu_percent(interval=1)
    RAM = ps.virtual_memory()
    disco = ps.disk_usage('/')
    processos = len({p.pid: p.info for p in ps.process_iter(['name', 'username'])})

    if(possuiBateria == True):
        bateria = ps.sensors_battery()
        bateria = round(bateria.percent,1)
    else:
        bateria = "N/A"

    dados["timestamp"].append(timestamp)
    dados["ID"].append(id)
    dados["Modelo"].append(modelo)
    dados["Area"].append(area)
    dados["CPU"].append(cpuPercent)
    dados["RAM"].append(RAM.percent)
    dados["Disco"].append(round(disco.used / 1024 ** 3))
    dados["Processos"].append(processos)
    dados["Bateria"].append(bateria)
    


def salvar_csv():
    df = pd.DataFrame(dados)
    df.to_csv("coletaGeralGrupo2.csv", encoding="utf-8", index=False)



def monitoramento():
    
        while True:
            obter_uso()

            print(f"\nData/Hora: {dados['timestamp'][-1]} \nID: {dados["ID"][-1]}\nModelo: {dados["Modelo"][-1]}\nÁrea: {dados["Area"][-1]} \nUso da CPU: {dados["CPU"][-1]}% \nUso de RAM: {dados["RAM"][-1]}% \nDisco usado: {dados["Disco"][-1]} Gb \nProcessos: {dados["Processos"][-1]}\nBateria: {dados["Bateria"][-1]}%")

            salvar_csv()
            time.sleep(5)

monitoramento()
