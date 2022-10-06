import logging

def getLogger(name, verbose):
    mylogger = logging.getLogger(name)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(name)s - %(levelname)s - %(message)s"))
    mylogger.addHandler(ch)
    mylogger.setLevel(logging.DEBUG if verbose else logging.INFO)
    return mylogger