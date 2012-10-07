class Queue:
    def __init__(self,size=20):
        self.queue=[]
        self.size=size
        self.end=-1

    def setSize(self,size):
        self.size=size

    def In(self,element):
        if self.end < self.size -1:
            self.queue.append(element)
            self.end = self.end + 1
        else:
            raise "QueueFull"

    def Out(self):
        if self.end != -1:
            element = self.queue[0]
            self.queue=self.queue[1:]
            self.end = self.end-1
            return element
        else:
            raise "QueueEmpty"

    def End(self):
        return self.end

    def empty(self):
        self.queue=[]
        self.end=-1

if __name__ == "__main__":
    
    queue=Queue()
    for i in range(10):
        queue.In(i)
    print queue.End()

    for i in range(10):
        print queue.Out()
        
            
