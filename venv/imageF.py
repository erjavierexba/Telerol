# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageChops
import numpy as np
import random
import math
import time, signal
import os.path
def gcd(x, y):
	while y != 0:
		(x, y) = (y, x % y)  

	return x
def mallado(tam, filas, columnas, color, forcesquare, grosor):
	imagMallada = Image.new("RGBA", tam,(255,255,255,0))
	x = 0
	y = 0
	if forcesquare == True :
		x = min (tam[0],tam[1])
		y = max (tam[0],tam[1])
		num = gcd(y,x)
		x = num
		y = num
	else:
		x = int(float(tam[0])/float(columnas))	
		y = int(float(tam[1])/float(filas))
	areaCelda = (int(x),int(y))
	draw = ImageDraw.Draw(imagMallada)
	for i in range(1,filas+1):
		draw.line(((0,i*y),(tam[0],i*y)), color, grosor)
	for i in range(1,columnas+1):
		draw.line(((i*x,0),(i*x,tam[1])), color, grosor)
	imagMallada.save("malla.png","PNG")
	return imagMallada, areaCelda
def createDefaultProfilePhoto (color):
	if (os.path.isfile(color[0]+".png")==False):
		im = Image.open('default.png')
		im = im.convert('RGBA')

		data = np.array(im)
		red, green, blue, alpha = data.T
		white_areas = (red == 0) & (blue == 0) & (green == 0)
		data[..., :-1][white_areas.T] = (color[1][0], color[1][1], color[1][2])  # Transpose back needed
		Image.fromarray(data).save("profile-photos/"+color[0]+".png","PNG")
def changeBackground (mapp, bg):
	m1 = Mapa(bg,mapp.meshSize,mapp.meshSquare,mapp.color)
	return m1



def createToken(tam, color, rate, innerColor,tokenR, strToken):
	token = Image.open(strToken)
	tokenRate = token.size
	tokenRate = float(tokenRate[0])/float(tokenRate[1])
	token = token.resize( (int(tam*rate*tokenR*tokenRate),int(tam*rate*tokenR)) ,Image.BILINEAR)
	minTam = min(token.size[0],token.size[1])
	imgFinal = Image.new("RGBA",(tam,tam),(0,0,0,0))
	draw = ImageDraw.Draw(imgFinal)
	draw.ellipse((0,0,tam,tam),color)
	draw.ellipse((tam/2-int(tam*0.5*rate),tam/2-int(tam*0.5*rate),tam/2+int(tam*0.5*rate), tam/2+int(tam*0.5*rate)),innerColor)
	imgAux = Image.new("RGBA", (tam,tam),(0,0,0,0))
	coor =  (tam/2-token.size[0]/2, tam/2-token.size[1]/2,tam/2+token.size[0]/2,tam/2+token.size[1]/2)
	token = token.resize((coor[2]-coor[0],coor[3]-coor[1]), Image.BILINEAR)
	imgAux.paste(token,coor)
	imgFinal= Image.alpha_composite(imgFinal,imgAux)
	return imgFinal







