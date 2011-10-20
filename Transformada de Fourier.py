import cv
import sys
import os

def cvShiftDFT(src_arr, dst_arr ):

    size = cv.GetSize(src_arr)
    dst_size = cv.GetSize(dst_arr)

    if dst_size != size:
        cv.Error( cv.CV_StsUnmatchedSizes, "cv.ShiftDFT", "as imagens devem ter tamanhos iguais", __FILE__, __LINE__ )

    if(src_arr is dst_arr):
        tmp = cv.CreateMat(size[1]/2, size[0]/2, cv.GetElemType(src_arr))

    cx = size[0] / 2
    cy = size[1] / 2 # image center

    q1 = cv.GetSubRect( src_arr, (0,0,cx, cy) )
    q2 = cv.GetSubRect( src_arr, (cx,0,cx,cy) )
    q3 = cv.GetSubRect( src_arr, (cx,cy,cx,cy) )
    q4 = cv.GetSubRect( src_arr, (0,cy,cx,cy) )
    d1 = cv.GetSubRect( src_arr, (0,0,cx,cy) )
    d2 = cv.GetSubRect( src_arr, (cx,0,cx,cy) )
    d3 = cv.GetSubRect( src_arr, (cx,cy,cx,cy) )
    d4 = cv.GetSubRect( src_arr, (0,cy,cx,cy) )

    if(src_arr is not dst_arr):
        if( not cv.CV_ARE_TYPES_EQ( q1, d1 )):
            cv.Error( cv.CV_StsUnmatchedFormats, "cv.ShiftDFT", "as imagens devem ter o mesmo formato", __FILE__, __LINE__ )

        cv.Copy(q3, d1)
        cv.Copy(q4, d2)
        cv.Copy(q1, d3)
        cv.Copy(q2, d4)

    else:
        cv.Copy(q3, tmp)
        cv.Copy(q1, q3)
        cv.Copy(tmp, q1)
        cv.Copy(q4, tmp)
        cv.Copy(q2, q4)
        cv.Copy(tmp, q2)


class Transformada:

    def __init__(self, imagem):

        self.imagem = imagem
        self.raio = 0
        cv.NamedWindow( "Transformada de Fourier", 1 )
        cv.NamedWindow( "Inversa da Fourier", 1 )
        cv.CreateTrackbar("Filtro passa baixa", "Transformada de Fourier", self.raio, 50, self.atualiza_versao)
        self.atualiza_foto()


    def atualiza_versao(self, valor):
        self.raio = valor
        self.atualiza_foto()


    def atualiza_foto(self):
		real = cv.CreateImage( cv.GetSize(imagem), cv.IPL_DEPTH_64F, 1)
		imaginario = cv.CreateImage( cv.GetSize(imagem), cv.IPL_DEPTH_64F, 1)
		complexo = cv.CreateImage( cv.GetSize(imagem), cv.IPL_DEPTH_64F, 2)

		cv.Scale(imagem_cinza, real, 1.0, 0.0)
		cv.Zero(imaginario)
		cv.Merge(real, imaginario, None, None, complexo)

		Altura_M = cv.GetOptimalDFTSize( imagem.height - 1 )
		Largura_N = cv.GetOptimalDFTSize( imagem.width - 1 )
		Vetor_dft = cv.CreateMat(Altura_M, Largura_N, cv.CV_64FC2 )

		imagem_Real = cv.CreateImage( (Largura_N, Altura_M), cv.IPL_DEPTH_64F, 1)
		imagem_Imaginaria = cv.CreateImage( (Largura_N, Altura_M), cv.IPL_DEPTH_64F, 1)

		temporario = cv.GetSubRect( Vetor_dft, (0,0, imagem.width, imagem.height))
		cv.Copy( complexo, temporario, None )
		if(Vetor_dft.width > imagem.width):
			temporario = cv.GetSubRect(Vetor_dft, (imagem.width,0, Largura_N - imagem.width, imagem.height))
			cv.Zero( temporario )

		# APLICANDO FOURIER

		cv.DFT( Vetor_dft, Vetor_dft, cv.CV_DXT_FORWARD,complexo.height )

		cv.Split( Vetor_dft,imagem_Real, imagem_Imaginaria, None, None )

		cv.Pow( imagem_Real, imagem_Real, 2.0)
		cv.Pow( imagem_Imaginaria, imagem_Imaginaria, 2.0)
		cv.Add( imagem_Real, imagem_Imaginaria, imagem_Real, None)
		cv.Pow( imagem_Real, imagem_Real, 0.5 )

		cv.AddS( imagem_Real, cv.ScalarAll(1.0), imagem_Real, None )
		cv.Log( imagem_Real, imagem_Real )

		cvShiftDFT(imagem_Real,imagem_Real)
		min, max, pt1, pt2 = cv.MinMaxLoc(imagem_Real)
		cv.Scale(imagem_Real, imagem_Real, 1.0/(max-min), 1.0*(-min)/(max-min))

        #APLICANDO FILTRO passa-baixa circular

		cv.Circle(Vetor_dft,(0,0),self.raio,[0,0,0],-1,1,0)
		cv.Circle(Vetor_dft,(Vetor_dft.cols,0),self.raio,[0,0,0],-1,1,0)
		cv.Circle(Vetor_dft,(0,Vetor_dft.rows),self.raio,[0,0,0],-1,1,0)
		cv.Circle(Vetor_dft,(Vetor_dft.cols,Vetor_dft.rows),self.raio,[0,0,0],-1,1,0)

		cv.Split( Vetor_dft,imagem_Real, imagem_Imaginaria, None, None )
		cv.Pow( imagem_Real, imagem_Real, 2.0)
		cv.Pow( imagem_Imaginaria, imagem_Imaginaria, 2.0)
		cv.Add( imagem_Real, imagem_Imaginaria, imagem_Real, None)
		cv.Pow( imagem_Real, imagem_Real, 0.5 )
		cv.AddS( imagem_Real, cv.ScalarAll(1.0), imagem_Real, None )
		cv.Log( imagem_Real, imagem_Real )
		cvShiftDFT(imagem_Real,imagem_Real)
		min, max, pt1, pt2 = cv.MinMaxLoc(imagem_Real)
		cv.Scale(imagem_Real, imagem_Real, 1.0/(max-min), 1.0*(-min)/(max-min))

		cv.ShowImage("Transformada de Fourier", imagem_Real)

		# APLICANDO A INVERSA de Fourier

		cv.DFT( Vetor_dft, Vetor_dft, cv.CV_DXT_INVERSE_SCALE,Largura_N )
		cv.Split( Vetor_dft,imagem_Real, imagem_Imaginaria, None, None )
		min, max, pt1, pt2 = cv.MinMaxLoc(imagem_Real)
		if((pt1<0) or (pt2>255)):
		    cv.Scale(imagem_Real, imagem_Real, 1.0/(max-min), 1.0*(-min)/(max-min))
		else:
		    cv.Scale(imagem_Real, imagem_Real, 1.0/255, 0)

		cv.ShowImage("Inversa da Fourier", imagem_Real)


if __name__ == "__main__":
    imagem = cv.LoadImageM('foto.jpg')
    imagem_cinza = cv.CreateImage( cv.GetSize(imagem), 8, 1 )
    cv.CvtColor( imagem, imagem_cinza, cv.CV_BGR2GRAY )

    Fourier = Transformada(imagem_cinza)

    print("\nProcessamento de Imagens")
    print("Elisson Michael : UENF")
    print("Trabalho 2 -> Transformada de Fourier \n")
    cv.WaitKey(0)

