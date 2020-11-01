import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s[%(module)s,%(lineno)d] %(levelname)s "%(message)s"', datefmt='%Y-%m-%d %H:%M:%S',filename='fish.log', filemode='a')
logger = logging