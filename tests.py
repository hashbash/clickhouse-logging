import clickhouse_logging
from logging import INFO
import random

from logging.handlers import HTTPHandler

# CH connection
CH_HTTP_INTERFACE = 'http://localhost:8123'
# CH_HTTP_INTERFACE = 'http://user:password@fc:8123'

ch_logger = clickhouse_logging.getLogger(name=__name__,
                                         capacity=100000,  # capacity before send to CH
                                         filename='log.txt',  # optional,  if specified also send to local file
                                         level=INFO,
                                         ch_table='test.log',  # target CH table
                                         ch_conn=CH_HTTP_INTERFACE)

ch_logger.info('test', extra={'col': 'x', 'dt': '2019-10-13'})

for i in range(10_000):
    ch_logger.info('test', extra={'col': str(random.randint(1, 1000)), 'dt': '2019-10-13'})
