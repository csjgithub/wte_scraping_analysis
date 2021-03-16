import requests as r
from bs4 import BeautifulSoup
import lxml #Using lxml+cchardet significantly speeds up bs4 parsing of HTML response
import cchardet
import csv
import os
import mysql
import db_config

def get_subforum_pages(URL):
    page = r.get(URL)
    soup = BeautifulSoup(page.content, 'lxml')

    # Get total number of pages with threads for subforum
    page_indicators = soup.find_all('a', class_='page-link')
    num_pages = 0
    for page_indicator in page_indicators:
        if len(page_indicator.get_text()) > 0:
            num_pages = max(int(page_indicator.get_text()), num_pages)

    return num_pages


def get_all_thread_hrefs(URL, num_pages):
    base_url = 'https://community.whattoexpect.com/'
    href_list = []
    for pagenum in range(1,num_pages+1):
       # Set and get the next subforum page
       loop_url = URL + '?page=' + str(pagenum)
       page = r.get(URL)
       soup = BeautifulSoup(page.content, 'lxml')

       # Find links to all threads on page
       topics = soup.find_all('a', class_='linkDiscussion')
       for thread in topics:
           full_url = base_url + thread['href']
           href_list.append(full_url)
       break ## REMOVE LATER

    return href_list


def upload_csv_to_mysql(table_name, forum_name, list_to_upload):
    filename = 'href_' + forum_name +'.csv'
    with open(filename, 'w', newline='') as f:

        write = csv.writer(f)
        write.writerows(list_to_upload)
    conn = mysql.connector.connect(user = db_config.mysql['user'], password = db_config.mysql['password'],
                               host = db_config.mysql['host'], database = db_config.mysql['database'])
    cursor = conn.cursor()


    upload_statement = """LOAD DATA INFILE '%s'
                        INTO TABLE thread_hrefs
                        FIELDS TERMINATED BY ','
                        LINES TERMINATED BY '\\n';""" % (os.getcwd().replace('\\','\\\\')+ '\\\\' + filename)

    cursor.execute(upload_statement)
    conn.commit()

    cursor.close()
    conn.close()

