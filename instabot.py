import os
import time
import pickle
import datetime
from random import randint as rn
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from db.database import DataBase as db





class InstaBot:
    def __init__(self, user, headless=False):
        
        self.USER = user
        options = uc.ChromeOptions()
        options.headless = headless
        options.page_load_strategy = 'eager'
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        if self.USER.proxy != None:
            
            PROXY_FOLDER = os.path.join('extension', 'proxy_folder')
            
            manifest_json = """
            {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy",
                "permissions": [
                    "proxy",
                    "tabs",
                    "unlimitedStorage",
                    "storage",
                    "<all_urls>",
                    "webRequest",
                    "webRequestBlocking"
                ],
                "background": {
                    "scripts": ["background.js"]
                },
                "minimum_chrome_version":"22.0.0"
            }
            """

            background_js = """
            var config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (self.USER.proxy['PROXY_HOST'],
                self.USER.proxy['PROXY_PORT'],
                self.USER.proxy['PROXY_USER'],
                self.USER.proxy['PROXY_PASS'])
            
            with open(f"{PROXY_FOLDER}/manifest.json","w") as f:
                f.write(manifest_json)
            with open(f"{PROXY_FOLDER}/background.js","w") as f:
                f.write(background_js)   
                
                options.add_argument(f"--load-extension={PROXY_FOLDER}") 
            
            
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        stealth(driver=self.driver,
                    user_agent=self.USER.user_agent,
                    languages=["en-EN", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    run_on_insecure_origins=True,
                    )
        
        self.driver.set_window_size(1920, 1080)


    def login(self):
        # Open Instagram
        self.driver.get("https://www.instagram.com/")
        # Wait for the login elements to become available
     
        wait = WebDriverWait(self.driver, 10)
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        # Find the login elements and enter email and password
        email_field.send_keys(self.USER.login)
        password_field.send_keys(self.USER.password)

        # Submit the login form
        password_field.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to adjust the delay based on your internet speed)
        time.sleep(12)  # Wait for 5 seconds (adjust as needed)
        time.sleep(50)
        self.driver.get(f"https://www.instagram.com/{self.USER.login}/")
        time.sleep(2)
        #cookies
        pickle.dump(self.driver.get_cookies(), open(f"cookie/{self.USER.login}_cookies", "wb"))
        
        print(f'{self.USER.login} - cookies saved. input completed')
        time.sleep(4)
    
    
    def load_accaunt(self):
        wait = WebDriverWait(self.driver, 10)
        try:
        
            self.driver.get("https://www.instagram.com/")
            try:
                for cookie in pickle.load(open(f"cookie/{self.USER.login}_cookies", 'rb')):
                    self.driver.add_cookie(cookie)
                print(f'{self.USER.login} - COOKIE LOADED')
            except Exception as ex:
                print(ex)
                self.login()
                return
            
            time.sleep(7)
            
            self.driver.get("https://www.instagram.com/")
            time.sleep(5)
            try:
                self.login()
            except Exception as ex:
                print(f'{self.USER.login} - log in with cookies')

                self.driver.get(f"https://www.instagram.com/{self.USER.login}/")

                time.sleep(3)
        except Exception as ex:
            print(ex)
            
    
    def user_links_liking_by_photo(self, link_photo):
            """get user photo and return user who like this photo"""
            self.driver.get(f"{link_photo}")
            time.sleep(8)
            # get links page and selekt liked_by link
            liinks_liked_by = self.driver.find_elements(By.TAG_NAME, 'a')
            link_liked_by = ''
            for item in liinks_liked_by:
                if 'liked_by' in item.get_attribute('href'):
                    link_liked_by = item.get_attribute('href')

            # get liked_by link and return user links list who liked this photo
            self.driver.get(f"{link_liked_by}")
            time.sleep(7)
            
            liinks = self.driver.find_elements(By.TAG_NAME, 'a')
            
            links_list = []
            for item in liinks:
                links_list.append(item.get_attribute('href'))
            # select links
            links_accounts_for_liking = []
            for i in range(6, len(links_list) - 1):
                if links_list[i] == links_list[i+1] and links_list[i] not in links_accounts_for_liking:
                    if 'liked_by' not in links_list[i] and f'{self.USER.login}' not in links_list[i]: 
                        links_accounts_for_liking.append(links_list[i])

            # print(*links_accounts_for_liking[:], sep='\n')
            print(f'\n{self.USER.login} - all find accounts for liking - {len(links_accounts_for_liking)}')
            return links_accounts_for_liking[3:]

    def liking_for_list(self, user_links):
            """liking users for users link list
            return all users, liked users list, empty users lists"""
            
            print(f'\n{self.USER.login} - start liking!')
            
            
            all_users = len(user_links)
            like_users = []
            empty_users = []
            
            for user in user_links:
                self.driver.get(f'{user}')
                time.sleep(11)
                
                liinks = self.driver.find_elements(By.TAG_NAME, 'a')        
                for item in liinks:
                    if '/p/' in item.get_attribute('href'):  
                        db.add_users('like_users.txt', value=user, name=False)
                        self.driver.get(item.get_attribute('href'))
                        time.sleep(7)
                        try:
                            like = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div')
                            like.click()
                        except Exception as ex:
                            print(ex)
                            time.sleep(20)
                            like = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div')
                            like.click()
                        print(f"{self.USER.login} - {user.split('com/')[1][:-1]} - Like!", end=' ')
                        like_users.append(user)
                        t = rn(12, 40)
                        print(f'timeout {t} seconds')
                        time.sleep(t)
                        break
                else:
                    print(f"{self.USER.login} - {user.split('com/')[1][:-1]}  - is empty account")
                    empty_users.append(user)
                    db.add_users('like_users.txt', value=user, name=False)
                
            
            return all_users, like_users, empty_users
        
    def like_by_photo(self, link_photo):
        """liked users who like this photo"""
        user_links = self.user_links_liking_by_photo(link_photo)
        all_users, like_users, empty_users = self.liking_for_list(user_links)
        
        print(f"{self.USER.login} - \nall users - {all_users} \n all likes - {like_users} \n empty users - {empty_users} \n" )
        time.sleep(3)

        print(f'\n{self.USER.login} - liking succsessful')


    def like_post(self, link):

        self.driver.get(link)
        time.sleep(7)

        like_condition = self.driver.find_element(By.CLASS_NAME, 'x1lliihq x1n2onr6 xxk16z8')
        print(like_condition.text)

        'x1lliihq x1n2onr6 xxk16z8'
        like = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div')
        like.click()
        
        # like_condition = self.driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div/span/svg/title')
        # print(like_condition.text)
        
        time.sleep(450)
  
    
    def close(self):

        pickle.dump(self.driver.get_cookies(), open(f"{self.USER.login}_cookies", "wb"))
        print(f'{self.USER.login} - cookie saved')
        time.sleep(2)
        self.driver.close()
        self.driver.quit()
    
    def extra_close(self):
        self.driver.close()
        self.driver.quit()
