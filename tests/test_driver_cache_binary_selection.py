from webdriver_manager.core.driver_cache import DriverCacheManager


def test_get_binary_skips_third_party_notices_for_chromedriver(tmp_path):
    cache = DriverCacheManager(root_dir=str(tmp_path))
    files = [
        "chromedriver-mac-arm64/THIRD_PARTY_NOTICES.chromedriver",
        "chromedriver-mac-arm64/LICENSE.chromedriver",
        "chromedriver-mac-arm64/chromedriver",
    ]

    binary = cache._DriverCacheManager__get_binary(files, "chromedriver")

    assert binary == "chromedriver-mac-arm64/chromedriver"
