from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd

# basic website scraping
driver_loc = "/Users/noel/Documents/SCBC/Drivers/chromedriver"  # driver location should be inputted by user
driver = webdriver.Chrome(executable_path=driver_loc)

website = "https://med-ed.case.edu/searchfacultyinfo/SearchFaculty.aspx"
driver.get(website)

search_button = driver.find_element_by_name("ctl00$cphBody$img_Search_top")

element = driver.find_element_by_xpath("//select[@name='ctl00$cphBody$ddlistSearch_LN']")
all_options = element.find_elements_by_tag_name("option")

contact_info_list = pd.DataFrame()

doctors = []
for option in all_options[1:]:
    doctors.append(option.text)

for doctor in doctors:
    driver.get(website)
    select = Select(driver.find_element_by_xpath("//select[@name='ctl00$cphBody$ddlistSearch_LN']"))
    select.select_by_value(doctor)
    search_button = driver.find_element_by_name("ctl00$cphBody$img_Search_top")
    search_button.click()

    sub_dfs = pd.read_html(driver.page_source)
    contact_info_list = contact_info_list.append(sub_dfs[5], ignore_index=True)

driver.close()

# data cleaning
contact_info_list = contact_info_list.drop(columns=['PubMed'])
contact_info_list.rename(columns={'Contact Info.': 'Emails'}, inplace=True)

# removing phone number
for index, email in enumerate(contact_info_list['Emails']):
    if isinstance(email, str) == True:
        for text in email.split(' '):
            if text.find('@') != -1:
                contact_info_list['Emails'][index] = text
