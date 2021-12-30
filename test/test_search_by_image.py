import sys
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def wait_and_click(browser, xpath):
    #  Sometimes click fails unreasonably. So tries to click at all cost.
    try:
        w = WebDriverWait(browser, 15)
        elem = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
    except Exception as e:
        see_more_xpath = '//*[@id="islmp"]/div/div[1]/div/div[2]/span'
        wait_and_click(browser, see_more_xpath)
    return True


chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:10888")
browser = webdriver.Chrome(executable_path="../chromedriver/chromedriver_linux", chrome_options=chrome_options)

browser.get("https://www.google.com/imghp?hl=en&authuser=0&ogbl")
browser.find_element_by_xpath('//*[@id="sbtc"]/div[2]/div[3]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="dRSWfb"]/div/a').click()
w = WebDriverWait(browser, 15)
elem = w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="awyMjb"]')))
elem.send_keys(sys.argv[1])
elem = w.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rso"]/div[2]/div/div[2]/g-section-with-header/div[1]/title-with-lhs-icon/a/div[2]/h3')))
elem.click()

time.sleep(1)
elem = browser.find_element_by_tag_name("body")
print('Scraping links')

wait_and_click(browser, '//div[@data-ri="0"]')
time.sleep(1)

links = []
count = 1

last_scroll = 0
scroll_patience = 0

while True:
    try:
        xpath = '//div[@id="islsp"]//div[@class="v4dQwb"]'
        div_box = browser.find_element(By.XPATH, xpath)

        xpath = '//img[@class="n3VNCb"]'
        img = div_box.find_element(By.XPATH, xpath)

        xpath = '//div[@class="k7O2sd"]'
        loading_bar = div_box.find_element(By.XPATH, xpath)

        # Wait for image to load. If not it will display base64 code.
        while str(loading_bar.get_attribute('style')) != 'display: none;':
            time.sleep(0.1)

        src = img.get_attribute('src')

        if src is not None:
            links.append(src)
            print('%d: %s' % (count, src))
            count += 1

    except StaleElementReferenceException:
        # print('[Expected Exception - StaleElementReferenceException]')
        pass
    except Exception as e:
        print('[Exception occurred while collecting links from google_full] {}'.format(e))

    scroll = browser.execute_script("return window.pageYOffset;")
    if scroll == last_scroll:
        scroll_patience += 1
    else:
        scroll_patience = 0
        last_scroll = scroll

    if scroll_patience >= 30:
        break

    elem.send_keys(Keys.RIGHT)

links = list(dict.fromkeys(links))
print(links)
browser.close()
