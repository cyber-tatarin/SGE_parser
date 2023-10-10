import os
import time
import uuid

from bs4 import BeautifulSoup
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


def get_chromedriver(proxy_setup=True, user_agent=True):
    chrome_options = Options()
    
    # chrome_options.add_argument("--user-data-dir=C:\\Users\\Dima Tatarin\\AppData\\Local\\Google\\Chrome\\User Data")
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless=new')
    # prefs = {'profile.default_content_setting_values': {'images': 2}}
    # chrome_options.add_experimental_option('prefs', prefs)
    # chrome_options.add_argument('--ignore-ssl-errors=yes')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--disable-crash-reporter')
    # 'OSrXXb', 'Uq97l'
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--disable-plugins")
    # # # # chrome_options.add_argument("--disable-local-storage")
    # chrome_options.add_argument("--disable-cache")
    # chrome_options.add_argument("--disable-application-cache")
    # chrome_options.add_argument("--disable-file-system")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    
    if user_agent:
        chrome_options.add_argument(
            f'--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
    
    if proxy_setup:
        seleniumwire_options = {
            'proxy': {
                'http': os.getenv('PROXY_SETUP'),
                'https': os.getenv('PROXY_SETUP'),
                # 'no_proxy': 'localhost,127.0.0.1'  # excludes
            },
            # 'verify_ssl': False
        }
        
        driver = webdriver.Chrome(options=chrome_options,
                                  seleniumwire_options=seleniumwire_options)
        
        driver.get('http://httpbin.org/ip')
        print(driver.find_element(By.TAG_NAME, 'body').text)  # { "origin": "185.199.229.156" }
        
        return driver
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('http://httpbin.org/ip')
    print(driver.find_element(By.TAG_NAME, 'body').text)  # { "origin": "185.199.229.156" }
    
    return driver


def match_class(target):
    classes_to_match = ['OSrXXb', 'Uq97l']
    if target.has_attr("class"):
        if any(single_class in target["class"] for single_class in classes_to_match):
            return True
    return False


class Handler:
    def __init__(self):
        self.driver = get_chromedriver(True)
        self.__gmail_login_url = 'https://accounts.google.com/v3/signin/identifier?checkedDomains=youtube&continue=https%3A%2F%2Fwww.google.com%2Fsearch%3Fq%3Dbest%2Bcartoons%26oq%3D%26gs_lcrp%3DEgZjaHJvbWUqCQgAEEUYOxjCAzIJCAAQRRg7GMID0gELNDc3MzQzMmowajeoAgGwAgE%26sourceid%3Dchrome%26ie%3DUTF-8&flowEntry=ServiceLogin&flowName=GlifWebSignIn&hl=be&ifkv=AYZoVhfBz2-77cFkDJweXVeWhNhq_QJ42BrbfL7b2oCq87uOAKfyCqw22D13yqz5HtlmoVNwNp-i0w&pstMsg=1&theme=glif&dsh=S-251460639%3A1695898568231402'
    
    def login(self):
        self.driver.get(url=self.__gmail_login_url)
        gmail_login_input = self.driver.find_element(by=By.ID, value='identifierId')
        gmail_login_input.send_keys(os.getenv('GMAIL_LOGIN'))
        
        gmail_login_next = self.driver.find_element(by=By.XPATH, value='//*[@id="identifierNext"]/div')
        gmail_login_next.click()
        
        time.sleep(5)
        
        retry = 5
        while retry >= 0:
            try:
                gmail_password_input = self.driver.find_element(by=By.XPATH,
                                                                value='//*[@id="password"]/div[1]/div/div[1]/input')
                gmail_password_input.send_keys(os.getenv('GMAIL_PASSWORD'))
                break
            
            except Exception as x:
                retry -= 1
                time.sleep(5)
        
        gmail_passw_next = self.driver.find_element(by=By.XPATH, value='//*[@id="passwordNext"]/div/button/span')
        gmail_passw_next.click()
        time.sleep(5)
    
    def go(self, list_of_prompts):
        result_list = list()
        
        for prompt in list_of_prompts:
            url = f"https://www.google.com/search?q={prompt}"
            self.driver.execute_script(f"window.open('{url}', '_blank');")
        
        # --------------------------------------------------------------------------------------------------
        for index, window_handle in enumerate(self.driver.window_handles[1:]):
            self.driver.switch_to.window(window_handle)
            time.sleep(2)
            try:
                converse_element = self.driver.find_element(By.XPATH,
                                                            '//*[@id="bqHHPb"]/div/div/div[1]/div[1]/a/div/span[2]')
                converse_element.click()
            
            except Exception as x:
                print(x)
        
        # --------------------------------------------------------------------------------------------------
        for window_handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(window_handle)
            
            retry = 5
            while retry >= 0:
                try:
                    show_more_elements = self.driver.find_elements(By.CLASS_NAME, 'clOx1e sjVJQd')
                    for element in show_more_elements:
                        try:
                            if element.text == 'Show more':
                                element.click()
                                break
                        except Exception as x:
                            print(x)
                    retry -= 1
                    time.sleep(1)
                except Exception as x:
                    retry -= 1
                    time.sleep(1)
        
        # --------------------------------------------------------------------------------------------------
        
        for window_handle in self.driver.window_handles[1:]:
            self.driver.switch_to.window(window_handle)
            time.sleep(2)
            retry = 5
            while retry >= 0:
                try:
                    response_div = self.driver.find_element(By.CLASS_NAME, 'oO0fve')
                    
                    soup = BeautifulSoup(response_div.get_attribute('innerHTML'), 'html.parser')
                    divs = soup.find_all(match_class)
                    divs = [div.get_text() for div in divs]
                    
                    prompt_on_page = uuid.uuid4()
                    
                    try:
                        prompt_on_page = self.driver.find_element(By.CLASS_NAME, 'E7FNse').text
                    except Exception as x:
                        print(x)
                    
                    final_response = ' '.join(divs)
                    if len(final_response) > 40:
                        result_list.append({str(prompt_on_page): final_response})
                    
                    break
                except Exception as x:
                    retry -= 1
                    time.sleep(2)
        
        successful_prompts = [key for d in result_list for key in d.keys()]
        unsuccessful_prompts = [p for p in list_of_prompts if p not in successful_prompts]
        
        print(result_list, successful_prompts, unsuccessful_prompts)
        
        return {
            'result': result_list,
            'successful_prompts': successful_prompts,
            'unsuccessful_prompts': unsuccessful_prompts
        }
        
        # --------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    handler = Handler()
    handler.login()
    handler.go([
        'best businessman in 2023',
        'best city in Belarus',
        'best car to buy',
        'best cruise to Alaska',
        'best cruise to France',
        'best cruise to Italy',
        'best car brand in 2023',
        'best barbershop for man',
        'best car brand',
        # 'best phone to buy',
        # 'best city in Belarus',
        # 'best car to buy',
        # 'best cruise to Alaska',
        # 'best cruise to France',
        # 'best cruise to Italy',
        # 'best car brand in 2023',
        # 'best barbershop for man',
        # 'best car brand',
        # 'best phone to buy'
    ])


