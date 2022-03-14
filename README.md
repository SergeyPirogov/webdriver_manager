# Webdriver Manager for Python

[![Tests](https://github.com/SergeyPirogov/webdriver_manager/actions/workflows/test.yml/badge.svg)](https://github.com/SergeyPirogov/webdriver_manager/actions/workflows/test.yml)
[![PyPI](https://img.shields.io/pypi/v/webdriver_manager.svg)](https://pypi.org/project/webdriver-manager)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/webdriver_manager.svg)](https://pypi.org/project/webdriver-manager/)
[![codecov](https://codecov.io/gh/SergeyPirogov/webdriver_manager/branch/master/graph/badge.svg)](https://codecov.io/gh/SergeyPirogov/webdriver_manager)

[Patreon](https://www.patreon.com/automation_remarks)

The main idea is to simplify management of binary drivers for different browsers.

For now support:

- [ChromeDriver](#use-with-chrome)

- [GeckoDriver](#use-with-firefox)

- [IEDriver](#use-with-ie)

- [OperaDriver](#use-with-opera)

- [EdgeChromiumDriver](#use-with-edge)

Compatible with Selenium 4.x and below.

Before:
You should download binary chromedriver, unzip it somewhere in you PC and set path to this driver like this:

```python
from selenium import webdriver
driver = webdriver.Chrome('/home/user/drivers/chromedriver')
```

It’s boring!!! Moreover every time the new version of driver released, you should go and repeat all steps again and again.

With webdriver manager, you just need to do two simple steps:

#### Install manager:

```bash
pip install webdriver-manager
```

#### Use with Chrome

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
```

#### Use with Chromium

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
```

#### Use with Brave

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
```

#### Use with Firefox

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
```

#### Use with IE

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.microsoft import IEDriverManager

driver = webdriver.Ie(IEDriverManager().install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.microsoft import IEDriverManager

driver = webdriver.Ie(service=Service(IEDriverManager().install()))
```

#### Use with Edge

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(EdgeChromiumDriverManager().install())
```
```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
```

#### Use with Opera

```python
# selenium 3 & 4
from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager

driver = webdriver.Opera(executable_path=OperaDriverManager().install())
```

If the Opera browser is installed in a location other than `C:/Program Files` or `C:/Program Files (x86)` on windows
and `/usr/bin/opera` for all unix variants and mac, then use the below code,

```python
from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager

options = webdriver.ChromeOptions()
options.add_argument('allow-elevated-browser')
options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options)
```

## Configuration

**webdriver_manager** has several configuration variables you can be interested in.

### `GH_TOKEN`
**webdriver_manager** downloading some webdrivers from their official GitHub repositories but GitHub has [limitations](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) like 60 requests per hour for unauthenticated users.
In case not to face an error related to github credentials, you need to [create](https://help.github.com/articles/creating-an-access-token-for-command-line-use) github token and place it into your environment: (\*)

Example:

```bash
# bash
export GH_TOKEN = "asdasdasdasd"
```

(\*) access_token required to work with GitHub API [more info](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).

There is also possibility to set same variable via ENV VARIABLES, example:

```python
# python
import os
os.environ['GH_TOKEN'] = "asdasdasdasd"
```

### `Logging`
Make sure to configure the logging facility the way it suits your use case before running your tests, to be able to capture your output.


At the moment, in case no configuration is provided, log messages will be print to a console output and only for levels equal or higher than `Warning` [more info](https://docs.python.org/3/howto/logging.html).
As of current version all messages logged by webdriver manager are of level `Info` so nothing will be printed out.

To get log messages of level `Info` make sure to properly configure logging before using webdriver message, otherwise default configuration will be applied.

E.g.
```python
import logging
logging.basicConfig(level=logging.INFO)

```

#### `WDM_LOG_LEVEL`
You can customize the loggin level of webdriver manager by using the env variable `WDM_LOG_LEVEL` before running your selenium tests.

The values are set using logging setLevel method, you can find more info [here](https://docs.python.org/3/library/logging.html).

At the moment the values are as follows:

| Level    | Numeric value |
|----------|---------------|
| CRITICAL | 50            |
| ERROR    | 40            |
| WARNING  | 30            |
| INFO     | 20            |
| DEBUG    | 10            |
| NOTSET   | 0             |

E.g. to silent `webdriver_manager` logs and remove them from console, initialize env variable `WDM_LOG_LEVEL` with `'0'`:

```python
import os

os.environ['WDM_LOG_LEVEL'] = '0'
``` 

#### `WDM_PRINT_FIRST_LINE`
By default webdriver manager prints a blank space before its log output if logging is enabled. If you want to disable this, initialize `WDM_PRINT_FIRST_LINE` with `'False'` before your tests:

```python
import os

os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
``` 

or via constructor:

```python
ChromeDriverManager("2.26", print_first_line=False).install()
```

### `WDM_LOCAL`
By default all driver binaries are saved to user.home/.wdm folder. You can override this setting and save binaries to project.root/.wdm.

```
import os

os.environ['WDM_LOCAL'] = '1'
```

### `WDM_SSL_VERIFY`
SSL verification can be disabled for downloading webdriver binaries in case when you have troubles with SSL Certificates or SSL Certificate Chain. Just set the environment variable `WDM_SSL_VERIFY` to `"0"`.

```
import os

os.environ['WDM_SSL_VERIFY'] = '0'
```

### `version`
Specify the version of webdriver you need. And webdriver-manager will download it from sources for your os.
```python
ChromeDriverManager(version="2.26").install()
```

### `cache_valid_range`
Driver cache by default is valid for 1 day. You are able to change this value using constructor parameter:

```python
ChromeDriverManager("2.26", cache_valid_range=1).install()
```

This will make your test automation more elegant and robust!

Cheers
