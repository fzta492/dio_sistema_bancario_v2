import textwrap

# --- Funções de Operações Bancárias ---

def sacar(*, saldo, valor, extrato, limite_valor_saque, numero_saques_realizados, limite_saques_diarios):
    """
    Realiza um saque na conta.
    Argumentos são keyword-only.
    Retorna o novo saldo, o novo extrato e o novo número de saques realizados.
    """
    excedeu_saldo = valor > saldo
    excedeu_limite_valor = valor > limite_valor_saque
    excedeu_limites_saques = numero_saques_realizados >= limite_saques_diarios

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    elif excedeu_limite_valor:
        print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {limite_valor_saque:.2f} por operação. @@@")
    elif excedeu_limites_saques:
        print(f"\n@@@ Operação falhou! Número máximo de {limite_saques_diarios} saques diários excedido. @@@")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques_realizados += 1
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato, numero_saques_realizados


def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta.
    Argumentos são positional-only.
    Retorna o novo saldo e o novo extrato.
    """
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta.
    'saldo' é positional-only, 'extrato' é keyword-only.
    """
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


# --- Funções de Gerenciamento de Usuários e Contas ---

def criar_usuario(usuarios):
    """Cria um novo usuário (cliente do banco)."""
    cpf_input = input("Informe o CPF (somente números): ")
    # Remove caracteres não numéricos do CPF
    cpf = "".join(filter(str.isdigit, cpf_input))

    if not cpf: # Verifica se o CPF ficou vazio após a limpeza
        print("\n@@@ CPF inválido! Forneça apenas números. @@@")
        return

    usuario_existente = filtrar_usuario(cpf, usuarios)
    if usuario_existente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n=== Usuário criado com sucesso! ===")


def filtrar_usuario(cpf, usuarios):
    """Busca um usuário na lista de usuários pelo CPF."""
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta_corrente(agencia_padrao, proximo_numero_conta, usuarios, contas):
    """Cria uma nova conta corrente vinculada a um usuário."""
    if not usuarios:
        print("\n@@@ Nenhum usuário cadastrado. Crie um usuário antes de abrir uma conta. @@@")
        return proximo_numero_conta # Retorna o mesmo número, pois a conta não foi criada

    cpf_input = input("Informe o CPF do usuário para vincular a conta: ")
    cpf = "".join(filter(str.isdigit, cpf_input))

    if not cpf:
        print("\n@@@ CPF inválido para vincular a conta! Forneça apenas números. @@@")
        return proximo_numero_conta

    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        nova_conta = {
            "agencia": agencia_padrao,
            "numero_conta": proximo_numero_conta,
            "usuario": usuario, # Armazena a referência do dicionário do usuário
            "saldo": 0.0,
            "extrato": "",
            "numero_saques_realizados_hoje": 0,
        }
        contas.append(nova_conta)
        print(f"\n=== Conta corrente número {proximo_numero_conta} criada com sucesso para o usuário {usuario['nome']}! ===")
        return proximo_numero_conta + 1 # Retorna o próximo número de conta a ser usado
    else:
        print("\n@@@ Usuário com CPF informado não encontrado! Fluxo de criação de conta encerrado. @@@")
        return proximo_numero_conta # Retorna o mesmo número, pois a conta não foi criada


