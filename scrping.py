from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
driver = webdriver.Chrome()

# navigate to Google.com
driver.get("https://jobs.apple.com/en-us/search?search=python&sort=relevance&location=united-states-USA")

time.sleep(2)

try:
    # Try to find the element by id
    element = driver.find_element("id", 'findPerfectRole')
    print('Element with id "findPerfectRole" found on the page.')
except NoSuchElementException:
    print('Element with id "findPerfectRole" not found on the page.')



# close the browser
driver.quit()