
import sys
def add():
    print('add')
    1/0
def my_excepthook(type, value, traceback):
    f = open("demofile2.txt", "a")
    f.write('\n'+str(type)+str(value)+str(traceback))
    f.close()

sys.excepthook = my_excepthook


add()
