import multiprocessing as mp
import os
import getpass
import sys
import time

def timeout(func, timeout = 1, process_kill='iexplore.exe', args=(10,)):
    pool = mp.Pool(processes = 1)
    result = pool.apply_async(func, args=args)
    process = mp.current_process()
    print(process.pid)
    try:
        val = result.get(timeout = timeout)
    except mp.TimeoutError:
        print(str(timeout) + " Second timeout exceed")
        if process_kill=='iexplore.exe':
            os.system('taskkill /F /IM '+'IEDriverServer.exe'+' /FI "USERNAME eq '+getpass.getuser())
            os.system('taskkill /F /IM '+'msedge.exe'+' /FI "USERNAME eq '+getpass.getuser())
            os.system('taskkill /F /IM '+process_kill+' /FI "USERNAME eq '+getpass.getuser())
        else :
            os.system('taskkill /F /IM '+process_kill+' /FI "USERNAME eq '+getpass.getuser())
        pool.terminate()
        return True
    else:
        pool.close()
        pool.join()
        return False

def met(sleep):
    time.sleep(sleep)

if __name__ == '__main__':
    try :
        # Add the directory to the search path
        sys.path.append(os.getcwd())
        
        if len(sys.argv)>2 :
            print(timeout(met, timeout = int(sys.argv[1]), process_kill=str(sys.argv[2]), args=(int(sys.argv[1]),)))
        else :
            print(timeout(met, timeout = 10))
    except :
        print('Error in calling function please follow this order')
        print('python timeout.py [Timeout In Seconds] [process.exe]')
        print('True')
    

    
        
    
    
