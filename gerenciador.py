# TESTE DE PERFORMANCE 1

"""
MAESTRO
Gerenciador de Estúdio Musical

Permite:
- Adicionar novas sessões
- Listar sessões agendadas
- Marcar sessões como concluídas
- Remover sessões
"""

print(" <<< MAESTRO >>> ")
print("Gerenciador de Estúdio Musical")

def menu_opcoes():
    print("\nMENU:")
    print("1 - ADICIONAR NOVA SESSÃO")
    print("2 - LISTAR SESSÕES AGENDADAS")
    print("3 - MARCAR SESSÃO COMO CONCLUÍDA")
    print("4 - REMOVER SESSÃO")
    print("5 - SAIR")
    
class Sessao:
    """
    Classe usada para representar as Sessões (Agendamentos) do Estúdio Musical.
    
    Atributos:
        id_sessao (int): ID da sessão, valor sequencial.
        data_sessao (str): Data de agendamento da sessão.
        artista (str): Nome do artista.
        estudio (str): Nome do estúdio/sala onde será a sessão.
        duracao (str): Duração em horas da sessão.
        descricao (str): Informações adicionais sobre a sessão.
        status (str): Status da Sessão, pode ser "Agendada" ou "Concluída".
    """
    def __init__(self, id_sessao, data_sessao, artista, estudio, duracao, descricao, status="Agendada"):
        self.id_sessao = id_sessao
        self.data_sessao = data_sessao
        self.artista = artista
        self.estudio = estudio
        self.duracao = duracao
        self.descricao = descricao
        self.status = status
        
sessoes = []
         
def adicionar_sessao():
    """
    Função utilizada para criar novas sessões e adicioná-las a lista de sessões.
    
    Recebe do usuário os valores Data da Sessão, Artista, Estúdio, Duração e Descrição,
    Cria um novo objeto Sessao e o adiciona à lista sessoes.
    """
    
    id_sessao = len(sessoes) + 1 
    data_sessao = input("Data da sessão (ex: 2025-08-23): ")
    artista = input("Nome do artista: ")
    estudio = input("Nome do estúdio/sala: ")
    duracao = input("Duração em horas: ")
    descricao = input("Descrição: ")
    sessao = Sessao(
        id_sessao = id_sessao, 
        data_sessao = data_sessao, 
        artista = artista, 
        estudio = estudio, 
        duracao = duracao, 
        descricao = descricao
    )
    
    sessoes.append(sessao)
    print("Sessão adicionada com sucesso!")
           
def listar_sessoes():
    """
    Função que apresenta todas as sessões agendadas.
    
    Cria lista provisória de sessões com status "Agendada"
    e exibe os detalhes dos objetos correspondentes.
    """
    
    agendadas = []

    for sessao in sessoes:
        if sessao.status == "Agendada":
            agendadas.append(sessao)
    
    if not agendadas:
        print("Não há sessões agendadas.")
        return 
    
    for sessao in agendadas:
            print(f"""\nID DA SESSÃO: {sessao.id_sessao}
            Data da Sessão: {sessao.data_sessao}
            Artista: {sessao.artista}
            Estúdio: {sessao.estudio}
            Duração (h): {sessao.duracao}
            Descrição: {sessao.descricao}
            Status: {sessao.status}""")  
    
    
def concluir_sessao():
    """
    Função que altera o status da sessão para Concluída.
    
    Utiliza a função de listar sessões, e solicita ao usuário o ID da sessão,
    Altera o status do objeto sessao cujo ID corresponde ao informado para "Concluída".
    """
    listar_sessoes()
    id_selecionado = int(input("\nDigite o ID da Sessão a ser marcada como concluída: "))
    for sessao in sessoes:
        if sessao.id_sessao == id_selecionado:
            sessao.status = "Concluída"
            print(f"Sessão {sessao.id_sessao} marcada como Concluída!")
            return
    print("Sessão não encontrada.")
    
def remover_sessao():
    """
    Função que remove sessões.
    
    Utiliza a função de listar sessões, e solicita ao usuário o ID da sessão,
    Retira da lista a sessão cujo ID corresponde ao informado.
    """
    listar_sessoes()
    id_selecionado = int(input("\nDigite o ID da Sessão a ser removida: "))
    for sessao in sessoes:
        if sessao.id_sessao == id_selecionado:
            sessoes.remove(sessao)
            print(f"Sessão {sessao.id_sessao} removida com sucesso!")
            return
    print("Sessão não encontrada.")
    
while True:
    menu_opcoes()
    opcao = input("Escolha a opção desejada: ")
    
    if opcao == "1":
        print("\nADICIONE UMA NOVA SESSÃO")
        adicionar_sessao()
    elif opcao == "2":
        print("\nLISTANDO SESSÕES AGENDADAS")
        listar_sessoes()
    elif opcao == "3":
        concluir_sessao()
    elif opcao == "4":
        remover_sessao()
    elif opcao == "5":
        break
    else: 
        print("Opção inválida.")
