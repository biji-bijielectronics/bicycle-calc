import serial
import time
import redis
import sys

ser1 = serial.Serial()

strPort = '/dev/ttyACM0'

ser1 = serial.Serial('/dev/ttyACM0', 115200)
ser1.last_read = time.time()

try:
	ser2 = serial.Serial('/dev/ttyACM1', 115200)
	ser2.last_read = time.time()
except:
	ser2 = None


current = 0.0


delay = 0.1

r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe(['adc_control'])

running = True



def processMsg(msg):
	global running, delay
	print msg
	if msg == 'start':
		running = True
	elif msg == 'stop':
		running = False
	elif msg[0:5] == 'delay':
		print 'delay: ' + msg[6:]
		delay = float(msg[6:]) - 0.01
	else:
		print msg	

def read_serial(serial):
	try:
		line = serial.readline()
		bike, data = line.split('\t')
		val = float(data)
		#print bike, data
		current = val
		if current == 0:
			voltage = 0
		else:
			voltage = 12.4
		if time.time() - serial.last_read >= delay and running:
			msg =  {'bike': bike, 'current': round(current,2), 'voltage': voltage , 'time': time.time() }
			#print msg
			r.publish('adc', msg)
			serial.last_read = time.time()
		
		item = pubsub.get_message()
		if item is not None:
			msg = str(item['data'])
			processMsg(msg)
	except ValueError:
		pass		

	except KeyboardInterrupt:
		raise


while 1:
	read_serial(ser1)
	if ser2:
		read_serial(ser2)

