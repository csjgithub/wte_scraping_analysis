import config
import numpy as np
import json
import re
import helper_functions

import mysql.connector
import db_config


print('connected to db')
for URL in config.subforums:
    forum_name = URL.split('/')[-1].replace('.html', '')

    href_list = helper_functions.get_all_thread_hrefs(URL, helper_functions.get_subforum_pages(URL))

    print('number of threads: ' + str(len(href_list)))

    list_to_upload = [(href_list[i], forum_name) for i in range(0, len(href_list))]
    helper_functions.upload_csv_to_mysql('thread_hrefs', forum_name, list_to_upload)



##TODO figure out how to save to the MySQL server

print('done')
