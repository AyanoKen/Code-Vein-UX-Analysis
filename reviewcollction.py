from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

def get_reviews():
    url = f"https://steamcommunity.com/app/678960/reviews/?browsefilter=toprated&snr=1_5_100010_"
    driver = webdriver.Chrome()  # You may need to specify the path to your chromedriver executable
    driver.get(url)

    reviews = []
    scroll_pause_time = 2  # Adjust as needed

    screen_height = driver.execute_script("return window.screen.height;")   # Get the screen height of the web
    i = 1

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == screen_height or i == 10:  # Break after 10 scrolls or if the page height doesn't change
            break
        screen_height = new_height
        i += 1

    review_summary = driver.find_elements(By.XPATH, "//div[@class='apphub_UserReviewCardContent']/div[@class='vote_header']/div[@class='reviewInfo']/div[@class='title']")
    review_hours = driver.find_elements(By.XPATH, "//div[@class='apphub_CardContentMain']/div[@class='apphub_UserReviewCardContent']/div[@class='vote_header']/div[@class='reviewInfo']/div[@class='hours']")
    review_text = driver.find_elements(By.XPATH, "//div[@class='apphub_UserReviewCardContent']/div[@class='apphub_CardTextContent']")

    summaries = []
    hours = []
    reviews = []

    for element in review_summary:
        summaries.append(element.text)

    for element in review_hours:
        hours.append(element.text)

    for element in review_text:
        child_elements = element.find_elements(By.XPATH, ".//*")

        all_text = ""

        for child in child_elements:
            print(child.text)
            all_text += child.text + "\n"
    
        reviews.append(all_text)

    print(reviews[0])
        
    print("Done Scrolling all the way down")

    driver.quit()

    data = zip(hours, summaries, reviews)

    with open('output.csv', 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Column1', 'Column2', 'Column3'])  # Header row
        for row in data:
            writer.writerow(row)

    print("Done writing to the file")







get_reviews()