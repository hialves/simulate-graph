import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import matplotlib.gridspec as gridspec

from helpers import calculateMovingAverage, calculateStandardDeviation, getCsvValues

# Inicializar variáveis
PontoA = 0.0
PontoB = 0.0
DistanciaAB = 0.0
#
Tendencia = 'Baixa'
atingiuLimiar = 'Não'
#
Indice = np.array([])
SARParabolic = np.array([])
Fechamento = np.array([])
Movimento = np.array([])
Correcao = np.array([])
MovimentoArtificial = np.array([])
MovimentoArtificialRand = np.array([])
MovimentoArtificialRandAcumulado = np.array([])
CorrecaoArtificial = np.array([])
CorrecaoArtificialRand = np.array([])
CorrecaoArtificialRandAcumulado = np.array([])
PontoArtificial = np.array([])

Dados = pd.read_csv('ada.csv')
#DadosFechamento = Dados['Último']
#print(DadosFechamento)
#DadosFechamentoOrdenados = list(reversed(DadosFechamento))
DadosFechamentoOrdenados = getCsvValues('ada.csv', 'Último')
#DadosFechamentoOrdenados = list(reversed(Dados['Último']))

# Escolher a quantidade de preços a serem considerados
#print('Digite a quantidade de preços de fechamento')
#Tamanho = int(input('Digite a quantidade de preços de fechamento'))
Tamanho = 200
if Tamanho > len(DadosFechamentoOrdenados):
  Tamanho = len(DadosFechamentoOrdenados)
# Somente os preços de fechamento de 0 até Tamanho
for i in range(Tamanho):
  Fechamento = np.append(Fechamento,i)
  Fechamento[i] = DadosFechamentoOrdenados[i]
  #Depurar
  #print(i,Fechamento[i])
# Encontrar os Pontos A e B dos Movimentos e Correções
#
# Indicador SARParabolic sinalizando qual o sentido do Movimento ou Correcao
for i in range(len(Fechamento)):
  Indice = np.append(Indice,i)
  SARParabolic = np.append(SARParabolic,0)
  # Inicializar o SARParabolic no Primeiro preço de Fechamento
  if i == 0:
    SARParabolic[i] = Fechamento[i]
  else:
    if atingiuLimiar == 'Sim':
      atingiuLimiar = 'Não'
      SARParabolic[i] = Fechamento[i-2]
      if Tendencia == 'Alta':
        Tendencia = 'Baixa'
        # Encontrar maior ponto do vetor
        PontoA = SARParabolic[i]
        # Calcular Movimento  
        if PontoB > 0:
          DistanciaAB = (PontoA - PontoB) / PontoB           
          if DistanciaAB > 0:
            Movimento = np.append(Movimento,DistanciaAB)
            #print(Movimento)
          else:  
            if DistanciaAB < 0:
              Correcao = np.append(Correcao,abs(DistanciaAB))            
              #print(Correcao)
      else: #Tendencia == 'Baixa'
        Tendencia = 'Alta' 
        # Encontrar maior ponto do vetor
        PontoB = SARParabolic[i]
        # Calcular Movimento  
        if PontoA > 0:
          DistanciaAB = (PontoB - PontoA)  / PontoA
          if DistanciaAB > 0:
            Movimento = np.append(Movimento,DistanciaAB)
            #print(Movimento)
          else:
            if DistanciaAB < 0:  
              Correcao = np.append(Correcao,abs(DistanciaAB))
              #print(Correcao)
    else: #atingiuLimiar == 'Não':  
        # Atualizar o valor de SARParabolic com fator de 0.02   
        fator = 0.02
        if Tendencia == 'Alta':
          SARParabolic[i] = SARParabolic[i-1] * (1+fator)
        else: #Tendencia == 'Baixa':
            SARParabolic[i] = SARParabolic[i-1] * (1-fator)
        # Verificar se o Fechamento atingiu o limiar para mudar o sentido da tendência       
        if Tendencia == 'Alta':
          if Fechamento[i] < SARParabolic[i]:
            atingiuLimiar = 'Sim'
        else: #Tendencia == 'Baixa':
          if Fechamento[i] > SARParabolic[i]:
            atingiuLimiar = 'Sim'    

# Calcular Média e Desvio Padrão usando Logaritmo
#MovimentoMu = np.mean(Movimento)
MovimentoMu = calculateMovingAverage(Movimento)
#MovimentoSigma = np.std(Movimento)
MovimentoSigma = calculateStandardDeviation(Movimento,MovimentoMu)
#CorrecaoMu = np.mean(Correcao)
CorrecaoMu = calculateMovingAverage(Correcao)
#CorrecaoSigma = np.std(Correcao)
CorrecaoSigma = calculateStandardDeviation(Correcao,CorrecaoMu)
# Gerar arrays de Movimento e Correção
#MovimentoArtificialRand = np.random.lognormal(MovimentoMu, MovimentoSigma, len(Movimento))
# Testar geração de números randômicos
for i in range(Tamanho):
  MovimentoArtificialRand = np.append(MovimentoArtificialRand,0)
  MovimentoArtificialRandAcumulado = np.append(MovimentoArtificialRandAcumulado,0)  
  CorrecaoArtificialRand = np.append(CorrecaoArtificialRand,0)
  CorrecaoArtificialRandAcumulado = np.append(CorrecaoArtificialRandAcumulado,0)
  if i == 0:
    MovimentoArtificialRand[i] = 0
    CorrecaoArtificialRand[i] = 0
  if i > 0:
    MovimentoArtificialRand[i] = np.random.lognormal(MovimentoMu, MovimentoSigma, 1)
    CorrecaoArtificialRand[i] = np.random.lognormal(CorrecaoMu, CorrecaoSigma, 1)
    # Falta acompanhar a média dos valores randômicos para atender à probalidade de cada classe
    MovimentoArtificialRandAcumulado[i] = MovimentoArtificialRand[i] / i
    CorrecaoArtificialRandAcumulado[i] = CorrecaoArtificialRand[i] / i
