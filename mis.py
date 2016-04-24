# -*- coding: utf-8 -*-
"""
Get this shit done quickly.
"""

from getpass import getpass
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import (WebDriverWait,
                                           Select)
from selenium.webdriver.support import expected_conditions as EC

class MIS:
    """
    MIS Base
    """
    URL = "http://mis.nitt.edu/prm/index.html"
    LOGIN_CHECK = "Wel-Come"

    def __init__(self, email, passwd):
        self.email = email
        self.passwd = passwd
        self.driver = webdriver.PhantomJS()
        self.driver.implicitly_wait(10)
        self.driver.get(MIS.URL)

    
    def login(self):
        """
        Login into MIS
        :params email: User's email
        :params passwd: User's password 
        :returns: True if logged in otherwise False
        """
        user_id = self.driver.find_element_by_id('user')
        user_pwd = self.driver.find_element_by_id('passwd')
        
        user_id.send_keys(self.email)
        user_pwd.send_keys(self.passwd)
        user_pwd.send_keys(Keys.RETURN)

        return MIS.LOGIN_CHECK in self.driver.title


def main():
    
    email = raw_input(">Username:  ")
    passwd = getpass(">Password:   ")

    mis = MIS(email, passwd)
    
    if not mis.login():
        try:
            raise Exception("Invalid username/password. Try again.")
        except Exception as e:
            print(e)

    mis.driver.switch_to.frame('contents')
    # Shit works atm. Make it better later
    hall_link = mis.driver.find_element_by_xpath("/html/body/form/div[1]/div/table/tbody/tr[4]/td/a")
    hall_link.click()

    try:
        elementFound = WebDriverWait(mis.driver, 10).until(
            EC.presence_of_element_located((By.ID, "BtnHallTicket")))
    except TimeoutException:
        hall_link.click()
    mis.driver.switch_to.default_content()
    mis.driver.switch_to.frame('main')
    subject_count = len(mis.driver.find_elements_by_css_selector(
                        '#DataGrid1 > tbody > tr')) - 1
    for subject in range(2, subject_count + 2):
        sub_id = "DataGrid1__ctl{}_RadioButton1".format(subject)
        print(sub_id)
        mis.driver.find_element_by_id(sub_id).click()
        mis.driver.find_element_by_id('Button1').click()
        # try:
        #     # Wait until the form has been loaded
        #     elementFound = WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.ID, "DataGrid1__ctl2_dt1")))
        # except TimeoutException:
        #     print("Timeout, retrying..")
        #     mis.driver.find_element_by_id('Button1').click()

        for op in xrange(2,12):
            op_id = "DataGrid1__ctl{}_dt1".format(op)
            select = Select(mis.driver.find_element_by_id(op_id))
            # 7 score
            select.select_by_visible_text('7')

        for op in xrange(1, 5):
            comment_id = 'TxtF{}'.format(op)
            # Default message
            mis.driver.find_element_by_id(comment_id).send_keys('NA')
            if op == 4:
                print("subj {} done.".format(subject))
                mis.driver.find_element_by_id(comment_id).submit()
        
        mis.driver.find_element_by_id("Button3").click() 
    
    mis.driver.find_element_by_id("BtnHallTicket").click()
    print('plugin downloading..')
    mis.driver.find_element_by_id("plugin").click()


if __name__ == "__main__":
    main()
