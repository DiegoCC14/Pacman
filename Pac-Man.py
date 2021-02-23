from pynput import keyboard as kb
import time , random , os

class MatrizNew():
		def __init__(self,filas,columnas):
				self.matriz = []
				for i in range(filas):
						self.matriz.append(['[ ]']*columnas)

		def mostrarMatriz(self):
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")
				for x in range(len(self.matriz)-1,-1,-1):
						for i in range(len(self.matriz[0])):
								print(self.matriz[x][i],end=" ")
						print("")
				for x in range(len(self.matriz)):
					print("-",end="")
				print("")

class Tablero_Packman(MatrizNew):
	def __init__(self):
		
		MatrizNew.__init__(self,9,7)
		self.Introduce_Bloques_limite()
		self.Frutas = [[0,0],[0,6],[8,0],[8,6]] #Posicion de las frutas
		self.Fantasmas = [Fantasma([4,2],'right') , Fantasma([4,3],'left') , Fantasma([4,4],'left')]#Derecha
		self.Packman = Packman([2,3],'left') #Extremo inferior

	def Introduce_Bloques_limite(self):
		for x in range(1,len(self.matriz),2):
			for y in range(1,len(self.matriz[0]),2):
				self.matriz[x][y] = '▣' #Bloques_Bloqueados

		for x in range(len(self.matriz)):
			for y in range(len(self.matriz[0])):
				if self.matriz[x][y]!='▣':
					self.matriz[x][y] = '□' #Casillas

	def Fantasma_vulnetable(self,condicion_vulnerable):
		for fantasma in self.Fantasmas:
			fantasma.vulnerable = condicion_vulnerable

	def Introduciendo_tablero_Frutas_Fantasma_Packman(self):
		
		for pos_fruta in self.Frutas:
			self.matriz[pos_fruta[0]][pos_fruta[1]] = '✫'
		
		for fants in self.Fantasmas:

			if fants.vulnerable == False: 
				self.matriz[ fants.pos_tablero[0] ][ fants.pos_tablero[1] ] = '☠'
			else:
				self.matriz[ fants.pos_tablero[0] ][ fants.pos_tablero[1] ] = '☑'

		self.matriz[self.Packman.pos_tablero[0]][self.Packman.pos_tablero[1]] = '♚'
	
	def Borrando_Fantasmas_Packman(self):
		for fants in self.Fantasmas:
			self.matriz[fants.pos_tablero[0]][fants.pos_tablero[1]] = '□'
		self.matriz[self.Packman.pos_tablero[0]][self.Packman.pos_tablero[1]] = '□'

	def Verificando_Estados(self):
		
		if self.Packman.tiempo_fantasma_indefenso == 0:
			self.Fantasma_vulnetable(False)
		else:
			self.Fantasma_vulnetable(True)
			self.Packman.tiempo_fantasma_indefenso -=1

		self.Borrando_Fantasmas_Packman()

		self.Moviendo_Packman()
		self.Moviendo_Fantasmas()
		
		self.Introduciendo_tablero_Frutas_Fantasma_Packman()

		for pos_fruta in self.Frutas:
			if pos_fruta == self.Packman.pos_tablero:
				self.Frutas.remove(pos_fruta)
				self.Packman.tiempo_fantasma_indefenso += 17
				break

		for fants in self.Fantasmas:
			if fants.pos_tablero == self.Packman.pos_tablero:
				
				if fants.vulnerable == True:
					self.Fantasmas.remove(fants)
					self.Packman.Aumenta_Puntuacion()
				else:
					self.Packman.vivo = False
					return() #Terminamos juego 

		for fants in self.Fantasmas: #Calculamos los posibles movimientos de fantasmas
			fants.Posibles_Movimientos(self.matriz)
		self.Packman.Posibles_Movimientos(self.matriz)

		

	def Moviendo_Fantasmas(self):
		for fants in self.Fantasmas:
			fants.Moviendose_en_direccion()

	def Moviendo_Packman(self):
		if self.Packman.direccion == 'up' and self.Packman.pos_tablero[0]+1 < len(self.matriz):
			self.Packman.Moviendose_en_direccion()
		elif self.Packman.direccion == 'down' and self.Packman.pos_tablero[0]-1 >=0:
			self.Packman.Moviendose_en_direccion()
		elif self.Packman.direccion == 'left' and self.Packman.pos_tablero[1]+1 < len(self.matriz[0]):
			self.Packman.Moviendose_en_direccion()
		elif self.Packman.direccion == 'right' and self.Packman.pos_tablero[1]-1 >= 0:
			self.Packman.Moviendose_en_direccion()
			

