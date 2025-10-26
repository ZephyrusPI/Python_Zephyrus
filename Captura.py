import psutil as ps
import pandas as pd
import time
import boto3
from datetime import datetime

# Dicionário de dados
dados = {
    "timestamp": [],
    "ID": [],
    "Modelo": [],
    "Area": [],
    "CPU": [],
    "RAM": [],
    "Disco": [],
    "Processos": [],
    "Bateria": []
}

# Função para coletar métricas
def obter_uso():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = 2  # ID do ventilador
    modelo = "Dx3873"
    area = "UTI"
    possuiBateria = True

    cpuPercent = ps.cpu_percent(interval=1)
    RAM = ps.virtual_memory()
    disco = ps.disk_usage('/')
    processos = len({p.pid: p.info for p in ps.process_iter(['name', 'username'])})

    if possuiBateria:
        bat = ps.sensors_battery()
        bateria = round(bat.percent, 1) if bat else "N/A"
    else:
        bateria = "N/A"

    # Adiciona ao dicionário
    dados["timestamp"].append(timestamp)
    dados["ID"].append(id)
    dados["Modelo"].append(modelo)
    dados["Area"].append(area)
    dados["CPU"].append(cpuPercent)
    dados["RAM"].append(RAM.percent)
    dados["Disco"].append(round(disco.used / 1024 ** 3))
    dados["Processos"].append(processos)
    dados["Bateria"].append(bateria)

# Função para salvar em CSV
def salvar_csv():
    df = pd.DataFrame(dados)
    df.to_csv("coletaGeralGrupo2.csv", encoding="utf-8", index=False)


def enviar_s3():
    s3_client = boto3.client(
        's3',
        aws_access_key_id='',
        aws_secret_access_key='',
        aws_session_token='',
        region_name='us-east-1'
    )

    nome_bucket = 'raw-zephyrus'
    caminho_arquivo = 'coletaGeralGrupo2.csv'
    nome_objeto = 'coletaRawZephyrus.csv'

    s3_client.upload_file(caminho_arquivo, nome_bucket, nome_objeto)
   

def monitoramento(intervalo=5, intervalo_enviar=60):
    print("Iniciando monitoramento...")
    contador = 0  

    while True:
        obter_uso()
        print(
            f"\nData/Hora: {dados['timestamp'][-1]}"
            f"\nID: {dados['ID'][-1]}"
            f"\nModelo: {dados['Modelo'][-1]}"
            f"\nÁrea: {dados['Area'][-1]}"
            f"\nCPU: {dados['CPU'][-1]}%"
            f"\nRAM: {dados['RAM'][-1]}%"
            f"\nDisco usado: {dados['Disco'][-1]} GB"
            f"\nProcessos: {dados['Processos'][-1]}"
            f"\nBateria: {dados['Bateria'][-1]}"
        )

        salvar_csv()
        contador += intervalo

       
        if contador >= intervalo_enviar:
            enviar_s3()
            contador = 0

        time.sleep(intervalo)



monitoramento(intervalo=5, intervalo_enviar=60)
