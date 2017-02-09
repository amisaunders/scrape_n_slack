#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script scrapes cl
    and posts to slack"""

# import internal library function
from ppcl_fun import *
from ppcl_constants import AREAS, MAX_POSTS, CHANNEL


# execute the code to scrape cl and post to slack

# AREAS=[('sfbay', 'sfc'), ('sfbay', 'pen'), ('sfbay', 'eby'), ('losangeles', 'lgb')]

# posts = areas_iter(AREAS)


slack.chat.post_message(
    CHANNEL, # '#parkspot', 
    text="Hi, I'm checking to see if there are any new spots available for rent today, and will let you know of any new parking spots.  Standby!", 
    username="PiedBot", 
    # icon_emoji=":robot_face:" 
    icon_emoji=":oncoming_automobile:"
    )


for area in AREAS:
    # get all areas for scraping on cl
    site = area[0]
    area = area[1]

    # iterate over the area
    posts = scrape_cl(site, area, MAX_POSTS)

    for post in posts:
        # print post
        np = filter_new_post(post)
        if np != None:
            post_to_slack(np, CHANNEL)
            # comment out after it's working
            print np
        # comment out after it's working
        else:
            print "Old"
            # continue




