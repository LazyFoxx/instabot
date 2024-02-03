import os
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from config import littlleaurora_reels





class InstaBot:
    def __init__(self, user):
        
        self.USER = user
        options = uc.ChromeOptions()
        
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
        time.sleep(8)  # Wait for 5 seconds (adjust as needed)
        




if __name__ == '__main__':
    bot = InstaBot(littlleaurora_reels)
    print('d')
    bot.login()
    time.sleep(30)
    
    self.driver.close()
    self.driver.quit()

