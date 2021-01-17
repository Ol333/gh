# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tkinter import Tk
import time

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome('C:/Users/o-bob/Downloads/chromedriver_win32/chromedriver.exe')
driver.get("https://system.81dojo.com/en/kifus/0999999#document")

driver.wait = WebDriverWait(driver, 10)

element = driver.wait.until(EC.presence_of_element_located((By.ID, "viewer_frame")))
element.get_property('height')
act = webdriver.common.action_chains.ActionChains(driver)
act.move_to_element(element)
act.move_by_offset(144,-213)
# act.move_by_offset(30,71) #download
act.move_by_offset(30,53) #copy
act.click()
act.pause(5)
act.perform()

out = Tk().clipboard_get()
print(out)