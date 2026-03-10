from fastapi import FastAPI #importa o fastapi
import os #importa a biblioteca os
import csv #importa a biblioteca csv
from pydantic import BaseModel
from datetime import date #importa a data da biblioteca datetime 
from fastapi import FastAPI, HTTPException


app = FastAPI()

#Nome dos Arquivos CSV
clientes_file = "Clientes.csv"
produtos_file = "Produtos.csv"
ordens_file = "OrdemDeVendas.csv"

#Criação do Arquivos csv
#Arquivo Cliente
if not os.path.exists(clientes_file):    
    with open(clientes_file, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')

#Arquivo Produtos
if not os.path.exists(produtos_file):    
    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')

#Arquivo Ordem De Vendas 
if not os.path.exists(ordens_file):    
    with open(ordens_file, mode='w', newline='', encoding='utf-8') as file:
        data = [
            ["ID","ID_CLIENTE","ID_PRODUTO"]
        ]
        writer = csv.writer(file)
        writer.writerows(data)
else:
    print('O arquivo já existe!')


#Class de Clientes - Produtos - OrdemDeVendas na BaseModel
class Clientes(BaseModel):
    nome: str
    sobrenome: str
    data_de_nascimento: date
    cpf: str

class Produtos(BaseModel):
    nome: str
    fornecedor: str
    quantidade: int

class OrdensDeVendas(BaseModel):
    cliente_id: int
    produto_id: int


# Rota Padrão
@app.get("/")
def home():
    return {"mensagem": "API funcionando"} 

# Gets Padrão
# Get Clientes - listar todos os clientes
@app.get("/clientes")
def get_clientes():
    clientes = {}
    try:
        with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                if row:  # Verificar se a linha não está vazia
                    clientes[row[0]] = {
                        "nome": row[1],
                        "sobrenome": row[2],
                        "data_nascimento": row[3],
                        "cpf": row[4]
                    }
        return clientes
    except Exception as e:
        return {"erro": str(e)}

#Get Produtos - listar todos os produtos
@app.get("/produtos")
def produtos():
    Produtos = {}
    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                Produtos[row[0]] = row[1]
    return Produtos

#Get OrdemDeVendas - listar todas as ordens de vendas
@app.get ("/ordens")
def ordens():
    Ordens = {}
    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                Ordens[row[0]] = row[1]

    return Ordens

# Posts Padrão
# Post Clientes - Adicionar um novo cliente
@app.post("/add_clientes")
def add_cliente(cliente: Clientes):
    data = [["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]]
    ultimo_id = 0

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "ID":
                continue
            # Verificar CPF duplicado
            if row[4] == cliente.cpf:
                return {"erro": "CPF já cadastrado"}
            data.append(row)
            if int(row[0]) > ultimo_id:
                ultimo_id = int(row[0])

    novo_id = ultimo_id + 1
    novo_cliente = [
        str(novo_id),
        cliente.nome,
        cliente.sobrenome,
        str(cliente.data_de_nascimento),
        cliente.cpf
    ]
    data.append(novo_cliente)

    with open(clientes_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {
        "mensagem": "Cliente cadastrado com sucesso",
        "id": novo_id
    }


# Post Produtos - Adicionar um novo produto
@app.post("/produtos")
async def add_produtos(produto:produtos):
    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]

    Produtos = {}

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)

    novo = [produtos.id, produtos.nome, produtos.fornecedor, produtos.quantidade]
    data.append(novo)

    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                Produtos[row[0]] = row[1]

    return Produtos

# Post Ordens de Vendas - Criar uma nova ordem de vendas
@app.post("/ordens")
async def 


# Deletes Padrão
# Delete Clientes - Remover um cliente
@app.delete("/clientes/{cliente_id}")
def del_cliente(cliente_id:int):
    data = [
        ["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]
    ]
    
    Clientes = {}

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)
    
    cont = False
    for linha in data:
        if linha[0] == cliente_id:
            data.pop(data.index(linha))
            cont = True

    if cont != True:
        return {"ERRO":"ID informado não existe"}        
    
    with open(clientes_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                Clientes[row[0]] = row[1]

    return Clientes

# Delete Produtos - Remover um produto
@app.delete("/delete_produto/{id}")
def delete_produto(id:int):
    
    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]
    
    produto_dict = {}

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)
    
    cont = False
    for linha in data:
        if linha[0] == str(id):
            data.pop(data.index(linha))
            cont = True

    if cont != True:
        return {"ERRO":"ID informado não existe"}        
    
    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                produto_dict[row[0]] = row[1]

    return produto_dict

# Delete OrdensDeVendas - Remover uma ordem de venda



# Put Padrão
# Put Clientes - Editar um cliente


# Put Produtos - Editar um produto


# Put OrdemDeVendas - Editar a ordem
#@app.put("/ordem") :