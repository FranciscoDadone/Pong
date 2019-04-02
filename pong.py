from tkinter import *
import random

class PongApp:
	def __init__(self, root):
		self.width=1280
		self.height=720
		root.geometry("1280x720")
		root.title("Pong!")
		root.bind("<Escape>", lambda e:self.root.quit())
		self.canvas=Canvas(root, bg="black", width=self.width, height=self.height)
		self.canvas.pack()
		self.Game=Game(self.canvas, self.width, self.height, root)

class Game(PongApp):
	def __init__(self, canvas, height, width, root):
		self.canvas=canvas
		self.height=height
		self.width=width
		self.x=self.height/2
		self.y=self.width/2
		self.randomDir=""
		self.xSpeed=0
		self.ySpeed=0
		self.puntosP1P=0
		self.puntosP2P=0

		self.lineaMedio=canvas.create_line(self.height/2, 0, self.height/2, self.width, fill="white", dash=10)
		self.puntosP1=canvas.create_text(self.height/4, 80, fill="white", text=self.puntosP1P, font="Arial 50")
		self.puntosP2=canvas.create_text((self.height-320), 80, fill="white", text=self.puntosP2P, font="Arial 50")

		self.pelota=canvas.create_rectangle(self.x-8,self.y-8,self.x+8,self.y+8, fill="white")
		self.player1=canvas.create_rectangle(20,280,35,420, fill="white")
		self.player2=canvas.create_rectangle(1260,280,1245,420, fill="white")
		self.movimentoPelota()

		root.bind('<Key>', self.movePlayer1)
		root.bind('<Up>', lambda e:self.movePlayer2("up"))
		root.bind('<Down>', lambda e:self.movePlayer2("down"))

	def movePlayer1(self, event):
		print(self.posPlayer1)
		if event.char=="w" or event.char=="W":
			if self.posPlayer1[1]>0:
				self.canvas.move(self.player1, 0, -10)
		elif event.char=="s" or event.char=="S":
			if self.posPlayer1[3]<self.width:
				self.canvas.move(self.player1, 0, 10)

	def movePlayer2(self, arrow):
		if arrow=="up":
			if self.posPlayer2[1]>0:
				self.canvas.move(self.player2, 0, -10)
		elif arrow=="down":
			if self.posPlayer2[3]<self.width:
				self.canvas.move(self.player2, 0, 10)

	def movimentoPelota(self):
		self.canvas.move(self.pelota, self.xSpeed, self.ySpeed)
		self.posPlayer1=self.canvas.coords(self.player1)
		self.posPlayer2=self.canvas.coords(self.player2)
		self.posPelota=self.canvas.coords(self.pelota)
		if self.randomDir=="":
			self.randomDir=random.choice(["+", "-", "+-", "-+"])
		else:
			if self.randomDir=="+":
				self.xSpeed=2
				self.ySpeed=2
				self.randomDir="chosed"
			elif self.randomDir=="-":
				self.xSpeed=-2
				self.ySpeed=-2
				self.randomDir="chosed"
			elif self.randomDir=="+-":
				self.xSpeed=2
				self.ySpeed=-2
				self.randomDir="chosed"
			elif self.randomDir=="-+":
				self.xSpeed=-2
				self.ySpeed=2
				self.randomDir="chosed"
			elif self.randomDir=="chosed":
				pass
		if self.posPelota[3]>=self.width:
			self.ySpeed=-self.ySpeed
		elif self.posPelota[1]<=0:
			self.ySpeed=-self.ySpeed
		elif self.posPelota[2]>=self.height:
			self.xSpeed=-self.xSpeed
			self.punto("player1")
		elif self.posPelota[0]<=0:
			self.xSpeed=-self.xSpeed
			self.punto("player2")
		#Rebote contra las raquetas
		elif self.posPelota[2]<=self.posPlayer1[2]+10 and self.posPelota[1]>=self.posPlayer1[1] and self.posPelota[0]<=self.posPlayer1[0]+10 and self.posPelota[3]<=self.posPlayer1[3]:
			self.xSpeed=-self.xSpeed
			print("pong p1", self.posPelota, self.posPlayer1)
		elif self.posPelota[2]>=self.posPlayer2[2]-10 and self.posPelota[1]>=self.posPlayer2[1] and self.posPelota[0]>=self.posPlayer2[0]-10 and self.posPelota[3]<=self.posPlayer2[3]:
			self.xSpeed=-self.xSpeed
			print("pong p2", self.posPelota, self.posPlayer2)
		root.after(10, self.movimentoPelota)

	def punto(self, p):
		self.canvas.coords(self.pelota, self.x-8,self.y-8,self.x+8,self.y+8)
		self.randomDir=""
		if p=="player1":
			self.puntosP1P+=1
			if self.puntosP1P==5:
				self.winGame("¡Ganó el jugador 1!")
			else:
				self.canvas.itemconfig(self.puntosP1, text=self.puntosP1P)
		elif p=="player2":
			self.puntosP2P+=1
			if self.puntosP2P==5:
				self.winGame("¡Ganó el jugador 2!")
			else:
				self.canvas.itemconfig(self.puntosP2, text=self.puntosP2P)

	def winGame(self, text):
		self.canvas.delete("all")
		self.textWin=self.canvas.create_text(self.height/2, self.width/2, text=text, fill="white", font="Arial 80")

if __name__=="__main__":
	root=Tk()
	p=PongApp(root)
	root.mainloop()