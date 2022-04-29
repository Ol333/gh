# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tkinter import Tk
import time
import rab_with_db as rwd

chrome_options = Options()
chrome_options.add_argument("--headless")



#12596
for i in range(18155,5565999):
    try:
        driver = webdriver.Chrome('C:/Users/o-bob/Downloads/chromedriver_win32/chromedriver.exe')
        driver.wait = WebDriverWait(driver, 7)
        driver.get("https://system.81dojo.com/en/kifus/"+"%07d" % (i))
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

        kifu_id = rwd.kifu_add(out)
        counter = 0
        out = out.split('\n')
        for line in out:
            if counter == 5:
                player_id = rwd.player_check_add(line[3:])
                rwd.participation_add(player_id,kifu_id)
            if counter == 6:
                player_id = rwd.player_check_add(line[3:])
                rwd.participation_add(player_id,kifu_id)
                break
            counter += 1
    except TimeoutException:
        print(i)
    finally:
        driver.close()

