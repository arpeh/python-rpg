import os

class TextContainer:
    text=None

    def __init__(self,text=None):
        self.text = text

    def set_text(self,text):
        self.text = text

    def add_text(self,text):
        if self.text == None:
            self.text = text
        else:
            self.text = self.text +'\n'+ text

class CodeReader:
    '''Class used to read and execute user written code.'''

    #Filename of the code to be run
    current_code_file = None

    def __init__(self):
        self.current_code_file = 'test.py'


    def run_code(self,input_object_dict=None):
        '''Runs the code named current_code_file
        input: dictionary of variables to be passed into user's code
        output: none
        '''

        text=TextContainer()
        try:
            #Replace the built-in print function in user's code 
            def write_to_textcontainer(string):
                text.add_text(string)

            input_object_dict['printt']=write_to_textcontainer

            execfile(os.path.join(os.path.dirname(__file__),'mycodes',self.current_code_file),input_object_dict,{})
        except Exception as e:
            print 'ERROR: ', e
        
        return text.text
