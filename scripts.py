from instabot import InstaBot
from config import littlleaurora_reels
from random import randint as rn
import time
import datetime
from db.database import DataBase as db


def add_users_from_txt(account, shadow=True):
    users_now = db.get_users('users_for_likes.txt', value=99999)
    print(f'{account.login} all users before add - {len(users_now)}')
    
    list_users = db.get_users('users_photos.txt', value=40, remove=True)
    if len(list_users) > 0:
        bot = InstaBot(user=account, headless=shadow)
        bot.load_accaunt()
        
        users_for_likes = []
        for link in list_users:
            if len(link) < 10:
                continue
                print(f'--{link}--')
            
            users_for_likes = bot.user_links_liking_by_photo(link)
            db.add_users('users_for_likes.txt', users_for_likes, name=False)
        
        bot.close()
    
    users_now = db.get_users('users_for_likes.txt', value=99999)
    print(f'{account.login} all users after add - {len(users_now)}')


def liking_for_list_users(account, count=300, shadow=True):
    
    users_now = db.get_users('users_for_likes.txt', value=99999)
    print(f'{account.login} all users for likes in DB - {len(users_now)}')

    def chunked(lst, n):
        res = []
        for i in range(0, len(lst), n):
            res.append(lst[i:i + n])
        return res


 
    
    like_users_check = db.get_users('like_users.txt', 9999999, remove=False)
    users_for_likes = db.get_users('users_for_likes.txt', value=count, remove=True)
    print(f'{account.login} get {len(users_for_likes)} users from {count}')
    users_for_likes = db.check_list(users_for_likes, like_users_check)
    print(f'{account.login} start massliking for {len(users_for_likes)} users\n')
    time.sleep(15)
    users_for_likes = chunked(users_for_likes, 30)

    
    t_start = datetime.datetime.now()
    all_users, like_users, empty_users, ERRORS = 0, [], [], 0
    for user in users_for_likes:
        print(f'----------\n{datetime.datetime.now()}\n----------')
        try:
            bot = InstaBot(user=account, headless=shadow)
            bot.load_accaunt()
            chank_users, chank_like_users, chank_empty_users = bot.liking_for_list(user)
            bot.close()
            
            if user!= users_for_likes[-1]:
                t = rn(400, 900)
                print(f'{account.login}\n -------------\ntimeout {t} seconds\n-------------')
                time.sleep(t)
        except Exception as ex:
            print('ERROR. trying continue')
            print(f"{account.login} - all users - {all_users} all likes - {len(like_users)} empty users - {len(empty_users)} \n" )
            print(ex)
            bot.extra_close()
            ERRORS += 1
            time.sleep(300)
            continue
        
        all_users += chank_users
        like_users += chank_like_users
        empty_users += chank_empty_users
        
    
    t_end = datetime.datetime.now()
    print(f'{account.login} end massliking for {len(users_for_likes)} users\n')
    print(f"{account.login} {t_start} \n{account.login} {t_end}")
    print(f"{account.login} - all users - {all_users} all likes - {len(like_users)} empty users - {len(empty_users)} \n" )
    
    users_now = db.get_users('users_for_likes.txt', value=99999)
    print(f'{account.login} all users for likes in DB - {len(users_now)}')
    
    
    
    
def proxy(account):
        bot = InstaBot(user=account, headless=False)
        bot.login()
        time.sleep(400)
    
