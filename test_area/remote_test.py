from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from functional import seq

from globals import chromedriver
from globals import path_to_dataset_folder

import pandas as pd


# Example of listing all content from plain files in github with ajax requests
def connect_to_opened_chrome(path_to_chrome_driver, port):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:" + str(port))
    chrome_driver = path_to_chrome_driver
    return webdriver.Chrome(chrome_driver, options=chrome_options)

# ----------------------------------
# Connect by port number and driver path
driver = connect_to_opened_chrome(chromedriver, 9222)
# Set up waiting
main_wait = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
# ----------------------------------
# elems = seq(arrayOfWebElements)
# print pairs of file name and file type (dir of plain file)
# example for js with only file name
# document.querySelectorAll("div.Details div.Box-row")[0].querySelector("a[title]").getAttribute("title")
# example with pair of type and title
# Array.from(document.querySelectorAll("div.Details div.Box-row")).map(elem => "title: " + elem.querySelector("svg[aria-label]").getAttribute("aria-label") + " type: " + elem.querySelector("a[title]").getAttribute("title"))
# ----------------------------------
# Origin code - Github repo interspection
# print(elems.map(lambda elem:
#     "type: " +
#     elem.find_element_by_css_selector("svg[aria-label]").get_attribute("aria-label")
#     + " titile: " +
#     elem.find_element_by_css_selector("a[title]").get_attribute("title"))
# )

# ----------------------------------
# Example 1
# StackOverflow: Gradient Descent question - votes count
# driver.get("https://stackoverflow.com/questions/17784587/gradient-descent-using-python-and-numpy")
# ----------------------------------
# Additional test-links:
# driver.get("https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy")
# driver.get("https://stackoverflow.com/questions/9537392/git-fetch-remote-branch")
# ----------------------------------
# topic_title = driver.find_elements_by_css_selector("div#question-header")
# topic_tags = driver.find_elements_by_css_selector("div.post-taglist a.post-tag")
# arrayOfWebElements = driver.find_elements_by_css_selector("div.votecell")
# elems = seq(arrayOfWebElements)
# ----------------------------------
# print(seq(topic_title).map(lambda title:
#     title.find_element_by_css_selector("a.question-hyperlink").get_attribute("text"))[0], '\n', \
#     "Topic tags: ", seq(topic_tags).map(lambda tag:
#     tag.get_attribute("text")), '\n', \
#     elems.map(lambda elem: "Topic-starter_votes: " +
#     elem.find_element_by_css_selector("div.js-vote-count").get_attribute("data-value"))[0], \
#     '\n', "Answers_votes:",\
#     elems.map(lambda elem: elem.find_element_by_css_selector("div.js-vote-count").get_attribute("data-value"))[1:]
# )
# ----------------------------------
# Example 2
# Compare Vacancies from HeadHunter
# driver.get("https://spb.hh.ru/vacancies/data-scientist")
driver.get("https://hh.ru/vacancies/data-scientist")
wait_1 = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException]). \
    until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
vacancies = driver.find_elements_by_css_selector("div.vacancy-serp-item")

# pages = driver.find_elements_by_css_selector("span.bloko-button-group")
# pages = driver.find_elements_by_css_selector('div[data-qa="pager-block"]')
next_button = driver.find_elements_by_css_selector("a.HH-Pager-Controls-Next")

pages = []

def page_clicker():
    first_element = driver.find_elements_by_css_selector('span[data-qa="pager-page"]')
    elements = driver.find_elements_by_css_selector('span a.bloko-button')
    links = [link.get_attribute("href") for link in elements]
    pages.extend(links)

page_clicker()
print(pages)

# for page in pages:
#     print(page)
#     try:
#         pass
#     except:
#         pass

vacancies_df = pd.DataFrame()

