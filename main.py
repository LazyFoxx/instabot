from instabot import InstaBot
import scripts
from config import littlleaurora_reels, lionsin__, littlleaurora

def main():
    # Scripts

    scripts.add_users_from_txt(account=lionsin__)
    scripts.liking_for_list_users(littlleaurora, count=1000, shadow=False)
    

if __name__ == '__main__':
    main()


