#!coding=utf-8
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
import time


class TBCrawl():
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.get("https://rate.taobao.com/user-rate-UvCHWvG84MGvYMgTT.htm?spm=a1z10.1-c.0.0.z0hM8L")
        #self.driver.get("https://rate.taobao.com/user-rate-UvFvYvmNuvmH4.htm?spm=2013.1.0.0.7h9GED")
        self.handle = self.driver.current_window_handle
        print self.handle

    def get_items(self):
        elem = self.driver.find_elements_by_xpath('//div[contains(@class, "rate-item")]')
    #for item in elem: 
    #    item. 
    #elem = driver.find_element_by_xpath('//div[contains(@class, "reviews-list")]/div[1]//a')
        for item in elem:
            try:
                link = item.find_element_by_tag_name('a').text
                date = item.find_element_by_class_name('tb-r-date').text
                price =  item.find_element_by_class_name('price').text
#                if not (link and date and price):
#                    return False
                print link
                print date
                print price
            except StaleElementReferenceException as e: 
                print "**********Except*************"

                continue
                link = item.find_element_by_tag_name('a').text
                date = item.find_element_by_class_name('tb-r-date').text
                price =  item.find_element_by_class_name('price').text
                

    def write_to_mysql(self):
        pass

    def pages_loop(self):
        #driver = webdriver.PhantomJs()

        print self.driver.title
        #elem = driver.find_element_by_xpath('//div[contains(@class, "rate-item")][1]/div[1]/a')
        weekly = self.driver.find_element_by_xpath('//ul[contains(@class, "menu-tab")]/li[1]')
        weekly.click()
        goods = self.driver.find_element_by_xpath('//a[@class="J_show_list"]')
        goods.click()

        #print elem[0].tag_name, elem[0].text
        #elem.clear()
        self.get_items()
        while True:
            try:
                #nextpage = self.driver.find_element_by_class_name('pg-next')        
                #nextpage.click()
                ##WebDriverWait(self.driver, 4).until(self.get_items())
                #self.get_items()

                self.get_items()
                for i in range(100):
                    print str(i) + "*****"
                    time.sleep(0.5)
                    element = self.driver.find_element_by_class_name('pg-next')
                    print str(i) + "------"

                    actions = ActionChains(self.driver);

                    actions.move_to_element(element).click().perform()
                    #self.driver.find_element_by_class_name('pg-next').click()
                self.get_items()

                try:
                    self.driver.find_element_by_class_name('pg-disabled')
                    print "=========page over=========="
                    break
                except Exception as e:
                    continue
            except WebDriverException as e:
                print "Oops"
                time.sleep(5)
                print self.driver.find_element_by_id("J_sufei").find_element_by_tag_name("iframe")
                self.driver.switch_to_frame(self.driver.find_element_by_id("J_sufei").find_element_by_tag_name("iframe"))
                self.driver.find_element_by_id('J_LoginBox')
                self.driver.find_element_by_id('TPL_username_1').send_keys("user")
                self.driver.find_element_by_id('TPL_password_1').send_keys("********")
                self.driver.find_element_by_id('J_SubmitStatic').click()
                self.driver.switch_to_default_content()
                handlers = self.driver.window_handles
                print len(handlers)
                self.driver.switch_to_window(handlers[0])
                #break
                #print "Continue"
                continue
        assert "No results found." not in self.driver.page_source

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    tbcrawl = TBCrawl()
    tbcrawl.pages_loop()
    tbcrawl.close()
