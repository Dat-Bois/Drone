from logger import log, flush

x=0 
while(x<20):
    log("Hello")
    x=x+1

flush("log.txt")