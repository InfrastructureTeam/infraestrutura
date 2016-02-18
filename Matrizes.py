# coding=UTF-8
import argparse
import csv
import math
import matplotlib.pyplot as plt


class Calculo:
    def __init__(self, matriz, dist):
        self.matrizNula = matriz
        self.dist = dist
        self.matrizResistividade = self.transforma_resistividade(self.matrizNula, self.dist)
        self.vetorMedia = [self.media(array) for array in self.matrizResistividade]
        self.matrizCorrigida = self.medidas_corretas(self.matrizResistividade, self.vetorMedia)
        self.vetorMediaCorrecao = [self.media(array) for array in self.matrizCorrigida]
        self.kp = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99]
        self.kn = [-0.1, -0.2, -0.3, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -0.99]
        self.ha = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8]
        self.razaoresistp = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.razaoresistn = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def transforma_resistividade(self, matriz, dist):  # Como o terrometro mostra a resistencia entre os eletrodos este
        # metodo transformara as resistencias em resistividades
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
        
    def medidas_corretas(self, matriz, media):  #Este metodo filtra as resistividades que tem um desvio em relaca a media maior que 50%
        ''' isso faz a mesma coisa que o return, usei forma inline porque era mais facil separar as linhas 
        out = []
        for i, m in enumerate(media): # gostaria de nao usar o enumerate mas nao consegui pensar em uma forma melhor
        	out.append([])
            for r in matriz[i]:
                if(((r - m) / m)<=.5):
                    out[i].append(m)
        '''
        return [[r for r in matriz[i] if(((r - m) / m) <= .5) ] for i, m in enumerate(media)]

    def tipo_de_curva(self):
        """
        Este método verificará o comportamento da curva pxa (self.vetorMediaCorrecao x self.dist) para determinar qual
        extratificação será feita se a curva for somente ascendente ou descendente será realizada a estratificação em
        duas camadas e este método deverá retornar o valor de k, porém se a curva apresentar períodos diferentes de
        ascendencia e descendencia então será realizada a estratificação em várias camadas e este método deverá retornar
        os
        """
        comportamento = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        transposicao = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ascendencia = self.vetorMediaCorrecao[0] - self.vetorMediaCorrecao[1]
        j = 0
        duascamadas = 0  # Esta variavel indica o tipo de estratificacao 1 duas camadas e 0 varias camadas
        if ascendencia < 0:
            comportamento[j] = 1
            for i in range(1, len(self.vetorMediaCorrecao) - 1):
                ascendencia = self.vetorMediaCorrecao[i] - self.vetorMediaCorrecao[i + 1]
                if ascendencia < 0 and comportamento[j] != 1:
                    j += 1
                    comportamento[j] = 1
                    transposicao[j] = self.vetorMediaCorrecao[i]
                elif ascendencia > 0 and comportamento[j] == 1:
                    j += 1
                    comportamento[j] = 0
                    transposicao[j] = self.vetorMediaCorrecao[i]
                elif i == len(self.vetorMediaCorrecao) - 1 and j == 0:
                    duascamadas = 1
        return duascamadas, comportamento, j, transposicao

    # Estratificação em duas camadas
    def resistividade_camada_superior(self, comparacao):
        """
        Este método prolongará a curva pxa (self.vetorMediaCorrecao x self.dist) obtida pelo método de Wenner até
        o eixo y , e o valor de y será a resistividade da primeira camada,portanto esse valor deverá ser retornado por
        este método.
        """
        self.resistividadePrimeira = int(self.vetorMediaCorrecao[0])
        if comparacao == 1:
            while int(self.resistividadePrimeira) % 10 != 0:
                self.resistividadePrimeira += 1
            # print(self.resistividadePrimeira)
            self.papn = self.resistividadePrimeira / self.vetorMediaCorrecao[1]

        else:
            while self.resistividadePrimeira % 10 != 0 and self.resistividadePrimeira > 0:
                self.resistividadePrimeira -= 1
            # print(self.resistividadePrimeira)
            self.papn = self.vetorMediaCorrecao[1] / self.resistividadePrimeira

    def curvas_teoricas(self):
        """
        Este método fará o cálculo das curvas teóricas p(a)/p1 (ou p1/p(a)) x h/a dependendo do sinal de k que será
        retornado pelo método (tipo_de_curva)
        """
        w = 0
        l = 0

        for j in range(0, 10):
            for i in range(0, 10):
                for n in range(1, 1000):
                    w += math.pow(self.kp[j], n) * ((1 / math.sqrt(1 + math.pow(2 * n * self.ha[i], 2))) -
                                                    (1 / math.sqrt(4 + math.pow(2 * n * self.ha[i], 2))))
                self.razaoresistp[j][i] = 1 / (1 + 4 * w)
                w = 0
        for j in range(0, 10):
            for i in range(10):
                for n in range(1, 1000):
                    l += math.pow(self.kn[j], n) * ((1 / math.sqrt(1 + math.pow(2 * n * self.ha[i], 2))) -
                                                    (1 / math.sqrt(4 + math.pow(2 * n * self.ha[i], 2))))
                    # print(l)
                self.razaoresistn[j][i] = 1 + 4 * l
                l = 0

    def tabela_k_ha_h(self):
        """
        Este método retornará uma tabela dos valores de K h/a e h, para isso será necessário escolher um valor qualquer
        de espaçamento na curva (self.vetorMediaCorrecao x self.dist) e pegar o valor de resistividade relacionado
        , após isso esse valor será utilizado na razão p(a)/p1 (ou p1/p(a)) dependendo do valor de k, com o valor da
        razão serão pegos todos h/a do método (curvas_teoricas) que se relacionam com o valor da razão,então esses
        valores de h/a serão multiplicados pelo valor de espaçamento aleatório escolhido anteriormente, assim teremos os
        valores de h após isso será escolhido outro valor de espaçamento aleatório e o processo será repitido.
        """
        pass

    def curva_kh(self):
        """
        Com as tabelas retornadas no método(tabela_k_ha_h) esse método plotará as curvas K x h
        """
        pass

    def encontro_das_curvas(self):
        """
        Com as duas curvas esse método encontrará a intersecção entre elas e retornará o valor de h que será a altura da
        primeira camada.
        """
        pass

    # Estratificação método de Pirson para várias camadas
    def altura_segunda_camada(self):
        """
        Este método calculará a profundidade da segunda camada utilizando a fórmula de Lancaster-Jones,e a retornará
        """
        pass
    def resistividade_terceira(self):
        """
        Este método calculará a resistividade da terceira camada
        """
        pass

    # Dimensionamento de sistemas de aterramento
    # Resistividade aparente
    def resistividade_aparente(self):
        """
        Este método retornará a resistividade aparente do solo
        """
        pass


    def hummel(self, profundidade, solo):
        '''
        Este metodo calcula a resistividade aparente de uma haste utilizando a formula de Hummel para um solo de varias
        camadas
        '''
        dividendo = profundidade
        divisor = 0
        for camada in solo:
            if(profundidade<camada[0]):
                divisor += profundidade/camada[1]
                break
            divisor+=camada[0]/camada[1]
            profundidade-=camada[0]
        roa = dividendo/divisor
        return roa

    def haste_vertical(self, haste):
        '''
        f(g) para uma haste vertical
        '''
        return (1/(2*math.pi*haste[0]))*(math.log((4*haste[0])/haste[1]))


    def resistencia_haste(self, haste, solo):
        """
        Este método calculará a resistência do sistema de aterramento com uma haste vertical do tipo cantoneira ou
        circular
        """
        roa = self.hummel(haste[0], solo)
        r = roa * self.haste_vertical(haste)
        return r

    def resistencia_hastes_mesma_distancia(self, haste, solo, distancia, num_hastes):
        """
        Este método calculará a resistência do sistema de aterramento com hastes em paralelo igualmente espaçadas
        """
        roa = self.hummel(haste[0], solo)
        num_hastes = 4
        haste=[2.4, 0.0127]
        d = [distancia*i for i in range(num_hastes)] # distancia de cada haste em relacao a primeira haste
        r = np.array([[0.0]*num_hastes]*num_hastes)
        for i in range(num_hastes):
            for j in range(num_hastes):
                if(i==j):
                    r[i][i] = self.haste_vertical(haste) # f(g)*roa das hastes sem presenca das outras
                e = abs(d[j] - d[i])
                b = math.sqrt(e**2 + haste[0]**2)
                p = (((b + haste[0])**2)-e**2)/((e**2)-(b-haste[0])**2)
                r[i][j] = roa*(1/(4*math.pi*haste[0]))*math.log(p)
        rt = 1/sum([1/sum(e) for e in r])
        return rt

    def resistencia_hastes_triangulo(self):
        """
        Este método calculará a resistência do sistema de aterramento com hastes em triângulo
        """
        pass

    def resistencia_quadrado_vazio(self):
        """
        Este método calculará a resistência do sistema de aterramento com hastes em quadrado vazio
        """
        pass

    def resistencia_hastes_circunferencia(self):
        """
        Este método calculará a resistência do sistema de aterramento com hastes em circunferência
        """
        pass

    def resistencia_anel(self):
        """
        Este método calculará a resistência do sistema de aterramento de condutores enrrolados em forma de anel
        enterrados horizontalmente
        """
        pass

    def resistencia_condutor_horizontal(self):
        """
        Este método calculará a resistência do sistema de aterramento com condutor enterrado horizontalmente no solo
        """
        pass

    def resistencia_angulo_reto(self):
        """
        Este método calculará a resistência do sistema de aterramento com dois condutores em angulo reto
        """
        pass

    def resistencia_estrela_tres(self):
        """
        Este método calculará a resistência do sistema de aterramento em estrela com três pontas
        """
        pass

    def resistencia_estrela_quatro(self):
        """
        Este método calculará a resistência do sistema de aterramento em estrela com quatro pontas
        """
        pass

    def resistencia_estrela_seis(self):
        """
        Este método calculará a resistência do sistema de aterramento em estrela com seis pontas
        """
        pass

    def resistencia_malha(self):
        """
        Este método calculará a resistência da Malha de terra
        """
        pass

    def potencial_toque(self):
        """
        Este método calcula o potencial de toque
        """
        pass

    def potencial_passo(self):
        """
        Este método calcula o potencial de passo
        """
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='csv file with data')
    args = parser.parse_args()
    with open(args.file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        # por simplicidade vou assumir que o numero de colunas -1 e a quantidade de leituras
        header = next(reader)
        data = [[float(item) for item in row] for row in reader]  # passa todo mundo para float
        dist = [item[0] for item in data]  # distancias
        values = [item[1:] for item in data]  # valores
        matriz = Calculo(values, dist)
        duas, alteracao, quantidade, transicao = matriz.tipo_de_curva()
        matriz.resistividade_camada_superior(alteracao[0])
        matriz.curvas_teoricas()
        # plt.plot(matriz.dist, matriz.vetorMediaCorrecao)
        plt.plot(matriz.ha, matriz.razaoresistp[0], matriz.ha, matriz.razaoresistp[1], matriz.ha,
        matriz.razaoresistp[2], matriz.ha, matriz.razaoresistp[3], matriz.ha, matriz.razaoresistp[4],
        matriz.ha, matriz.razaoresistp[5], matriz.ha, matriz.razaoresistp[6], matriz.ha, matriz.razaoresistp[7],
        matriz.ha, matriz.razaoresistp[8], matriz.ha, matriz.razaoresistp[9])
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
