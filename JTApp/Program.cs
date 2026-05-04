using System;
using System.Collections.Generic;
using System.Linq;
using BCrypt.Net;

namespace JTSystems
{
    // Banco de dados em memória
    public static class Db
    {
        public static List<Cliente> Clientes = new List<Cliente>();
        public static List<Gerente> Gerentes = new List<Gerente>();
        public static List<Loja> Lojas = new List<Loja>();
    }

    // Guarda o usuário logado no menu principal
    public class Program
    {
        private static Usuario you = null;

        public static void MostrarTracinhos(string pos)
        {
            // Controla uma pequena moldura visual do terminal
            if (pos == "0")
                Console.WriteLine();

            Console.WriteLine("-=" + new string('-', 18) + "-");

            if (pos == "1")
                Console.WriteLine();
        }

        public static void LimparTerminal()
        {
            Console.Clear();
        }

        public static void Cadastro()
        {
            LimparTerminal();

            // O tipo escolhido define quais dados extras serão pedidos
            Console.Write("Deseja se cadastrar como gerente (1) ou cliente (2): ");
            string tipo = Console.ReadLine().Trim();
            Console.Write("Digite o seu nome: ");
            string nome = Console.ReadLine().Trim();
            Console.Write("Digite o seu email: ");
            string email = Console.ReadLine().Trim();
            Console.Write("Digite a sua senha: ");
            string senha = Console.ReadLine().Trim();

            if (tipo == "1")
            {
                Console.Write("Digite o seu percentual de bonificacao: ");
                double bonificacao = double.Parse(Console.ReadLine());
                new Gerente(nome, email, senha, bonificacao);
            }
            else
            {
                Console.Write("Digite o seu endereço: ");
                string endereco = Console.ReadLine().Trim();
                Console.Write("Digite o seu saldo inicial: R$");
                double saldo = double.Parse(Console.ReadLine());
                new Cliente(nome, email, senha, endereco, saldo);
            }

            Console.WriteLine("\nCadastro concluído com sucesso, já pode fazer login com suas credenciais");
        }

        public static Usuario Login()
        {
            while (true)
            {
                LimparTerminal();

                Console.Write("Deseja logar como gerente (1) ou cliente (2): ");
                string tipo = Console.ReadLine().Trim();
                Console.Write("Digite o seu email: ");
                string email = Console.ReadLine().Trim();
                Console.Write("Digite a sua senha: ");
                string senha = Console.ReadLine().Trim();

                string categoria = tipo == "1" ? "gerentes" : "clientes";
                Usuario usuarioEncontrado = null;

                // Procura o email dentro do grupo selecionado
                if (categoria == "gerentes")
                {
                    foreach (var usuario in Db.Gerentes)
                    {
                        if (usuario.Email == email && usuario.ValidarSenha(senha))
                        {
                            usuarioEncontrado = usuario;
                            break;
                        }
                    }
                }
                else
                {
                    foreach (var usuario in Db.Clientes)
                    {
                        if (usuario.Email == email && usuario.ValidarSenha(senha))
                        {
                            usuarioEncontrado = usuario;
                            break;
                        }
                    }
                }

                if (usuarioEncontrado == null)
                {
                    Console.WriteLine("Credenciais inválidas, tente novamente: ");
                    Console.ReadLine();
                }
                else
                {
                    return usuarioEncontrado;
                }
            }
        }

        public static Loja BuscarLojaPorGerente(Gerente gerente)
        {
            Loja lojaGerente = null;

            // Se o gerente já tiver loja vinculada, busca o objeto correspondente
            if (gerente.LojaId != null)
            {
                foreach (var loja in Db.Lojas)
                {
                    if (loja.Id == gerente.LojaId)
                    {
                        lojaGerente = loja;
                        break;
                    }
                }
            }

            return lojaGerente;
        }

