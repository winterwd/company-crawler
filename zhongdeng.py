#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://192.168.1.23:8090/login.action")

os_username = driver.find_element(By.ID, "os_username")
os_username.send_keys('weidong@zhidekan.me')

os_password = driver.find_element(By.ID, "os_password")
os_password.send_keys('weidong@zhidekan.me')

loginButton = driver.find_element(By.ID, "loginButton")
loginButton.submit()