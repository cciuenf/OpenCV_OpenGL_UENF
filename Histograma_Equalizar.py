import cv
import sys

class Histograma:

    def __init__(self, imagem_fonte):

        self.imagem_fonte = imagem_fonte
        self.imagem_destino = cv.CloneMat(imagem_fonte)
        self.imagemHistograma = cv.CreateImage((512, 100), 8, 1)
        self.histograma = cv.CreateHist([512], cv.CV_HIST_ARRAY,[[0, 256]], 1)

        self.brilho = 0
        self.contraste = 0

        cv.NamedWindow("Foto Tons Cinza", 1)
        cv.NamedWindow("Foto Equalizada", 1)
        cv.NamedWindow("Histograma Equalizado", 1)

        cv.CreateTrackbar("Brilho", "Histograma Equalizado", 100, 200, self.atualiza_brilho)
        cv.CreateTrackbar("Contraste", "Histograma Equalizado", 100, 200, self.atualiza_contraste)

        self.atualiza_brilhocontraste()

    def calcularHistograma(self):
        cv.CalcArrHist([self.imagem_destino], self.histograma)
        valorMaximoMinimo=cv.GetMinMaxHistValue(self.histograma)
        cv.Rectangle(self.imagemHistograma,(0,0),(512,100), cv.CV_RGB(0,0,0),-1)

        for i in range(512):
			valor = cv.QueryHistValue_1D(self.histograma, i)
			normalizado = cv.Round(valor * 100 / valorMaximoMinimo[1])
			cv.Line(self.imagemHistograma,(i,100),(i,100-normalizado),cv.CV_RGB(255,255,255))

    def atualiza_brilho(self, valor):
        self.brilho = valor - 100
        self.atualiza_brilhocontraste()

    def atualiza_contraste(self, valor):
        self.contraste = valor - 100
        self.atualiza_brilhocontraste()

    def atualiza_brilhocontraste(self):

        if self.contraste > 0:
            delta = 127. * self.contraste / 100
            a = 255. / (255. - delta * 2)
            b = a * (self.brilho - delta)
        else:
            delta = -128. * self.contraste / 100
            a = (256. - delta * 2) / 255.
            b = a * self.brilho + delta

        cv.ConvertScale(self.imagem_fonte, self.imagem_destino, a, b)
        cv.ShowImage("Foto Tons Cinza", self.imagem_destino)
        self.calcularHistograma()
        cv.ShowImage("Histograma", self.imagemHistograma)

        cv.EqualizeHist(self.imagem_destino,self.imagem_destino)
        cv.ShowImage("Foto Equalizada", self.imagem_destino)
        self.calcularHistograma()
        cv.ShowImage("Histograma Equalizado", self.imagemHistograma)

if __name__ == "__main__":
    imagem = cv.LoadImageM('foto.jpg')
    cv.NamedWindow("Foto Original", 0)
    cv.ShowImage("Foto Original", imagem)
    imagem_cinza = cv.GetMat(cv.LoadImage('foto.jpg', 0))
    histograma = Histograma(imagem_cinza)
    cv.WaitKey(0)