class Mapa:
	def __init__(self, background, meshSize, meshSquare, color, resize, grosor):
		tempImg = Image.open(background)
		tempImg = tempImg.convert("RGBA")
		tempImg = tempImg.resize((int(float(tempImg.size[0])*resize), int(float(tempImg.size[1])*resize)),  Image.BILINEAR)
		self.background= tempImg
		self.meshSize = meshSize
		self.meshSquare = meshSquare
		self.color = color
		self.grosor = grosor		
		self.imageMesh, self.area = mallado(tempImg.size, self.meshSize[0],self.meshSize[1],self.color, self.meshSquare, grosor)	
		self.paint = Image.new("RGBA", tempImg.size,(0,0,0,0))
	def resize(self,size ,filterImage, grosor = 0):
		if grosor == 0 :
			grosor = self.grosor		
		background = self.background.resize(size, filterImage)
		imageMesh = mallado(background.size, self.meshSize[0],self.meshSize[1],self.color, self.meshSquare,self.grosor)	
		paint = self.paint.resize(size, filterImage)
	def painter(self, newPaint, coor= None):
		self.paint.paste(newPaint, box=coor)
	def paintInPosition (self, newPaint, position,square):
		if square == True:
			newPaint=self.boxxed(newPaint)
		tam = self.paint.size
		minTam = min(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))
		maxTam = max(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))	
		if minTam == float(tam[0])/float(self.meshSize[0]):
			newPaint = newPaint.resize((int(minTam)-1-self.grosor/2,int(maxTam)-1-self.grosor/2), Image.BILINEAR)
		else:
			newPaint = newPaint.resize((int(maxTam)-1,int(minTam)-1), Image.BILINEAR)
		coor = ( int(float(tam[0])/float(self.meshSize[0]))*position[0] +1+self.grosor/2, int(float(tam[1])/float(self.meshSize[1]))*position[1]  +1+self.grosor/2)		
		self.painter(newPaint, coor)	
			
	
	def	printMap(self, name= "final"):
		ImgFinal = Image.alpha_composite(self.background, self.imageMesh)
		ImgFinal =  Image.alpha_composite(ImgFinal, self.paint)
		ImgFinal.save(name+ ".png", "PNG")

	def eraseBox(self, position):
		tam = self.paint.size
		minTam = min(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))
		maxTam = max(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))	
		erase = Image.new("RGBA",(int(minTam)-1-self.grosor/2,int(maxTam)-1-self.grosor/2),(0,0,0,0))
		self.paintInPosition(erase,position,False)

	def copy(self, position):
		tam = self.paint.size
		imgToCopy = self.paint.crop(( int(float(tam[0])/float(self.meshSize[0]))*position[0] +1+self.grosor/2, int(float(tam[1])/float(self.meshSize[1]))*position[1]+1+self.grosor/2, int(float(tam[0])/float(self.meshSize[0]))*(position[0]+1) , int(float(tam[1])/float(self.meshSize[1]))*(position[1]+1)))
		return imgToCopy	
	def boxxed(self, img):
		tam = self.paint.size
		minTam = min(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))
		maxTam = max(float(tam[0])/float(self.meshSize[0]), float(tam[1])/float(self.meshSize[1]))	
		res = Image.new("RGBA",(int(minTam)-1-self.grosor/2,int(maxTam)-1-self.grosor/2),(0,0,0,0))
		img = img.resize(((int(minTam)-1-self.grosor/2,int(minTam)-1-self.grosor/2)),Image.BILINEAR)
		if minTam == float(tam[0])/float(self.meshSize[0]):
			res.paste(img,(0,int((maxTam-img.size[1])/2)))
		else:
			res.paste(img,(int((maxTam-img.size[1])/2),0))
		return res
	def move(self, origen, destino):
		imgToCopy = self.copy(origen)
		self.eraseBox(origen)
		tam=imgToCopy.size
		
		if tam[0]> tam[1]:
			cut = ((tam[0]-tam[1])/2,0,tam[0]-((tam[0]-tam[1])/2),tam[1])		
		else:
			cut = (0,(tam[1]-tam[0])/2,tam[0],tam[1]-((tam[1]-tam[0])/2))				
		imgToCopy =	imgToCopy.resize((imgToCopy.size[0]+self.grosor/2,imgToCopy.size[1]+self.grosor/2), Image.BILINEAR)
		self.paintInPosition(imgToCopy, destino,False)
	def paintCircle(self, coor, radius, color):
		draw = ImageDraw.Draw(self.paint)
		draw.ellipse((0+coor[0],0+coor[1],2*radius+coor[0],2*radius+coor[1]), color)
	def paintSquare(self, coor, tam, color):
		draw = ImageDraw.Draw(self.paint)
		draw.polygon(((coor[0],coor[1]),(tam[0]+coor[0],coor[1]),(tam[0]+coor[0],tam[1]+coor[1]),(coor[0],tam[1]+coor[1])), color)


#Ejemplo:
#m1 = Mapa('imgBG nuevo.jpg',(12,12), False, (0,0,0,255), 3.5,5)

#m1.printMap("m1")
'''
m1.paintSquare((400,400),(100,100),(255,255,255,255))
m1.printMap("m2")
createToken(600, (255,0,0,255), 0.8, (255,255,255,255),0.9, "character.png")
'''

