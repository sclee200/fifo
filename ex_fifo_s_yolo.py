# -*- coding: utf-8 -*-
"""Copy of python_systemprogram.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PhFHEku5p3VxAIFemk5pGfyLum-B_ezA
"""

# import os
# cmd = 'ls -l'
# os.system(cmd)
# cmd = 'ls -al'
# os.system(cmd)
# os.system("date")
# os.system("echo Hello from the other side!")
# f = os.popen('date')
# now = f.read()
# print("Today is ", now)
# os.system('ifconfig')

# """FIFO 예제

# https://gist.github.com/egorps/7695667
# """

import os
import codecs
import tempfile
import time
#import thread
import _thread     #error 2

FIFO_FROM_YOLO = "/tmp/from_yolo_fifo"
FIFO_TO_YOLO = "/tmp/to_yolo_fifo"

def reader(fifo_path):
     
    pipein = open(fifo_path, 'r')
    
    while True:
        line = pipein.readline()[:-1]
        if(line):
         print("got: %s " % (line))

def mkfifo():
   os.chdir("/")
   fifo_from = os.path.join(FIFO_FROM_YOLO)
   if(os.path.isfile(fifo_from)):
      os.mkfifo(fifo_from)
   os.chdir("/")
   fifo_to = os.path.join(FIFO_TO_YOLO)
   if(os.path.isfile(fifo_to)):
      os.mkfifo(fifo_to)
   return fifo_from, fifo_to

def child_procs(fifo):
   # if(os.fork() == 0):
      os.fork()       
      reader(fifo)  
    

def child_threads(fifo):
   
   #thread.start_new_thread(reader, (id, fifo))
   _thread.start_new_thread(reader, (fifo,))    # error 2      


def writer(num, child_type):
    #fifos = [mkfifo() for fifo in xrange(num)]  # error 1
    fifo_from, fifo_to = mkfifo() 
    print("fifo_from : %s, fifo_to : %s" % (fifo_from, fifo_to))

    if child_type == 'threads':
        child_threads(fifo_from)
    else:
        child_procs(fifo_from)

    count = 0
    while True:
      message = "Message %d\n" % count
      print("================== ")
      print("Writing: ", message)
      
      fd = open(fifo_to, 'w')
      # os.write(fd, "%s" % ( message))
      #os.write(pipe, "aaaaaaaaaa".encode())  # error 3
      os.write(fd, ("%s" % (message)).encode())
      count += 1
      time.sleep(1)
      # if(count == 10):
      #    break


if __name__ == '__main__':
   try:
      writer(1, 'threads')
      # writer(1, 'process')
   except Exception as e:    
    print('예외가 발생했습니다.', e)



# writer(2, 'process')

# """Python 3 - Multithreaded Programming

# https://www.tutorialspoint.com/python3/python_multithreading.htm

# Starting a New Thread

# while문에서 끝나지 않음

# thread 가 끝나도 main process는 끝나지 않음
# """

# #!/usr/bin/python3
 

# import os
# import codecs
# import tempfile
# import time
# #import thread
# import _thread   

# # # Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# # Create two threads as follows
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: unable to start thread")

# while 1:
#    pass   #parent proess가 죽으면 thread가 죽으니까.





# #!/usr/bin/python3
# import os
# import codecs
# import tempfile
# import time
# #import thread
# import _thread   
# state_count = 0                 # add for end

# # Define a function for the thread
# def print_time( threadName, delay):
#     global state_count              # add for end
#     count = 0
#     while count < 5:
#         time.sleep(delay)
#         count += 1
#         print ("%s: %s" % ( threadName, time.ctime(time.time()) ))
#     state_count += 1            # add for end

# # Create two threads as follows
# try:
#    _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#    _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print("Error: unable to start thread")

# while 1:
#     #pass
#     if state_count == 2:        # add for end
#         break

# """The Threading Module"""

# #!/usr/bin/python3

# import threading
# import time

# exitFlag = 0

# class myThread (threading.Thread):
#    def __init__(self, threadID, name, counter):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.counter = counter

#    def run(self):
#       print ("Starting " + self.name)
#       print_time(self.name, self.counter, 5)
#       print ("Exiting " + self.name)

# def print_time(threadName, delay, counter):
#    while counter:
#       if exitFlag:
#          threadName.exit()
#       time.sleep(delay)
#       print ("%s: %s" % (threadName, time.ctime(time.time())))
#       counter -= 1

# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# # Start new Threads
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print ("Exiting Main Thread")

# """Synchronizing Threads"""

# #!/usr/bin/python3
# import threading
# import time
# class myThread (threading.Thread):
#    def __init__(self, threadID, name, counter):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.counter = counter
#    def run(self):
#       print ("Starting " + self.name)
#       # Get lock to synchronize threads
#       threadLock.acquire()
#       print_time(self.name, self.counter, 3)
#       # Free lock to release next thread
#       threadLock.release()

# def print_time(threadName, delay, counter):
#    while counter:
#       time.sleep(delay)
#       print ("%s: %s" % (threadName, time.ctime(time.time())))
#       counter -= 1

# threadLock = threading.Lock()
# threads = []

# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)

# # Start new Threads
# thread1.start()
# thread2.start()

# # Add threads to thread list
# threads.append(thread1)
# threads.append(thread2)

# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")

# """Multithreaded Priority Queue"""

# #!/usr/bin/python3

# import queue
# import threading
# import time

# exitFlag = 0

# class myThread (threading.Thread):
#    def __init__(self, threadID, name, q):
#       threading.Thread.__init__(self)
#       self.threadID = threadID
#       self.name = name
#       self.q = q
#    def run(self):
#       print ("Starting " + self.name)
#       process_data(self.name, self.q)
#       print ("Exiting " + self.name)

# def process_data(threadName, q):
#    while not exitFlag:
#       queueLock.acquire()
#       if not workQueue.empty():
#          data = q.get()
#          queueLock.release()
#          print ("%s processing %s" % (threadName, data))
#       else:
#          queueLock.release()
#          time.sleep(1)

# threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
# queueLock = threading.Lock()
# workQueue = queue.Queue(10)
# threads = []
# threadID = 1

# # Create new threads
# for tName in threadList:
#    thread = myThread(threadID, tName, workQueue)
#    thread.start()
#    threads.append(thread)
#    threadID += 1

# # Fill the queue
# queueLock.acquire()
# for word in nameList:
#    workQueue.put(word)
# queueLock.release()

# # Wait for queue to empty
# while not workQueue.empty():
#    pass

# # Notify threads it's time to exit
# exitFlag = 1

# # Wait for all threads to complete
# for t in threads:
#    t.join()
# print ("Exiting Main Thread")