from instabot import InstaBot
import scripts
from config import littlleaurora_reels, lionsin__, littlleaurora
import time

def main():
    # Scripts

    # scripts.add_users_from_txt(account=lionsin__, shadow=False)
    # for i in range(4):
    #     for i in range(6):
    #         scripts.liking_for_list_users(account=littlleaurora, count=100, shadow=False)
    #         time.sleep(700)
    #     time.sleep(10000)


    
    scripts.proxy(littlleaurora)
if __name__ == '__main__':
    main()

