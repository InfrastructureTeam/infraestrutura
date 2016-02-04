import argparse
import csv
import math
import matplotlib.pyplot as plt

class Calculo():
    def __init__(self, matriz, dist):
        self.matrizNula = matriz
        self.dist = dist
        self.matrizResistividade = self.transforma_resistividade(self.matrizNula, self.dist)
        self.vetorMedia = [self.media(array) for array in self.matrizResistividade]
        self.matrizCorrigida = self.medidas_corretas(self.matrizResistividade, self.vetorMedia)
        self.vetorMediaCorrecao = [self.media(array) for array in self.matrizCorrigida]
        

    def transforma_resistividade(self, matriz, dist): #Como o terrometro mostra a resistencia entre os eletrodos este metodo transformara as resistencias em resistividades
        ''' isso faz a mesma coisa que o return, usei forma inline porque era mais facil separar as linhas 
        out =[]
        for i, d in enumerate(dist):
        	out.append([])
        	for r in matriz[i]:
        		out[i].append(2*r*math.pi*d)
        '''
        return [[2*r*math.pi*d for r in matriz[i]] for i, d in enumerate(dist)]

    def media(self, array): #Este metodo calculara a media de um array
        return sum(array)/len(array)
        
    def medidas_corretas(self, matriz, media): #Este metodo filtra as resistividades que tem um desvio em relaca a media maior que 50%
        ''' isso faz a mesma coisa que o return, usei forma inline porque era mais facil separar as linhas 
        out = []
        for i, m in enumerate(media): # gostaria de nao usar o enumerate mas nao consegui pensar em uma forma melhor
        	out.append([])
            for r in matriz[i]:
                if(((r - m) / m)<=.5):
                    out[i].append(m)
        '''
        return [[r for r in matriz[i] if(((r - m) / m)<=.5) ] for i, m in enumerate(media)]

	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', help='csv file with data')
	args = parser.parse_args()
	with open(args.file, 'r') as file:
		reader = csv.reader(file, delimiter=',')
		# por simplicidade vou assumir que o numero de colunas -1 e a quantidade de leituras
		header = next(reader)
		data = [[float(item) for item in row] for row in reader] # passa todo mundo para float
		dist = [item[0] for item in data] # distancias
		values = [ item[1:] for item in data] # valores
		matriz = Calculo(values, dist)
		plt.plot(matriz.dist, matriz.vetorMediaCorrecao)
		plt.xlabel('Distancia (m)')
		plt.ylabel('Resistividade (ohm*m)')
		plt.show()
		print(matriz.matrizNula)
		print(matriz.matrizCorrigida)
		print(matriz.vetorMedia)
		print(matriz.matrizResistividade)
		print(matriz.vetorMediaCorrecao)

if __name__ == '__main__':
	main()