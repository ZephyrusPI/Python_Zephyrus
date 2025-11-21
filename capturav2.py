import psutil as ps
import pandas as pd
import time
import boto3
import pymysql
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

# Configuração do MySQL 
config_mysql = {
    "host": "",
    "port":3306,
    "user": "",
    "password": "",
    "database": "",
    "connect_timeout":10
}

# Função para coletar métricas 
nomeUser = ps.users()[0].name
def obter_uso():

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = 2  # ID do ventilador
    modelo = "Drager Evita Infinity V500"
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
    df.to_csv(f"coleta{nomeUser}.csv", encoding="utf-8", index=False)


#Salvar no banco MySQL
def salvar_mysql():
    print("entrei no salvar_mysql")
    try:
        conexao = pymysql.connect(**config_mysql)
        cursor = conexao.cursor()
        for i in range(len(dados["timestamp"])):
           cursor.execute("""
    INSERT INTO coleta
    (timestamp, ID_Equipamento, Modelo, Area, CPU, RAM, Disco, Processos, Bateria)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
""", (
    dados["timestamp"][i],
    dados["ID"][i],
    dados["Modelo"][i],
    dados["Area"][i],
    dados["CPU"][i],
    dados["RAM"][i],
    dados["Disco"][i],
    dados["Processos"][i],
    str(dados["Bateria"][i])
))

        conexao.commit()
        print(f"{len(dados['timestamp'])} registros salvos no MySQL.")
    except Exception as e:
        print("Erro ao salvar no MySQL:", e)
    finally:
        try:
            cursor.close()
            conexao.close()
        except:
            pass


def enviar_s3():
    import io

    s3_client = boto3.client(
        's3',
        aws_access_key_id='',
        aws_secret_access_key='',
        aws_session_token='',
        region_name='us-east-1'
    )

    nome_bucket = 'raw-zephyrus'
    caminho_arquivo_local = f"coleta{nomeUser}.csv"
    nome_objeto = f"coleta{nomeUser}.csv"

    try:
        # 1. Tenta baixar o arquivo existente do S3
        buffer = io.BytesIO()
        s3_client.download_fileobj(nome_bucket, nome_objeto, buffer)
        buffer.seek(0)

        # 2. Lê o CSV existente
        df_existente = pd.read_csv(buffer)

        # 3. Lê o CSV novo local
        df_novo = pd.read_csv(caminho_arquivo_local)

        # 4. Concatena (mantém histórico)
        df_final = pd.concat([df_existente, df_novo], ignore_index=True)

    except s3_client.exceptions.NoSuchKey:
        print("Nenhum arquivo existente no S3. Criando novo...")
        df_final = pd.read_csv(caminho_arquivo_local)
    except Exception as e:
        print(f"Erro ao baixar arquivo do S3: {e}")
        df_final = pd.read_csv(caminho_arquivo_local)

    # 5. Salva o resultado em um buffer
    csv_buffer = io.StringIO()
    df_final.to_csv(csv_buffer, index=False)

    # 6. Faz upload do CSV combinado para o S3
    s3_client.put_object(
        Bucket=nome_bucket,
        Key=nome_objeto,
        Body=csv_buffer.getvalue()
    )

    print("Arquivo atualizado enviado ao S3 com sucesso!")


# Loop principal 
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
            salvar_mysql()
            enviar_s3()
            contador = 0

        time.sleep(intervalo)


monitoramento(intervalo=5, intervalo_enviar=60)
