class Interprator:

    def __init__(self):
        pass

    def interprator(self,input=None):
        while True:
            cmd=raw_input(">>> ")
            if(cmd=="exit"):
                return
            try:
                exec(cmd)
            except:
                print("Can't execute!")
            del cmd
