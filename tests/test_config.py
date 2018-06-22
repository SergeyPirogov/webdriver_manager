import os

from webdriver_manager.config import Configuration

expect_mz_latest = 'https://api.github.com/repos/mozilla/geckodriver/releases/latest'
expect_mz_tag = 'https://api.github.com/repos/mozilla/geckodriver/releases/tags/{0}'


def test_config_with_default_params():
    config = Configuration(config_folder=os.path.dirname(__file__), section="GeckoDriver", file_name="config.ini")
    assert config.driver_latest_release_url == expect_mz_latest
    assert config.mozila_release_tag == expect_mz_tag


def test_config_variables_with_default_params():
    config = Configuration(section="GeckoDriver", file_name="", config_folder="")
    assert config.driver_latest_release_url == expect_mz_latest
    assert config.mozila_release_tag == expect_mz_tag


def test_config_with_custom_file():
    config = Configuration(config_folder=os.path.dirname(__file__), file_name="wd_config.ini", section="GeckoDriver")
    assert config.driver_latest_release_url == "test_release"


def test_config_can_get_variable_from_env():
    os.environ["OFFLINE"] = 'true'
    config = Configuration(config_folder=os.path.dirname(__file__), file_name="wd_config.ini", section="GeckoDriver")
    assert config.offline == 'true'
    os.environ["OFFLINE"] = 'false'


def test_config_can_get_variable_from_file_if_no_env_variable_set():
    config = Configuration(config_folder=os.path.dirname(__file__), file_name="wd_config.ini", section="GeckoDriver")
    assert config.offline == 'false'
