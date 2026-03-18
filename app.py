from fastapi import FastAPI #importa o fastapi
import os #importa a biblioteca os
import csv #importa a biblioteca csv
from pydantic import BaseModel
from datetime import date #importa a data da biblioteca datetime 


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
if not os.path.exists(produtos_file):#verifica se o arquivo existe
    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        data = [#lista
            ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]#Cabeçalho do arquivo CSV, indicando as colunas "ID", "NOME", "FORNECEDOR" e "QUANTIDADE".
        ]
        writer = csv.writer(file)#Cria um objeto writer para escrever no arquivo CSV.
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

class Cliente(BaseModel):
    id: int
    nome: str
    sobrenome: str
    data_de_nascimento: date
    cpf: str
    

class Produtos(BaseModel):#Define o formato de dados que a API aceita.
    nome: str
    fornecedor: str
    quantidade: int

class Produto(BaseModel):#Define o formato de dados que a API aceita.
    id:int
    nome: str
    fornecedor: str
    quantidade: int

class OrdensDeVendas(BaseModel):
    cliente_id: int
    produto_id: int

class OrdensDeVenda(BaseModel):
    id: int
    cliente_id: int
    produto_id: int



# Rota Padrão
@app.get("/")
def home():
    return {"mensagem": "API funcionando"} 

# Gets Padrão
# Get Clientes - listar todos os clientes
@app.get("/clientes")
def clientes():
    Clientes_dic = {}#Dicionário para armazenar os clientes lidos do arquivo CSV.
    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)#le o arquivo
        for linha in reader:#percorre cada linha
            if linha[0] == 'ID': 
                continue
            else:
                Clientes_dic[linha[0]] = {"NOME":linha[1], "SOBRENOME":linha[2], "DATA DE NASCIMENTO":linha[3],"CPF":linha[4] }#Adiciona o cliente ao dicionário "Clientes", onde a chave é o ID do cliente (linha[0]) e o valor é o nome do cliente (linha[1]).
    return Clientes_dic

#Get Produtos - listar todos os produtos
@app.get("/produtos")
def produtos():
    produtos_dic = {}#Dicionário para armazenar os clientes lidos do arquivo CSV.
    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)#le o arquivo
        for linha in reader:#percorre cada linha
            if linha[0] == 'ID':#Se a primeira coluna da linha for "ID", significa que é o cabeçalho, então a linha é ignorada e o loop continua para a próxima iteração.
                continue
            else:
                produtos_dic[linha[0]] = {"NOME":linha[1], "FORNECEDOR":linha[2], "QUANTIDADE":linha[3]}#Adiciona o cliente ao dicionário "Clientes", onde a chave é o ID do cliente (linha[0]) e o valor é o nome do cliente (linha[1]).
    return produtos_dic

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
                Ordens[row[0]] = {
                    "ID_CLIENTE": row[1],
                    "ID_PRODUTO": row[2]
                }


    return Ordens

