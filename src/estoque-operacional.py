def ler_arquivo_produtos(arq_produtos):
  detalhes_produtos = {}
  conteudo = arq_produtos.readline().strip()
  while conteudo != '':
    codigo, qtde_em_estoque, qtde_minima = conteudo.split(';')
    detalhes_produtos[codigo] = [int(qtde_em_estoque), int(qtde_minima)]
    conteudo = arq_produtos.readline().strip()
  return detalhes_produtos

def ler_arquivo_vendas(arq_vendas, produtos):
  codigos_divergentes = ['135', '999', '190']
  vendas_divergentes = {}
  lista_de_vendas = {}
  conteudo = arq_vendas.readline().strip()
  linha = 1
  while conteudo != "":
    codigo, qtde_vendida, situacao_venda, canal_de_venda = conteudo.split(';')
    if situacao_venda in codigos_divergentes or codigo not in produtos:
      vendas_divergentes[linha] = [codigo, qtde_vendida, situacao_venda, canal_de_venda]
    else:
      if codigo in lista_de_vendas:
        total_vendas = lista_de_vendas[codigo][0] + int(qtde_vendida)
        lista_de_vendas[codigo] = [total_vendas, situacao_venda, canal_de_venda]
      else:
        lista_de_vendas[codigo] = [int(qtde_vendida), situacao_venda, canal_de_venda]
    conteudo = arq_vendas.readline().strip()
    linha += 1
  return vendas_divergentes, lista_de_vendas

def calcular_transferencia(produtos, vendas):
  dados_transferencia = {}
  for codigo, items in vendas.items():
    total_vendas, _, _ = items
    estoque_apos_venda = produtos[codigo][0] - total_vendas
    necessidade_reposicao = produtos[codigo][1] - estoque_apos_venda if estoque_apos_venda - produtos[codigo][1] < 0 else 0
    transferencia = necessidade_reposicao if  necessidade_reposicao > 10 or necessidade_reposicao == 0 else 10
    dados_transferencia[codigo] = [produtos[codigo][0], produtos[codigo][1], total_vendas, estoque_apos_venda, necessidade_reposicao, transferencia]
  criar_arquivo_transferencia(dados_transferencia)

def criar_arquivo_transferencia(dados_transferencia):
  with open('TRANSFERE.txt', 'w') as arquivo:
    dados_ordenados = dict(sorted(dados_transferencia.items()))
    arquivo.write('Necessidade de Transferência Armazém para CO\n')
    arquivo.write(f'{'produtos':<12}{'QtCO':<12}{'QtMin':<12}{'QtVendas':<12}{'Estq.após Vendas':<20}{'Necess.':<12}{'Transf.de Arm p/ CO':<12}\n')
    for codigo, items in dados_ordenados.items():
      qtde_CO, minimo, total_vendas, estoque_apos_venda, necessidade_reposicao, transferencia = items
      texto = f'{codigo:<10} {qtde_CO:>5} {minimo:>12} {total_vendas:>14} {estoque_apos_venda:>20} {necessidade_reposicao:>10} {transferencia:>23}\n'
      arquivo.write(texto)

def main():
  arq_produtos, arq_vendas = 'Casos-de-teste/c1_produtos.txt', 'Casos-de-teste/c1_vendas.txt'
  with open(arq_produtos, 'r') as arquivo:
    produtos = ler_arquivo_produtos(arquivo)
  
  with open(arq_vendas, 'r') as arquivo:
    divergentes, vendas = ler_arquivo_vendas(arquivo, produtos)
  calcular_transferencia(produtos, vendas)

main()