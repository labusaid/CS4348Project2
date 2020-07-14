import random
import threading
import time
from queue import Queue

managerLock = threading.Semaphore(1) # limits getting manager approval to one teller
safeLock = threading.Semaphore(2) # limits safe use to two tellers

# allows inter-thread communication
commLock = threading.Semaphore(1)
commID = 0
commTransaction = 'None'

clientQueue = Queue()

tellerCount = 0
def teller(id):
    # setup
    global tellerCount
    tellerCount += 1
    print(f'Teller {id} is available')

    # serve clients
    while not clientQueue.empty():
        serving = clientQueue.get()
        print(f'Teller {id} is serving Client {serving}')
        # check for withdraw
        if True:
            # get approval from manager
            print(f'Teller {id} is getting the manager\'s approval')
            managerLock.acquire()
            time.sleep(random.uniform(.01,.05))
            managerLock.release()
            print(f'Teller {id} got the manager\'s approval')
        # access safe
        print(f'Teller {id} is going to the safe')
        safeLock.acquire()
        print(f'Teller {id} is using the safe')
        time.sleep(random.uniform(.005, .03))
        safeLock.release()
        # respond to client
        # wait for client to acknowledge
    print(f'Teller {id} closes')


actions = ('Deposit', 'Withdraw')
clientCount = 0
def client(id):
    # setup
    global clientCount
    clientCount += 1

    # actions
    action = random.choice(actions) # decide to deposit/withdraw
    clientQueue.put(id) # join queue
    print(f'Client {id} waits in line to make a {action}')

    # print(f'Client {id} goes to Teller {tellerID}')

# Start client threads
for i in range(2):
    t = threading.Thread(target=client,args=(i,))
    t.start()

# Start teller threads
threads = []
for i in range(2):
    t = threading.Thread(target=teller,args=(i,))
    t.start()
    threads.append(t)

# Wait for all tellers to close
for t in threads:
    t.join()
print('Bank closes')