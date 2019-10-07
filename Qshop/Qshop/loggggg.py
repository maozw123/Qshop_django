import logging


logging_header=logging.FileHandler("test.log",encoding="utf-8")
stream_header=logging.StreamHandler()

log_format="%(asctime)s-%(levelname)s-%(message)s"   #日志格式
time_format="%Y-%m-%d %H:%M:%S"  #日志时间

logging.basicConfig(level=logging.DEBUG,format=log_format,datefmt=time_format,handlers=[logging_header,stream_header])

logging.debug("这是一个debug信息")
logging.info("这是一个info信息")
logging.warning("这是一个warning信息")
logging.error("这是一个error信息")
logging.critical("这是一个critical信息")
