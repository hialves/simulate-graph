import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
import matplotlib.gridspec as gridspec

from helpers import calculateMovingAverage, calculateStandardDeviation, getCsvValues

# Função para Calcular a Precisão
def ObterPrecisaoH(TamanhoAmostra,DesvioPadrao,Alfa):
  TabelaStudentT = pd.read_csv("https://raw.githubusercontent.com/cgionc/SimuladorBotAtivoFinanceiro/main/TabelaStudentT.csv")
  TAlfa = str(float(Alfa) / 2)
  TabelaStudentTAlfa = TabelaStudentT[TAlfa]
  TabelaStudentTN = TabelaStudentT['v']
  NStudent = TamanhoAmostra - 1
  t = 0
  for i in range(len(TabelaStudentTAlfa)):
    if NStudent == TabelaStudentTN[i]:
      t = TabelaStudentTAlfa[i]
    elif NStudent >= 30 and NStudent < 32:
        t = TabelaStudentTAlfa[29]
    elif NStudent >= 32 and NStudent < 34:
        t = TabelaStudentTAlfa[30]  
    elif NStudent >= 34 and NStudent < 36:
        t = TabelaStudentTAlfa[31] 
    elif NStudent >= 36 and NStudent < 38:
        t = TabelaStudentTAlfa[32]   
    elif NStudent >= 38 and NStudent < 40:
        t = TabelaStudentTAlfa[33]   
    elif NStudent >= 40 and NStudent < 42:
        t = TabelaStudentTAlfa[34]
    elif NStudent >= 42 and NStudent < 44:
        t = TabelaStudentTAlfa[35]
    elif NStudent >= 44 and NStudent < 46:
        t = TabelaStudentTAlfa[36]
    elif NStudent >= 46 and NStudent < 48:
        t = TabelaStudentTAlfa[37]
    elif NStudent >= 48 and NStudent < 50:
        t = TabelaStudentTAlfa[38]
    elif NStudent >= 50 and NStudent < 52:
        t = TabelaStudentTAlfa[39]
    elif NStudent >= 52 and NStudent < 54:
        t = TabelaStudentTAlfa[40]
    elif NStudent >= 54 and NStudent < 56:
        t = TabelaStudentTAlfa[41]
    elif NStudent >= 56 and NStudent < 58:
        t = TabelaStudentTAlfa[42]
    elif NStudent >= 58 and NStudent < 60:
        t = TabelaStudentTAlfa[43]
    elif NStudent >= 60 and NStudent < 120:
        t = TabelaStudentTAlfa[44]
    elif NStudent == 120:
        t = TabelaStudentTAlfa[45]      
    elif NStudent > 120:
        t = TabelaStudentTAlfa[46]  
  # 
  print('TTTTTTTTTTTT', t)
  ValorPrecisao = t * (DesvioPadrao / math.sqrt(TamanhoAmostra))
  return ValorPrecisao
# Função para Estimar o valor de N  
def EstimarNnovo(TamanhoAmostra,Hpretendido,Hestimado):
  Nestimado = round(TamanhoAmostra * pow((Hestimado / Hpretendido),2))
  return Nestimado

# Inicializar variáveis
#
PontoA = 0.0
PontoB = 0.0
DistanciaAB = 0.0
#
Tendencia = 'Baixa'
AtingiuLimiar = 'Não'
#
Indice = np.array([])
SARParabolic = np.array([])
Fechamento = np.array([])
Movimento = np.array([])
Correcao = np.array([])
MovimentoArtificial = np.array([])
MovimentoArtificialRand = np.array([])
MovimentoArtificialRandAcumulado = np.array([])
MovimentoArtificialRandAcumuladoMedio = np.array([])
CorrecaoArtificial = np.array([])
CorrecaoArtificialRand = np.array([])
CorrecaoArtificialRandAcumulado = np.array([])
CorrecaoArtificialRandAcumuladoMedio = np.array([])
PontoArtificial = np.array([])