def listar_contas(contas):
    """Lista todas as contas correntes cadastradas."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']} (CPF: {conta['usuario']['cpf']})
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print(textwrap.dedent(linha))
        print("------------------------------------------")
    print("==============================================")


def selecionar_conta_para_operacao(contas):
    """Permite ao usuário selecionar uma conta para realizar operações."""
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada para realizar operações. @@@")
        return None

    listar_contas(contas) # Mostra as contas disponíveis
    
    try:
        num_conta_selecionada_str = input("Digite o número da conta para realizar a operação: ")
        if not num_conta_selecionada_str.isdigit():
            print("\n@@@ Número da conta inválido. Deve ser um número. @@@")
            return None
        num_conta_selecionada = int(num_conta_selecionada_str)

        for conta in contas:
            if conta["numero_conta"] == num_conta_selecionada:
                return conta
        print("\n@@@ Conta não encontrada. @@@")
        return None
    except ValueError: # Caso a conversão para int falhe (embora o isdigit já cubra)
        print("\n@@@ Entrada inválida para o número da conta. @@@")
        return None

# --- Função Principal (Menu) ---

def menu():
    """Exibe o menu principal e gerencia a interação com o usuário."""
    AGENCIA_PADRAO = "0001"
    VALOR_LIMITE_POR_SAQUE = 500  # R$ 500,00 por saque
    LIMITE_SAQUES_DIARIOS = 3     # Máximo de 3 saques por dia por conta

    usuarios = []  # Lista para armazenar dicionários de usuários
    contas = []    # Lista para armazenar dicionários de contas
    proximo_numero_conta_disponivel = 1

    texto_menu = """
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExibir Extrato
    [nu]\tNovo Usuário
    [nc]\tNova Conta
    [lc]\tListar Contas
    [q]\tSair
    => """

    while True:
        opcao = input(textwrap.dedent(texto_menu)).strip().lower()

        if opcao == "d":
            print("\n--- Depósito ---")
            conta_selecionada = selecionar_conta_para_operacao(contas)
            if conta_selecionada:
                try:
                    valor_str = input(f"Informe o valor do depósito para a conta {conta_selecionada['numero_conta']}: R$ ")
                    valor = float(valor_str)
                    
                    novo_saldo, novo_extrato = depositar(
                        conta_selecionada["saldo"],
                        valor,
                        conta_selecionada["extrato"]
                    )
                    conta_selecionada["saldo"] = novo_saldo
                    conta_selecionada["extrato"] = novo_extrato
                except ValueError:
                    print("\n@@@ Valor de depósito inválido. Por favor, insira um número. @@@")

        elif opcao == "s":
            print("\n--- Saque ---")
            conta_selecionada = selecionar_conta_para_operacao(contas)
            if conta_selecionada:
                try:
                    valor_str = input(f"Informe o valor do saque para a conta {conta_selecionada['numero_conta']}: R$ ")
                    valor = float(valor_str)

                    novo_saldo, novo_extrato, novo_num_saques = sacar(
                        saldo=conta_selecionada["saldo"],
                        valor=valor,
                        extrato=conta_selecionada["extrato"],
                        limite_valor_saque=VALOR_LIMITE_POR_SAQUE,
                        numero_saques_realizados=conta_selecionada["numero_saques_realizados_hoje"],
                        limite_saques_diarios=LIMITE_SAQUES_DIARIOS
                    )
                    conta_selecionada["saldo"] = novo_saldo
                    conta_selecionada["extrato"] = novo_extrato
                    conta_selecionada["numero_saques_realizados_hoje"] = novo_num_saques
                except ValueError:
                    print("\n@@@ Valor de saque inválido. Por favor, insira um número. @@@")
        
        elif opcao == "e":
            print("\n--- Extrato ---")
            conta_selecionada = selecionar_conta_para_operacao(contas)
            if conta_selecionada:
                exibir_extrato(
                    conta_selecionada["saldo"],
                    extrato=conta_selecionada["extrato"]
                )

        elif opcao == "nu":
            print("\n--- Novo Usuário ---")
            criar_usuario(usuarios)

        elif opcao == "nc":
            print("\n--- Nova Conta ---")
            numero_conta_atualizado = criar_conta_corrente(
                AGENCIA_PADRAO,
                proximo_numero_conta_disponivel,
                usuarios,
                contas
            )
            # Atualiza o próximo número de conta apenas se uma nova conta foi realmente criada
            if numero_conta_atualizado > proximo_numero_conta_disponivel:
                 proximo_numero_conta_disponivel = numero_conta_atualizado

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\n Saindo do sistema... Obrigado por usar nossos serviços!")
            break

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

# --- Ponto de Entrada do Programa ---
if __name__ == "__main__":
    menu()
