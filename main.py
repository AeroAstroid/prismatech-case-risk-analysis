import pandas as pd
from datetime import datetime as dt

# Dados de faixa de risco (faixa: valor_min)
# Ordenadas de forma decrescente para facilitar a busca
FAIXAS_RISCO = {
    "ALTO": 0.7,
    "MEDIO": 0.4,
    "BAIXO": 0.0
}

def avaliar_risco(valor :float) -> str:
    '''
    Retorna uma descrição do risco associado a um valor de score.

    A configuração das faixas pode ser feita modificando a constante FAIXAS_RISCO.
    Por padrão, a distribuição é a sugerida pelo README:

    Baixo risco: score ≤ 0.4
    Médio risco: 0.4 < score ≤ 0.7
    Alto risco: score > 0.7
    '''

    for faixa, v_min in FAIXAS_RISCO.items():
        if valor > v_min:
            return faixa


def tabela_agregada(dados_csv :pd.DataFrame) -> pd.DataFrame:
    '''
    Função base para busca de dados agregados de cliente.

    Trabalha com um CSV de dados fornecido em formato de DataFrame do Pandas.
    '''

    colunas_tabela = [
        "qtd_contratos", "valor_total", "prazo_medio", "score_medio", "faixa_risco",
        "inadimplencias", "percentual_inadimplencia", "mes_ultimo_contrato"
    ]

    # Preparar a tabela estilo DataFrame
    tabela = {coluna: {} for coluna in colunas_tabela}

    clientes_para_lookup = set(dados_csv["id_cliente"])

    # Faz o lookup e agregação de todas as linhas relevantes para cada cliente
    for id_atual in clientes_para_lookup:
        indices = [
            i for i in range(len(dados_csv["id_cliente"]))
            if dados_csv["id_cliente"][i] == id_atual
        ]

        # Calcular antes os dados que são necessários para o cálculo de outros dados...
        qtd_contratos = len(indices)
        inadimplencias = sum([dados_csv["inadimplente"][i] for i in indices])
        score_medio = sum([dados_csv["score_risco"][i] for i in indices])/qtd_contratos

        # ... e também o "mes_ultimo_contrato", que requer mais de uma só operação
        meses_contratos = [dt.strptime(dados_csv["data_contrato"][i], '%Y-%M-%d') for i in indices]
        # ordem decrescente = mais recente primeiro -> pegar o mês em formato padronizado
        mes_ultimo_contrato = sorted(meses_contratos, reverse=True)[0].strftime('%Y-%M')

        # Então, preencher as colunas para esse ID
        tabela["qtd_contratos"][id_atual] = qtd_contratos
        tabela["valor_total"][id_atual] = sum([dados_csv["valor_contrato"][i] for i in indices])
        tabela["prazo_medio"][id_atual] = sum([dados_csv["prazo_meses"][i] for i in indices])/qtd_contratos
        tabela["score_medio"][id_atual] = score_medio
        tabela["faixa_risco"][id_atual] = avaliar_risco(score_medio)
        tabela["inadimplencias"][id_atual] = sum([dados_csv["inadimplente"][i] for i in indices])
        tabela["percentual_inadimplencia"][id_atual] = inadimplencias/qtd_contratos
        tabela["mes_ultimo_contrato"][id_atual] = mes_ultimo_contrato
    
    if not tabela["qtd_contratos"]:
        raise KeyError("Nenhum resultado encontrado para a query de busca de clientes!")

    tabela_em_df = pd.DataFrame(tabela)

    # Mudar os IDs pra ser coluna ao invés do índice
    tabela_em_df['id_cliente'] = tabela_em_df.index
    tabela_em_df.reset_index(drop=True, inplace=True)

    return tabela_em_df


def analise_de_risco_agregada(tabela :pd.DataFrame) -> dict:
    '''
    Retorna dados sobre cada grupo de risco.

    Compatível com o retorno da função dados_agregados, e com a análise de faixas de risco da 
    função avaliar_risco.
    '''

    # Cada faixa terá dados de número de clientes, taxa de inadimplência por contrato, -
    # - e valor médio por contrato.
    dados_faixa = {faixa: [0, 0, 0] for faixa in FAIXAS_RISCO.keys()}

    for faixa_atual in dados_faixa.keys():
        # Todos os indices de clientes nessa faixa
        indices = [
            i for i, faixa_linha in enumerate(tabela["faixa_risco"]) if faixa_linha == faixa_atual
        ]

        num_clientes = len(indices)

        # Por que não usar só a média da coluna percentual_inadimplencia? Pois resultaria em uma -
        # - falha estatística: o dado que é mais estatisticamente relevante é a taxa média por -
        # - contratos, e não a média das médias de cada cliente. Acumulando o número total de - 
        # - contratos e de inadimplências, conseguimos uma estimativa melhor do efeito da faixa -
        # - de risco na inadimplência de um dado contrato.
        total_contratos = sum([tabela["qtd_contratos"][i] for i in indices])
        total_inadimplencias = sum([tabela["inadimplencias"][i] for i in indices])
        taxa_inadimplencia = total_inadimplencias/total_contratos

        valor_total = sum([tabela["valor_total"][i] for i in indices])
        valor_medio = valor_total/total_contratos

        dados_faixa[faixa_atual] = [num_clientes, taxa_inadimplencia, valor_medio]
    
    return dados_faixa