# Importar dados reais do arquivo de trace do ativo
DadosFechamentoOrdenados = getCsvValues('mglu3.csv', 'Último')
# Considerar todo o arquivo de trace
TamanhoReal = len(DadosFechamentoOrdenados)
# Somente os preços de fechamento de 0 até Tamanho Real
for i in range(TamanhoReal):
  Fechamento = np.append(Fechamento,i)
  Fechamento[i] = DadosFechamentoOrdenados[i]

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
    if AtingiuLimiar == 'Sim':
      AtingiuLimiar = 'Não'
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
          else:  
            if DistanciaAB < 0:
              Correcao = np.append(Correcao,abs(DistanciaAB))            
      else: #Tendencia == 'Baixa'
        Tendencia = 'Alta' 
        # Encontrar maior ponto do vetor
        PontoB = SARParabolic[i]
        # Calcular Movimento  
        if PontoA > 0:
          DistanciaAB = (PontoB - PontoA)  / PontoA
          if DistanciaAB > 0:
            Movimento = np.append(Movimento,DistanciaAB)
          else:
            if DistanciaAB < 0:  
              Correcao = np.append(Correcao,abs(DistanciaAB))
    else: #AtingiuLimiar == 'Não':  
      # Atualizar o valor de SARParabolic com fator de 0.02   
      fator = 0.02
      if Tendencia == 'Alta':
        SARParabolic[i] = SARParabolic[i-1] * (1+fator)
      else: #Tendencia == 'Baixa':
        SARParabolic[i] = SARParabolic[i-1] * (1-fator)
      # Verificar se o Fechamento atingiu o limiar para mudar o sentido da tendência       
      if Tendencia == 'Alta':
        if Fechamento[i] < SARParabolic[i]:
          AtingiuLimiar = 'Sim'
      else: #Tendencia == 'Baixa':
        if Fechamento[i] > SARParabolic[i]:
          AtingiuLimiar = 'Sim'    
####################################################
# Calcular Média e Desvio Padrão usando Logaritmo
#
if len(Movimento) > 1 and len(Correcao) > 1:
  # Mu calculado para Lognormal
  MovimentoMu = calculateMovingAverage(Movimento)
  # Sigma calculado para Lognormal
  MovimentoSigma = calculateStandardDeviation(Movimento,MovimentoMu)
  # Mu calculado para Lognormal
  CorrecaoMu = calculateMovingAverage(Correcao)
  # Sigma calculado para Lognormal
  CorrecaoSigma = calculateStandardDeviation(Correcao,CorrecaoMu)
else:
  MovimentoMu = 0
  MovimentoSigma = 0
  CorrecaoMu = 0
  CorrecaoSigma = 0
####################################################
# Se o N estimado não for atendido, será preciso gerar mais números randômicos
print('Digite a quantidade inicial de Pontos Artificiais')
AmostraPiloto = int(input())
if AmostraPiloto > 2:
  # Metade para Movimento e metade para Correção
  Amostra = round(AmostraPiloto / 2)
  #TamanhoArtificial = Amostra
else:
  #TamanhoArtificial = 2
  Amostra = 2
