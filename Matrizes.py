import argparse
import csv
import math
import matplotlib.pyplot as plt

class Calculo():
    def __init__(self, matriz, dist):
        # self.matrizNula = [[0, 0, 0, 0, 0, 0], [2, 27.06, 25.07, 29.44, 23.48, 27.85],
        #                    [4, 20.69, 19.10, 35.81, 21.88, 19.50], [6, 17.24, 15.38, 15.12, 16.18, 16.31],
        #                    [8, 16.91, 18.18, 17.47, 18.00, 20.09], [16, 6.86, 4.97, 5.47, 4.77, 5.99],
        #                    [32, 1.15, 1.42, 0.97, 0.92, 2.05]]
        self.matrizNula = matriz
        self.dist = dist
        self.linha = len(self.dist)
        self.coluna = len(self.matrizNula[0])
        self.matrizResistividade = self.transforma_resistividade(self.matrizNula, self.dist)
        self.vetorMedia = [0] * (self.linha)
        self.vetorMediaCorrecao = [0] * (self.linha)
        self.matrizCorrigida = [0] * (self.linha)
        for i in range(self.linha):
            self.matrizCorrigida[i] = [0] * (self.coluna)    
        print(self.matrizResistividade)
        

    def transforma_resistividade(self, matriz, dist): #Como o terrometro mostra a resistencia entre os eletrodos este metodo transformara as resistencias em resistividades
        return [[2*r*math.pi*d for r in matriz[i]] for i, d in enumerate(dist)]

    def media(self): #Este metodo calculara a media das medidas para a mesma distancia
        for i in range(self.linha):
            for j in range(self.coluna):
                self.vetorMedia[i] += self.matrizResistividade[i][j]
                print(self.matrizResistividade[i][j])
            self.vetorMedia[i] /= self.coluna
        print(self.vetorMedia)
        

    def medidas_corretas(self): #Este metodo comparara as resistividades calculadas
        for i in range(self.linha):
            for j in range(self.coluna):
                if(((self.matrizResistividade[i][j] - self.vetorMedia[i]) / self.vetorMedia[i]) * 100 <= 50):
                    self.matrizCorrigida[i][j] = self.matrizResistividade[i][j]
                else:
                    self.matrizCorrigida[i][j] = 0

    def media_correcao(self):
        for i in range(self.linha):
            for j in range(self.coluna):
                self.vetorMediaCorrecao[i] +=  self.matrizCorrigida[i][j]
            self.vetorMediaCorrecao[i] /= (self.coluna)

	
def main():
	# col = int(input("Em quantos locais diferentes as medidas foram realizadas"))
	# lin = int(input("Qual a quantidade de distancias diferentes foram utilizadas para os locais"))
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
		# matriz.transforma_resistividade()
		matriz.media()
		matriz.medidas_corretas()
		matriz.media_correcao()
		plt.plot([2, 4, 6, 8, 16, 32], matriz.vetorMediaCorrecao)
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