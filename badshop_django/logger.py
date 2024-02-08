import logging
import sys

FORMAT = '!!! %(filename)s %(lineno)d %(funcName)20s() %(levelname)s %(asctime)s %(message)s'

logging.basicConfig(filename='logs.log',
                    filemode='a',
                    encoding='utf-8-sig',
                    format=FORMAT,
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG
                    )

logger = logging.getLogger()

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(console_handler)

def main():              
    logger.debug('hello')

if __name__ == '__main__':
    main()