#
MovimentoArtificialHpretendido = 0.01
CorrecaoArtificialHpretendido = 0.01
#
TamanhoArtificial = Amostra
while (TamanhoArtificial != 0):
  # Inicializar arrays de dados artificiais
  MovimentoArtificial = []
  MovimentoArtificialRand = []
  MovimentoArtificialRandAcumulado = []
  MovimentoArtificialRandAcumuladoMedio = []
  #
  CorrecaoArtificial = []
  CorrecaoArtificialRand = []
  CorrecaoArtificialRandAcumulado = []
  CorrecaoArtificialRandAcumuladoMedio = []
  #
  PontoArtificial = []
  # Gerar dados artificiais
  #
  # Gerar todos os valores artificiais dos arrays de Movimento e Correção com a mesma semente e de uma única vez
  MovimentoArtificialRand = np.random.lognormal(MovimentoMu, MovimentoSigma, TamanhoArtificial)
  CorrecaoArtificialRand = np.random.lognormal(CorrecaoMu, CorrecaoSigma, TamanhoArtificial)
  # Acumular a média de números randômicos para analisar posteriormente
  for i in range(TamanhoArtificial):
    MovimentoArtificialRandAcumulado = np.append(MovimentoArtificialRandAcumulado,MovimentoArtificialRand[0])  
    MovimentoArtificialRandAcumuladoMedio = np.append(MovimentoArtificialRandAcumuladoMedio,0)  
    CorrecaoArtificialRandAcumulado = np.append(CorrecaoArtificialRandAcumulado,CorrecaoArtificialRand[0])
    CorrecaoArtificialRandAcumuladoMedio = np.append(CorrecaoArtificialRandAcumuladoMedio,0)
    if i > 0:
      MovimentoArtificialRandAcumulado[i] = MovimentoArtificialRandAcumulado[i-1] + MovimentoArtificialRand[i]
      CorrecaoArtificialRandAcumulado[i] = CorrecaoArtificialRandAcumulado[i-1] + CorrecaoArtificialRand[i]
      MovimentoArtificialRandAcumuladoMedio[i] = MovimentoArtificialRandAcumulado[i] / i
      CorrecaoArtificialRandAcumuladoMedio[i] = CorrecaoArtificialRandAcumulado[i] / i 
  WarmUP = 0.001
  Transitorio = round(WarmUP * TamanhoArtificial)
  for i in range(TamanhoArtificial):
    if i >= Transitorio:
      MovimentoArtificial = np.append(MovimentoArtificial,MovimentoArtificialRand[i])
      CorrecaoArtificial = np.append(CorrecaoArtificial,CorrecaoArtificialRand[i])    

  # Gerar Pontos Artificiais
  Permanente = TamanhoArtificial - Transitorio
  for i in range(Permanente):
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

  # Recalcula o novo desvio padrão para saber se é hora de parar
  MovimentoArtificialMediaNovo = np.mean(MovimentoArtificial)
  MovimentoArtificialDesvioPadraoNovo = np.std(MovimentoArtificial)
  CorrecaoArtificialMediaNovo = np.mean(CorrecaoArtificial)
  CorrecaoArtificialDesvioPadraoNovo = np.std(CorrecaoArtificial)
  # Alfa para 99% = 0.01; Alfa para 95% = 0.05; Alfa para 90% = 0.10; Alfa para 80% = 0.20
  MovimentoArtificialH = ObterPrecisaoH(TamanhoArtificial,MovimentoArtificialDesvioPadraoNovo,'0.20')
  MovimentoArtificialN = EstimarNnovo(TamanhoArtificial,MovimentoArtificialHpretendido,MovimentoArtificialH)
  #  
  CorrecaoArtificialH = ObterPrecisaoH(TamanhoArtificial,CorrecaoArtificialDesvioPadraoNovo,'0.20')
  CorrecaoArtificialN = EstimarNnovo(TamanhoArtificial,CorrecaoArtificialHpretendido,CorrecaoArtificialH)
  #
  if (MovimentoArtificialH > MovimentoArtificialHpretendido) or (CorrecaoArtificialH > CorrecaoArtificialHpretendido):
    if MovimentoArtificialH > CorrecaoArtificialH:
      TamanhoArtificial = MovimentoArtificialN    
    else:
      if MovimentoArtificialH < CorrecaoArtificialH:
        TamanhoArtificial = CorrecaoArtificialN
  else:
    TamanhoArtificial = 0
  if TamanhoArtificial > 0:  
    print('Amostra Inicial = ',Amostra,' Replicação com N estimado =',TamanhoArtificial)   

  # mm = calculateMovingAverage(MovimentoArtificial) 
  mm = calculateMovingAverage(Fechamento)
  print(mm - MovimentoArtificialH, '<= u <', mm + MovimentoArtificialH)

print((calculateMovingAverage(MovimentoArtificial) + calculateMovingAverage(CorrecaoArtificial)) / 2)
print('media dados de fechamento', calculateMovingAverage(Fechamento))
print('mm', mm)
print('MovimentoArtificialH', MovimentoArtificialH)

