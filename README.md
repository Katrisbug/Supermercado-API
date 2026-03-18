# **API de Supermercado com CSV**

API RESTful desenvolvida com FastAPI para gerenciamento completo de clientes, produtos e ordens de venda, utilizando arquivos CSV como banco de dados.

---

## **📋 Sobre o Projeto**

Esta API permite realizar operações CRUD (Create, Read, Update, Delete) para:

- **Clientes**: Cadastro com nome, sobrenome, data de nascimento e CPF
- **Produtos**: Cadastro com nome, fornecedor e quantidade em estoque
- **Ordens de Venda**: Vinculação de clientes a produtos

Os dados são persistidos em arquivos CSV, eliminando a necessidade de um banco de dados tradicional.

---

## **🚀 Como Executar**

### **Pré-requisitos**

- Python 3.7 ou superior instalado
- Pip (gerenciador de pacotes do Python)
- Postman (para teste da API)

### **Passo a Passo**

1. **Crie e ative um ambiente virtual (recomendado)**

```python
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. **Instale o FastAPI com todas as dependências padrão**

```python
pip install "fastapi[standard]"
```

3. **Salve o código da API** em um arquivo (ex: `app.py`)
4. **Inicie o servidor**

```python
fastapi dev app.py #em vez de app.py coloque o nome do arquivo que você criou
```

> O comando `fastapi dev` já inclui o --reload automaticamente para desenvolvimento.
> 
5. **Acesse a API**
- API base: `http://localhost:8000`

---

## **📁 Estrutura de Arquivos**

Ao iniciar a API pela primeira vez, serão criados automaticamente:

- `Clientes.csv` - Armazena dados dos clientes
- `Produtos.csv` - Armazena dados dos produtos
- `OrdemDeVendas.csv` - Armazena as ordens de venda

---

## **🔌 Endpoints Disponíveis**

### **📊 Status da API**

| **Método** | **Endpoint** | **Descrição** |
| --- | --- | --- |
| GET | `/` | Verifica se a API está funcionando (rota padrão) |

### **👥 Clientes**

| **Método** | **Endpoint** | **Descrição** |
| --- | --- | --- |
| GET | `/clientes` | Lista todos os clientes cadastrados |
| POST | `/clientes` | Cadastra um novo cliente |
| PUT | `/clientes/{cliente_id}` | Atualiza dados de um cliente específico |
| DELETE | `/clientes/{cliente_id}` | Remove um cliente do sistema |

### **📦 Produtos**

| **Método** | **Endpoint** | **Descrição** |
| --- | --- | --- |
| GET | `/produtos` | Lista todos os produtos cadastrados |
| POST | `/produtos` | Cadastra um novo produto |
| PUT | `/produtos/{produto_id}` | Atualiza dados de um produto específico |
| DELETE | `/produtos/{produto_id}` | Remove um produto do sistema |

### **📝 Ordens de Venda**

| **Método** | **Endpoint** | **Descrição** |
| --- | --- | --- |
| GET | `/ordens` | Lista todas as ordens de venda |
| POST | `/ordens` | Cria uma nova ordem (vincula cliente e produto) |
| DELETE | `/ordens/{ordem_id}` | Cancela/remove uma ordem específica |

---

## **📦 Modelos de Dados**

### **Cliente (POST/PUT /clientes)**

```json
{
  "nome": "João",
  "sobrenome": "Silva",
  "data_de_nascimento": "1990-05-15",
  "cpf": "123.456.789-00"
}
```

### **Produto (POST/PUT /produtos)**

```json
{
  "nome": "Notebook",
  "fornecedor": "Tech Ltda",
  "quantidade": 10
}
```

### **Ordem de Venda (POST /PUT /ordens)**

```json
{
  "cliente_id": 1,
  "produto_id": 2
}
```

---

## **📮 Testando com Postman**

### **Configuração Inicial no Postman**

1. **Abra o Postman**
2. **Crie uma nova Collection** (ex: "API Vendas")
3. **Configure a variável de ambiente** (opcional):
    - Adicione variável `base_url` com valor `http://localhost:8000`

