
from urllib import urlretrieve

def  firstNoBlank(lines):
    for eachLine in lines:
        if not eachLine.strip():
            continue
        else:
            return eachLine

def firstLast(webpage):
    f = open(webpage)
    lines= f.readlines()
    f.close()
    print firstNoBlank(lines),lines.reverse()
    print firstNoBlank(lines),

def download(url = "http://www.cqupt.edu.cn",process=firstLast):
    try:
        retval = urlretrieve(url)[0]
    except IOError:
        retval = None
    if retval:
        process(retval)
if __name__ == "__main__":
    download()