class Seres_Juego():
	def __init__(self,pos_tabl,dir_inicial):
		self.direccion = dir_inicial
		self.pos_tablero = pos_tabl
		self.posibles_movimientos = [] #Lista que contendra los posibles movimientos

	def Moviendose_en_direccion(self):
		
		if self.direccion == 'left':
			self.pos_tablero[1] +=  1
		
		elif self.direccion == 'right':
			self.pos_tablero[1] -=  1

		elif self.direccion == 'up':
			self.pos_tablero[0] += 1

		elif self.direccion == 'down':
			self.pos_tablero[0] -= 1

	def Posibles_Movimientos(self,tablero):
		self.posibles_movimientos = [] 
		if self.pos_tablero[0]+1 < len(tablero) and tablero[self.pos_tablero[0]+1][self.pos_tablero[1]] != '▣':
			self.posibles_movimientos.append('up')
		if self.pos_tablero[0]-1 >= 0 and tablero[self.pos_tablero[0]-1][self.pos_tablero[1]] != '▣':
			self.posibles_movimientos.append('down')
		if self.pos_tablero[1]+1 < len(tablero[0]) and tablero[self.pos_tablero[0]][self.pos_tablero[1]+1] != '▣':
			self.posibles_movimientos.append('left')
		if self.pos_tablero[1]-1 >= 0 and tablero[self.pos_tablero[0]][self.pos_tablero[1]-1] != '▣':
			self.posibles_movimientos.append('right')


class Fantasma(Seres_Juego):
	def __init__(self,pos_tabl,direccion):
		Seres_Juego.__init__(self,pos_tabl,direccion)
		self.vulnerable = False
	def Movimiendo_random(self):
		if len(self.posibles_movimientos)>1:
			eleccion_dir = random.randint(0,len(self.posibles_movimientos)-1)
			self.direccion = self.posibles_movimientos[eleccion_dir]

class Packman(Seres_Juego):
	def __init__(self,pos_tabl,direccion):
		Seres_Juego.__init__(self,pos_tabl,direccion)
		self.puntuacion = 0 #Por cada fantasma suma puntuacion	
		self.vivo = True
		self.tiempo_fantasma_indefenso = 0

	def Aumenta_Puntuacion(self):
		self.puntuacion += 25

	def Cambio_Direccion(self,direccion_tomada):
		direccion_tomada = str(direccion_tomada)
		direccion_tomada = direccion_tomada[4:len(direccion_tomada)]

		for pos_validas in self.posibles_movimientos:
			if pos_validas == direccion_tomada:
				self.direccion = direccion_tomada




tablero = Tablero_Packman()
tablero.Introduciendo_tablero_Frutas_Fantasma_Packman()

tiempo_vulnerable = 0
with kb.Listener(tablero.Packman.Cambio_Direccion) as keyboart:
	while tablero.Packman.vivo and tablero.Fantasmas!=[]:

		for fants in tablero.Fantasmas:
			fants.Movimiendo_random()

		tablero.Verificando_Estados()
		tablero.mostrarMatriz()		
		time.sleep(0.4)
		
		
		if os.name=='posix': #Borramos la terminal o consola 
	 		os.system('clear')
		else: #Window
			os.system('cls')
		


tablero.mostrarMatriz()
if tablero.Packman.vivo:
	print('Gandor')
else:
	print('Perdiste') 