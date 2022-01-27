# -*- coding: utf-8 -*-
"""Copy of python_systemprogram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PhFHEku5p3VxAIFemk5pGfyLum-B_ezA
"""

import os
cmd = 'ls -l'
os.system(cmd)

!ls

import os
cmd = 'ls -al'
os.system(cmd)

!date

import os
os.system("date")

import os

os.system("echo Hello from the other side!")

import os
f = os.popen('date')
now = f.read()
print("Today is ", now)

!ifconfig

import os
os.system('ifconfig')

"""FIFO 예제

https://gist.github.com/egorps/7695667
"""

import os
import codecs
import tempfile
import time
#import thread
import _thread     #error 2

def reader(id, fifo_path):
    print("in reader %d" % id)
    pipein = open(fifo_path, 'r')
    print("reader %d opened fifo" % id)
    while True:
        line = pipein.readline()[:-1]
        print("Reader %d got: %s " % (id, line))

def mkfifo():
    fifo_path = os.path.join(tempfile.mkdtemp(), 'fifo')
    os.mkfifo(fifo_path)
    return fifo_path

def child_procs(fifos):
    pipes = []
    for id, fifo in enumerate(fifos):
        if not os.fork():
            print("starting reader %d" % id)
            reader(id, fifo)
            return
        else:
            pipes.append((id, os.open(fifo, os.O_WRONLY)))
    print("Readers started")
    return pipes

def child_threads(fifos):
    pipes = []
    for id, fifo in enumerate(fifos):
        #thread.start_new_thread(reader, (id, fifo))
        _thread.start_new_thread(reader, (id, fifo))    # error 2
        pipes.append((id, os.open(fifo, os.O_WRONLY)))
    return pipes


def writer(num, child_type):
    #fifos = [mkfifo() for fifo in xrange(num)]  # error 1
    fifos = [mkfifo() for fifo in range(num)]
    print("FIFOs: %s" % fifos)

    if child_type == 'threads':
        pipes = child_threads(fifos)
    else:
        pipes = child_procs(fifos)

    count = 0
    while True:
        message = "Message %d\n" % count
        print("================== ")
        print("Writing: ", message)
        for (id, pipe) in pipes:
            #os.write(pipe, "%d: %s" % (id, message))
            #os.write(pipe, "aaaaaaaaaa".encode())  # error 3
            os.write(pipe, ("%d: %s" % (id, message)).encode())
        count += 1
        time.sleep(1)
        if(count == 10):
            break

#writer(2, 'threads')
writer(2, 'process')

"""Python 3 - Multithreaded Programming

https://www.tutorialspoint.com/python3/python_multithreading.htm

Starting a New Thread

while문에서 끝나지 않음

thread 가 끝나도 main process는 끝나지 않음
"""

#!/usr/bin/python3

import _thread
import time

# Define a function for the thread
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: unable to start thread")

while 1:
   pass

#!/usr/bin/python3

import _thread
import time

state_count = 0                 # add for end

# Define a function for the thread
def print_time( threadName, delay):
    global state_count              # add for end
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
    state_count += 1            # add for end

# Create two threads as follows
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print("Error: unable to start thread")

while 1:
    #pass
    if state_count == 2:        # add for end
        break

"""The Threading Module"""

#!/usr/bin/python3

import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter

   def run(self):
      print ("Starting " + self.name)
      print_time(self.name, self.counter, 5)
      print ("Exiting " + self.name)

def print_time(threadName, delay, counter):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print ("Exiting Main Thread")

"""Synchronizing Threads"""

#!/usr/bin/python3

import threading
import time

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print ("Starting " + self.name)
      # Get lock to synchronize threads
      threadLock.acquire()
      print_time(self.name, self.counter, 3)
      # Free lock to release next thread
      threadLock.release()

def print_time(threadName, delay, counter):
   while counter:
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1

threadLock = threading.Lock()
threads = []

# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()

# Add threads to thread list
threads.append(thread1)
threads.append(thread2)

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")

"""Multithreaded Priority Queue"""

#!/usr/bin/python3

import queue
import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, q):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.q = q
   def run(self):
      print ("Starting " + self.name)
      process_data(self.name, self.q)
      print ("Exiting " + self.name)

def process_data(threadName, q):
   while not exitFlag:
      queueLock.acquire()
      if not workQueue.empty():
         data = q.get()
         queueLock.release()
         print ("%s processing %s" % (threadName, data))
      else:
         queueLock.release()
         time.sleep(1)

threadList = ["Thread-1", "Thread-2", "Thread-3"]
nameList = ["One", "Two", "Three", "Four", "Five"]
queueLock = threading.Lock()
workQueue = queue.Queue(10)
threads = []
threadID = 1

# Create new threads
for tName in threadList:
   thread = myThread(threadID, tName, workQueue)
   thread.start()
   threads.append(thread)
   threadID += 1

# Fill the queue
queueLock.acquire()
for word in nameList:
   workQueue.put(word)
queueLock.release()

# Wait for queue to empty
while not workQueue.empty():
   pass

# Notify threads it's time to exit
exitFlag = 1

# Wait for all threads to complete
for t in threads:
   t.join()
print ("Exiting Main Thread")