# Posts Padrão
# Post Clientes - Adicionar um novo cliente
@app.post("/clientes")
def add_cliente(cliente: Clientes):
    data = [["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]]
    ids = []

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # pula o cabeçalho

        for row in reader:
            # Verificar CPF duplicado
            if row[4] == cliente.cpf:
                return {"erro": "CPF já cadastrado"}
            
            ids.append(int(row[0]))  # guarda os IDs
            data.append(row)

    # gera novo ID automaticamente
    novo_id = max(ids, default=0) + 1

    novo_cliente = [
        novo_id,
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
def add_produtos(produto: Produtos):  
    data = [
            ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
        ]  # Cabeçalho 
    produto_id = 0

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file: 
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "ID":  
                continue
            data.append(row)  
            if int(row[0]) > produto_id:  
                produto_id = int(row[0])

    novo_id = produto_id + 1  
    novo_produto = [  
        str(novo_id),
        produto.nome,
        produto.fornecedor,
        str(produto.quantidade)
    ]
    data.append(novo_produto)  

    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:  
        writer = csv.writer(file)
        writer.writerows(data)

    return {  # retornar mensagem + ID de produtos
        "mensagem": "Produto cadastrado com sucesso",
        "id": novo_id
    }

# Post Ordens de Vendas - Criar uma nova ordem de vendas
@app.post("/ordens")
def add_ordens(ordem: OrdensDeVendas):
    data = [
        [ "ID", "ID_CLIENTE", "ID_PRODUTO"]
    ]
    ultimo_id = 0

    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "ID":
                continue
            
            data.append(row)
            
            if int(row[0]) > ultimo_id:
                ultimo_id = int(row[0])
    
    novo_id = ultimo_id + 1
    nova_ordem = [str(novo_id), str(ordem.cliente_id), str(ordem.produto_id)]

    data.append(nova_ordem)

    with open(ordens_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return {
        "mensagem": "Ordem de venda criada com sucesso",
        "id": novo_id,
        "cliente_id": ordem.cliente_id,
        "produto_id": ordem.produto_id
    }

# Deletes Padrão
# Delete Clientes - Remover um cliente

@app.delete("/clientes/{clientes_id}")
def deletar_clientes(clientes_id:str):
    data = [
            ["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]
        ]
    
    cliente_dic = {}

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                data.append(linha)
    for linha in data:
        if linha[0] == clientes_id:
            data.pop(data.index(linha))
            break
    else:
        return {"ERRO": "ID informado não existe"} 
    
    with open(clientes_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                cliente_dic[linha[0]] = {
    "NOME": linha[1],
    "SOBRENOME": linha[2],
    "DATA DE NASCIMENTO": linha[3],
    "CPF": linha[4]
}

    return cliente_dic


# Delete Produtos - Remover um produto
@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id:str):
    data = [
    ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
]
    
    produtos_dic = {}

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                data.append(linha)
    for linha in data:
        if linha[0] == produto_id:
            data.pop(data.index(linha))
            break
    else:
        return {"ERRO": "ID informado não existe"} 
    
    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                produtos_dic[linha[0]] = {"NOME":linha[1], "FORNECEDOR":linha[2], "QUANTIDADE":linha[3]}

    return produtos_dic

# Delete OrdensDeVendas - Remover uma ordem de venda
@app.delete("/ordens/{ordens_id}")
def deletar_ordens(ordens_id:str):
    data = [
    ["ID", "ID_CLIENTE", "ID_PRODUTO"]
]
    
    ordens_dic = {}

    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                data.append(linha)
    for linha in data:
        if linha[0] == ordens_id:
            data.pop(data.index(linha))
            break
    else:
        return {"ERRO": "ID informado não existe"} 
    
    with open(ordens_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                ordens_dic[linha[0]] = { "ID_CLIENTE":linha[1], "ID_PRODUTO":linha[2]}

    return ordens_dic



# Put Padrão
# Put Clientes - Editar um cliente
# Put Padrão
# Put Clientes - Editar um cliente
@app.put("/clientes")
async def edit_cliente(cliente: Cliente):
    data = [
        ["ID", "NOME", "SOBRENOME", "DATA DE NASCIMENTO", "CPF"]
    ]
    
    clientes_dic = {}

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)

    for linha in data:
        if linha[0] == "ID":
            continue

        if int(linha[0]) == cliente.id:
            linha[1] = cliente.nome
            linha[2] = cliente.sobrenome
            linha[3] = str(cliente.data_de_nascimento)
            linha[4] = cliente.cpf
            break
    else:
        return {"ERRO": "ID informado não existe"}

    with open(clientes_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    with open(clientes_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                clientes_dic[linha[0]] = {
                    "NOME": linha[1],
                    "SOBRENOME": linha[2],
                    "DATA DE NASCIMENTO": linha[3],
                    "CPF": linha[4]
                }

    return clientes_dic


# Put Produtos - Editar um produto
@app.put("/produtos")
async def edit_produto(produto: Produto):
    data = [
        ["ID", "NOME", "FORNECEDOR", "QUANTIDADE"]
    ]
    
    produtos_dic = {}

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)

    for linha in data:
        if linha[0] == "ID":
            continue

        if int(linha[0]) == produto.id:
            linha[1] = produto.nome
            linha[2] = produto.fornecedor
            linha[3] = str(produto.quantidade)
            break
    else:
        return {"ERRO": "ID informado não existe"}

    with open(produtos_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    with open(produtos_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                produtos_dic[linha[0]] = {
                    "NOME": linha[1],
                    "FORNECEDOR": linha[2],
                    "QUANTIDADE": linha[3]
                }

    return produtos_dic

@app.put("/ordens")
async def edit_ordem(ordem: OrdensDeVenda):
    data = [
        ["ID", "ID_CLIENTE", "ID_PRODUTO"]
    ]
    
    ordens_dic = {}

    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'ID':
                continue
            else:
                data.append(row)

    for linha in data:
        if linha[0] == "ID":
            continue

        if int(linha[0]) == ordem.id:
            linha[1] = str(ordem.cliente_id)
            linha[2] = str(ordem.produto_id)
            break
    else:
        return {"ERRO": "ID informado não existe"}

    with open(ordens_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    with open(ordens_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for linha in reader:
            if linha[0] == 'ID':
                continue
            else:
                ordens_dic[linha[0]] = {
                    "ID_CLIENTE": linha[1],
                    "ID_PRODUTO": linha[2]
                }

    return ordens_dic