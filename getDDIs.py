################### NOT USED, COULD NOT GET TO WORK ###################

# import selenium stuff
# needs pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# to have waits
import time

# disable cache to improve memory hopefully
options = webdriver.ChromeOptions()
options.add_argument("--disable-application-cache")
options.add_argument("--headless")

# create webdriver object
driver = webdriver.Chrome(options=options)

# causes bug in headless mode otherwise
driver.maximize_window()

# get website url, this link has filters pre applied
driver.get("https://go.drugbank.com/drugs?approved=0&approved=1&nutraceutical=0&illicit=0&investigational=0&withdrawn=0&experimental=0&us=0&us=1&ca=0&eu=0&commit=Apply+Filter")

# init action chains to scroll to elements
actions = ActionChains(driver)

# get rid of navbar bc its really annoying
time.sleep(1)
nav = driver.find_element(By.CLASS_NAME, "close-banner")
nav.click()

# get table of all drugs with applied filter above
table = driver.find_element(By.XPATH, "//*[@id=\"drugs-table\"]/tbody")

# with table, grab all the elements within the table
rows = table.find_elements(By.TAG_NAME, "tr")

# since the xpath iterates with the element index, we can just iterate through those
# test value, will use for loop later
index = 5
rows[index].find_element(By.XPATH, "//*[@id=\"drugs-table\"]/tbody/tr[" + str(index + 1) + "]/td[1]/strong/a").click()

time.sleep(1) # so selenium can catch up to webpage and we dont overload servers

# debug print
print("Drug name: ")
drug = driver.find_elements(By.CLASS_NAME, "col-xl-4")
print(drug[0].text)
print("\nDrug id: ")
print(drug[1].text)

# now we can grab all the interactions
interactionTable = driver.find_elements(By.XPATH, "//*[@id=\"drug-interactions-table\"]/tbody")

if(len(interactionTable) == 0):

    print("No interactions found")
else:

    interactionRows = interactionTable[0].find_elements(By.TAG_NAME, "tr")
    print("\nInteractions found! length of table: " + str(len(interactionTable)))

    # scroll table into view
    actions.move_to_element(interactionTable[0]).perform()

    # read all drug names and ID on table
    limit = int(driver.find_element(By.XPATH,"//*[@id=\"drug-interactions-table_paginate\"]/ul/li[8]/a").text)

    for i in range(limit - 1):

        # debug
        time.sleep(0.5)

        # this scrolls up a little bit so that the navbar doesnt block view
        moveup = driver.find_element(By.XPATH, "//*[@id=\"interactions-sidebar-header\"]")
        moveup.click()
        moveup.send_keys(Keys.PAGE_UP)

        # refind element so that it isnt stale when we move pages
        interactionTable = driver.find_elements(By.XPATH, "//*[@id=\"drug-interactions-table\"]/tbody")
        interactionRows = interactionTable[0].find_elements(By.TAG_NAME, "tr")

        time.sleep(3)

        # scroll table into view
        actions.move_to_element(interactionTable[0]).perform()

        # read all drugs on table
        for tableIndex in range(len(interactionRows)): # enumerate does not work since tableIndex becomes a tuple

            # click on link to get drug name and ID
            interactionLink = interactionTable[0].find_element(By.XPATH, "//*[@id=\"drug-interactions-table\"]/tbody/tr[" + str(tableIndex + 1) + "]/td[1]/a")

            # need to scroll down to element so that it is clickable
            if(tableIndex > 3): # dont scroll on first few since it may go too far and be blocked by navbar
                actions.move_to_element(interactionLink).perform()

            # rest for a bit so that we dont overload servers and give time to move down
            time.sleep(1)
            interactionLink.click()

            # wait for new page to load
            time.sleep(1)

            # get interaction drug name
            interaction = driver.find_elements(By.CLASS_NAME, "col-xl-4")

            print(tableIndex)

            # debug print
            # print("interaction name: " + interaction[0].text)
            # print("interaction id: " + interaction[1].text)

            # go back a page to return to interaction table
            driver.back()

        # go to next page on the table
        button = driver.find_element(By.XPATH, "//*[@id=\"drug-interactions-table_next\"]/a")
        actions.move_to_element(button).perform()
        button.click()

        # print to see how far it got in headless mode
        print(i)

# go back to original table
driver.back()

time.sleep(10)

# close driver
driver.quit()