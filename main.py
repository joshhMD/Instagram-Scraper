import getpass
from insta import InstagramBot
import pprint

INSTA_USERNAME = input("Enter Username: ")
INSTA_PASSWORD = getpass.getpass("Enter Password: ")

scrape_choice = input("press 1 to scrape hashtags, or 2 to scrape user accounts: ")
choice = int(scrape_choice)

# Scrapes hashtag and saves information
if choice==1:
    target  = input("Type in name hashtag name: ")
    instagram_bot = InstagramBot(INSTA_USERNAME, INSTA_PASSWORD)
    user_info = instagram_bot.get_hashtag(target)
    instagram_bot.save_file(user_info)

# Scrapes user account and saves information
if choice==2:
    target  = input("Type in account name: ")
    instagram_bot = InstagramBot(INSTA_USERNAME, INSTA_PASSWORD)
    user_info = instagram_bot.get_account_info(target)
    # user_info = instagram_bot.get_picture_info(target)
    instagram_bot.save_file(user_info)

    # ~~extra methods that can be used~~
    # instagram_bot.automate_like()
    # instagram_bot.automate_comment(content = "woow!")
    # instagram_bot.automate_follow()