#
#Fibonacci = 0.5
Fibonacci = 0.382
# Fibonacci = 0.618
#
P1 = np.array([])
P2 = np.array([])
P3 = np.array([])
#
Gatilho = np.array([])
StopLoss = np.array([])
StopGain = np.array([])
#
Saldo = 0.0
SaldoAcumulado = np.array([])
#
for i in range(round(len(PontoArtificial)/3)):
  if i == 0:
    Operacao = ''
    P1 = np.append(P1,PontoArtificial[0])
    P2 = np.append(P2,PontoArtificial[1])
    P3 = np.append(P3,PontoArtificial[2])
    Posicao = P1[0]
  else:
    P1 = np.append(P1,PontoArtificial[i+0])
    P2 = np.append(P2,PontoArtificial[i+1])
    P3 = np.append(P3,PontoArtificial[i+2])
  # Entrar na Compra se Tendência de Alta
  if P2[i-1] > P1[i-1] and P3[i-1] < P2[i-1] and P3[i-1] > P1[i-1] and Operacao != 'Comprado':
    PosicaoAnterior = Posicao
    Posicao = P2[i-1]
    # print('\n Tentar Comprar em: ',Posicao)      
    Gatilho = np.append(Gatilho,Posicao)
    # Sair da Operação por Reverter Tendência
    if Operacao == 'Vendido':
        Sair = PosicaoAnterior - Posicao
        # print('\n Comprar para Sair da Reversão de Tendência ',Operacao,' com ',Sair)
        SL = 0.0
        SG = 0.0
        Posicao = 0.0
        Saldo = Saldo + Sair
        # print('\n Saldo Parcial = ',Saldo)
        Operacao = 'Observando'    
    else:
      if P3[i] > Posicao:
        Operacao = 'Comprado'
        SL = P2[i]
        SG = P1[i] * (1 + MovimentoArtificial[i-1])
        StopLoss = np.append(StopLoss,SL)
        StopGain = np.append(StopGain,SG)        
        # print('\n Comprado em ',Posicao,' Stop Loss: ',SL,' Stop Gain: ',SG)      
      # else:  
          # print('\n Desistiu da Compra')  
  # Entrar na Venda se Tendência de Baixa
  else:
    if P2[i-1] < P1[i-1] and P3[i-1] > P2[i-1] and P3[i-1] < P1[i-1] and Operacao != 'Vendido':
      PosicaoAnterior = Posicao
      Posicao = P2[i-1]
      # print('\n Tentar Vender em: ',Posicao)  
      Gatilho = np.append(Gatilho,Posicao)
      # Sair da Operação por Reverter Tendência
      if Operacao == 'Comprado':
        Sair = Posicao - PosicaoAnterior
        # print('\n Vender para Sair da Reversão de Tendência ',Operacao,' com ',Sair)
        SL = 0.0
        SG = 0.0
        Posicao = 0.0
        Saldo = Saldo + Sair
        # print('\n Saldo Parcial = ',Saldo)
        Operacao = 'Observando'    
      else:  
        if P3[i] < Posicao:
          Operacao = 'Vendido'        
          SL = P2[i]
          SG = P1[i] * (1 - CorrecaoArtificial[i-1])
          StopLoss = np.append(StopLoss,SL)
          StopGain = np.append(StopGain,SG)        
          # print('\n Vendido em ',Posicao,' Stop Loss: ',SL,' Stop Gain: ',SG)  
        # else:  
          # print('\n Desistiu da Venda')
    # else:
      # print('\n Observar')  
  # print('\n Pontos Encontrados: P1=',P1[i],'P2=',P2[i],'P3=',P3[i])  

  # Verificar se houve Perda ou Ganho por SL ou SG
  if Operacao == 'Comprado':
    if P1[i] < SL or P2[i] < SL or P3[i] < SL:
      Perda = SL - Posicao
      # print('\n Perda',Operacao,' de ',Perda)      
      SL = 0.0
      SG = 0.0
      Posicao = 0.0
      Saldo = Saldo + Perda
      # print('\n Saldo Parcial = ',Saldo)
      Operacao = 'Observando'    
    else:
      if P1[i] >= SG or P2[i] >= SG or P3[i] >= SG:
        Ganho = SG - Posicao
        # print('\n Ganho',Operacao,' de ',Ganho)
        SL = 0.0
        SG = 0.0
        Posicao = 0.0
        Saldo = Saldo + Ganho
        # print('\n Saldo Parcial = ',Saldo)
        Operacao = 'Observando'    
  #        
  else:
    if Operacao == 'Vendido':
      if P1[i] > SL or P2[i] > SL or P3[i] > SL:
        Perda = Posicao - SL
        # print('\n Perda',Operacao,' de ',Perda)
        SL = 0.0
        SG = 0.0
        Posicao = 0.0
        Saldo = Saldo + Perda
        # print('\n Saldo Parcial = ',Saldo)
        Operacao = 'Observando'        
      else:
        if P1[i] <= SG or P2[i] <= SG or P3[i] <= SG:
          Ganho = Posicao - SG
          # print('\n Ganho',Operacao,' de ',Ganho)
          Posicao = 0.0
          SL = 0.0
          SG = 0.0
          Saldo = Saldo + Ganho
          # print('\n Saldo Parcial = ',Saldo)
          Operacao = 'Observando'        
    #          
    else:
      SaldoAcumulado = np.append(SaldoAcumulado,Saldo)
