#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This script defines functions
    to scrape craigstlist
    and to post to slack"""

# system library modules
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# external library modules
from craigslist import CraigslistHousing
from slacker import Slacker

# internal python modules
from ppcl_sql import *

# import the slack API key from the dot env file
slack = Slacker(os.environ['SLACK_TOKEN'])


# msg = 'Hi again!'

# def post_to_slack(msg):
#     slack.chat.post_message(
#         '#parkspot', 
#         text=msg, 
#         username="Pythonbot", 
#         icon_emoji=":robot_face:"
#         )

# post_to_slack(msg)


# scrape craigslist
def scrape_cl(site, area, max_posts):
    cl_h = CraigslistHousing(
        site=site, #'sfbay'
        area=area, #'sfc' 
        category='prk', 
        filters={#'posted_today': True, 
            'query': 'parking'}
        )

    posts = cl_h.get_results(
        sort_by='newest', 
        limit=max_posts
        )

    return posts


#def slack_message(post):
def post_to_slack(post, channel):
    msg = "Post ID# {0} | {1} | {2}".format(
        post['id'], 
        post['name'], 
        post['url']
        )

    slack.chat.post_message(
        channel, # '#parkspot', 
        text=msg, 
        username="PiedBot", 
        # icon_emoji=":robot_face:" 
        icon_emoji=":oncoming_automobile:"
        )

