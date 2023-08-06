# python-supporter

https://pypi.org/project/python-supporter
<pre>
pip install python-supporter
</pre>

```
from python_supporter import logging

logging.basicConfig(logging.ERROR)
#logging.basicConfig(logging.INFO)
#logging.basicConfig(logging.DEBUG)
#logging.basicConfig(logging.ERROR, filename='log.txt')
#logging.basicConfig(logging.INFO, filename='log.txt')
#logging.basicConfig(logging.DEBUG, filename='log.txt')

logging.error('This is error message') #2023-03-19 22:36:47: ERROR: This is error message
logging.info('This is info message')
logging.debug('This is debug message')
```
