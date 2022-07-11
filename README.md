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
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
```

#### Use with Chromium

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
```

```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
```

#### Use with Brave

```python
# selenium 3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install())
```

```python
# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))
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
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
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
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager

driver = webdriver.Ie(service=IEService(IEDriverManager().install()))
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
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
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
Any variable can be set using either .env file or via python directly

### `GH_TOKEN`
**webdriver_manager** downloading some webdrivers from their official GitHub repositories but GitHub has [limitations](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) like 60 requests per hour for unauthenticated users.
In case not to face an error related to github credentials, you need to [create](https://help.github.com/articles/creating-an-access-token-for-command-line-use) github token and place it into your environment: (\*)

Example:

```bash
export GH_TOKEN = "asdasdasdasd"
```

(\*) access_token required to work with GitHub API [more info](https://help.github.com/articles/creating-an-access-token-for-command-line-use/).

There is also possibility to set same variable via ENV VARIABLES, example:

```python
import os

os.environ['GH_TOKEN'] = "asdasdasdasd"
```

### `WDM_LOG`
Turn off webdriver-manager logs use:

```python
import logging
import os

os.environ['WDM_LOG'] = str(logging.NOTSET)
```

### `WDM_LOCAL`
By default, all driver binaries are saved to user.home/.wdm folder. You can override this setting and save binaries to project.root/.wdm.

```python
import os

os.environ['WDM_LOCAL'] = '1'
```

### `WDM_SSL_VERIFY`
SSL verification can be disabled for downloading webdriver binaries in case when you have troubles with SSL Certificates or SSL Certificate Chain. Just set the environment variable `WDM_SSL_VERIFY` to `"0"`.

```python
import os

os.environ['WDM_SSL_VERIFY'] = '0'
```

### `path`
Set the directory where you want to download and save the webdriver. You can use relative and absolute paths.

```python
from webdriver_manager.chrome import ChromeDriverManager

ChromeDriverManager(path = r".\\Drivers").install()
```

### `version`
Specify the version of webdriver you need. And webdriver-manager will download it from sources for your os.
```python
from webdriver_manager.chrome import ChromeDriverManager

ChromeDriverManager(version="2.26").install()
```

### `cache_valid_range`
Driver cache by default is valid for 1 day. You are able to change this value using constructor parameter:

```python
from webdriver_manager.chrome import ChromeDriverManager

ChromeDriverManager("2.26", cache_valid_range=1).install()
```

### Custom HTTP Client
If you need to add custom HTTP logic like session or proxy you can define your custom HttpClient implementation.

```python
import os

import requests
from requests import Response

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.download_manager import WDMDownloadManager
from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.logger import log

class CustomHttpClient(HttpClient):

    def get(self, url, params=None, **kwargs) -> Response:
        """
        Add you own logic here like session or proxy etc.
        """
        log("The call will be done with custom HTTP client")
        return requests.get(url, params, **kwargs)


def test_can_get_chrome_driver_with_custom_http_client():
    http_client = CustomHttpClient()
    download_manager = WDMDownloadManager(http_client)
    path = ChromeDriverManager(download_manager=download_manager).install()
    assert os.path.exists(path)
```

This will make your test automation more elegant and robust!

Cheers
