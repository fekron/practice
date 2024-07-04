from selenium import webdriver

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
url = 'https://www.codewars.com/users/fekron'
driver.get(url)

# Set a value into ls
driver.execute_script("localStorage.setItem('Key', 'Miracle');")

# Getting the value from ls
value = driver.execute_script("return localStorage.getItem('Key');")
print(f"Value from localStorage: {value}")

# Delete the value from ls
driver.execute_script("localStorage.removeItem('Key');")

# Check if deleted
value = driver.execute_script("return localStorage.getItem('Key');")
print(f"Value after deleting: {value}")

driver.get(url)

# Set a cookie
driver.add_cookie({"name": "UnknownCookie", "value": "Known"})

# Getting the value of a cookie
cookie = driver.get_cookie("UnknownCookie")
print(f"Getting the value of a cookie: {cookie['value']}")

# Delete the cookie
driver.delete_cookie("UnknownCookie")

# Check if deleted
cookie = driver.get_cookie("UnknownCookie")
print(f"Cookie after deleting: {cookie}")

driver.quit()