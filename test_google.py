import os
import sys
import inspect
from nose.tools import with_setup
from selenium import webdriver
from sauceclient import SauceClient

browsers = [{
    "platform": "Windows 10",
    "browserName": "internet explorer",
    "version": "11"
}, {
    "platform": "OS X 10.11",
    "browserName": "safari",
    "version": "9.0"
}]

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

def launchBrowser(caps):
    caps['name'] = inspect.stack()[1][3]
    return webdriver.Remote(
            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (username, access_key),
            desired_capabilities = caps);

def teardown_func():
    global driver
    driver.quit()
    sauce_client = SauceClient(username, access_key)
    status = sys.exc_info() == (None, None, None)
    sauce_client.jobs.update_job(driver.session_id, passed=status)
    print "SauceOnDemandSessionID=%s job-name=%s" % (driver.session_id, "abc")

# Will generate a test for each browser and os configuration
def test_generator_verify_google():
    for browser in browsers:
        yield verify_google, browser

@with_setup(None, teardown_func)
def verify_google(browser):
    global driver
    driver = launchBrowser(browser)
    driver.get("http://www.google.com")
    assert ("Google" in driver.title), "Unable to load google page"
    elem = driver.find_element_by_name("q")
    elem.send_keys("Sauce Labs")
    elem.submit()
