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
    id = 0 #ID 
    modelo = "VENTILADOR2000" #modelo do ventilador
    area = "UTI" #Digite a área
    possuiBateria = True #digite se o modelo tem bateria
    cpuPercent = ps.cpu_percent(interval=1)
    RAM = ps.virtual_memory()
    disco = ps.disk_usage('/')
    processos = len({p.pid: p.info for p in ps.process_iter(['name', 'username'])})
    if(possuiBateria == True):
        bateria = ps.sensors_battery()
    else:
        bateria == None

    dados["timestamp"].append(timestamp)
    dados["ID"].append(id)
    dados["Modelo"].append(modelo)
    dados["Area"].append(area)
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

            print(f"\nData/Hora: {dados['timestamp'][-1]} \nID: {dados["ID"][-1]}\nModelo: {dados["Modelo"][-1]}\nÁrea: aa{dados["Area"][-1]} \nUso da CPU: {dados["CPU"][-1]}% \nUso de RAM: {dados["RAM"][-1]} Gb \nDisco usado: {dados["Disco"][-1]} Gb \nProcessos: {dados["Processos"][-1]}\nBateria: {dados["Bateria"][-1]}%")

            salvar_csv()
            time.sleep(5)

monitoramento()
