import datetime
from shutil import copyfile

log_list = []
#x=0

def log(log_text):
    global log_list
    log_list.append(str(datetime.datetime.now()) + '  :  ' + str(log_text) + '\r\n')

def flush(file_name):
    global log_list
    tempFile = '/home/pi/logs/' + file_name + ' ' + str(datetime.datetime.now() + '.txt')
    #tempFile = file_name
    file = open(tempFile, "w")
    file.close()
    x=0
    file = open(tempFile, "a")
    while(x < len(log_list)):
        file.write(log_list[x])
        x=x+1
    file.close()

#while(x<20):
#    x = x+1
#    hello = "hello"
#    log(hello)

#flush('log.txt')