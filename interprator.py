class Interprator:
    '''Class responsible for the usage of the shell during the game
    (probably obsolete in near future)'''

    def __init__(self):
        pass

    def interprator(self,input=None):
        '''This asks keyboard input from the user and tries to execute it
        Quits with 'exit'
        '''
        while True:
            cmd=raw_input(">>> ")
            if(cmd=="exit"):
                return
            try:
                exec(cmd)
            except:
                print("Can't execute!")
            del cmd
