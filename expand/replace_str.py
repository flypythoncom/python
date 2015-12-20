# replace char<i> to <!> in the  string typed: 
#扩展成在字符串中把特定字符替换成规定字符
import re
def printReplace(srcStr,word):
    for letter in srcStr:
        if letter == word:
            srcStr = srcStr.replace(letter,'!') #字符串不可更改
    return srcStr

def printReplace_re(srcStr,word):
    srcStr=re.sub(word,'!',srcStr)
    return srcStr

def main():    
    srcStr = raw_input("Please type a string：")
    destStr=printReplace_re(srcStr,'i')
    print destStr


if __name__ == "__main__":
    main()
            
