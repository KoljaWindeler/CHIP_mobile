import pygame
import arduino_bridge
import time

def update():
	#print("update")
	salsa.digitalWrite(14,dl) # in3, dir righ
	salsa.setPWM(0,pl) # en3, en right 
	salsa.digitalWrite(13,dr) # in1 dir left
	salsa.setPWM(9,pr) # en1, left
	#print("done")

pygame.init()
j=pygame.joystick.Joystick(0)
j.init()

file1 = 'meep6.mp3'
file2 = 'start.mp3'
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()

print("pygame done")


salsa = arduino_bridge.connection()
salsa.setup_ws2812_unique_color_output(6,5)
salsa.setup_pwm_output(0) # right pwm
salsa.setup_pwm_output(9) # left pwm 
salsa.setup_pwm_freq(0,15)
salsa.setup_pwm_freq(9,15)
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
bx=0
by=0

down = []
police = 0

t=time.time()
s=0

update()


def led():
	global t,s
	if((s%8==0 or s%8==2) and s<32):
		salsa.ws2812set(6,cA1)
		t=time.time()+on
	elif(s%2==1):
		salsa.ws2812set(6,cA0)
		t=time.time()+off
	elif((s%8==4 or s%8==6) and s<32):
		salsa.ws2812set(6,cA2)
		t=time.time()+on

	elif((s%8==0 or s%8==2) and s>=32):
		salsa.ws2812set(6,cA3)
		t=time.time()+on

	elif((s%8==4 or s%8==6) and s>=32):
		salsa.ws2812set(6,cA4)
		t=time.time()+on
	s = (s + 1)%64
		

while 1:
	if(time.time()>=t and police==1):
		led()

	for event in pygame.event.get():

		if(hasattr(event, 'button')):
			if(not(event.button in down)):
				down.append(event.button)
				if(event.button == 0):
					pygame.mixer.music.load(file1)
					pygame.mixer.music.play(1)
				elif(event.button == 1):
					pygame.mixer.music.load(file2)
					pygame.mixer.music.play(1)
				elif(event.button == 2):
					police = (police + 1)%2
					if(police == 0):
						salsa.ws2812set(6,cA0)

						

			else:
				down.remove(event.button)

		#print(dir(event))
		#print(event.dict)
		x = j.get_axis(0)			
		y = j.get_axis(1)
		t = (j.get_axis(4)+1)/2

		if(round(x,1)!=bx or round(y,1)!=by):
			bx=round(x,1)
			by=round(y,1)
			print(str(bx)+"/"+str(by)+"     -     "+str(dr)+"/"+str(dl)+"/"+str(pr)+"/"+str(pl))

		
		if(3 in down):
			dr=0
			dl=0
		else:
			dr=1
			dl=1
		
		if(x<=0):
			pr=t*255
		else:
			pr=t*255*(1-x)

		if(x>=0):
			pl=t*255
		else:
			pl=t*255*(1+x)


		pl=int(pl)
		pr=int(pr)
	
		if(bpl!=pl or bpr!=pr or bdl!=dl or bdr!=dr):
			update()
			bpl=pl
			bpr=pr
			bdl=dl
			bdr=dr

 
