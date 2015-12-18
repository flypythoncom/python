def safe_float(obj):
    try:
        retval = float(obj)
    except (ValueError,TypeError),diag:
        retval = str(diag)
    return retval

def main():
    log = open("cardlog.txt","w")
    try:
        ccfile = open("carddata.txt","r")
    except IOError,e:
        log.write("no txns this \n")
        log.close()
        return
    txns = ccfile.readlines()
    ccfile.close()
    total = 0.00
    log.write("account log:\n")

    for eachTxn in txns:
        result = safe_float(eachTxn)
        if isinstance(result,float):
            total += result
            log.write("data ....processed\n")
        else:
            log.write("ignored: %s" % result)
    print "$%.2f (new balance)" % (total)
    log.close()

if __name__ == '__main__':
    print "run"
    main()
