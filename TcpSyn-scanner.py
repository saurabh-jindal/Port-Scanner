#!/usr/bin/env py 


import threading 
import time 
from scapy.all import *
import Queue 


class Workerthread(threading.thread):

	def __init__(self,queue, tid):
		self.queue =  queue
		self.tid = tid
		print 'Worker %d is now working'%tid
	


	def run(self):
		total_ports = 0
		while True:
			port = 0
			try:	
				port = self.queue.get(timeout = 1)
			except Queue.empty:	
				print 'worker exiting %d Scanned ports %d'%(tid,total_ports)


			# scapy will do the next work 
			
			ip = sys.argv[1]
			response = sr1(IP(dst = ip)/TCP(dport = port, flags = "S"),  verbose = False, timeout = 0.2)

			if response:
				if response[TCP].flags == 18:
					print 'ThreadID %d ,port %d is open'%(self.tid, port)


			

			self.queue.task_done()

			total_ports += 1




queue = Queue.Queue


threads =[]


for i in range(1,10):
	print 'Creating worker thread %d'%i
	worker = Workerthread(queue, i)
	worker.setDaemon(True)
	worker.start()
	threads.append(worker)


	print 'Worker thread created %d'%i					

for j in range(1,5000):
	queue.put(j)


queue.join()

for item in threads:
	item.join()


print 'Scanning complete!...'


	