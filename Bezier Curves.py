from graphics import *
import win32api
import math
import time
import random

class bezier3Curve():
	def __init__(self, p1, p2, p3, w):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.w = w

		self.t = 0
		self.bridgeA = (lerp(self.p1[0], self.p2[0], self.t), lerp(self.p1[1], self.p2[1], self.t))
		self.bridgeB = (lerp(self.p2[0], self.p3[0], self.t), lerp(self.p2[1], self.p3[1], self.t))
		self.bPoint = (lerp(self.bridgeA[0], self.bridgeB[0], self.t), lerp(self.bridgeA[1], self.bridgeB[1], self.t))

		self.quality = 10

		self.showedArms = 0
		self.showedDrawing = 0

		self.arm1 = Line(Point(self.p1[0], self.p1[1]), Point(self.p2[0], self.p2[1]))
		self.arm2 = Line(Point(self.p2[0], self.p2[1]), Point(self.p3[0], self.p3[1]))
		self.arm1.setFill("yellow")
		self.arm2.setFill("yellow")

		self.bridge = Line(Point(self.bridgeA[0], self.bridgeA[1]), Point(self.bridgeB[0], self.bridgeB[1]))
		self.bridge.setFill("blue")
		self.bPointCircle = Circle(Point(self.bPoint[0], self.bPoint[1]), 5)
		self.bPointCircle.setFill("red")

	def setCurveQ(self, quality):
		self.quality = quality
		self.curve = []
		for i in range(self.quality):
			self.curve.append(Line(Point(0, 0), Point(0, 0)))
			self.curve[-1].setWidth(4)
			self.curve[-1].draw(self.w)
		self.updateCurve()

	def updateCurve(self):
		for t in range(self.quality):
			self.curve[t].undraw()

			a = self.bridgePoint(t / self.quality)
			b = self.bridgePoint((t + 1) / self.quality)
			self.curve[t].p1 = Point(a[0], a[1])
			self.curve[t].p2 = Point(b[0], b[1])

			self.curve[t].draw(self.w)

	def updatePoints(self, p1, p2, p3):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3

		self.bridgeA = (lerp(self.p1[0], self.p2[0], self.t), lerp(self.p1[1], self.p2[1], self.t))
		self.bridgeB = (lerp(self.p2[0], self.p3[0], self.t), lerp(self.p2[1], self.p3[1], self.t))
		self.bPoint = self.bridgePoint(self.t)

	def bridgePoint(self, t):
		bA = (lerp(self.p1[0], self.p2[0], t), lerp(self.p1[1], self.p2[1], t))
		bB = (lerp(self.p2[0], self.p3[0], t), lerp(self.p2[1], self.p3[1], t))
		return((lerp(bA[0], bB[0], t), lerp(bA[1], bB[1], t)))


	def updateArm(self):
		if(self.showedArms):
			self.arm1.undraw()
			self.arm2.undraw()
			self.bridge.undraw()
			self.bPointCircle.undraw()

			self.arm1.p1 = Point(self.p1[0], self.p1[1])
			self.arm1.p2 = Point(self.p2[0], self.p2[1])

			self.arm2.p1 = Point(self.p2[0], self.p2[1])
			self.arm2.p2 = Point(self.p3[0], self.p3[1])

			self.bridge.p1 = Point(self.bridgeA[0], self.bridgeA[1])
			self.bridge.p2 = Point(self.bridgeB[0], self.bridgeB[1])

			self.bPointCircle.move(self.bPoint[0] - self.bPointCircle.p1.getX() - self.bPointCircle.radius, 
								   self.bPoint[1] - self.bPointCircle.p1.getY() - self.bPointCircle.radius)

			self.arm1.draw(self.w)
			self.arm2.draw(self.w)
			self.bridge.draw(self.w)
			self.bPointCircle.draw(self.w)

	def showArm(self):
		if(self.showedArms == 0): 
			self.showedArms = 1
			self.arm1.draw(self.w)
			self.arm2.draw(self.w)
			self.bridge.draw(self.w)
		else:
			self.showedArms = 0
			self.arm1.undraw()
			self.arm2.undraw()
			self.bridge.undraw()

def lerp(a, b, t):
	return(b + (a - b) * t)

def mousePos(w):
	w.bind('<Motion>', motion)
	return(pos)

pos = (0, 0)
def motion(event):
	global pos
	pos = (event.x, event.y)

def dist(x1, y1, x2, y2):
	return(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

win = GraphWin("Curve", 600, 600, autoflush = False)
win.setBackground("gray")

points = []
for i in range(3):
	points.append((random.randint(50, win.width - 50), random.randint(50, win.height - 50)))

c = []
for i in range(len(points)):
	c.append(Circle(Point(points[i][0], points[i][1]), 10))
	c[-1].setWidth(2)
	c[-1].draw(win)

bc = bezier3Curve(points[0], points[1], points[2], win)
bc.t = 0.5
bc.showArm()
bc.setCurveQ(20)

dt = 0.4
dtime = 0

while(win.isClosed() == 0):
	start = time.time()
	mouse = mousePos(win)
	mouseClick = win32api.GetAsyncKeyState(0x01)

	# Draging points
	if(mouseClick == -32767): #Find nearest point
		nearest = -1
		for i in range(len(points)):
			distance = dist(points[i][0], points[i][1], mouse[0], mouse[1])
			if(distance < c[i].radius + 20):
				nearest = i

	elif(mouseClick == -32768 and nearest != -1): # Move nearest point to mouse
		points[nearest] = mouse
		c[nearest].move(points[nearest][0] - c[nearest].p1.getX() - c[nearest].radius, 
						points[nearest][1] - c[nearest].p1.getY() - c[nearest].radius)
		

	bc.updatePoints(points[0], points[1], points[2])
	bc.updateArm()
	bc.updateCurve()

	bc.t += dt * dtime
	if(bc.t > 1):
		bc.t = 1
		dt *= -1
	elif(bc.t < 0):
		bc.t = 0
		dt *= -1
	

	win.update()
	end = time.time()
	dtime = end - start
