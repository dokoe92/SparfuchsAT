from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get("https://www.roksh.at/hofer/home")

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "accordionExample")))

category_ul = driver.find_element(By.ID, "accordionExample")
category_li = category_ul.find_elements(By.TAG_NAME, "li")

for li in category_li[1:]:
    a_link = li.find_element(By.TAG_NAME, "a")
    a_link.click()




