# Changelog

---
## 3.5.2
### Features
- SSL verification can be disabled by setting `os.environ['WDM_SSL_VERIFY']='0'` in case if you have troubles with SSL Certificates or SSL Certificate Chain (like in issues
  [#219](https://github.com/SergeyPirogov/webdriver_manager/issues/219), [#226](https://github.com/SergeyPirogov/webdriver_manager/issues/226))
### Fixes
- Log duplication ([#259](https://github.com/SergeyPirogov/webdriver_manager/issues/259))
- Failed to Download the Edge driver for particular Version ([#251](https://github.com/SergeyPirogov/webdriver_manager/issues/251))
- WDM_LOG_LEVEL not work ([#255](https://github.com/SergeyPirogov/webdriver_manager/issues/255))
### Improvements
- Softly download latest webdriver version even if browser version is unknown. ([#254](https://github.com/SergeyPirogov/webdriver_manager/issues/254), also fixes [#251](https://github.com/SergeyPirogov/webdriver_manager/issues/251))
- Speed up when using "latest" version ([#259](https://github.com/SergeyPirogov/webdriver_manager/issues/259))
---
## 3.5.1
### IEDriver
- Fix: huge typo in IEDriver (appeared accidentally in 3.5.0 version)
- Adopt finding latest IEDriverSever for irregular releases in selenium ([#247](https://github.com/SergeyPirogov/webdriver_manager/issues/247))
### EdgeDriver
- Feature: finding EdgeDriver version for MAC & LINUX depends on MSEdge browser version and OS type [#243](https://github.com/SergeyPirogov/webdriver_manager/issues/243), Fix for [#242](https://github.com/SergeyPirogov/webdriver_manager/issues/242)
- Fix: Add rights to execute edgedriver binary on linux.
- Test Coverage: More tests for EdgeDriver

---
## 3.5.0
### Fixes
- Fix: WinError6 while executing script, packed in .exe by pyinstaller ([#198](https://github.com/SergeyPirogov/webdriver_manager/issues/198))
- Fix: stdio problem when making exe using pyinstaller with noconsole flag ([#198](https://github.com/SergeyPirogov/webdriver_manager/issues/198))
- Fix: error with execution right on linux afer extraction from zip ([#208](https://github.com/SergeyPirogov/webdriver_manager/issues/208))
- Fix: In Manager.DriverManager constructor named argument log_level is never passed to log() (#[172](https://github.com/SergeyPirogov/webdriver_manager/issues/172))
- Fix: first-line not hidden when logs disabled ([#212](https://github.com/SergeyPirogov/webdriver_manager/issues/212))

### Features
- Download IEDriverServer from GitHub ([#227](https://github.com/SergeyPirogov/webdriver_manager/issues/227))

### Other
- webdriver_manager now tests on 3.6, **3.7, 3.8, 3.9, 3.10** ([#235](https://github.com/SergeyPirogov/webdriver_manager/issues/235))
- webdriver_manager now supports not only 3.6, 3.7, 3.8, but also **3.9, 3.10** ([#235](https://github.com/SergeyPirogov/webdriver_manager/issues/235)) (tbh always has been)
- webdriver_manager now releases to pypi by clicking "Publish GitHub release" button ([#238](https://github.com/SergeyPirogov/webdriver_manager/issues/238))
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
