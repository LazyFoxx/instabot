from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver as uc
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium_stealth import stealth
from config import PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USER

class InstaBot:
    def __init__(self):
        options = uc.ChromeOptions()
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
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
        with open(f"{PROXY_FOLDER}/manifest.json","w") as f:
            f.write(manifest_json)
        with open(f"{PROXY_FOLDER}/background.js","w") as f:
            f.write(background_js)   
            
            options.add_argument(f"--load-extension={PROXY_FOLDER}") 
        
        
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        stealth(driver=self.driver,
                    user_agent='Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    languages=["en-EN", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    run_on_insecure_origins=True,
                    )


    def main(self):
        self.driver.get('https://www.instagram.com/')
        sleep(500)
        self.driver.close()
        self.driver.quit()


bot = InstaBot()
if __name__ == '__main__':
    print('d')
    bot.main()

