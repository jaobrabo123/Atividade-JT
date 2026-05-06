import os
from uuid import uuid4

import bcrypt


db = {
    "clientes": [],
    "gerentes": [],
    "lojas": [],
}

# Guarda o usuário logado no menu principal.
you = None

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        # A senha é salva apenas em formato criptografado.
        self.senha = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())
        self.id = str(uuid4())

    def validar_senha(self, senha_fornecida):
        return bcrypt.checkpw(senha_fornecida.encode(), self.senha)

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")

class Cliente(Usuario):
    def __init__(self, nome, email, senha, endereco, saldo):
        super().__init__(nome, email, senha)
        self.endereco = endereco
        self.saldo = saldo
        db["clientes"].append(self)

    def depositar_saldo(self, dep):
        # Impede depósitos inválidos.
        if dep < 0:
            raise ValueError("Depósito não pode ser negativo")

        self.saldo += dep

    def sacar_saldo(self, sac):
        # Valida o saque antes de alterar o saldo.
        if sac < 0:
            raise ValueError("Saque não pode ser negativo")
        if sac > self.saldo:
            raise ValueError("Você não tem esse dinherio para sacar.")

        self.saldo -= sac

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")
        print(f"Endereço: {self.endereco}")
        print(f"Saldo: {self.saldo}")


class Loja:
    def __init__(self, nome, descricao, endereco, setor):
        self.nome = nome
        self.descricao = descricao
        self.endereco = endereco
        self.setor = setor
        self.id = str(uuid4())
        self.produtos = []
        # Toda loja criada já entra no banco em memória.
        db["lojas"].append(self)

    def definir_gerente(self, gerente):
        if not isinstance(gerente, Gerente):
            raise TypeError("Deve ser um gerente")
        self.gerente_id = gerente.id

    def addproduto(self):
        print("\n ---Adicionar Produto---")
        nome = input("Digite o Nome do Produto: ").strip()
        preco = float(input("Preço: R$"))
        quantidade = int(input("Quantidade em estoque: "))

        # Cria o produto e adiciona ao estoque da loja.
        novo_produto = Produto(nome, preco, quantidade)
        self.produtos.append(novo_produto)

        print("\n")
        print(f"Produto {nome} foi adicionado com sucesso!")

    def remover_produto(self, id):
        # Mantém apenas os produtos com id diferente do informado.
        self.produtos = [produto for produto in self.produtos if produto.id != id]

    def listarTodos(self):
        if not self.produtos:
            print("\n")
            print("Ops! Nenhum Produto Encontrado!!!")
            return

        print("\n" + "=" * 60)
        print("LISTA DE PRODUTOS CADASTRADOS")
        print("=" * 60)

        for produto in self.produtos:
            print(
                f"ID: {produto.id} | Produto: {produto.nome} | "
                f"Valor R${produto.preco:.2f} | Estoque: {produto.quantidade}"
            )

        input("Ok? ")

    def buscarproduto(self):
        if not self.produtos:
            print("\n")
            print("Nenhum Produto Foi Encontrado!")
            print("\n")

        termo_busca = input("Digite o Nome do Produto ").strip().lower()
        # Busca parcial pelo nome do produto.
        encontrados = [produto for produto in self.produtos if termo_busca in produto.nome.lower()]

        if not encontrados:
            print("\n" + "~" * 60)
            print(f"Nenhum produto encontrado no nome {termo_busca}")
            print("~" * 60)
        else:
            print(f"\n ---Iten encontrado no nome {termo_busca}---")

        for produto in encontrados:
            print(
                f"ID: {produto.id} | Produto: {produto.nome} | "
                f"Valor R${produto.preco:.2f} | Estoque: {produto.quantidade}"
            )

    def listarpreco(self):
        if not self.produtos:
            print("\n")
            print("Nenhum Produto cadastrado!!")
            return

        try:
            minpreco = float(input("Digite o preço Minimo: R$"))
            maxpreco = float(input("Digite o preço Maximo: R$"))

            # Filtra os itens dentro da faixa informada.
            filtrados = [
                produto
                for produto in self.produtos
                if minpreco <= produto.preco <= maxpreco
            ]

            if not filtrados:
                print(f"Nenhum item encontrado entre o valor R${minpreco:.2f} e R${maxpreco:.2f}")
                return

            print(f"Produtos encontrados Entre os valores R${minpreco} e R${maxpreco}")
            for produto in filtrados:
                print(
                    f"ID: {produto.id} | Produto: {produto.nome} | "
                    f"Valor R${produto.preco:.2f} | Estoque: {produto.quantidade}"
                )
        except ValueError:
            print("Preço Invalidos!")

    def menu_produtos(self):
        while True:
            print("\n" + "=" * 40)
            print("==Sistema de Produto==")
            print("=" * 40)
            print("1 - Adicionar Produto")
            print("2 - Listar Todos os Produtos")
            print("3 - Listar pelo Nome Produto")
            print("4 - Listar pelo Preço Produto")
            print("0 - Sair do Sistema")

            opcao = input("\n Escolha Uma Opção: ").strip()

            if opcao == "1":
                self.addproduto()
            elif opcao == "2":
                self.listarTodos()
            elif opcao == "3":
                self.buscarproduto()
            elif opcao == "4":
                self.listarpreco()
            elif opcao == "0":
                break
            else:
                print("\n")
                print("Opção Invalida!")

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Descricao: {self.descricao}")
        print(f"Endereco: {self.endereco}")
        print(f"Setor: {self.setor}")

