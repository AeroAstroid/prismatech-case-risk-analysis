# Resumo da Resolução

Vídeo de Explicação: www.youtube.com/watch?v=U2DRG_Lez8k

O problema se baseia na coleta e análise de dados de um arquivo csv com contratos bancários. Em cases como esse, o Pandas geralmente é a melhor opção, por conta das ferramentas que tem pra lidar com dados, especialmente o DataFrame.

No start-up do programa, o arquivo é lido e transformado em DataFrame para ser analisado. A agregação da tabela é feita de forma a criar um "DataFrame" de mímica, seguindo o formato de dicionário de colunas, cujos valores são as células individuais em cada linha da coluna. No fim da função tabela_agregada(), esses dados são transformados em um DataFrame próprio para ser salvo em seu próprio arquivo.

Visto que essa agregação demora um tempo, também tem a opção de ler a tabela agregada de um arquivo próprio, se é que já está salva no sistema. Assim, não é necessário recalculá-la caso o csv original não tenha mudanças.

Para a análise de faixas de risco, a informação de cada faixa é salva em um dicionário e agregada de forma semelhante à agregação original dos dados por id_cliente. Cada faixa tem seu valor definido num dicionário constante, e checado com uma função simples.

Finalmente, o dataset final pode ser criado de todos os dados calculados na função tabela_agregada(), e escrito com a função escrever_dataset_final(), acessado pela operação 5. Como foi pedido, esse arquivo foi salvo como `dataset_final.csv`.