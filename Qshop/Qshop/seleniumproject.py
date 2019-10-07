from time import sleep
from selenium import webdriver

chrome=webdriver.Chrome()

chrome.get('https://www.baidu.com/')
chrome.find_element_by_id('kw').send_keys('qq空间')
chrome.find_element_by_id('kw').click()
chrome.find_element_by_id('kw').click()
chrome.find_element_by_xpath('//*[@id="1"]/h3/a[1]')