        public static void VizualizacaoGerente(Gerente you)
        {
            while (true)
            {
                LimparTerminal();
                MostrarTracinhos("0");
                Console.WriteLine($"Olá, {you.Nome}".PadLeft(20 + you.Nome.Length / 2));
                MostrarTracinhos("1");

                Console.WriteLine(@"Qual ação deseja realizar?
1 - Ver/Cadastrar Loja
2 - Gerenciar Produtos
0 - Deslogar");
                Console.Write("Digite aqui: ");
                string acao = Console.ReadLine().Trim();

                switch (acao)
                {
                    case "1":
                        Loja minhaLoja = BuscarLojaPorGerente(you);

                        if (minhaLoja != null)
                        {
                            Console.WriteLine();
                            minhaLoja.MostrarDados();
                        }
                        else
                        {
                            // Caso ainda não exista loja, o gerente pode criar uma na hora
                            Console.WriteLine("\nVocê ainda não possui uma loja, vamos cadastrá-la agora");
                            Console.Write("Digite o nome da sua loja: ");
                            string nome = Console.ReadLine().Trim();
                            Console.Write("Digite o descricao da sua loja: ");
                            string descricao = Console.ReadLine().Trim();
                            Console.Write("Digite o endereco da sua loja: ");
                            string endereco = Console.ReadLine().Trim();
                            Console.Write("Digite o setor da sua loja: ");
                            string setor = Console.ReadLine().Trim();

                            Loja novaLoja = new Loja(nome, descricao, endereco, setor);
                            novaLoja.DefinirGerente(you);
                            you.DefinirLoja(novaLoja);

                            Console.WriteLine();
                            novaLoja.MostrarDados();
                        }

                        Console.Write("\nOk? ");
                        Console.ReadLine();
                        break;
                    case "2":
                        Loja minhaLoja2 = BuscarLojaPorGerente(you);

                        if (minhaLoja2 != null)
                        {
                            minhaLoja2.MenuProdutos();
                        }
                        else
                        {
                            Console.WriteLine("Você não tem loja cadastrada ainda.");
                        }
                        break;
                    case "0":
                        return;
                }
            }
        }

        public static void VizualizacaoCliente(Cliente you)
        {
            while (true)
            {
                LimparTerminal();
                MostrarTracinhos("0");
                Console.WriteLine($"Olá, {you.Nome}".PadLeft(20 + you.Nome.Length / 2));
                MostrarTracinhos("1");

                Console.WriteLine(@"Qual ação deseja realizar?
1 - Ver Saldo
2 - Depositar dinheiro
3 - Sacar dinheiro
4 - Ver lojas
5 - Fazer compras
0 - Deslogar");
                Console.Write("Digite aqui: ");
                string acao = Console.ReadLine().Trim();

                switch (acao)
                {
                    case "1":
                        Console.WriteLine($"\nSeu saldo: R${you.Saldo}");
                        Console.Write("\nOk? ");
                        Console.ReadLine();
                        break;
                    case "2":
                        while (true)
                        {
                            try
                            {
                                Console.Write("\nDigite o valor a ser depositado: R$");
                                double dep = double.Parse(Console.ReadLine());
                                you.DepositarSaldo(dep);
                                Console.Write("\nDepósito realizado, Ok? ");
                                Console.ReadLine();
                                break;
                            }
                            catch (Exception e)
                            {
                                if (e is ArgumentException)
                                    Console.WriteLine(e.Message);
                                Console.WriteLine("Digite um valor válido.");
                            }
                        }
                        break;
                    case "3":
                        while (true)
                        {
                            try
                            {
                                Console.Write("\nDigite o valor a ser sacado: R$");
                                double sac = double.Parse(Console.ReadLine());
                                you.SacarSaldo(sac);
                                Console.Write("\nSaque realizado, Ok? ");
                                Console.ReadLine();
                                break;
                            }
                            catch (Exception e)
                            {
                                if (e is ArgumentException)
                                    Console.WriteLine(e.Message);
                                Console.WriteLine("Digite um valor válido.");
                            }
                        }
                        break;
                    case "4":
                        foreach (var loja in Db.Lojas)
                        {
                            Console.WriteLine();
                            loja.MostrarDados();
                        }
                        Console.Write("\nOK? ");
                        Console.ReadLine();
                        break;
                    case "5":
                        while (true)
                        {
                            // Primeiro o cliente escolhe em qual loja deseja comprar
                            foreach (var loja in Db.Lojas)
                            {
                                Console.WriteLine();
                                loja.MostrarDados();
                            }

                            Console.Write("\nDigite o id da loja que você deseja fazer compras (0 para sair): ");
                            string idBusca = Console.ReadLine().Trim();

                            if (idBusca == "0")
                                break;

                            Loja lojaCompras = null;
                            foreach (var loja in Db.Lojas)
                            {
                                if (loja.Id == idBusca)
                                {
                                    lojaCompras = loja;
                                }
                            }

                            if (lojaCompras == null)
                            {
                                LimparTerminal();
                                Console.WriteLine("\nNão foi encontrado nenhuma loja com esse Id\n");
                                continue;
                            }

                            bool compraFinalizada = false;

                            while (true)
                            {
                                // Depois escolhe um produto daquela loja
                                foreach (var produto in lojaCompras.Produtos)
                                {
                                    Console.WriteLine();
                                    produto.MostrarDados();
                                }

                                Console.Write("\nDigite o Id do produto que deseja comprar (0 para sair): ");
                                string idProduto = Console.ReadLine().Trim();

                                if (idProduto == "0")
                                    break;

                                Produto produtoCompra = null;
                                foreach (var produto in lojaCompras.Produtos)
                                {
                                    if (produto.Id == idProduto)
                                    {
                                        produtoCompra = produto;
                                    }
                                }

                                if (produtoCompra == null)
                                {
                                    LimparTerminal();
                                    Console.WriteLine("\nNão foi encontrado nenhum produto com esse Id\n");
                                    continue;
                                }

                                Console.Write("Digite a quantidade que você deseja comprar: ");
                                int quantidade = int.Parse(Console.ReadLine());

                                if (quantidade <= 0)
                                {
                                    LimparTerminal();
                                    Console.WriteLine("\nDigite uma quantidade válida\n");
                                    continue;
                                }
                                else if (quantidade > produtoCompra.Quantidade)
                                {
                                    LimparTerminal();
                                    Console.WriteLine("\nNão possui essa quantidade em estoque\n");
                                    continue;
                                }

                                double precoTotal = produtoCompra.Preco * quantidade;

                                try
                                {
                                    // O saldo é descontado antes de atualizar o estoque
                                    you.SacarSaldo(precoTotal);
                                    produtoCompra.Quantidade -= quantidade;
                                }
                                catch (ArgumentException e)
                                {
                                    LimparTerminal();
                                    Console.WriteLine(e.Message);
                                    continue;
                                }

                                compraFinalizada = true;
                                break;
                            }

                            if (compraFinalizada)
                            {
                                Console.Write("Compra finalizada com sucesso, ok? ");
                                Console.ReadLine();
                                break;
                            }
                        }
                        break;
                    case "0":
                        return;
                }
            }
        }

        public static void Main(string[] args)
        {
            // Dados iniciais para facilitar os testes do sistema
            Gerente g1 = new Gerente("Carlos Silva", "carlos@empresa.com", "1234", 0.1);
            Gerente g2 = new Gerente("Ana Souza", "ana@empresa.com", "1234", 0.15);

            Cliente c1 = new Cliente("João", "joao@email.com", "1234", "Rua A", 1000);
            Cliente c2 = new Cliente("Maria", "maria@email.com", "1234", "Rua B", 500);

            Loja l1 = new Loja("Loja Centro", "Eletrônicos", "Centro", "Tecnologia");
            Loja l2 = new Loja("Loja Norte", "Roupas", "Zona Norte", "Vestuário");

            l1.Produtos.AddRange(new List<Produto>
            {
                new Produto("Notebook", 3500.00, 10),
                new Produto("Mouse", 80.00, 25),
                new Produto("Teclado", 150.00, 15)
            });

            l2.Produtos.AddRange(new List<Produto>
            {
                new Produto("Camiseta", 59.90, 30),
                new Produto("Calça Jeans", 129.90, 20),
                new Produto("Jaqueta", 199.90, 12)
            });

            l1.DefinirGerente(g1);
            g1.DefinirLoja(l1);

            l2.DefinirGerente(g2);
            g2.DefinirLoja(l2);

            while (true)
            {
                try
                {
                    LimparTerminal();

                    MostrarTracinhos("0");
                    Console.WriteLine("JT SYSTEMS".PadLeft(20 + "JT SYSTEMS".Length / 2));
                    MostrarTracinhos("1");

                    Console.WriteLine(@"Qual ação deseja realizar?
1 - Cadastro
2 - Login
3 - Ver Lojas
0 - Sair");
                    Console.Write("Digite aqui: ");
                    string acao = Console.ReadLine().Trim();

                    switch (acao)
                    {
                        case "1":
                            Cadastro();
                            break;
                        case "2":
                            you = Login();
                            Console.WriteLine("\nSeus dados: ");
                            you.MostrarDados();
                            Console.Write("\nOK? ");
                            Console.ReadLine();

                            // Cada tipo de usuário segue para o seu próprio menu
                            if (you is Gerente)
                            {
                                VizualizacaoGerente((Gerente)you);
                            }
                            else
                            {
                                VizualizacaoCliente((Cliente)you);
                            }

                            // Ao sair do menu, o usuário deixa de estar logado
                            you = null;
                            break;
                        case "3":
                            foreach (var loja in Db.Lojas)
                            {
                                Console.WriteLine();
                                loja.MostrarDados();
                            }
                            Console.Write("\nOK? ");
                            Console.ReadLine();
                            break;
                        case "0":
                            return;
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine("Erro: " + e.Message);
                    Console.ReadLine();
                }
            }
        }
    }

    public class Usuario
    {
        public string Nome { get; set; }
        public string Email { get; set; }
        public string Senha { get; set; } // A senha é salva apenas em formato criptografado
        public string Id { get; set; }

        public Usuario(string nome, string email, string senha)
        {
            Nome = nome;
            Email = email;
            Senha = BCrypt.Net.BCrypt.HashPassword(senha);
            Id = Guid.NewGuid().ToString();
        }

        public bool ValidarSenha(string senhaFornecida)
        {
            return BCrypt.Net.BCrypt.Verify(senhaFornecida, Senha);
        }

        public virtual void MostrarDados()
        {
            Console.WriteLine($"Id: {Id}");
            Console.WriteLine($"Nome: {Nome}");
            Console.WriteLine($"Email: {Email}");
        }
    }

    public class Cliente : Usuario
    {
        public string Endereco { get; set; }
        public double Saldo { get; set; }

        public Cliente(string nome, string email, string senha, string endereco, double saldo)
            : base(nome, email, senha)
        {
            Endereco = endereco;
            Saldo = saldo;
            Db.Clientes.Add(this);
        }

        public void DepositarSaldo(double dep)
        {
            // Impede depósitos inválidos
            if (dep < 0)
                throw new ArgumentException("Depósito não pode ser negativo");

            Saldo += dep;
        }

        public void SacarSaldo(double sac)
        {
            // Valida o saque antes de alterar o saldo
            if (sac < 0)
                throw new ArgumentException("Saque não pode ser negativo");
            if (sac > Saldo)
                throw new ArgumentException("Você não tem esse dinherio para sacar.");

            Saldo -= sac;
        }

        public override void MostrarDados()
        {
            Console.WriteLine($"Id: {Id}");
            Console.WriteLine($"Nome: {Nome}");
            Console.WriteLine($"Email: {Email}");
            Console.WriteLine($"Endereço: {Endereco}");
            Console.WriteLine($"Saldo: {Saldo}");
        }
    }

    public class Loja
    {
        public string Nome { get; set; }
        public string Descricao { get; set; }
        public string Endereco { get; set; }
        public string Setor { get; set; }
        public string Id { get; set; }
        public List<Produto> Produtos { get; set; }
        public string GerenteId { get; set; }

        public Loja(string nome, string descricao, string endereco, string setor)
        {
            Nome = nome;
            Descricao = descricao;
            Endereco = endereco;
            Setor = setor;
            Id = Guid.NewGuid().ToString();
            Produtos = new List<Produto>();
            // Toda loja criada já entra no banco em memória
            Db.Lojas.Add(this);
        }

        public void DefinirGerente(Gerente gerente)
        {
            if (!(gerente is Gerente))
                throw new ArgumentException("Deve ser um gerente");
            GerenteId = gerente.Id;
        }

        public void AddProduto()
        {
            Console.WriteLine("\n ---Adicionar Produto---");
            Console.Write("Digite o Nome do Produto: ");
            string nome = Console.ReadLine().Trim();
            Console.Write("Preço: R$");
            double preco = double.Parse(Console.ReadLine());
            Console.Write("Quantidade em estoque: ");
            int quantidade = int.Parse(Console.ReadLine());

            // Cria o produto e adiciona ao estoque da loja
            Produto novoProduto = new Produto(nome, preco, quantidade);
            Produtos.Add(novoProduto);

            Console.WriteLine("\n");
            Console.WriteLine($"Produto {nome} foi adicionado com sucesso!");
        }

        public void RemoverProduto(string id)
        {
            // Mantém apenas os produtos com id diferente do informado
            Produtos = Produtos.Where(produto => produto.Id != id).ToList();
        }

        public void ListarTodos()
        {
            if (Produtos.Count == 0)
            {
                Console.WriteLine("\n");
                Console.WriteLine("Ops! Nenhum Produto Encontrado!!!");
                return;
            }

            Console.WriteLine("\n" + new string('=', 60));
            Console.WriteLine("LISTA DE PRODUTOS CADASTRADOS");
            Console.WriteLine(new string('=', 60));

            foreach (var produto in Produtos)
            {
                Console.WriteLine(
                    $"ID: {produto.Id} | Produto: {produto.Nome} | " +
                    $"Valor R${produto.Preco:F2} | Estoque: {produto.Quantidade}"
                );
            }

            Console.Write("Ok? ");
            Console.ReadLine();
        }

        public void BuscarProduto()
        {
            if (Produtos.Count == 0)
            {
                Console.WriteLine("\n");
                Console.WriteLine("Nenhum Produto Foi Encontrado!");
                Console.WriteLine("\n");
            }

            Console.Write("Digite o Nome do Produto ");
            string termoBusca = Console.ReadLine().Trim().ToLower();
            // Busca parcial pelo nome do produto
            var encontrados = Produtos.Where(produto => produto.Nome.ToLower().Contains(termoBusca)).ToList();

            if (encontrados.Count == 0)
            {
                Console.WriteLine("\n" + new string('~', 60));
                Console.WriteLine($"Nenhum produto encontrado no nome {termoBusca}");
                Console.WriteLine(new string('~', 60));
            }
            else
            {
                Console.WriteLine($"\n ---Iten encontrado no nome {termoBusca}---");
            }

            foreach (var produto in encontrados)
            {
                Console.WriteLine(
                    $"ID: {produto.Id} | Produto: {produto.Nome} | " +
                    $"Valor R${produto.Preco:F2} | Estoque: {produto.Quantidade}"
                );
            }
        }

        public void ListarPreco()
        {
            if (Produtos.Count == 0)
            {
                Console.WriteLine("\n");
                Console.WriteLine("Nenhum Produto cadastrado!!");
                return;
            }

            try
            {
                Console.Write("Digite o preço Minimo: R$");
                double minpreco = double.Parse(Console.ReadLine());
                Console.Write("Digite o preço Maximo: R$");
                double maxpreco = double.Parse(Console.ReadLine());

                // Filtra os itens dentro da faixa informada
                var filtrados = Produtos
                    .Where(produto => minpreco <= produto.Preco && produto.Preco <= maxpreco)
                    .ToList();

                if (filtrados.Count == 0)
                {
                    Console.WriteLine($"Nenhum item encontrado entre o valor R${minpreco:F2} e R${maxpreco:F2}");
                    return;
                }

                Console.WriteLine($"Produtos encontrados Entre os valores R${minpreco} e R${maxpreco}");
                foreach (var produto in filtrados)
                {
                    Console.WriteLine(
                        $"ID: {produto.Id} | Produto: {produto.Nome} | " +
                        $"Valor R${produto.Preco:F2} | Estoque: {produto.Quantidade}"
                    );
                }
            }
            catch (FormatException)
            {
                Console.WriteLine("Preço Invalidos!");
            }
        }

        public void MenuProdutos()
        {
            while (true)
            {
                Console.WriteLine("\n" + new string('=', 40));
                Console.WriteLine("==Sistema de Produto==");
                Console.WriteLine(new string('=', 40));
                Console.WriteLine("1 - Adicionar Produto");
                Console.WriteLine("2 - Listar Todos os Produtos");
                Console.WriteLine("3 - Listar pelo Nome Produto");
                Console.WriteLine("4 - Listar pelo Preço Produto");
                Console.WriteLine("0 - Sair do Sistema");

                Console.Write("\n Escolha Uma Opção: ");
                string opcao = Console.ReadLine().Trim();

                if (opcao == "1")
                {
                    AddProduto();
                }
                else if (opcao == "2")
                {
                    ListarTodos();
                }
                else if (opcao == "3")
                {
                    BuscarProduto();
                }
                else if (opcao == "4")
                {
                    ListarPreco();
                }
                else if (opcao == "0")
                {
                    break;
                }
                else
                {
                    Console.WriteLine("\n");
                    Console.WriteLine("Opção Invalida!");
                }
            }
        }

        public void MostrarDados()
        {
            Console.WriteLine($"Id: {Id}");
            Console.WriteLine($"Nome: {Nome}");
            Console.WriteLine($"Descricao: {Descricao}");
            Console.WriteLine($"Endereco: {Endereco}");
            Console.WriteLine($"Setor: {Setor}");
        }
    }

    public class Gerente : Usuario
    {
        public double Bonificacao { get; set; }
        public string LojaId { get; set; }

        public Gerente(string nome, string email, string senha, double bonificacao)
            : base(nome, email, senha)
        {
            Bonificacao = bonificacao;
            LojaId = null;
            // Todo gerente criado já fica disponível para login
            Db.Gerentes.Add(this);
        }

        public void DefinirLoja(Loja loja)
        {
            if (!(loja is Loja))
                throw new ArgumentException("Deve ser uma loja");
            LojaId = loja.Id;
        }

        public override void MostrarDados()
        {
            Console.WriteLine($"Id: {Id}");
            Console.WriteLine($"Nome: {Nome}");
            Console.WriteLine($"Email: {Email}");
            Console.WriteLine($"Loja Id: {LojaId}");
        }
    }

    public class Produto
    {
        public string Nome { get; set; }
        public double Preco { get; set; }
        public int Quantidade { get; set; }
        public string Id { get; set; }

        public Produto(string nome, double preco, int quantidade)
        {
            Nome = nome;
            Preco = preco;
            Quantidade = quantidade;
            Id = Guid.NewGuid().ToString();
        }

        public void MostrarDados()
        {
            Console.WriteLine($"Id: {Id}");
            Console.WriteLine($"Nome: {Nome}");
            Console.WriteLine($"Preço: {Preco}");
            Console.WriteLine($"Quantidade: {Quantidade}");
        }
    }
}