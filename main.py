import mysql.connector

def cadastrar_cliente():
    # 1. Coleta os dados do usuário
    nome = input("Nome do cliente: ")
    endereco = input("Endereço: ")
    cpf = input("CPF: ")
    telefone = input("Telefone: ")

    try:
        # 2. Conecta ao banco de dados MySQL
        conexao = mysql.connector.connect(
            host="localhost",       # Onde o banco está rodando
            user="root",            # Usuário do banco (geralmente 'root')
            password="@HitoriSan123",   # Substitua pela senha real
            database="estacionamento" # Nome do banco que você criou
        )

        # 3. Cria o cursor (o "garçom")
        cursor = conexao.cursor()

        # 4. Prepara o comando SQL para inserir os dados
        comando = """
            INSERT INTO cliente (nome, endereco, cpf, telefone)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, endereco, cpf, telefone)

        # 5. Executa o comando
        cursor.execute(comando, valores)

        # 6. Confirma a inserção no banco de dados
        conexao.commit()

        print("✅ Cliente cadastrado com sucesso!")

    except mysql.connector.Error as erro:
        print("Erro ao cadastrar cliente:", erro)

    finally:
        # 7. Fecha o cursor e a conexão
        cursor.close()
        conexao.close()



    # input() para coletar dados
    # INSERT no banco

def cadastrar_veiculo():
    marca = input("Digite a marca do veículo: ")
    modelo = input("Digite o modelo do veículo: ")
    ano = input("Qual o ano do veículo: ")
    placa = input("Número da placa do veículo: ")

    # Aqui pedimos o ID do cliente responsável pelo veículo
    cliente_id = input("ID do cliente proprietário: ")

    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@HitoriSan123",  # substitua pela sua senha real
            database="estacionamento"
        )

        cursor = conexao.cursor()

        comando = """
            INSERT INTO veiculo (marca, modelo, ano, placa, cliente_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (marca, modelo, ano, placa, cliente_id)

        cursor.execute(comando, valores)
        conexao.commit()  # estava errado no seu código: era cursor.commit()

        print("✅ Veículo cadastrado com sucesso!")

    except mysql.connector.Error as erro:
        print("Erro ao cadastrar veículo:", erro)

    finally:
        cursor.close()
        conexao.close()



def listar_clientes():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@HitoriSan123",  # troque pela sua senha real
            database="estacionamento"
        )

        cursor = conexao.cursor()

        cursor.execute("SELECT id, nome, endereco, cpf, telefone FROM cliente")
        clientes = cursor.fetchall()

        print("\n===== LISTA DE CLIENTES =====")
        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"ID: {cliente[0]}")
                print(f"Nome: {cliente[1]}")
                print(f"Endereço: {cliente[2]}")
                print(f"CPF: {cliente[3]}")
                print(f"Telefone: {cliente[4]}")
                print("-" * 30)

    except mysql.connector.Error as erro:
        print("Erro ao listar clientes:", erro)

    finally:
        cursor.close()
        conexao.close()

def listar_veiculos():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@HitoriSan123",  # troque pela sua senha real
            database="estacionamento"
        )

        cursor = conexao.cursor()
        comando = """
            SELECT v.id, v.marca, v.modelo, v.ano, v.placa, c.nome
            FROM veiculo v
            JOIN cliente c ON v.cliente_id = c.id
        """
        cursor.execute(comando)


        veiculos = cursor.fetchall() # obter todos os dados em lista de tupla  
        print("\n===== LISTA DE CLIENTES =====")
        if not veiculos:
            print("Nenhum veiculo cadastrado.")
        else: 
            for veiculo in veiculos: 
                print(f"ID: {veiculo[0]}")
                print(f"MARCA: {veiculo[1]}")
                print(f"MODELO: {veiculo[2]}")
                print(f"AN0: {veiculo[3]}")
                print(f"PLACA: {veiculo[4]}")
                print(f"DONO: {veiculo[5]}")
                print("-" * 30)

    except mysql.connector.Error as erro:
        print("Erro ao listar veiculos:", erro)

    finally:
        cursor.close()
        conexao.close()
    
def editar_cliente():
    try:
        id_cliente = input("Digite o ID do cliente que deseja editar: ")

        # Conecta ao banco
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@HitoriSan123",
            database="estacionamento"
        )
        cursor = conexao.cursor()

        # Verifica se o cliente existe
        cursor.execute("SELECT * FROM cliente WHERE id = %s", (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("❌ Cliente não encontrado.")
            return

        print("Deixe em branco para manter o valor atual.")
        novo_nome = input(f"Novo nome ({cliente[1]}): ") or cliente[1]
        novo_endereco = input(f"Novo endereço ({cliente[2]}): ") or cliente[2]
        novo_cpf = input(f"Novo CPF ({cliente[3]}): ") or cliente[3]
        novo_telefone = input(f"Novo telefone ({cliente[4]}): ") or cliente[4]

        # Atualiza os dados
        cursor.execute("""
            UPDATE cliente
            SET nome = %s, endereco = %s, cpf = %s, telefone = %s
            WHERE id = %s
        """, (novo_nome, novo_endereco, novo_cpf, novo_telefone, id_cliente))

        conexao.commit()
        print("✅ Cliente atualizado com sucesso!")

    except mysql.connector.Error as erro:
        print("Erro ao editar cliente:", erro)

    finally:
        cursor.close()
        conexao.close()

   

def excluir_cliente():
    try:
        id_cliente = input("Digite o ID do cliente que deseja excluir: ")

        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="@HitoriSan123",
            database="estacionamento"
        )
        cursor = conexao.cursor()

        # Verifica se o cliente existe
        cursor.execute("SELECT * FROM cliente WHERE id = %s", (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("❌ Cliente não encontrado.")
            return

        confirmacao = input(f"Tem certeza que deseja excluir o cliente {cliente[1]}? (s/n): ").lower()
        if confirmacao != "s":
            print("❌ Operação cancelada.")
            return

        # Exclui o cliente
        cursor.execute("DELETE FROM cliente WHERE id = %s", (id_cliente,))
        conexao.commit()

        print("✅ Cliente excluído com sucesso!")

    except mysql.connector.Error as erro:
        print("Erro ao excluir cliente:", erro)

    finally:
        cursor.close()
        conexao.close()


def menu():
    while True:
        print("\n1 - Cadastrar Cliente")
        print("2 - Cadastrar Veículo")
        print("3 - Listar Clientes")
        print("4 - Listar Veículos")
        print("5 - Editar Cliente")
        print("6 - Excluir Cliente")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            cadastrar_veiculo()
        elif opcao == "3":
            listar_clientes()
        elif opcao == "4":
            listar_veiculos()
        elif opcao == "5":
            editar_cliente()
        elif opcao == "6":
            excluir_cliente()
        elif opcao == "0":
            break

menu()
