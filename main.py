import time
import argparse

import re
import demoji
import os

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver as wd

def go(exe_path, youtube_link, filename):
    ## CHECK START TIME
    start = time.time()

    driver = wd.Chrome(executable_path=exe_path)

    # INPUT YOUTUBE URL
    url = youtube_link
    driver.get(url)

    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2.5)       # INTERVAL MUST BE OVER 1 (CONSIDERING LOADING TIME)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height

    html_source = driver.page_source
    driver.close()

    # HTML TAG SCRAP
    soup = BeautifulSoup(html_source, "lxml")

    youtube_user_IDs = soup.select("div#header-author > a > span")
    youtube_comments = soup.select("yt-formatted-string#content-text")

    str_youtube_userIDs = []   # USER ID LIST
    str_youtube_comments = []  # USER COMMENT LIST

    # REPLACE DATA/PREPROCESS FOR EMOJI
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                           "]+", flags=re.UNICODE)
    han = re.compile(r'[ㄱ-ㅎㅏ-ㅣ^!?~,".\n\r\t#\ufeff\u200d]')

    for i in range(len(youtube_user_IDs)):
        str_tmp = str(youtube_user_IDs[i].text)
        str_tmp = str_tmp.replace('\n', '')
        str_tmp = str_tmp.replace('\t', '')
        str_tmp = str_tmp.replace('   ','')
        str_youtube_userIDs.append(str_tmp)

        str_tmp = str(youtube_comments[i].text)
        str_tmp = re.sub(emoji_pattern, "", str_tmp)
        str_tmp = re.sub(han, "", str_tmp)
        str_tmp = demoji.replace(str_tmp, "")
        str_youtube_comments.append(str_tmp)

    ## MODIFY VIEW FORMAT
    pd_data = {"ID":str_youtube_userIDs, "comment":str_youtube_comments}
    youtube_pd = pd.DataFrame(pd_data)

    ## OUTPUT FILE PATH
    OUTPUT_PATH = "outputs/"
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    SAVE_PATH = OUTPUT_PATH+filename

    ## WRITE AS TSV
    youtube_pd.to_csv(SAVE_PATH, index=False, header=None, sep="\t")
    print("Running Time : ", time.time() - start)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='YouTube comments')
    parser.add_argument('--exe_path', default="chromedriver.exe", type=str)
    parser.add_argument('--link', default="", type=str)
    parser.add_argument('--filename', default="data.tsv", type=str)
    args = parser.parse_args()

    go(exe_path=args.exe_path, youtube_link=args.link, filename=args.filename)
