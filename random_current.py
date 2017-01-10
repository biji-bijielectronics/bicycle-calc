import time
import redis
import sys
import random

r = redis.Redis()

delay = 0.1
current = 5
voltage = 12.0
while 1:

	dif = random.random() - 0.5 

	voltage += dif 
	current += dif * 0.1 

	if voltage < 0.1:
		voltage = 0.11

	if current < 0.1:
		current = 0.11	

	msg =  {'bike': 'a', 'current': round(current,2), 'voltage': voltage , 'time': time.time() }
	r.publish('adc', msg)

	msg =  {'bike': 'b', 'current': round(current,2), 'voltage': voltage , 'time': time.time() }
	r.publish('adc', msg)
	

	print current, voltage
	time.sleep(delay)
