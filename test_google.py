import os
import sys
import inspect
from nose.tools import with_setup
from selenium import webdriver
from sauceclient import SauceClient

browser = {
    "platform": "Windows 10",
    "browserName": "firefox",
    "version": "47"
}

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

caps = {}
caps.update(browser)
caps['name'] = inspect.stack()[1][3]
caps['build'] = os.environ.get('SAUCE_BUILD_NAME') or 'nosebuild'


def teardown_func():
    global driver
    driver.quit()
    sauce_client = SauceClient(username, access_key)
    status = sys.exc_info() == (None, None, None)
    sauce_client.jobs.update_job(driver.session_id, passed=status)
    print("SauceOnDemandSessionID={} job-name={}".format(driver.session_id, "abc"))


@with_setup(None, teardown_func)
def test_verify_google():
    global driver
    driver = webdriver.Remote(
        command_executor = "http:/{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key),
        desired_capabilities = caps);

    driver.get("http://www.google.com")
    assert ("Google" in driver.title), "Unable to load google page"

    elem = driver.find_element_by_name("q")
    elem.send_keys("Sauce Labs")
    elem.submit()
