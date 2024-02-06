from instabot import InstaBot
import scripts
from config import littlleaurora_reels, lionsin__, littlleaurora
import time

def main():
    # Scripts

    scripts.add_users_from_txt(account=lionsin__)
    scripts.liking_for_list_users(account=littlleaurora, count=150)
    time.sleep(1342)
    scripts.liking_for_list_users(account=littlleaurora, count=150)
    time.sleep(1111)
    scripts.liking_for_list_users(account=littlleaurora, count=150)
    time.sleep(976)
    scripts.liking_for_list_users(account=littlleaurora, count=150)
    time.sleep(996)
    scripts.liking_for_list_users(account=littlleaurora, count=150)
    time.sleep(1033)
    scripts.liking_for_list_users(account=littlleaurora, count=150)

if __name__ == '__main__':
    main()