#
for i in range(len(Movimento)):
  #MovimentoArtificial = np.append(MovimentoArtificial,0)
  WarmUP = round(Tamanho * 0.1) + i
  MovimentoArtificial = np.append(MovimentoArtificial,MovimentoArtificialRand[WarmUP])
  #MovimentoArtificial[i] = np.random.lognormal(MovimentoMu, MovimentoSigma, 1)  
#
#CorrecaoArtificialRand = np.random.lognormal(CorrecaoMu, CorrecaoSigma, len(Correcao))
for i in range(len(Correcao)):
  #CorrecaoArtificial = np.append(CorrecaoArtificial,0)
  WarmUP = round(Tamanho * 0.1) + i
  CorrecaoArtificial = np.append(CorrecaoArtificial,CorrecaoArtificialRand[WarmUP])
  #CorrecaoArtificial[i] = np.random.lognormal(CorrecaoMu, CorrecaoSigma, 1)

# Gerar Pontos Artificiais
for i in range(len(MovimentoArtificial)):
  PontoArtificial = np.append(PontoArtificial,0)
  if i == 0:
    PontoArtificial[i] = Fechamento[0]
    Impar = True
    Par = False
    j = 0
    k = 0
  else:
    if Par == True:  
      PontoArtificial[i] = PontoArtificial[i-1] * (1 + MovimentoArtificial[j])
      j+=1
      Par = False
      Impar = True
    else:
      if Impar == True:
        PontoArtificial[i] = PontoArtificial[i-1] * (1 - CorrecaoArtificial[k])
        k+=1
        Impar = False
        Par = True
  #Depurar
  #print(i,PontoArtificial[i],j,MovimentoArtificial[j],k,CorrecaoArtificial[k]) 
#TODO: Continuar implementando a geração de números randômicos obedecendo a probabilidade de cada classe acontecer
#TODO: Criar rotina para entrar e sair na operação de compra ou venda
#TODO: Usar conceitos de Replicação e Rodada com base no intervalo de confiança  
#TODO: Verificar porque os dados randômicos não estão gerando valores acompanhando as máximas do ativo
# Imprimir dados de fechamento reais com SARParabolic e pontos artificiais
fig = plt.figure(figsize=(20, 25)) 
fig2 = plt.figure(figsize=(20, 25)) 
fig.suptitle('Resultados Reais e Artificiais - Criptomoeda ADA',fontsize=20)
fig2.suptitle('Histograma - Criptomoeda ADA',fontsize=20)
spec = fig.add_gridspec(ncols=2, nrows=5)
#
axs1 = fig.add_subplot(spec[0, :])
axs2 = fig.add_subplot(spec[2, :])
axs3 = fig.add_subplot(spec[4, :])
#
axs1.plot(Fechamento,'-o',SARParabolic,'sg')
axs1.set_title('Dados Fechamento Reais')
axs1.set_xlabel('Iteração')
axs1.set_ylabel('Preço de Fechamento')
#
axs2.plot(PontoArtificial,'-sg')
axs2.set_title('Pontos Artificiais')
axs2.set_xlabel('Pontos')
axs2.set_ylabel('Preço de Fechamento')
#
#axs3.plot(MovimentoArtificialRandAcumulado[WarmUP:],'-+',CorrecaoArtificialRandAcumulado[WarmUP:],'--')
axs3.plot(MovimentoArtificialRandAcumulado,'-+',CorrecaoArtificialRandAcumulado,'--')
axs3.set_title('Acumulados Randômicos: Movimento Artificial & Correção Artificial')
axs3.set_xlabel('Iteração')
axs3.set_ylabel('Valores Randômicos')
# Imprimir histogramas
axs4 = fig2.add_subplot(spec[0,0])
axs5 = fig2.add_subplot(spec[0,1])
axs6 = fig2.add_subplot(spec[2,0])
axs7 = fig2.add_subplot(spec[2,1])
#
axs4.hist(Movimento,10,color='green')
axs4.set_title('Movimento Real')
axs4.set_xlabel('Pontos')
axs4.set_ylabel('Preços de Fechamento')
#
axs5.hist(Correcao,10,color='red')
axs5.set_title('Correção Real')
axs5.set_xlabel('Pontos')
axs5.set_ylabel('Preços de Fechamento')
#
axs6.hist(MovimentoArtificial,10,color='green')
axs6.set_title('Movimento Artificial')
axs6.set_xlabel('Pontos')
axs6.set_ylabel('Preços de Fechamento')
#
axs7.hist(CorrecaoArtificial,10,color='red')
axs7.set_title('Correção Artificial')
axs7.set_xlabel('Pontos')
axs7.set_ylabel('Preços de Fechamento')
#
plt.show()
