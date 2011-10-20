import sys
import cv
import os

class Filtros:
	def __init__(self,imagem_cinza):
		self.imagem_cinza = imagem_cinza
		versao = 0
		cv.NamedWindow("Foto Cinza", 1)
		cv.NamedWindow("Foto Filtrada", 1)
		cv.ShowImage("Foto Cinza",imagem_cinza)
		cv.CreateTrackbar("Filtros", "Foto Cinza", 0, 7, self.atualiza_matriz)
		self.atualiza_matriz(versao)
		
	
	def convolui_com_uma_matriz(self,matriz):
		imagem_resultado = cv.CreateImage( cv.GetSize(imagem), 8, 1 )
		print("Multiplicando ...\n")
		for x in range(imagem.height-1):
			for y in range(imagem.width-1):
				soma,magnitude = 0 , 0
				for i in range(-1,2):
					for j in range(-1,2):
						soma+=(self.imagem_cinza[x+i,y+j]*matriz[i+1][j+1])
				magnitude = abs(soma)
				if magnitude > 255 : magnitude = 255
				imagem_resultado[x,y] = magnitude
		print("Pronto !")
		cv.ShowImage("Foto Filtrada",imagem_resultado)
		
	def convolui_com_duas_matrizes(self,matriz_X,matriz_Y):
		imagem_resultado = cv.CreateImage( cv.GetSize(imagem), 8, 1 )
		print("Multiplicando ...\n")
		for x in range(imagem.height-1):
			for y in range(imagem.width-1):
				soma_X,soma_Y,magnitude = 0 , 0 , 0
				for i in range(-1,2):
					for j in range(-1,2):
						soma_X+=(self.imagem_cinza[x+i,y+j]*matriz_X[i+1][j+1])
						soma_Y+=(self.imagem_cinza[x+i,y+j]*matriz_Y[i+1][j+1])
				magnitude = abs(soma_X) + abs(soma_Y)
				if magnitude > 255 : magnitude = 255
				imagem_resultado[x,y] = magnitude
		print("Pronto !")
		cv.ShowImage("Foto Filtrada",imagem_resultado)
		
	def atualiza_matriz(self,versao):
		os.system('clear')
		if (versao == 0 ):
			print("Laplace [1]")
			matriz = [0,-1,0],\
					 [-1,4,-1],\
					 [0,-1,0]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 1 ):
			print("Laplace [2]")
			matriz = [-1,-1,-1],\
					 [-1,8,-1],\
					 [-1,-1,-1]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 2 ):
			print("Sobel [X]")
			matriz = [-1,-2,-1],\
					 [0,0,0],\
					 [1,2,1]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 3 ):
			print("Sobel [Y]")
			matriz = [-1,0,1],\
					 [-2,0,2],\
					 [-1,0,1]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 4 ):
			print("Sobel [X][Y]")
			matriz_X = [-1,0,1],\
					   [-2,0,2],\
					   [-1,0,1]
			matriz_Y = [-1,-2,-1],\
					   [0,0,0],\
					   [1,2,1]
			self.convolui_com_duas_matrizes(matriz_X,matriz_Y)
		if (versao == 5 ):
			print("Prewitt [X]")
			matriz = [-1,-1,-1],\
					 [0,0,0],\
					 [1,1,1]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 6 ):
			print("Prewitt [Y]")
			matriz = [-1,0,1],\
					 [-1,0,1],\
					 [-1,0,1]
			self.convolui_com_uma_matriz(matriz)
		if (versao == 7 ):
			print("Prewitt [X][Y]")
			matriz_X = [-1,0,1],\
					   [-1,0,1],\
					   [-1,0,1]
			matriz_Y = [-1,-1,-1],\
					   [0,0,0],\
					   [1,1,1]
			self.convolui_com_duas_matrizes(matriz_X,matriz_Y)
		
		
if __name__ == "__main__":
	imagem = cv.LoadImage('foto.jpg')
	imagem_cinza = cv.CreateImage( cv.GetSize(imagem), 8, 1 )
	cv.CvtColor(imagem,imagem_cinza, cv.CV_BGR2GRAY )
	filtros = Filtros(imagem_cinza)
	cv.WaitKey(0) 
	print("Elisson Michael [UENF] : Processamento de Imagens")
