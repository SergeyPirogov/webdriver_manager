# Webdriver Manager for Python

![Tests](https://github.com/SergeyPirogov/webdriver_manager/workflows/Tests/badge.svg)
[![PyPI](https://img.shields.io/pypi/v/webdriver_manager.svg)](https://pypi.org/project/webdriver-manager)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/webdriver_manager.svg)](https://pypi.org/project/webdriver-manager/)
[![codecov](https://codecov.io/gh/SergeyPirogov/webdriver_manager/branch/master/graph/badge.svg)](https://codecov.io/gh/SergeyPirogov/webdriver_manager)

[Patreon](https://www.patreon.com/automation_remarks)

The main idea is to simplify management of binary drivers for different browsers.

For now support:

- ChromeDriver

- GeckoDriver

- IEDriver

- OperaDriver

- EdgeChromiumDriver

Before:
You should download binary chromedriver, unzip it somewhere in you PC and set path to this driver like this:

```python
webdriver.Chrome('/home/user/drivers/chromedriver')

ChromeDriverManager(path=custom_path).install()
```

It’s boring!!! Moreover every time the new version of driver released, you should go and repeat all steps again and again.

With webdriver manager, you just need to do two simple steps:

Install manager:

```bash
pip install webdriver-manager
```

Use with Chrome:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
```

Use with Chromium:

```python
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
```

Use with FireFox:

```python
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
```

Use with IE

```python
from selenium import webdriver
from webdriver_manager.microsoft import IEDriverManager

driver = webdriver.Ie(IEDriverManager().install())
```

Use with Edge

```python
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(EdgeChromiumDriverManager().install())
```

Use with Opera

```python
from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager

driver = webdriver.Opera(executable_path=OperaDriverManager().install())
```

If the Opera browser is installed in a location other than C:/Program Files or C:/Program Files (x86) on windows
and /usr/bin/opera for all unix variants and mac, then use the below code,

```python
from selenium import webdriver
from webdriver_manager.opera import OperaDriverManager

options = webdriver.ChromeOptions()
options.add_argument('allow-elevated-browser')
options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options)
```

## Configuration

If you face error related to github credentials, you need to place github token: (\*)

Example:

```bash
export GH_TOKEN = "asdasdasdasd"
```

(\*) access_token required to work with Github API more info <https://help.github.com/articles/creating-an-access-token-for-command-line-use/>.

There is also possibility to set same variables via ENV VARIABLES.

To silent `webdriver_manager` logs and remove them from console, initialize env variable `WDM_LOG_LEVEL` with `'0'` value before your selenium tests:

```python
import os

os.environ['WDM_LOG_LEVEL'] = '0'
``` 

or via constructor:

```python
ChromeDriverManager("2.26", log_level=0).install()
```

By default webdriver manager prints a blank space before its log output if logging is enabled. If you want to disable this, initialize `WDM_PRINT_FIRST_LINE` with `'False'` before your tests:

```python
import os

os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
``` 

or via constructor:

```python
ChromeDriverManager("2.26", print_first_line=False).install()
```

By default all driver binaries are saved to user.home/.wdm folder. You can override this setting and save binaries to project.root/.wdm.

```
import os

os.environ['WDM_LOCAL'] = '1'
```

Driver cache by default is valid for 1 day. You are able to change this value using constructor parameter:

```python
ChromeDriverManager("2.26", cache_valid_range=1).install()
```

This will make your test automation more elegant and robust!
