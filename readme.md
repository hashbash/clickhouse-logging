Python logging to clickhouse
Write your logs direct to Clickhouse. 
Logger will send to CH all standard logging fields (like message, level ...) and all fields provided in `extra`.
By default parameter `input_format_skip_unknown_fields` is enabled.

Based on BufferingHandler, this means that inserts will do only by big batches, not each line.


Example usage:

```jql
create table test.log (
	col String,
	dt Date
)
engine MergeTree()
PARTITION BY toYYYYMM(dt)
ORDER BY col;
```

```python
import clickhouse_logging
from logging import INFO
import random

# CH connection
CH_HTTP_INTERFACE = 'http://localhost:8123'


ch_logger = clickhouse_logging.getLogger(name=__name__,
                                         capacity=100000,  # capacity before send to CH 
                                         filename='log.txt',  # optional,  if specified also send to local file
                                         level=INFO, 
                                         ch_table='test.log',  # target CH table
                                         ch_conn=CH_HTTP_INTERFACE)

ch_logger.info('test', extra={'col': 'x', 'dt': '2019-10-13'})

for i in range(10_000):
    ch_logger.info('test', extra={'col': str(random.randint(1, 1000)), 'dt': '2019-10-13'})
```


If Clickhouse server is not available or for any other reason, logger will raise something like this:

```log
Traceback (most recent call last):
  File "/Users/ed/PycharmProjects/clickhouse-logging/clickhouse_logging.py", line 83, in flush
    res.raise_for_status()
  File "/Users/ed/PycharmProjects/fc/venv/lib/python3.6/site-packages/requests/models.py", line 940, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: http://user:password@host:8123/?query=insert+into+test.log+format+JSONEachRow&input_format_skip_unknown_fields=1
Call stack:
  File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/logging/__init__.py", line 1943, in shutdown
    h.flush()
  File "/Users/ed/PycharmProjects/clickhouse-logging/clickhouse_logging.py", line 87, in flush
    self.handleError(record)
Message: b'Code: 26, e.displayText() = DB::Exception: Cannot parse JSON string: expected opening quote: (while read the value of key col): (at row 1)\n (version 19.13.3.26 (official build))\n'
Arguments: ()
```
