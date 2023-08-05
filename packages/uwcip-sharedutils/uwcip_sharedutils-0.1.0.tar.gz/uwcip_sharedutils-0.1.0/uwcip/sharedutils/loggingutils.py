import os
import yaml

from .configutils import get_config

"""
To use this module, first ensure that the following environment variables are setup:

```
export TOOLS_CAPTURER_ROOT=<path to the root of the tools-capturer repo>
```

Then create a `log_config.yaml` with the loggers you'll use. You can base this file off of
an existing project's `log_config.yaml`.

Then add the following lines of code to your program's main file:

```
from logging import config as logging_config
from uwcip.sharedutils import loggingutils
logging_config.dictConfig(loggingutils.get_logging_config('relative/path/to/log_config.yaml'))
```

Then whenever you want to setup a logger, add the following code:

```
import logging
logger = logging.getLogger('<your logger name>')
```

Note that your logger name must be in the `log_config.yaml` file.

Then you can use the `logger` from there, eg `logger.info('foo')`.
"""

def get_logging_config(path):
  with open(os.path.join(
        get_config('TOOLS_CAPTURER_ROOT'),
        path
     ), 'r') as f:
      return yaml.load(f, Loader=yaml.FullLoader)