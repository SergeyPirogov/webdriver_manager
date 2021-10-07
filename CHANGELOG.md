# Changelog


## 3.5.0
### Fixes
- Fix: WinError6 while executing script, packed in .exe by pyinstaller
- Fix: stdio problem when making exe using pyinstaller with noconsole flag
- Fix: error with execution right on linux afer extraction from zip
- Fix: In Manager.DriverManager constructor named argument log_level is never passed to log()
- Fix: first-line not hidden when logs disabled

### Features
- Download IEDriverServer from GitHub (#227)

### Other
- webdriver_manager tested on 3.6, **3.7, 3.8, 3.9, 3.10** (#235)
- webdriver_manager supports 3.6, 3.7, 3.8, **3.9, 3.10** (#235)
- webdriver_manager releases to pypi on publishing GitHub release (#238)
- renamed ci token from GITHUB_TOKEN to GH_TOKEN (#234)
---

lots releases ago...

---

## 1.7 (Released)
* Configuration supports environment variables
---
## 1.5 (Released)
* IEDriver bug fix for Win x64
* Additional logging addednged
* Cache path changed
---
## 1.4.5 (Released )
* Colorfull console output added
---
## 1.4.4 (Released )
* IEDriver support added
---
## 1.4.2 (Released 24.01.2017)
* PhantomJS support added
---
## 1.4 (Released 21.01.2017)
* Edge driver support added
* config.ini support added
---
## 1.3 (Released 29.12.2016)
* Python 3.5 support added
---
## 1.2 (Released 27.12.2016)
* Windows platform support added
* Github api token support added for Firefox
* Code refactoring
---
## 1.1 (Released 26.12.2016)
* Mac support added
* Cache support added
---
## 1.0 (Released 25.12.2016)
* Chrome support on linux
* Firefox support on linux