### **→ Exemplos de Requisições no Postman**

### **1. GET - Verificar Status da API**

- **Método**: `GET`
- **URL**: `http://localhost:8000/`
- **Resposta esperada**: `{"mensagem": "API funcionando", "status": "online"}`

### **2. POST - Criar um Cliente**

- **Método**: `POST`
- **URL**: `http://localhost:8000/clientes`
- **Body** (raw JSON):

```json
{
  "nome": "Maria",
  "sobrenome": "Oliveira",
  "data_de_nascimento": "1985-03-20",
  "cpf": "987.654.321-00"
}
```

### **3. GET - Listar Todos os Clientes**

- **Método**: `GET`
- **URL**: `http://localhost:8000/clientes`

### **4. POST - Criar um Produto**

- **Método**: `POST`
- **URL**: `http://localhost:8000/produtos`
- **Body** (raw JSON):

```json
{
  "nome": "Smartphone",
  "fornecedor": "Cell Ltda",
  "quantidade": 15
}
```

### **5. POST - Criar uma Ordem de Venda**

- **Método**: `POST`
- **URL**: `http://localhost:8000/ordens`
- **Body** (raw JSON):

```json
{
  "cliente_id": 1,
  "produto_id": 2
}
```

### **6. PUT - Atualizar um Cliente**

- **Método**: `PUT`
- **URL**: `http://localhost:8000/clientes/1`
- **Body** (raw JSON):

```json
{
  "nome": "Maria",
  "sobrenome": "Santos",
  "data_de_nascimento": "1985-03-20",
  "cpf": "987.654.321-00"
}
```

### **7. DELETE - Remover um Produto**

- **Método**: `DELETE`
- **URL**: `http://localhost:8000/produtos/3`

---

## **📚 Códigos de Resposta**

- **200 OK**: Requisição bem-sucedida;
- **201 Created**: Recurso criado com sucesso;
- **400 Bad Request**: Dados inválidos (ex: CPF duplicado);
- **404 Not Found**: Recurso não encontrado;
- **422 Unprocessable Entity**: Dados não atendem ao formato esperado;
- **500 Internal Server Error:** Está com erro dentro do servidor (código);

---

## **🛠️ Tecnologias Utilizadas**

- **FastAPI**: Framework web de alta performance.
- **FastAPI CLI**: Ferramenta de linha de comando para executar a API.
- **Pydantic**: Validação de dados e definição de modelos (já incluso no FastAPI).
- **CSV**: Armazenamento persistente de dados.
- **Postman**: Testes e funcionamento da API.

---

## **📁 Estrutura do CSV**

### **Clientes.csv**

```
ID,NOME,SOBRENOME,DATA DE NASCIMENTO,CPF
1,João,Silva,1990-05-15,123.456.789-00
2,Maria,Oliveira,1985-03-20,987.654.321-00
```

### **Produtos.csv**

```
ID,NOME,FORNECEDOR,QUANTIDADE
1,Notebook,Tech Ltda,10
2,Smartphone,Cell Ltda,15
```

### **OrdemDeVendas.csv**

```
ID,ID_CLIENTE,ID_PRODUTO
1,1,2
2,2,1
```

---

## **⚠️ Observações Importantes**

1. **IDs são gerados automaticamente** - Não é necessário informar IDs ao criar registros.
2. **CPF é único** - Não é possível cadastrar dois clientes com o mesmo CPF.
3. **Dados persistentes** - As informações são salvas em arquivos CSV e permanecem mesmo após reiniciar a API.
4. **Validações** - Todos os dados são validados antes de serem salvos.
5. **Ambiente virtual** - Recomenda-se sempre usar um ambiente virtual para isolar as dependências do projeto.
6. **Postman** - Ferramenta útil para testar todos os endpoints sem necessidade de interface gráfica.
7. **Não usar em produção** - Esta implementação com CSV é adequada para testes e aprendizado, mas para produção recomenda-se um banco de dados real.
