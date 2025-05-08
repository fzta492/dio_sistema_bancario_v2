import flet
from flet import Page, Tabs, Tab, Column, TextField, ElevatedButton, Row, Text, Divider, DataTable, DataRow, DataCell, DataColumn, Dropdown, DropdownOption, SnackBar, TextStyle


def main(page: Page):
    page.title = "Sistema Bancário"
    page.padding = 20

    # Dados e logs
    usuarios = []
    contas = []
    proximo_numero_conta = 1
    logs_usuario = []
    logs_conta = []
    logs_operacoes = []

    # Campo de logs
    logs_usuario_field = TextField(label="Logs Usuários", width=800, height=100, multiline=True, disabled=True, text_style=TextStyle(color="black"))
    logs_conta_field = TextField(label="Logs Contas", width=800, height=100, multiline=True, disabled=True, text_style=TextStyle(color="black"))
    logs_operacoes_field = TextField(label="Logs Operações", width=800, height=100, multiline=True, disabled=True, text_style=TextStyle(color="black"))

    # Controles Usuário
    cpf_field = TextField(label="CPF (somente números)", width=200)
    nome_field = TextField(label="Nome completo", width=300)
    data_nasc_field = TextField(label="Data nascimento (DD/MM/AAAA)", width=200)
    endereco_field = TextField(label="Endereço", width=400)
    criar_usuario_btn = ElevatedButton("Criar Usuário")

    # Controles Conta
    cpf_conta_field = TextField(label="CPF do usuário", width=200)
    criar_conta_btn = ElevatedButton("Criar Conta")
    listar_contas_btn = ElevatedButton("Listar Contas")
    contas_table = DataTable(
        columns=[
            DataColumn(Text("Agência")),
            DataColumn(Text("Número")),
            DataColumn(Text("Titular")),
            DataColumn(Text("Saldo")),
        ],
        rows=[]
    )

    # Controles Operações
    conta_dropdown = Dropdown(label="Conta", width=300, options=[])
    valor_deposito_field = TextField(label="Valor Depósito", width=150)
    depositar_btn = ElevatedButton("Depositar")
    valor_saque_field = TextField(label="Valor Saque", width=150)
    sacar_btn = ElevatedButton("Sacar")
    extrato_btn = ElevatedButton("Extrato")
    extrato_field = TextField(label="Extrato", width=600, height=200, multiline=True, disabled=True)

    # Funções auxiliares
    def log(msg):
        idx = tabs.selected_index
        if idx == 0:
            logs_usuario.append(msg)
            logs_usuario_field.value = "\n".join(logs_usuario)
        elif idx == 1:
            logs_conta.append(msg)
            logs_conta_field.value = "\n".join(logs_conta)
        elif idx == 2:
            logs_operacoes.append(msg)
            logs_operacoes_field.value = "\n".join(logs_operacoes)
        page.update()

    def show_message(msg):
        page.snack_bar = SnackBar(Text(msg))
        page.snack_bar.open = True
        page.update()

    def update_contas_table():
        contas_table.rows.clear()
        for c in contas:
            contas_table.rows.append(DataRow(cells=[
                DataCell(Text(c["agencia"])),
                DataCell(Text(str(c["numero_conta"]))),
                DataCell(Text(c["usuario"]["nome"])),
                DataCell(Text(f"R$ {c['saldo']:.2f}")),
            ]))
        page.update()

    def update_conta_dropdown():
        conta_dropdown.options = [
            DropdownOption(f"{c['numero_conta']} - {c['usuario']['nome']}")
            for c in contas
        ]
        page.update()

    # Handlers
    def on_criar_usuario(e):
        nonlocal usuarios
        cpf_valor = "".join(filter(str.isdigit, cpf_field.value or ""))
        if not cpf_valor:
            show_message("CPF inválido!")
            log("Falha criar usuário: CPF inválido")
            return
        if any(u["cpf"] == cpf_valor for u in usuarios):
            show_message("CPF já cadastrado!")
            log(f"Falha criar usuário: CPF {cpf_valor} já existe")
            return
        usuarios.append({
            "cpf": cpf_valor,
            "nome": nome_field.value or "",
            "data_nascimento": data_nasc_field.value or "",
            "endereco": endereco_field.value or ""
        })
        show_message("Usuário criado com sucesso!")
        log(f"Usuário criado: CPF {cpf_valor}, Nome {nome_field.value}")
        cpf_field.value = nome_field.value = data_nasc_field.value = endereco_field.value = ""
        page.update()

    def on_criar_conta(e):
        nonlocal contas, proximo_numero_conta
        if not usuarios:
            show_message("Nenhum usuário cadastrado.")
            log("Falha criar conta: sem usuários cadastrados")
            return
        cpf_valor = "".join(filter(str.isdigit, cpf_conta_field.value or ""))
        usuario = next((u for u in usuarios if u["cpf"] == cpf_valor), None)
        if not usuario:
            show_message("Usuário não encontrado!")
            log(f"Falha criar conta: CPF {cpf_valor} não encontrado")
            return
        nova = {
            "agencia": "0001",
            "numero_conta": proximo_numero_conta,
            "usuario": usuario,
            "saldo": 0.0,
            "extrato": "",
            "numero_saques_realizados_hoje": 0
        }
        contas.append(nova)
        proximo_numero_conta += 1
        show_message("Conta criada com sucesso!")
        log(f"Conta {nova['numero_conta']} criada para CPF {cpf_valor}")
        cpf_conta_field.value = ""
        update_contas_table()
        update_conta_dropdown()

    def on_listar_contas(e):
        update_contas_table()
        log("Listagem de contas atualizada")

    def on_depositar(e):
        if not conta_dropdown.value:
            show_message("Selecione uma conta.")
            log("Falha depósito: conta não selecionada")
            return
        numero = int(conta_dropdown.value.split(" - ")[0])
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        try:
            valor = float(valor_deposito_field.value or "0")
        except:
            show_message("Valor de depósito inválido.")
            log("Falha depósito: valor inválido")
            return
        if valor <= 0:
            show_message("Valor de depósito inválido.")
            log("Falha depósito: valor não positivo")
            return
        conta["saldo"] += valor
        conta["extrato"] += f"Depósito:\tR$ {valor:.2f}\n"
        show_message("Depósito realizado com sucesso!")
        log(f"Depósito R$ {valor:.2f} na conta {numero}")
        valor_deposito_field.value = ""
        update_contas_table()

    def on_sacar(e):
        if not conta_dropdown.value:
            show_message("Selecione uma conta.")
            log("Falha saque: conta não selecionada")
            return
        numero = int(conta_dropdown.value.split(" - ")[0])
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        try:
            valor = float(valor_saque_field.value or "0")
        except:
            show_message("Valor de saque inválido.")
            log("Falha saque: valor inválido")
            return
        if valor <= 0:
            show_message("Valor de saque inválido.")
            log("Falha saque: valor não positivo")
            return
        if valor > conta["saldo"]:
            show_message("Saldo insuficiente.")
            log(f"Falha saque: saldo insuficiente conta {numero}")
            return
        if valor > 500:
            show_message("Valor excede limite por saque (R$ 500).")
            log(f"Falha saque: valor {valor:.2f} excede limite")
            return
        if conta["numero_saques_realizados_hoje"] >= 3:
            show_message("Limite de saques diários excedido.")
            log(f"Falha saque: limite diário atingido conta {numero}")
            return
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque:\t\tR$ {valor:.2f}\n"
        conta["numero_saques_realizados_hoje"] += 1
        show_message("Saque realizado com sucesso!")
        log(f"Saque R$ {valor:.2f} na conta {numero}")
        valor_saque_field.value = ""
        update_contas_table()

    def on_extrato(e):
        if not conta_dropdown.value:
            show_message("Selecione uma conta.")
            log("Falha extrato: conta não selecionada")
            return
        numero = int(conta_dropdown.value.split(" - ")[0])
        conta = next((c for c in contas if c["numero_conta"] == numero), None)
        texto = conta["extrato"] or "Não foram realizadas movimentações."
        texto += f"\nSaldo:\tR$ {conta['saldo']:.2f}"
        extrato_field.value = texto
        page.update()
        log(f"Extrato exibido conta {numero}")

    # Atribuição handlers
    criar_usuario_btn.on_click = on_criar_usuario
    criar_conta_btn.on_click = on_criar_conta
    listar_contas_btn.on_click = on_listar_contas
    depositar_btn.on_click = on_depositar
    sacar_btn.on_click = on_sacar
    extrato_btn.on_click = on_extrato

    # Montagem de abas
    usuarios_tab = Tab(text="Usuários", content=Column([
        Text("Criar Usuário"),
        Row([cpf_field, nome_field]),
        Row([data_nasc_field, endereco_field]),
        criar_usuario_btn,
        logs_usuario_field
    ]))
    contas_tab = Tab(text="Contas", content=Column([
        Text("Contas"),
        Row([cpf_conta_field, criar_conta_btn]),
        listar_contas_btn,
        contas_table,
        logs_conta_field
    ]))
    operacoes_tab = Tab(text="Operações", content=Column([
        Text("Operações"),
        conta_dropdown,
        Row([valor_deposito_field, depositar_btn]),
        Row([valor_saque_field, sacar_btn, extrato_btn]),
        extrato_field,
        logs_operacoes_field
    ]))
    tabs = Tabs(selected_index=0, tabs=[usuarios_tab, contas_tab, operacoes_tab])

    page.add(tabs)
    page.update()


flet.app(target=main) 