class Gerente(Usuario):
    def __init__(self, nome, email, senha):
        super().__init__(nome, email, senha)
        self.loja_id = None
        # Todo gerente criado já fica disponível para login.
        db["gerentes"].append(self)

    def definir_loja(self, loja):
        if not isinstance(loja, Loja):
            raise TypeError("Deve ser uma loja")
        self.loja_id = loja.id

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Email: {self.email}")
        print(f"Loja Id: {self.loja_id}")

class Produto:
    def __init__(self, nome, preco, quantidade):
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.id = str(uuid4())

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Preço: {self.preco}")
        print(f"Quantidade: {self.quantidade}")


# Dados iniciais para facilitar os testes do sistema.
g1 = Gerente("Carlos Silva", "carlos@empresa.com", "1234", 0.1)
g2 = Gerente("Ana Souza", "ana@empresa.com", "1234", 0.15)

c1 = Cliente("João", "joao@email.com", "1234", "Rua A", 1000)
c2 = Cliente("Maria", "maria@email.com", "1234", "Rua B", 500)

l1 = Loja("Loja Centro", "Eletrônicos", "Centro", "Tecnologia")
l2 = Loja("Loja Norte", "Roupas", "Zona Norte", "Vestuário")

l1.produtos.extend(
    [
        Produto("Notebook", 3500.00, 10),
        Produto("Mouse", 80.00, 25),
        Produto("Teclado", 150.00, 15),
    ]
)

l2.produtos.extend(
    [
        Produto("Camiseta", 59.90, 30),
        Produto("Calça Jeans", 129.90, 20),
        Produto("Jaqueta", 199.90, 12),
    ]
)

l1.definir_gerente(g1)
g1.definir_loja(l1)

l2.definir_gerente(g2)
g2.definir_loja(l2)


def mostrar_tracinhos(pos):
    # Controla uma pequena moldura visual do terminal.
    if str(pos) == "0":
        print()

    print("-=" * 20 + "-")

    if str(pos) == "1":
        print()


def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def cadastro():
    limpar_terminal()

    # O tipo escolhido define quais dados extras serão pedidos.
    tipo = input("Deseja se cadastrar como gerente (1) ou cliente (2): ").strip()
    nome = input("Digite o seu nome: ").strip()
    email = input("Digite o seu email: ").strip()
    senha = input("Digite a sua senha: ").strip()

    if tipo == "1":
        Gerente(nome, email, senha)
    else:
        endereco = input("Digite o seu endereço: ").strip()
        saldo = float(input("Digite o seu saldo inicial: R$"))
        Cliente(nome, email, senha, endereco, saldo)

    print("\nCadastro concluído com sucesso, já pode fazer login com suas credenciais")


def login():
    while True:
        limpar_terminal()

        tipo = input("Deseja logar como gerente (1) ou cliente (2): ").strip()
        email = input("Digite o seu email: ").strip()
        senha = input("Digite a sua senha: ").strip()

        categoria = "gerentes" if tipo == "1" else "clientes"
        usuario_encontrado = None

        # Procura o email dentro do grupo selecionado.
        for usuario in db[categoria]:
            if usuario.email == email and usuario.validar_senha(senha):
                usuario_encontrado = usuario
                break

        if usuario_encontrado is None:
            print("Credenciais inválidas, tente novamente: ")
            input()
        else:
            return usuario_encontrado


def buscar_loja_por_gerente(gerente):
    loja_gerente = None

    # Se o gerente já tiver loja vinculada, busca o objeto correspondente.
    if gerente.loja_id is not None:
        for loja in db["lojas"]:
            if loja.id == gerente.loja_id:
                loja_gerente = loja
                break

    return loja_gerente


def vizualizacao_gerente(you):
    while True:
        limpar_terminal()
        mostrar_tracinhos(0)
        print(f"Olá, {you.nome}".center(40))
        mostrar_tracinhos(1)

        print(
"""Qual ação deseja realizar?
1 - Ver/Cadastrar Loja
2 - Gerenciar Produtos
0 - Deslogar"""
        )
        acao = input("Digite aqui: ").strip()

        match acao:
            case "1":
                minha_loja = buscar_loja_por_gerente(you)

                if minha_loja is not None:
                    print()
                    minha_loja.mostrar_dados()
                else:
                    # Caso ainda não exista loja, o gerente pode criar uma na hora.
                    print("\nVocê ainda não possui uma loja, vamos cadastrá-la agora")
                    nome = input("Digite o nome da sua loja: ").strip()
                    descricao = input("Digite o descricao da sua loja: ").strip()
                    endereco = input("Digite o endereco da sua loja: ").strip()
                    setor = input("Digite o setor da sua loja: ").strip()

                    nova_loja = Loja(nome, descricao, endereco, setor)
                    nova_loja.definir_gerente(you)
                    you.definir_loja(nova_loja)

                    print()
                    nova_loja.mostrar_dados()

                input("\nOk? ")
            case "2":
                minha_loja = buscar_loja_por_gerente(you)

                if minha_loja:
                    minha_loja.menu_produtos()
                else:
                    print("Você não tem loja cadastrada ainda.")
            case "0":
                break


