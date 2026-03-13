import json
import os
import sqlite3


produtos = []
faturamento_total = 0
vendas = []

#CONEXÃO COM SQLITE3

conexao = sqlite3.connect('acai.db')
cursor = conexao.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    quantidade INTEGER NOT NULL
)
''')
conexao.commit()

# SALVAR DADOS

def salvar_dados():
    import os
    print('Salvando em: ', os.getcwd())
    dados = {
        "produtos": produtos,
        "vendas": vendas,
        "faturamento_total": faturamento_total,
    }
    with open('dados.json', 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

    #CARREGAR DADOS

def carregar_dados():
    global produtos, vendas, faturamento_total
    if os.path.exists("dados.json"):
       with open("dados.json") as arquivo:
           dados = json.load(arquivo)
           produtos = dados["produtos"]
           vendas = dados["vendas"]
           faturamento_total = dados["faturamento_total"]

      # CRIACAO DO SISTEMA

def cadastrar_produtos():
    nome = input('Nome do produto: ')
    preco = float(input('Preço: '))
    quantidade = int(input('quantidade em estoque:'))

    cursor.execute(
        'INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)',
        (nome, preco, quantidade)
    )
    conexao.commit()
    print('Produtos cadastrados no Banco!\n')
def listar_produtos():
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()

    if not produtos:
        print('Nenhum produto cadastrado.\n')
        return
    print('\n Lista de produtos: ')
    for produtos in produtos:
        print(f'{produtos[0]} - {produtos[1]}, R${produtos[2]}, Estoque: {produtos[3]}')
    print()
2
      # FATURAMENTO

def realizar_vendas():
    global faturamento_total
    if not produtos:
        print('Nenhum produto cadastrado\n')
        return
    listar_produtos()
    try:
        escolha = int(input('Escolha o numero do produto: '))
        produto = produtos[escolha]
        quantidade = int(input('Quantidade Desejada: '))
        if quantidade > produto["quantidade"]:
            print('Estoque insuficiente!')
            return
        total = quantidade * produto["preco"]

    # ATUALIZAR ESTOQUE

        produto['quantidade'] -= quantidade

     # ATUALIZAR FATURAMENTO

        faturamento_total += total

     # REGISTRAR VENDA NO HISTORICO

        venda = {
            "nome": produto["nome"],
            "quantidade": quantidade,
            "total": total
        }
        vendas.append(venda)
        salvar_dados()
        print(f'Venda realizada!! total: R${total:.2f}\n')
    except(ValueError, IndexError):
        print('OPCÃO INVALIDA\n')

       # RELATORIO DO SISTEMA

def mostrar_relatorio():
    print('\n RELATORIO DE PRODUTOS')
    print(f'Faturamento total: {faturamento_total:.2f}')
    if not vendas:
        print('Nenhuma venda realizada')
        return

    total_items = sum(p['quantidade'] for p in produtos)
    print(f'Total de items em estoque: {total_items}\n')

    # PRODUTO MAIS VENDIDO
    contador = {}
    for venda in vendas:
        nome = venda["nome"]
        quantidade = venda["quantidade"]
        if nome in contador:
            contador[nome] += quantidade
        else:
            contador[nome] = quantidade
    produto_mais_vendido = max(contador, key=contador.get)
    print(f'Produtos mais vendidos: {produto_mais_vendido}')
    print('\n Historico de vendas')
    for venda in vendas:
        print(f'- {venda['nome']}, {venda["quantidade"]}, unidade(s) R${venda["total"]:.2f}')
    print()

    # MENU DO SISTEMA

def menu():
    while True:
        print('---- MENU AÇAI ----')
        print('\nMenu Principal')
        print('''
        1 - Cadastrar produto
        2 - Listar produtos
        3 - Total de produtos cadastrados
        4 - Sair do menu
        5 - Realizar vendas
        6 - Ver Relatorio
        ''')
        opcao = int(input('Digite uma opcao: '))
        if opcao == 1:
            cadastrar_produtos()
            carregar_dados()
        elif opcao == 2:
            listar_produtos()
        elif opcao == 4:
            print(' """ SAINDO DO MENU """ ')
            break
        elif opcao == 3:
            print(f'O total de produtos e {len(produtos)}')
        elif opcao == 5:
            realizar_vendas()
            carregar_dados()
        elif opcao == 6:
            mostrar_relatorio()
            carregar_dados()

        else:
            print('Opção invalida!')
carregar_dados()
menu()