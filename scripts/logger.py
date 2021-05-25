import logging
import sys
import datetime
import time
from pathlib import Path

Path('logs/').mkdir(parents=True, exist_ok=True)

timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%y%m%d_%H%M%S')
file_handler = logging.FileHandler(filename=('logs/test_{}.log'.format(timestamp)))
stdout_handler = logging.StreamHandler(sys.stdout)

logging.basicConfig(
  level=logging.NOTSET, 
  format='[%(asctime)s] [%(levelname)s] %(message)s',
  handlers=[file_handler, stdout_handler]
)

log = logging.getLogger('')
