#!/usr/bin/env python

from sys       import argv
from os        import makedirs,unlink,sep
from os.path   import dirname,exists,isdir,splitext
from string    import replace,find,lower
from htmllib   import HTMLParser
from urllib    import urlretrieve
from urlparse  import urlparse,urljoin
from formatter import DumbWriter,AbstractFormatter
from cStringIO import StringIO

class Retriever(object):#下载网页类

    def __init__(self,url):
        self.url = url
        self.file = self.filename(url)

    def filename(self,url,deffile ="index.htm"):
        parsedurl = urlparse(url,"http:",0) #解析路径
        path = parsedurl[1] + parsedurl[2]
        ext = splitext(path)
        if ext[1] == "": #如果没有文件，使用默认
            if path[-1] == "/":
                path += deffile
            else:
                path += "/" + deffile
        ldir = dirname(path) #本地目录
        if sep != "/":
            ldir = replace(ldir,"/",sep)
        if not isdir(ldir): #如果没有目录，创建一个
            if exists(ldir):unlink(ldir)
            makedirs(ldir)
        return path

    def download(self):# 下载网页
        try:
            retval = urlretrieve(self.url,self.file)
        except IOError:
            retval = ('***Error: invalid URL: "%s"' % self.url,)
        return retval

    def parseAndGetLinks(self): #解析HTML，保存链接
        self.parser = HTMLParser(AbstractFormatter(DumbWriter(StringIO())))
        self.parser.feed(open(self.file).read())
        self.parser.close()
        return self.parser.anchorlist
        

class Crawler(object): #管理类,管理整个爬行过程

    count = 0 #下载网页计数器

    def __init__ (self,url):
        self.q = [url]  #链接队列
        self.seen = []  #已下载
        self.dom = urlparse(url)[1] #判断链接是否为主链接的子域名

    def getPage(self,url):  #下载网页
        r = Retriever(url)
        retval = r.download()
        if retval[0] == "*": #错误，不解析
            print retval,"--- skipping parse"
            return
        Crawler.count += 1
        print '\n(',Crawler.count,')'
        print "URL:",url
        print "FILE:",retval[0]
        self.seen.append(url)

        links = r.parseAndGetLinks() #得到链接
        for eachLink in links:
            if eachLink[:4] != "http" and find(eachLink,"://") == -1:
                eachLink = urljoin(url,eachLink)
            print "* ",eachLink
            
            if find(lower(eachLink),"mailto:") != -1: #过滤邮箱链接 
                print "--- discarded,mailto link"
                continue
                
            if eachLink not in self.seen:
                if find(eachLink,self.dom) == -1:
                    print "---discarded,not in domain"
                else:
                    if eachLink not in self.q:
                        self.q.append(eachLink)
                        print "---new,add to Q"
                    else:
                        print "---discarded,already in Q"
            else:
                print "---discarded, arlready processed"
					
    def go(self):  #在队列里处理链接，启动
        while self.q:
            url=self.q.pop()
            self.getPage(url)
        
def  main():
    if len(argv) > 1:
        url = argv[1]
        
    else:
        try:
            url = raw_input("Enter starting URL:")
        except (KeyboardInterrupt,EOFError):
            url = ""
            
    if not url: return
    robot = Crawler(url)
    robot.go()
    
if __name__ == "__main__":
        main()
                
