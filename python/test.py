import pygame
import arduino_bridge
import time

def update():
	print("update")
	print("dr/dl/pr/pl = "+str(dr)+"/"+str(dl)+"/"+str(pr)+"/"+str(pl))
	salsa.digitalWrite(14,dl) # in3, dir righ
	salsa.setPWM(0,pl) # en3, en right 
	salsa.digitalWrite(13,dr) # in1 dir left
	salsa.setPWM(9,pr) # en1, left
	print("done")

pygame.init()
j=pygame.joystick.Joystick(0)
j.init()

file = 'meep6.mp3'
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file)

print("pygame done")


salsa = arduino_bridge.connection()
salsa.setup_ws2812_unique_color_output(6,5)
salsa.setup_pwm_output(0) # right pwm
salsa.setup_pwm_output(9) # left pwm 
salsa.setup_digital_output(13) #left
salsa.setup_digital_output(14) #right
print("salsa done")


cA0 = []
cA0.append(arduino_bridge.Color(0, 0, 0))
cA0.append(arduino_bridge.Color(0, 0, 0))
cA0.append(arduino_bridge.Color(0, 0, 0))
cA0.append(arduino_bridge.Color(0, 0, 0))
cA0.append(arduino_bridge.Color(0, 0, 0))

cA1 = []
cA1.append(arduino_bridge.Color(255, 0, 0))
cA1.append(arduino_bridge.Color(0, 0, 0))
cA1.append(arduino_bridge.Color(0,0,0))
cA1.append(arduino_bridge.Color(0, 0, 255))
cA1.append(arduino_bridge.Color(0, 0, 0))

cA2 = []
cA2.append(arduino_bridge.Color(0, 0, 0))
cA2.append(arduino_bridge.Color(255, 0, 0))
cA2.append(arduino_bridge.Color(0,0,0))
cA2.append(arduino_bridge.Color(0, 0, 0))
cA2.append(arduino_bridge.Color(0, 0, 255))

cA3 = []
cA3.append(arduino_bridge.Color(0, 0, 0))
cA3.append(arduino_bridge.Color(255, 0, 0))
cA3.append(arduino_bridge.Color(0,0,0))
cA3.append(arduino_bridge.Color(0, 0, 255))
cA3.append(arduino_bridge.Color(0, 0, 0))

cA4 = []
cA4.append(arduino_bridge.Color(255, 0, 0))
cA4.append(arduino_bridge.Color(0, 0, 0))
cA4.append(arduino_bridge.Color(0,0,0))
cA4.append(arduino_bridge.Color(0, 0, 0))
cA4.append(arduino_bridge.Color(0, 0, 255))

on=0.1
off=0.1

# stop
pl=0
pr=0
dr=0
dl=1
bpl=0
bpr=0
bdr=0
bdl=1
update()
down = []

t=time.time()
s=0

def led():
	global t,s
	if(s%2==0 and s<20):
		salsa.ws2812set(6,cA1)
		t=time.time()+on
	elif(s%2==1):
		salsa.ws2812set(6,cA0)
		t=time.time()+off
	elif(s%2==0 and s>=20):
		salsa.ws2812set(6,cA2)
		t=time.time()+on
	s = s + 1
		

while 1:
	if(time.time()>=t):
		led()


	for event in pygame.event.get():
		x = j.get_axis(0)			
		y = j.get_axis(1)			

		if(hasattr(event, 'button')):
			if(not(event.button in down)):
				down.append(event.button)
				if(event.button == 1):
					pygame.mixer.music.play(1)
			else:
				down.remove(event.button)

		#print(dir(event))
		#print(event.dict)

		if(abs(x)<0.4 and abs(y)<0.4):
			#top
			pl=0
			pr=0
			dr=0
			dl=0
		elif(x<-0.9 and abs(y)<0.2):
			# rotate ccw
			pl=100
			pr=100
			dr=1
			dl=0
		elif(x>0.9 and abs(y)<0.2):
			# rotate cw
			pl=100
			pr=100
			dr=0
			dl=1
		elif(y>0.9 and abs(x)<0.2):
			# back
			pl=100
			pr=100
			dr=0
			dl=0
		elif(y<-0.9 and abs(x)<0.2):
			# forward
			pl=100
			pr=100
			dr=1
			dl=1
	
		if(bpl!=pl or bpr!=pr or bdl!=dl or bdr!=dr):
			update()
			bpl=pl
			bpr=pr
			bdl=dl
			bdr=dr

 
