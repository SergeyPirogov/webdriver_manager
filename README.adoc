= Webdriver Manager for Python

image:https://travis-ci.org/SergeyPirogov/webdriver_manager.svg?branch=master["Build Status", link="https://travis-ci.org/SergeyPirogov/webdriver_manager"]
image:https://img.shields.io/pypi/v/webdriver_manager.svg["PyPI", link="https://pypi.org/project/webdriver-manager/"]

The main idea is to simplify management of binary drivers for different browsers.

For now support:

- ChromeDriver
- GeckoDriver
- IEDriver
- OperaDriver

Before:
You should download binary chromedriver, unzip it somewhere in you PC and set path to this driver like this:

```
webdriver.Chrome('/home/user/drivers/chromedriver')

ChromeDriverManager(path=custom_path).install()
```

It's boring!!! Moreover every time the new version of driver released, you should go and repeat all steps again and again.

With webdriver manager, you just need to do two simple steps:

Install manager:

```
pip install webdriver_manager
```

Use with Chrome:

```python
from webdriver_manager.chrome import ChromeDriverManager

webdriver.Chrome(ChromeDriverManager().install())
```
Use with FireFox:

```python
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
```
If you face error related to github credentials, you need to place github token: (*)

```python
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
```
(*) access_token required to work with Github API more info https://help.github.com/articles/creating-an-access-token-for-command-line-use/.

Use with IE

```python
from webdriver_manager.microsoft import IEDriverManager

driver = webdriver.Ie(IEDriverManager().install())

```

Use with Opera

```python
from webdriver_manager.opera import OperaDriverManager

driver = webdriver.Opera(executable_path=OperaDriverManager().install()
```

If the opera browser is installed in a location other than C:/Program Files or C:/Program Files (x86) on windows
and /usr/bin/opera for all unix variants and mac, then use the below code,

```python
from webdriver_manager.opera import OperaDriverManager

options = webdriver.ChromeOptions()
options.add_argument('allow-elevated-browser')
options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
driver = webdriver.Opera(executable_path=OperaDriverManager().install(), options=options)
```

== Configuration

There is also possibility to set same variables via ENV VARIABLES.

Example:

```
export GH_TOKEN = "asdasdasdasd"
```

This will make your test automation more elegant and robust!

