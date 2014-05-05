def interprator():
    while True:
        cmd=raw_input(">>> ")
        if(cmd=="exit"):
            return
        try:
            exec(cmd)
        except:
            print("Can't execute!")
        del cmd