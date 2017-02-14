#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# A simple web scraper to grab additional information
# missing from the Met Mueseum's Open Access Initative
# dataset.
#
# Copyright (c) 2017 Avital Pekker.
# Author: Avital Pekker (hello@avital.ca)
#
# For license information, see LICENSE.TXT
#

import pymysql.cursors
import requests
from bs4 import BeautifulSoup
import time
import sys

PY3 = (sys.version_info > (3, 0))

DB_HOST = "localhost"
DB_NAME = "themet"
DB_USER = "PUT_USERNAME_HERE"
DB_PASS = "PUT_PASSWORD_HERE"
DB_TABLE = "met_objects"

# Only public domain paintings that have an artist name
DB_FIELDS              = "obj_id, obj_num, title, artist_display_name, obj_begin_date, link_resource, full_img, collection_details"
DB_FILTER              = "is_public_domain = 1 AND LENGTH(artist_display_name) > 0 AND classification='Paintings'"
DB_MAX_RESULTS         = 8500
DB_SKIP_POPULATED_IMG  = True

connection = pymysql.connect(host=DB_HOST,
                             user=DB_USER,
                             password=DB_PASS,
                             db=DB_NAME,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
                             
try:
    with connection.cursor() as cursor:
        sql = "SELECT {0} FROM {1} WHERE {2} LIMIT {3}".format(DB_FIELDS, DB_TABLE, DB_FILTER, DB_MAX_RESULTS)
        cursor.execute(sql)
        db_matches = cursor.fetchall()

        insert_sql = "UPDATE {0} SET full_img = %s, collection_details = %s WHERE obj_id = %s".format(DB_TABLE)

        for row in db_matches:
            if row['full_img'] is not None and DB_SKIP_POPULATED_IMG:
                if PY3:
                    title = row['title']
                else:
                    title = row['title'].encode('utf-8')

                print('Object "{0}" already in DB, skipping...'.format(title))
                continue
            
            response = requests.get(row['link_resource'])
            soup = BeautifulSoup(response.text, "html.parser")
            
            for link in soup.find_all('a', href=True):
                if PY3:
                    attrib_avail = getattr(link.text, 'attr', str) is str
                else:
                    attrib_avail = getattr(link.text, 'attr', unicode) is unicode
                    
                if attrib_avail and link.text.strip() == "Download":
                        # Example link: 
                        # href="{{selectedOrDefaultDownload('http://images.metmuseum.org/CRDImages/ad/original/25592.jpg')}}"
                        
                        # Strip the text around the link
                        clean_link = link['href'][29:-4]
                        
                        # Some items have additional collection info
                        details_matches = soup.find_all('div', {'class': 'collection-details__label'})
                        clean_details = None
                        
                        if details_matches is not None:
                            clean_details = details_matches[0].text.strip()
                        
                        details_found = (clean_details is not None and len(clean_details) > 0)

                        if PY3:
                            title = row['title']
                        else:
                            title = row['title'].encode('utf-8')
                            
                        print('Object "{0}", original full image: {1}; details found: {2}' \
                            .format(title, clean_link, details_found))
                                
                        cursor.execute(insert_sql, (clean_link, clean_details, row['obj_id']))
            
            # Slow down - please don't bombard the site with requests.
            # Ideally, copy my database.
            time.sleep(3)
            
        # Save to DB - PyMySQL disables autocommit by default.
        connection.commit()
finally:
    connection.close()
