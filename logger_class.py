import logging

def getLog(nm):
    ## creating custom logger
    logger = logging.getLogger(nm)
    ## reading contents from properties file
    f = open("properties.txt",'r')
    if f.mode == 'r':
        loglevel = f.read()
    if loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    elif loglevel == "DEBUG":
        logger.setLevel(logging.DEBUG)
    ## creating Formatters
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    ## creating Handlers
    file_handler = logging.FileHandler('test.log')
    ## Adding Formatters to Handlers
    file_handler.setFormatter(formatter)
    ## Adding Handlers to logger
    logger.addHandler(file_handler)
    return logger