def escrever_tabela_agregada(arquivo :str, dados_df :pd.DataFrame):
    '''
    Escreve a tabela agregada com os dados requisitados em um arquivo.

    Compatível com o retorno de dados da função dados_agregados.
    '''

    dados_df.to_csv(arquivo, index=False,
    columns=['id_cliente', 'qtd_contratos', 'valor_total', 'prazo_medio',
    'score_medio', 'percentual_inadimplencia', 'mes_ultimo_contrato'])
    return

def printar_dados_de_risco(dados :dict):
    '''
    Escreve o dataset pre-processado em um arquivo.

    Compatível com o retorno de dados da função dados_agregados.
    '''
    print("\t\t\tN_CLIENTES\t\tTAXA_INADIMP\t\tVALOR_MEDIO")

    for faixa, dados_faixa in dados.items():
        print(f"[{faixa}]\t\t\t{dados_faixa[0]}\t\t\t{dados_faixa[1]*100:.2f}%\t\t\t{dados_faixa[2]:.2f}")
    return

def escrever_dataset(arquivo :str, dados_df :pd.DataFrame):
    '''
    'Printa' os dados de risco por faixa na tela.
    '''

    dados_df.to_csv(arquivo, index=False,
    columns=['id_cliente', 'faixa_risco', 'qtd_contratos', 'valor_total',
    'percentual_inadimplencia', 'prazo_medio', 'mes_ultimo_contrato'])
    return

if __name__ == "__main__":
    print("Lendo tabela de contratos...")
    CSV = pd.read_csv("data/contratos_clientes.csv")

    print("Dataset preparado!\n")

    tem_tabela = False
    tabela = None

    while True: # Loop de operação do programa
        print("Features de Risco Bancário! Digite uma operação a ser feita.")
        print(f"Tabela agregada {'NÃO ' if not tem_tabela else ''}DISPONÍVEL.")
        print("\t1 -> (re)calcular a tabela agregada")
        print("\t2 -> ler a tabela agregada de um arquivo")
        print("\t3 -> escrever tabela agregada em um arquivo")
        print("\t4 -> ver dados de risco por faixa na tela")
        print("\t5 -> escrever dataset pre-processado em um arquivo")
        print("\tquit -> fechar o programa\n")

        codigo = input("Operação: ")

        if codigo.lower() == "quit":
            exit()
        
        try:
            codigo = int(codigo)
        except ValueError:
            print("Código de operação inválido. Tente novamente.\n")
            continue
        
        match codigo:
            case 1:
                if tem_tabela: print("Recalculando tabela...")
                else: print("Calculando tabela...")
                tabela = tabela_agregada(CSV)
                tem_tabela = True
                print("Tabela agregada calculada!\n")
            
            case 2:
                arquivo = input("Nome do arquivo da tabela agregada: ")
                tabela = pd.read_csv(arquivo)
                print("Tabela agregada lida do arquivo!\n")

            case 3:
                if not tem_tabela:
                    print("Essa função precisa da tabela agregada! Calcule ou leia a tabela antes.\n")
                else:
                    arquivo = input("Nome do arquivo de saída: ")
                    escrever_tabela_agregada(arquivo, tabela)
                    print("Tabela agregada escrita no arquivo.\n")

            case 4:
                print("\n")
                if not tem_tabela:
                    print("Essa função precisa da tabela agregada! Calcule ou leia a tabela antes.\n")
                else:
                    dados_risco = analise_de_risco_agregada(tabela)
                    printar_dados_de_risco(dados_risco)
                    print("\n")
            
            case 5:
                if not tem_tabela:
                    print("Essa função precisa da tabela agregada! Calcule ou leia a tabela antes.\n")
                else:
                    arquivo = input("Nome do arquivo de saída: ")
                    escrever_dataset(arquivo, tabela)
                    print("Dataset final escrito no arquivo.\n")