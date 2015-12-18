import string

alphas = string.letters +'_'
nums = string.digits

print "Welcom to the indetifter Checker V1.0"
print "Test must be at least 2 Chars long"
myinput = raw_input("Iddentifter to test:\n")

if len(myinput) > 1:
    if myinput[0] not in alphas:
        print "invald: first symbol must be alphbetic"
    else:
        for otherChar in myinput[1:]:
            if alphas not in alphas + nums:
                print "invalid:remaining symbols must be alphanumeric"
                break
            else:
                print "ok as an identifier"
raw_input()
