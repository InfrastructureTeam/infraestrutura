import math
import matplotlib.pyplot as plt

class Calculo():
    def __init__(self, coluna, linha):
        self.matrizNula = [[0, 0, 0, 0, 0, 0], [2, 27.06, 25.07, 29.44, 23.48, 27.85],
                           [4, 20.69, 19.10, 35.81, 21.88, 19.50], [6, 17.24, 15.38, 15.12, 16.18, 16.31],
                           [8, 16.91, 18.18, 17.47, 18.00, 20.09], [16, 6.86, 4.97, 5.47, 4.77, 5.99],
                           [32, 1.15, 1.42, 0.97, 0.92, 2.05]]
        self.matrizResistividade = []
        self.vetorMedia = []
        self.vetorMediaCorrecao = []
        self.matrizCorrigida = []
        self.coluna = coluna
        self.linha = linha

    def gera_matriz(self): # Este metodo gera uma matriz nula
        #self.matrizNula = [0] * self.linha
        self.matrizResistividade = [0] * (self.linha)
        self.matrizCorrigida = [0] * (self.linha)
        self.vetorMedia = [0] * (self.linha - 1)
        self.vetorMediaCorrecao = [0] * (self.linha - 1)
        for i in range(self.linha):
            #self.matrizNula[i] = [0] * (self.coluna + 1)
            self.matrizResistividade[i] = [0] * (self.coluna)
            self.matrizCorrigida[i] = [0] * (self.coluna)

    def transforma_resistividade(self): #Como o terrometro mostra a resistencia entre os eletrodos este metodo transformara as resistencias em resistividades
        for i in range(1, self.linha):
            for j in range(1, self.coluna):
                self.matrizResistividade[i][j] = 2*self.matrizNula[i][j]*math.pi*self.matrizNula[i][0]

    def media(self): #Este metodo calculara a media das medidas para a mesma distancia
        for i in range(1, self.linha):
            for j in range(1, self.coluna):
                self.vetorMedia[i-1] = self.vetorMedia[i-1] + self.matrizResistividade[i][j]
                if j == (self.coluna - 1):
                    self.vetorMedia[i-1] = self.vetorMedia[i-1]/(self.coluna - 1)

    def medidas_corretas(self): #Este metodo comparara as resistividades calculadas
        for i in range(1, self.linha):
            for j in range(1, self.coluna):
                if ((self.matrizResistividade[i][j] - self.vetorMedia[i-1]) / self.vetorMedia[i-1]) * 100 <= 50:
                    self.matrizCorrigida[i][j] = self.matrizResistividade[i][j]
                else:
                    self.matrizCorrigida[i][j] = 0

    def media_correcao(self):
        for i in range(1, self.linha):
            for j in range(1, self.coluna):
                self.vetorMediaCorrecao[i-1] = self.vetorMediaCorrecao[i-1] + self.matrizCorrigida[i][j]
                if j == (self.coluna - 1):
                    self.vetorMediaCorrecao[i-1] = self.vetorMediaCorrecao[i-1]/(self.coluna - 1)

col = int(input("Em quantos locais diferentes as medidas foram realizadas"))
lin = int(input("Qual a quantidade de distancias diferentes foram utilizadas para os locais"))

matriz = Calculo(col + 1, lin + 1)

matriz.gera_matriz()
matriz.transforma_resistividade()
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