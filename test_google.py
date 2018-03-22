import os
import sys
import inspect
from nose.tools import with_setup
from selenium import webdriver
from sauceclient import SauceClient
from selenium.webdriver.remote.remote_connection import RemoteConnection


browser = {
    "platform": "Windows 10",
    "browserName": "firefox",
    "version": "47"
}

username = os.environ['SAUCE_USERNAME']
access_key = os.environ['SAUCE_ACCESS_KEY']

caps = {}
caps.update(browser)
caps['build'] = 'nosebuild'


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
    executor = RemoteConnection("http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key), resolve_ip=False)
    driver = webdriver.Remote(
        command_executor = executor,
        desired_capabilities = caps);

    driver.get("http://www.google.com")
    assert "Google" in driver.title

@with_setup(None, teardown_func)
def test_search_sauce():
    global driver
    executor = RemoteConnection("http://{}:{}@ondemand.saucelabs.com:80/wd/hub".format(username, access_key), resolve_ip=False)
    driver = webdriver.Remote(
        command_executor = executor,
        desired_capabilities = caps);

    driver.get("http://www.google.com")
    
    driver.find_element_by_name("q").send_keys("Sauce Labs")
    driver.find_element_by_name("q").submit()

    assert "Sauce Labs" in driver.title