#
####################################################
#TODO: Verificar porque os dados randômicos não estão gerando valores acompanhando as máximas do ativo
####################################################
# Imprimir dados de fechamento reais com SARParabolic e pontos artificiais
fig = plt.figure(figsize=(25, 35)) 
fig.suptitle('Resultados Reais e Artificiais do Simulador',fontsize=20)
spec = fig.add_gridspec(ncols=2, nrows=6)
#
axs0 = fig.add_subplot(spec[0, :])
axs1 = fig.add_subplot(spec[1, :])
axs2 = fig.add_subplot(spec[2, :])
axs3 = fig.add_subplot(spec[3, :])
#
axs0.plot(P1[0:AmostraPiloto],'s-b',P2[0:AmostraPiloto],'s-c',P3[0:AmostraPiloto],'s-y')
axs0.set_title('Dados Pontos Relevantes P1, P2 e P3')
axs0.set_xlabel('Iteração')
axs0.set_ylabel('Preço de Fechamento')
#
axs1.plot(Fechamento[0:AmostraPiloto],'-o',SARParabolic[0:AmostraPiloto],'sy')
axs1.set_title('Dados Fechamento Reais')
axs1.set_xlabel('Iteração')
axs1.set_ylabel('Preço de Fechamento')
#
axs2.plot(PontoArtificial[0:AmostraPiloto],'-sg')
axs2.set_title('Pontos Artificiais')
axs2.set_xlabel('Pontos')
axs2.set_ylabel('Pontos de Movimento e Correção')
#
axs3.plot(MovimentoArtificialRandAcumuladoMedio,'-+',CorrecaoArtificialRandAcumuladoMedio,'--')
axs3.set_title('Acumulados Randômicos: Movimento Artificial & Correção Artificial')
axs3.set_xlabel('Iteração')
axs3.set_ylabel('Valores Randômicos')
# Imprimir histogramas
axs4 = fig.add_subplot(spec[4,0])
axs5 = fig.add_subplot(spec[4,1])
axs6 = fig.add_subplot(spec[5,0])
axs7 = fig.add_subplot(spec[5,1])
#
axs4.hist(Movimento,10,color='green')
axs4.set_title('Movimento Real')
axs4.set_xlabel('Pontos')
axs4.set_ylabel('Frequência dos Pontos de Movimento')
#
axs5.hist(Correcao,10,color='red')
axs5.set_title('Correção Real')
axs5.set_xlabel('Pontos')
axs5.set_ylabel('Frequência dos Pontos de Correção')
#
axs6.hist(MovimentoArtificial,10,color='green')
axs6.set_title('Movimento Artificial')
axs6.set_xlabel('Pontos')
axs6.set_ylabel('Frequência dos Pontos de Movimento')
#
axs7.hist(CorrecaoArtificial,10,color='red')
axs7.set_title('Correção Artificial')
axs7.set_xlabel('Pontos')
axs7.set_ylabel('Frequência dos Pontos de Correção')
#
# plt.show()
