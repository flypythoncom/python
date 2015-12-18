import threading
from time import sleep,ctime

loops = [4,2]

class ThreadFunc(object):
    def __init__(self,func,args,name=""):
        self.name = name
        self.name = func
        self.args = args
    def __call__(self):
        apply(self.func,slef.args)
        
    def loop(nloop,nsec):
        print "start loop:",nloop,"at:",ctime()
        sleep(nsec)
        print "loop",nloop,"done at:",ctime()

    def main():
        print "starting at:",ctime()
        threads = []
        nloops = range(len(loops))
      #创建线程
        for i in nloops:
            t = threading.Thread(target = loop,args=(i,loops[i]))
            threads.append(t);
      #启动线程
        for i in nloops:
            threads[i].start()
      #等待线程
        for i in nloops:
            threads[i].join()
        print "all DONE at:",ctime()
        
if __name__　== "__main__":
    main()
    