# for link in vacancies[0:2]:
#     try:
#         link.find_element_by_css_selector("a.HH-LinkModifier").click()
#         driver.switch_to.window(driver.window_handles[1])
#         element = main_wait.until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa=\"vacancy-description\"]")))
#         vacancy_content = []
#
#         # vacancy_title = driver.find_element_by_css_selector("h1.bloko-header-1")
#         # vacancy_salary = driver.find_element_by_css_selector("p.vacancy-salary")
#         # vacancy_description = driver.find_element_by_css_selector("div[data-qa=\"vacancy-description\"]")
#         # vacancy_tags = driver.find_element_by_css_selector("div.bloko-tag-list")
#         # vacancy_content = ['vacancy_title', 'vacancy_salary', 'vacancy_description', 'vacancy_tags']
#         # vacancies_df = vacancies_df.append(vacancy_content)
#
#         vacancy_content.append(driver.find_element_by_css_selector("h1.bloko-header-1").text)
#         vacancy_content.append(driver.find_element_by_css_selector("a[data-qa=\"vacancy-company-name\"]").text)
#         vacancy_content.append(driver.find_element_by_css_selector("p[data-qa=\"vacancy-view-location\"]").text)
#         vacancy_content.append(driver.find_element_by_css_selector("span[data-qa=\"vacancy-experience\"]").text)
#         vacancy_content.append(driver.find_element_by_css_selector("p[data-qa=\"vacancy-view-employment-mode\"]").text)
#         vacancy_content.append(driver.find_element_by_css_selector("p.vacancy-salary").text)
#         vacancy_content.append(driver.find_element_by_css_selector("p.vacancy-creation-time").text)
#         vacancy_content.append(driver.find_element_by_css_selector("div[data-qa=\"vacancy-description\"]").text)
#         vacancy_content.append(driver.find_element_by_css_selector("div.bloko-tag-list").text)
#         vacancies_df = pd.concat([vacancies_df, pd.Series(vacancy_content)], axis=1)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])
#     except (NoSuchElementException, StaleElementReferenceException):
#         vacancy_content.append(None)
#         vacancies_df = pd.concat([vacancies_df, pd.Series(vacancy_content)], axis=1)
#         driver.close()
#         driver.switch_to.window(driver.window_handles[0])

# vacancies_df = pd.DataFrame(index=['vacancy_title', 'vacancy_salary', 'vacancy_description', 'vacancy_tags']).T
#
# for handle in driver.window_handles[1:]:
#     driver.switch_to.window(handle)
#     WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException]). \
#         until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa=\"vacancy-description\"]")))
#     vacancy_title = driver.find_element_by_css_selector("h1.bloko-header-1")
#     vacancy_salary = driver.find_element_by_css_selector("p.vacancy-salary")
#     vacancy_description = driver.find_element_by_css_selector("div[data-qa=\"vacancy-description\"]")
#     vacancy_tags = driver.find_element_by_css_selector("div.bloko-tag-list")
#     vacancy_content = [vacancy_title.text, vacancy_salary.text, vacancy_description.text, vacancy_tags.text]
#     vacancies_df = vacancies_df.append(vacancy_content)
#     driver.close()

vacancies_df.to_csv(path_to_dataset_folder + 'vacancies_data.csv')

# ----------------------------------
# Example 4
# Create dataset from vacancies from HeadHunter (see also Example 2 and Example 3)

# for link in vacancies[0:2]: # there's 50 vacancies on the page - let's test on some
#     link.find_element_by_css_selector("a.HH-LinkModifier").click()
#     driver.switch_to.window(driver.window_handles[0])
#     WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException]). \
#         until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
#
# for handle in driver.window_handles[1:]:
#     driver.switch_to.window(handle)
#     WebDriverWait(driver, 5, poll_frequency=1). \
#         until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-description")))
#     print("---")
#     print(driver.find_element_by_css_selector("div.bloko-tag-list").text)
#     driver.close()

# list_of_links = []

# for vacancy in seq(vacancies):
#     try:
#         # list_of_links.append(vacancy.find_element_by_css_selector("a.HH-LinkModifier").get_attribute("href"))
#         pass
#         wait = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException]). \
#             until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
#         vacancy.find_element_by_css_selector("a.HH-LinkModifier").get_attribute("href")
#
#     except:
#         pass

driver.quit()