def vizualizacao_cliente(you):
    while True:
        limpar_terminal()
        mostrar_tracinhos(0)
        print(f"Olá, {you.nome}".center(40))
        mostrar_tracinhos(1)

        print(
"""Qual ação deseja realizar?
1 - Ver Saldo
2 - Depositar dinheiro
3 - Sacar dinheiro
4 - Ver lojas
5 - Fazer compras
0 - Deslogar"""
        )
        acao = input("Digite aqui: ").strip()

        match acao:
            case "1":
                print(f"\nSeu saldo: R${you.saldo}")
                input("\nOk? ")
            case "2":
                while True:
                    try:
                        dep = float(input("\nDigite o valor a ser depositado: R$"))
                        you.depositar_saldo(dep)
                        input("\nDepósito realizado, Ok? ")
                        break
                    except Exception as e:
                        if isinstance(e, ValueError):
                            print(e)
                        print("Digite um valor válido.")
            case "3":
                while True:
                    try:
                        sac = float(input("\nDigite o valor a ser sacado: R$"))
                        you.sacar_saldo(sac)
                        input("\nSaque realizado, Ok? ")
                        break
                    except Exception as e:
                        if isinstance(e, ValueError):
                            print(e)
                        print("Digite um valor válido.")
            case "4":
                for loja in db["lojas"]:
                    print()
                    loja.mostrar_dados()
                input("\nOK? ")
            case "5":
                while True:
                    # Primeiro o cliente escolhe em qual loja deseja comprar.
                    for loja in db["lojas"]:
                        print()
                        loja.mostrar_dados()

                    id_busca = input(
                        "\nDigite o id da loja que você deseja fazer compras (0 para sair): "
                    ).strip()

                    if id_busca == "0":
                        break

                    loja_compras = None
                    for loja in db["lojas"]:
                        if loja.id == id_busca:
                            loja_compras = loja

                    if loja_compras is None:
                        limpar_terminal()
                        print("\nNão foi encontrado nenhuma loja com esse Id\n")
                        continue

                    compra_finalizada = False

                    while True:
                        # Depois escolhe um produto daquela loja.
                        for produto in loja_compras.produtos:
                            print()
                            produto.mostrar_dados()

                        id_produto = input(
                            "\nDigite o Id do produto que deseja comprar (0 para sair): "
                        ).strip()

                        if id_produto == "0":
                            break

                        produto_compra = None
                        for produto in loja_compras.produtos:
                            if produto.id == id_produto:
                                produto_compra = produto

                        if produto_compra is None:
                            limpar_terminal()
                            print("\nNão foi encontrado nenhum produto com esse Id\n")
                            continue

                        quantidade = int(input("Digite a quantidade que você deseja comprar: "))

                        if quantidade <= 0:
                            limpar_terminal()
                            print("\nDigite uma quantidade válida\n")
                            continue
                        elif quantidade > produto_compra.quantidade:
                            limpar_terminal()
                            print("\nNão possui essa quantidade em estoque\n")
                            continue

                        preco_total = produto_compra.preco * quantidade

                        try:
                            # O saldo é descontado antes de atualizar o estoque.
                            you.sacar_saldo(preco_total)
                            produto.quantidade -= quantidade
                        except ValueError as e:
                            limpar_terminal()
                            print(e)
                            continue

                        compra_finalizada = True
                        break

                    if compra_finalizada:
                        input("Compra finalizada com sucesso, ok? ").strip()
                        break
            case "0":
                break


while True:
    try:
        limpar_terminal()

        mostrar_tracinhos(0)
        print("INOVA SYSTEMS".center(40))
        mostrar_tracinhos(1)

        print(
"""Qual ação deseja realizar?
1 - Cadastro
2 - Login
3 - Ver Lojas
0 - Sair"""
        )
        acao = input("Digite aqui: ").strip()

        match acao:
            case "1":
                cadastro()
            case "2":
                you = login()
                print("\nSeus dados: ")
                you.mostrar_dados()
                input("\nOK? ")

                # Cada tipo de usuário segue para o seu próprio menu.
                if isinstance(you, Gerente):
                    vizualizacao_gerente(you)
                else:
                    vizualizacao_cliente(you)

                # Ao sair do menu, o usuário deixa de estar logado.
                you = None
            case "3":
                for loja in db["lojas"]:
                    print()
                    loja.mostrar_dados()
                input("\nOK? ")
            case "0":
                break
    except Exception as e:
        print("Erro:", e)
        input()
