from urllib.parse import urlparse
import os
from selenium import webdriver
import time
import requests

# InstagramBot: contains functions the bot can perform
class InstagramBot:

    def __init__(self, INSTA_USERNAME, INSTA_PASSWORD):
        self.username = INSTA_USERNAME
        self.password = INSTA_PASSWORD
        self.browser = webdriver.Firefox()

        url = "https://www.instagram.com"
        self.browser.get(url)

        time.sleep(2)
        username_element = self.browser.find_element_by_name("username")
        username_element.send_keys(self.username)

        time.sleep(2)
        password_element = self.browser.find_element_by_name("password")
        password_element.send_keys(self.password)

        time.sleep(2)
        submit_button_element = self.browser.find_element_by_css_selector("button[type='submit']")
        submit_button_element.click()

        body_element = self.browser.find_element_by_css_selector("body")
        html_text = body_element.get_attribute("innerHTML")


    # follows selected account
    def automate_follow(self):
        my_follow_button = "//button[contains(text(), 'Follow')][not(contains(text(), 'Following'))][not(contains(text(), 'Followers'))]"
        follow_button_elements = self.browser.find_elements_by_xpath(my_follow_button)

        for btn in follow_button_elements:
            time.sleep(2)
            try:
                btn.click()
            except:
                pass


    # grabs information for selected picture for target account
    # target: selected account user wants to scrape
    def get_picture_info(self, target):
        time.sleep(2)
        complete_url = f"https://www.instagram.com/{target}/"
        self.browser.get(complete_url)

        post_url_pattern = "https://www.instagram.com/p/<post-slug-id"
        post_xpath_str = "//a[contains(@href, '/p/')]"
        post_links = self.browser.find_elements_by_xpath(post_xpath_str)
        post_link_element = None

        if len(post_links) > 0:
            post_link_element = post_links[0]

        if post_link_element != None:
            post_href = post_link_element.get_attribute("href")
            self.browser.get(post_href)


        images_elements = self.browser.find_elements_by_xpath("//img")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, f"{target}-pictures")
        os.makedirs(self.data_dir, exist_ok=True)

        return images_elements


    # grabs information for selected account
    # target: selected account user wants to scrape
    def get_account_info(self, target):
        time.sleep(2)
        complete_url = f"https://www.instagram.com/{target}/"
        self.browser.get(complete_url)

        post_url_pattern = "https://www.instagram.com/p/<post-slug-id"
        post_xpath_str = "//a[contains(@href, '/p/')]"
        post_links = self.browser.find_elements_by_xpath(post_xpath_str)
        post_link_element = None

        images_elements = self.browser.find_elements_by_xpath("//img")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, f"{target}-account-pictures")
        os.makedirs(self.data_dir, exist_ok=True)

        return images_elements


    # grabs information for selected account
    # target: selected account user wants to scrape
    def get_hashtag(self, target):
        time.sleep(2)
        complete_url = f"https://www.instagram.com/explore/tags/{target}"
        self.browser.get(complete_url)

        post_url_pattern = "https://www.instagram.com/p/<post-slug-id"
        post_xpath_str = "//a[contains(@href, '/p/')]"
        post_links = self.browser.find_elements_by_xpath(post_xpath_str)
        post_link_element = None


        images_elements = self.browser.find_elements_by_xpath("//img")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(base_dir, f"hashtag-{target}")
        os.makedirs(self.data_dir, exist_ok=True)

        return images_elements


    # finds images and downloads them
    # elements: photos stored in list
    def save_file(self, elements):
        for el in elements:
            url = el.get_attribute('src')
            base_url = urlparse(url).path
            filename = os.path.basename(base_url)
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                continue

            print(filepath)

            # downloads content
            with requests.get(url, stream=True) as r:
                try:
                    r.raise_for_status()
                except:
                    continue
                with open(filepath, 'wb') as f:
                    for chunk in r.iter_content():
                        if chunk:
                            f.write(chunk)


    # comments on post
    # content: words to be used in the comment
    def automate_comment(self, content="That is cool!"):
        time.sleep(3)
        comment_xpath_str = "//textarea[contains(@placeholder, 'Add a comment')]"
        comment_element = self.browser.find_element_by_xpath(comment_xpath_str)
        comment_element.click()
        time.sleep(2)
        comment_element = self.browser.find_element_by_xpath(comment_xpath_str)
        comment_element.click()
        time.sleep(2)
        comment_element.send_keys(content)
        submit_buttons_xpath = "button[type='submit']"
        submit_button = self.browser.find_elements_by_css_selector(submit_buttons_xpath)

        for button in submit_button:
            try:
                time.sleep(4)
                button.click()
            except:
                pass


    # auto likes selected post
    def automate_like(self):
        #Iterates through and finds the max height for like button
        heart_xpath = "//*[contains(@aria-label, 'Like')]"
        heart_elements = self.browser.find_elements_by_xpath(heart_xpath)
        max_heart_height = -1
        for heart_element in heart_elements:
            h = heart_element.get_attribute("height")
            current_height = int(h)
            
            if current_height > max_heart_height:
                max_heart_height = current_height

        #Iterates through with condition, if met it likes the post
        heart_elements = self.browser.find_elements_by_xpath(heart_xpath)

        for heart_element in heart_elements:
            h = heart_element.get_attribute("height")
            if h == max_heart_height or h == f"{max_heart_height}":
                parent_like_button = heart_element.find_element_by_xpath('..')
                time.sleep(2)
                try:
                    parent_like_button.click()
                except:
                    pass