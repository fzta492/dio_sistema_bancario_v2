# Sistema Bancário com Interface Gráfica em Flet

Este projeto é uma aplicação de sistema bancário desktop desenvolvida em Python utilizando a biblioteca Flet. Ele oferece uma interface gráfica intuitiva para gerenciar usuários, contas bancárias e realizar operações financeiras básicas, seguindo os desafios propostos para a evolução de um sistema bancário simples.

## Funcionalidades Implementadas

O sistema é organizado em abas para facilitar a navegação e o uso:

### 1. Aba de Usuários
* **Criação de Novos Usuários:**
    * Campos para CPF (somente números), nome completo, data de nascimento e endereço.
    * Validação para garantir que o CPF contenha apenas números.
    * Validação para impedir o cadastro de CPFs duplicados.
* **Logs de Usuários:** Exibe um registro das ações realizadas nesta aba (criação de usuários, falhas).
  ![image](https://github.com/user-attachments/assets/29cab0b1-8abf-472d-bc3f-fed4950c78e3)


### 2. Aba de Contas
* **Criação de Novas Contas Correntes:**
    * Requer o CPF de um usuário previamente cadastrado para vincular a conta.
    * Agência padrão "0001".
    * Número da conta gerado sequencialmente.
* **Listagem de Contas:**
    * Exibe uma tabela com as contas cadastradas, mostrando agência, número da conta, nome do titular e saldo atual.
* **Logs de Contas:** Registra as ações de criação e listagem de contas.
  ![image](https://github.com/user-attachments/assets/a1a60c19-fb33-47c0-a736-d3d478f6d02d)


### 3. Aba de Operações
* **Seleção de Conta:** Um menu dropdown permite selecionar a conta com a qual se deseja operar.
* **Depósito:** Permite realizar depósitos na conta selecionada.
* **Saque:**
    * Permite realizar saques da conta selecionada.
    * Limite de R$ 500,00 por transação.
    * Limite de 3 saques diários por conta.
* **Extrato:** Exibe o histórico de transações (depósitos e saques) e o saldo atual da conta selecionada.
* **Logs de Operações:** Registra todas as operações financeiras e tentativas.
  ![image](https://github.com/user-attachments/assets/d308e7cb-2ef0-4f55-942c-30580c3f1594)


### Funcionalidades Gerais da Interface
* **Notificações:** Mensagens de feedback são exibidas para o usuário informando o sucesso ou falha das operações.
* **Interface Reativa:** Os componentes da interface são atualizados dinamicamente conforme as ações do usuário.

## Tecnologias Utilizadas
* **Python 3.13**
* **Flet:** Framework Python para criação de interfaces gráficas web, desktop e mobile.

## Pré-requisitos
* Python 3.6 ou superior instalado em sua máquina.
* A biblioteca Flet.

## Instalação

1.  Clone o repositório (ou baixe os arquivos):
    ```bash
    git clone https://github.com/fzta492/dio_sistema_bancario_v2.git
    cd dio_sistema_bancario_v2
    ```
2.  Instale a biblioteca Flet:
    ```bash
    pip install flet
    ```

## Como Executar

1.  Certifique-se de que você está no diretório do projeto onde o arquivo Python principal está localizado.
2.  Execute o seguinte comando no seu terminal:
    ```bash
    python main.py
    ```
    Ou, alternativamente, usando o comando específico do Flet:
    ```bash
    flet run main.py
    ```

## Desafio Original (v1)

Este projeto evoluiu a partir de um desafio inicial de sistema bancário em modo console, cujos requisitos incluíam:
* **Versão 1 (Console):**
    * Operações básicas: depósito, saque (com limites), extrato.
* **Versão 2 (Console - Otimizações):**
    * Modularização do código em funções.
    * Regras específicas para passagem de argumentos em funções (positional-only, keyword-only).
    * Novas funcionalidades:
        * **Criar Usuário:** Coletar nome, data de nascimento, CPF (armazenar apenas números, CPF único) e endereço (formato: `logradouro, número - bairro - cidade/sigla estado`).
        * **Criar Conta Corrente:** Vincular a um usuário, agência fixa "0001", número da conta sequencial.
        * Listar contas.
* **Versão Atual (Interface Gráfica com Flet):**
    * Implementação de uma interface gráfica para as funcionalidades da Versão 2, adaptando a interação para um ambiente visual e adicionando elementos como logs em tempo real e seleção de contas via dropdown.

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests com melhorias, correções de bugs ou novas funcionalidades.

---
