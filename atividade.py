import bcrypt
from uuid import uuid4
import os

db = {
    "clientes": [],
    "gerentes": [],
    "lojas": []
}

you = None

class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        salt = bcrypt.gensalt()
        senha_hash = bcrypt.hashpw(senha.encode(), salt)
        self.senha = senha_hash
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
        if dep < 0:
            raise ValueError("Depósito não pode ser negativo")
        
        self.saldo += dep

    def sacar_saldo(self, sac):
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
        db["lojas"].append(self)

    def definir_gerente(self, gerente):
        if not isinstance(gerente, Gerente):
            raise TypeError("Deve ser um gerente")
        self.gerente_id = gerente.id

    def mostrar_dados(self):
        print(f"Id: {self.id}")
        print(f"Nome: {self.nome}")
        print(f"Descricao: {self.descricao}")
        print(f"Endereco: {self.endereco}")
        print(f"Setor: {self.setor}")
    
class Gerente(Usuario):
    def __init__(self, nome, email, senha, bonificacao):
        super().__init__(nome, email, senha)
        self.bonificacao = bonificacao
        self.loja_id = None
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

# ===== DADOS INICIAIS =====

# Gerentes
g1 = Gerente("Carlos Silva", "carlos@empresa.com", "1234", 0.1)
g2 = Gerente("Ana Souza", "ana@empresa.com", "1234", 0.15)

# Clientes
c1 = Cliente("João", "joao@email.com", "1234", "Rua A", 1000)
c2 = Cliente("Maria", "maria@email.com", "1234", "Rua B", 500)

# Lojas
l1 = Loja("Loja Centro", "Eletrônicos", "Centro", "Tecnologia")
l2 = Loja("Loja Norte", "Roupas", "Zona Norte", "Vestuário")

# Relacionamentos
l1.definir_gerente(g1)
g1.definir_loja(l1)

l2.definir_gerente(g2)
g2.definir_loja(l2)  

def mostrar_tracinhos(pos):
    if str(pos) == '0':
        print()
    print("-=" * 20 + '-')
    if str(pos) == '1':
        print()

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def cadastro():
    limpar_terminal()
    tipo = input("Deseja se cadastrar como gerente (1) ou cliente (2): ")
    nome = input("Digite o seu nome: ")
    email = input("Digite o seu email: ")
    senha = input("Digite a sua senha: ")
    if tipo == '1':
        bonificacao = float(input("Digite o seu percentual de bonificacao: "))
        Gerente(nome, email, senha, bonificacao)
    else:
        endereco = input("Digite o seu endereço: ")
        saldo = float(input("Digite o seu saldo inicial: R$"))
        Cliente(nome, email, senha, endereco, saldo)

    print("\nCadastro concluído com sucesso, já pode fazer login com suas credenciais")

def login():
    while True: 
        limpar_terminal()
        tipo = input("Deseja logar como gerente (1) ou cliente (2): ")
        email = input("Digite o seu email: ")
        senha = input("Digite a sua senha: ")
        busca = None
        for usuario in db["gerentes" if tipo == '1' else "clientes"]:
            if usuario.email == email:
                if usuario.validar_senha(senha):
                    busca = usuario
                    break
        if busca is None:
            print("Credenciais inválidas, tente novamente: ")
            input()
        else:
            return busca

def buscar_loja_por_gerente(gerente):
    loja_gerente = None
    if gerente.loja_id != None:
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

        print("""Qual ação deseja realizar?
1 - Ver/Cadastrar Loja
2 - Ver Produtos
3 - Adicionar Produto
4 - Remover Produto
0 - Deslogar""")
        acao = input("Digite aqui: ")

        match acao:
            case "1":
                minha_loja = buscar_loja_por_gerente(you)

                if minha_loja != None:
                    print()
                    minha_loja.mostrar_dados()
                else:
                    print("\nVocê ainda não possui uma loja, vamos cadastrá-la agora")
                    nome = input("Digite o nome da sua loja: ")
                    descricao = input("Digite o descricao da sua loja: ")
                    endereco = input("Digite o endereco da sua loja: ")
                    setor = input("Digite o setor da sua loja: ")
                    nova_loja = Loja(nome, descricao, endereco, setor)
                    nova_loja.definir_gerente(you)
                    you.definir_loja(nova_loja)
                    print()
                    nova_loja.mostrar_dados()
                input("\nOk? ")
            case '2':
                input("Em desenvolvimento")
            case '3':
                input("Em desenvolvimento")
            case '4':
                input("Em desenvolvimento")
            case "0":
                break

def vizualizacao_cliente(you):
    while True:
        limpar_terminal()
        mostrar_tracinhos(0)
        print(f"Olá, {you.nome}".center(40))
        mostrar_tracinhos(1)

        print("""Qual ação deseja realizar?
1 - Ver Saldo
2 - Depositar dinheiro
3 - Sacar dinheiro
4 - Ver lojas
5 - Fazer compras
0 - Deslogar""")
        acao = input("Digite aqui: ")

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
                input("Em desenvolvimento")
            case "0":
                break

while True:
    try:
        limpar_terminal()

        mostrar_tracinhos(0)
        print("JT SYSTEMS".center(40))
        mostrar_tracinhos(1)

        print("""Qual ação deseja realizar?
1 - Cadastro
2 - Login
3 - Ver Lojas
0 - Sair""")
        acao = input("Digite aqui: ")

        match acao:
            case "1":
                cadastro()
            case "2":
                you = login()
                print("\nSeus dados: ")
                you.mostrar_dados()
                input("\nOK? ")
                if isinstance(you, Gerente):
                    vizualizacao_gerente(you)
                else:
                    vizualizacao_cliente(you)
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
