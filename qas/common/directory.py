import os
from os.path import basename
import shutil

class Directory(object):

    #def __init__(self):
       #print("Init class Directory")

    def scan_dir(self, dir):
        list=[]
        for name in os.listdir(dir):
            path= os.path.join(dir,name)
            if os.path.isfile(path) and not name.startswith('.') :
                list.append(path)
            #else:
                #scan_dir(path)

        return list

    def checkExistPath(self, path):
        if not os.path.exists(path):
            return False
        return True

    def createPath(self, path):
        os.makedirs(path)

    def delelefolder(self,path):
        shutil.rmtree(path)

    def get_filename(self, filename):
        if os.path.exists(filename):
            return basename(filename)