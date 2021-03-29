import math
import pandas as pd

def calculateMovingAverage(Distancia):
  count = len(Distancia)
  soma = sum([math.log(Distancia[i]) for i in range(0, count)])

  return soma/count

def calculateStandardDeviation(Distancia, media_mov):
  count = len(Distancia)
  soma = sum([(math.log(Distancia[i]) - media_mov)**2 for i in range(0, count)])

  return (soma/count)**(0.5)

def getCsvValues(path, field):
  data = pd.read_csv(path)[field]

  data = list(reversed(data))
  data[:] = [float(i.replace(',', '.')) for i in data]
  
  return data
  