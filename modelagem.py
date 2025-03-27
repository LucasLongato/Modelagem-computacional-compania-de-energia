import csv
from datetime import datetime

class Cliente:
    def __init__(self, cliente_id, nome, cpf, email, telefone):
        self.cliente_id = cliente_id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone

class Medidor:
    def __init__(self, medidor_id, cliente_id, num_medidor):
        self.medidor_id = medidor_id
        self.cliente_id = cliente_id
        self.num_medidor = num_medidor
        self.leitura_atual = 0

class Leitura:
    def __init__(self, leitura_id, medidor_id, mes_referencia, leitura_kwh, data_leitura):
        self.leitura_id = leitura_id
        self.medidor_id = medidor_id
        self.mes_referencia = mes_referencia
        self.leitura_kwh = leitura_kwh
        self.data_leitura = data_leitura
        self.situacao_leitura = "normal"

class Faturamento:
    def __init__(self, fatura_id, cliente_id, leitura_id, kwh_consumido, valor_fatura, data_emissao, situacao_fatura):
        self.fatura_id = fatura_id
        self.cliente_id = cliente_id
        self.leitura_id = leitura_id
        self.kwh_consumido = kwh_consumido
        self.valor_fatura = valor_fatura
        self.data_emissao = data_emissao
        self.situacao_fatura = situacao_fatura

def calcular_media_ultimos_tres(consumos):
    if len(consumos) < 3:
        return sum(consumos) / len(consumos) if consumos else 0
    return sum(consumos[-3:]) / 3

def verificar_leitura_atual(media_consumo, leitura_atual):
    variacao_aceitavel = media_consumo * 0.10
    limite_inferior = media_consumo - variacao_aceitavel
    limite_superior = media_consumo + variacao_aceitavel
    return limite_inferior <= leitura_atual <= limite_superior

def calcular_valor_fatura(kwh_consumido):
    if kwh_consumido <= 100:
        tarifa = 0.40
    elif kwh_consumido <= 200:
        tarifa = 0.50
    else:
        tarifa = 0.65
    return kwh_consumido * tarifa

def registrar_leitura_inconsistente(cliente_id, leitura_kwh, data_leitura):
    with open("leituras_inconsistentes.csv", "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([cliente_id, leitura_kwh, data_leitura, "inconsistente"])

def exportar_faturas_csv(faturas):
    with open("faturas.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["fatura_id", "cliente_id", "leitura_id", "kwh_consumido", "valor_fatura", "data_emissao", "situacao_fatura"])
        for fatura in faturas:
            writer.writerow([fatura.fatura_id, fatura.cliente_id, fatura.leitura_id, fatura.kwh_consumido, fatura.valor_fatura, fatura.data_emissao, fatura.situacao_fatura])

def processar_leitura(cliente, medidor, leituras, leitura_atual):
    media_consumo = calcular_media_ultimos_tres([leitura.leitura_kwh for leitura in leituras])
    
    if verificar_leitura_atual(media_consumo, leitura_atual):
        valor_fatura = calcular_valor_fatura(leitura_atual)
        fatura = Faturamento(
            fatura_id=len(leituras) + 1,
            cliente_id=cliente.cliente_id,
            leitura_id=len(leituras) + 1,
            kwh_consumido=leitura_atual,
            valor_fatura=valor_fatura,
            data_emissao=datetime.now().strftime("%Y-%m-%d"),
            situacao_fatura="pendente"
        )
        return f"Fatura gerada: {valor_fatura} R$"
    else:
        registrar_leitura_inconsistente(cliente.cliente_id, leitura_atual, datetime.now().strftime("%Y-%m-%d"))
        return "Leitura inconsistente. Nova leitura programada."

def carregar_dados_csv(arquivo):
    clientes = {}
    medidores = {}
    leituras = []
    
    with open(arquivo, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cliente_id = int(row['cliente_id'])
            if cliente_id not in clientes:
                clientes[cliente_id] = Cliente(cliente_id, row['nome'], row['cpf'], row['email'], row['telefone'])
            
            medidor_id = int(row['medidor_id'])
            if medidor_id not in medidores:
                medidores[medidor_id] = Medidor(medidor_id, cliente_id, row['num_medidor'])
            
            leituras.append(Leitura(
                int(row['leitura_id']),
                medidor_id,
                row['mes_referencia'],
                float(row['leitura_kwh']),
                row['data_leitura']
            ))
    return clientes, medidores, leituras

#teste de leitura 
dados_csv = "dados_leituras.csv"
clientes, medidores, leituras = carregar_dados_csv(dados_csv)
cliente = list(clientes.values())[0]
medidor = list(medidores.values())[0]

print(processar_leitura(cliente, medidor, leituras, 115))