#adapted from Aaron Jack tutorial on YouTube called "Building a simple Instagram bot with Python tutorial"
from selenium import webdriver
from time import sleep

class Instabot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(3)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
            .send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
            .send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]')\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
            .click()
        sleep(3)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(5)
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
            .click()
        following = self._get_names()
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        followers = self._get_names()
        not_following_back = [user for user in following if user not in followers]
        print("Number of people not following you back: ", len(not_following_back))
        print("Accounts: ")
        print(not_following_back)

    def _get_names(self):
        sleep(3)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[2]") 
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(3)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        # close button
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div[1]/div/div[2]/button")\
            .click()
        return names

    def like_stats(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        sleep(3)
        posts = self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text
        current_post = 0
        num_posts = int(posts)
        total_likes = 0
        most_likes = 0
        least_likes = 10000
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div[2]/article/div/div/div[1]/div[1]/a").click()
        sleep(2)
        while current_post != num_posts:
            current_post = current_post+1
            likes = self.driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/article/div[3]/section[2]/div/div[2]/button/span").text
            num_likes = int(likes) + 1 
            total_likes = total_likes + num_likes
            if num_likes > most_likes:
                most_likes  = num_likes
            if num_likes < least_likes:
                least_likes = num_likes
            if current_post == 1:
                sleep(2)
                self.driver.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a").click()
                sleep(1)
            if current_post < num_posts and current_post > 1:
                self.driver.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
                sleep(2)
        average_likes = total_likes/num_posts
        print("Total number of posts: ", num_posts)
        print("Average likes per post: ", average_likes)
        print("Most likes on a post: ", most_likes)
        print("Least likes on a post: ", least_likes)
        self.driver.find_element_by_xpath("/html/body/div[5]/div[3]/button")\
            .click()
            

    



igbot = Instabot('umich.grub', password)
igbot.get_unfollowers()
igbot.like_stats()

