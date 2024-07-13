import csv
import re
import time

from bs4 import BeautifulSoup, PageElement
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Chrome()
driver.get('http://www.olympedia.org/statistics/medal/country')
wait = WebDriverWait(driver, 1)



year_dd = driver.find_element(By.ID, 'edition_select')
gender_dd = driver.find_element(By.ID, "athlete_gender")

year_options = year_dd.find_elements(By.TAG_NAME, 'option')
gender_options = gender_dd.find_elements(By.TAG_NAME, "option")

usa_lst = [
    ["Gold", "Silber", "Bronze", "Total", "Geschlecht", "Jahr"]
]
for gender in gender_options[1:]:
    gender.click()
    gender_val = gender.get_attribute("text")
    for year in year_options[2:]:
        try:
            year.click()
            td_wait = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='countries/USA']")))
        except TimeoutException:
            print(f"Timeout beim Warten auf Element für Jahr {year.text}. Weiter mit nächstem Jahr.")
            continue
        year_val = ""
        try:
            the_soup = BeautifulSoup(driver.page_source, 'html.parser')
            year_val = year.get_attribute("text")
            head = the_soup.find(href=re.compile("USA"))

            medal_values = head.find_all_next("td", limit=5)
            val_lst = [x.string for x in medal_values[1:]]
        except:
            val_lst = ["0" for x in range(4)]

        val_lst.append(gender_val)
        val_lst.append(year_val)

        usa_lst.append(val_lst)

driver.quit()

output_f = open("output.csv", "w", newline="")
output_writer = csv.writer(output_f)

for row in usa_lst:
    output_writer.writerow(row)

output_f.close()