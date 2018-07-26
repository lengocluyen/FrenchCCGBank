import os

class CommandExecute(object):
    def __init__(self):
        print ("Init in class Command Execute")


    def exucute(self, command):
        reponse=os.popen(command)
        return reponse.read()
