import time
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class YoutubeCrawler:
    def __init__(self, chromedriver_path: str):
        self._chrome = chromedriver_path

    @staticmethod
    def get_comment(chromedriver_path: str, link: str, max_comment_pg_len: int)  -> list:
        data=[]
        with Chrome(executable_path=chromedriver_path) as driver:
            wait = WebDriverWait(driver, 15)
            driver.get(link)
            for item in range(max_comment_pg_len): 
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(15)
            for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
                data.append(comment.text)

        return data
    
    def get_comment(self, link: str, max_comment_pg_len: int) -> list:
        data=[]
        with Chrome(executable_path=self._chrome) as driver:
            wait = WebDriverWait(driver, 15)
            driver.get(link)
            for item in range(max_comment_pg_len): 
                wait.until(EC.visibility_of_element_located((By.TAG_NAME, "body"))).send_keys(Keys.END)
                time.sleep(15)
            for comment in wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#content"))):
                data.append(comment.text)

        return data

    def get_comment_df(self, links: list, max_comment_pg_len: int) -> pd.DataFrame:
        total_dict = dict()
        for i in range(len(links)):
            data = self.get_comment(links[i], max_comment_pg_len)
            if i==0:
                df = pd.DataFrame(data, columns=['comments'])
                df['link'] = links[0]
            else:
                temp_df = pd.DataFrame(data, columns=['comments'])
                temp_df['link'] = links[i]
                df = pd.concat([df, temp_df])
        df.dropna(how='any', inplace=True)
        
        return df        