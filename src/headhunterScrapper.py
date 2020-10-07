import sys
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *

from chromium import *

import pandas as pd

@dataclass
class ScrapperConfig:
    path_to_driver: str
    path_to_output: str
    command: str
    port: int

# Usage: path_to_driver path_to_output command (open|connect port)
def parseCliArguments():
    argv = len(sys.argv)
    if (argv < 4 or 5 < argv):
        raise ValueError("usage: path_to_driver path_to_output command (open|connect port)")
    args = sys.argv
    port = int(args[4]) if 5 == argv else -1
    command = "open" if "connect" != args[3] else "connect"
    return ScrapperConfig(args[1], args[2], command, port)


def page_scrapper():
    """
    Function for scrapping pages.

    Parameters
    ----------
        Takes no arguments.

    Returns
    -------
        Gives no return.

    For more information see source code.
    """

    global vacancies_df
    # Waiting for the presence of vacancies
    main_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
    # Take required elements
    vacancies = driver.find_elements_by_css_selector("div.vacancy-serp-item")
    # Iterating over list of vacancies
    for link in vacancies:
        vacancy_content = []
        try:
            # print('Checkpoint_1') # Required for debugging
            # Waiting for the presence of vacancies
            main_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.HH-LinkModifier")))
            link.find_element_by_css_selector("a.HH-LinkModifier").click()
            driver.switch_to.window(driver.window_handles[1])

            # Waiting for required information
            main_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa=\"vacancy-description\"]")))
            # Gather required information
            vacancy_content.append(driver.find_element_by_css_selector("h1.bloko-header-1").text)
            vacancy_content.append(driver.find_element_by_css_selector("a[data-qa=\"vacancy-company-name\"]").text)
            vacancy_content.append(driver.find_element_by_css_selector("p[data-qa=\"vacancy-view-location\"]").text)
            vacancy_content.append(driver.find_element_by_css_selector("span[data-qa=\"vacancy-experience\"]").text)
            vacancy_content.append(
                driver.find_element_by_css_selector("p[data-qa=\"vacancy-view-employment-mode\"]").text)
            vacancy_content.append(driver.find_element_by_css_selector("p.vacancy-salary").text)
            vacancy_content.append(driver.find_element_by_css_selector("p.vacancy-creation-time").text)
            vacancy_content.append(driver.find_element_by_css_selector("div[data-qa=\"vacancy-description\"]").text)
            vacancy_content.append(driver.find_element_by_css_selector("div.bloko-tag-list").text)

            # Appending collected data from page to DataSet
            vacancies_df = pd.concat([vacancies_df, pd.Series(vacancy_content)], axis=1)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except (NoSuchElementException, StaleElementReferenceException):
            vacancy_content.append(None)
            vacancies_df = pd.concat([vacancies_df, pd.Series(vacancy_content)], axis=1)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])


# ----------------------------------
scrapperConfig = parseCliArguments()
print(scrapperConfig)
# ----------------------------------
driver = open_chrome_browser(scrapperConfig.path_to_driver) if "open" == scrapperConfig.command else connect_to_opened_chrome(scrapperConfig.path_to_driver, scrapperConfig.port)
# ----------------------------------
# Set up waiting
main_wait = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException])
# ----------------------------------
# Get Vacancies from HeadHunter
driver.get("https://hh.ru/vacancies/data-scientist")
wait_1 = WebDriverWait(driver, 5, poll_frequency=1, ignored_exceptions=[NoSuchElementException]). \
    until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
# ----------------------------------
# HH by default determines geolocation and changes vacancies to local ones.
# We do not need this, therefore, we find the switch responsible for this and turn it off. Then rebooting the page.
main_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.bloko-icon_cancel"))).click()
driver.refresh()
# ----------------------------------
# Creating pandas DataFrame for storing collected data
vacancies_df = pd.DataFrame()
# Some additional variable for navigation
num_pages = len(driver.find_elements_by_css_selector("span a.bloko-button"))
# Iterating over pages with vacancies
for i in range(num_pages):
    print("Performing scrapping on page {}.".format(str(i + 1)))
    page_scrapper()
    # Go to next page with vacancies
    main_wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.HH-Pager-Controls-Next"))).click()
    print("Went on page {}.".format(str(i + 2)))

print("Performing scrapping on page {}.".format(str(num_pages+1)))
page_scrapper()
print("Scrapping is over. Congratulations!")
# ----------------------------------
# To CSV file
vacancies_df.to_csv(scrapperConfig.path_to_output + '/vacancies_data.csv')
# ----------------------------------
driver.quit()
