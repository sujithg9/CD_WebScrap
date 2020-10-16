#!/usr/bin/env python3
import os
import re
import pathlib
import requests
import numpy as np
import asyncio
import argparse
import logging
import logging.config
import tornado.ioloop
import functools
from bs4 import BeautifulSoup
from twilio.rest import Client
from tornado.platform.asyncio import AnyThreadEventLoopPolicy
from notify_run import Notify
from sample_cd_site import sample_cd_html as sample

log = logging.getLogger(__name__)

AVAILABILITY_CHECK_FREQUENCY = 60000
WEBSITE_URL = "https://www.crockettdoodles.com/available-puppies"
AVAILABLE_DIV_ID = "block-yui_3_17_2_1_1587610002145_"
NY_AVAIL_BLOCK_ID = f"{AVAILABLE_DIV_ID}14436"
PA_AVAIL_BLOCK_ID = f"{AVAILABLE_DIV_ID}36717"
PUPPIES_NOT_AVAILABLE_MSG = "No puppies available at this time."
SERVICE_ID = "cc24da037f744299be569c75eb14547a"
API_TOKEN = "796d78b8bad24108adddc460eb8cb725"
USER_AGENTS_FILE = os.path.join(pathlib.Path(__file__).parent.absolute(), "user_agents.txt")
PROXIES_FILE = os.path.join(pathlib.Path(__file__).parent.absolute(), "https_proxies.txt")
PREVIOUS_PUPPY_POSTS_COUNT = 0


def get_random_ua_proxy(ua_proxy_file):
    random_ua_proxy = ''
    try:
        with open(ua_proxy_file) as f:
            lines = f.readlines()
        if len(lines) :
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_ua_proxy = lines[int(idx)]
    except Exception as ex:
        log.exception(f'Exception in random_ua : {str(ex)}')

    finally:
        return random_ua_proxy.strip()


def cd_puppies_lookup(args):
    global PREVIOUS_PUPPY_POSTS_COUNT
    all_available_puppies = list()

    try:
        headers = {
            'user-agent': get_random_ua_proxy(USER_AGENTS_FILE),
        }
        proxies = {
            'http': get_random_ua_proxy(PROXIES_FILE)
        }

        if args.test:
            scrapper = BeautifulSoup(sample, 'html.parser')
        else:
            source_page = requests.get(WEBSITE_URL, headers=headers, proxies=proxies)
            scrapper = BeautifulSoup(source_page.content, 'html.parser')

        all_puppies_available = get_puppies_available_posts(scrapper)
        if all_puppies_available:
            for puppy_div in all_puppies_available:
                puppy_details = dict()
                name, desc, price, delivery = get_puppy_details(puppy_div)
                puppy_details["name"] = name
                puppy_details["description"] = desc
                puppy_details["price"] = price
                puppy_details["delivery_options"] = delivery
                all_available_puppies.append(puppy_details)
        else:
            log.info("No Puppy posts on CD ...")
            return
        all_cavapoo_cockapoo_breed_pups = [puppy for puppy in all_available_puppies if "Cavapoo".casefold() in
                                  puppy["description"].casefold() or "Cockapoo".casefold() in
                                  puppy["description"].casefold()]
        # all_cavapoos_cockapoo_near_me = [puppy for puppy in all_cavapoo_cockapoo_breed_pups if "NY area" or
        #                        "PA area" in puppy["description"]]
        if len(all_available_puppies) > 0:
            if PREVIOUS_PUPPY_POSTS_COUNT != len(all_available_puppies):
                PREVIOUS_PUPPY_POSTS_COUNT = len(all_available_puppies)
                log.info("Puppies posted on CD ...")
                send_push_notifications_android("New puppies posted on Crockett Doodle site ...")
                send_whatsapp_notification_twilio("New puppies posted on Crockett Doodle site ...")
                send_sms_notification_twilio("New puppies posted on Crockett Doodle site ...")
        else:
            PREVIOUS_PUPPY_POSTS_COUNT = 0
        if all_cavapoo_cockapoo_breed_pups:
            message = ""
            for pup in all_cavapoo_cockapoo_breed_pups:
                message += f"Puppy {pup['name']}, a cavapoo/cockapoo is available for {pup['price']}. " \
                    f"Delivery options : {pup['delivery_options']}"
                log.info("Cavapoo/Cockapoo Puppies available...\n" + message)
                send_push_notifications_android("Cavapoo/Cockapoo puppies available...\n" + message)
                send_whatsapp_notification_twilio(message)
                send_sms_notification_twilio(message)
    except Exception as ex:
        log.exception(f"Failed while Web Scraping CD Site ... : {str(ex)}")
    return


def get_puppies_available_posts(web_content_obj):
    all_puppies_posts = web_content_obj.find_all('div', attrs={"class":
                                                               re.compile("image-card\s+sqs-dynamic-text-container",
                                                                          re.I)})
    return all_puppies_posts


def get_puppy_details(puppy_div):
    puppy_name = puppy_div.find('div', attrs={"class": "image-title-wrapper"}).find(
        "div", attrs={"class": re.compile("image-title\s+sqs-dynamic-text", re.I)}).find("p").text.strip()
    puppy_details = puppy_div.find('div', attrs={"class": "image-subtitle-wrapper"}).find(
        "div", attrs={"class": re.compile("image-subtitle\s+sqs-dynamic-text", re.I)}).find_all("p")
    puppy_desc = puppy_details[0].text.strip()
    puppy_price_details = puppy_details[1].text.strip() if len(puppy_details) > 1 else "Price not Available !!!"
    puppy_delivery_options = puppy_details[2].text.strip() if len(puppy_details) > 1 else "Delivery Options " \
                                                                                          "not Available !!!"
    return puppy_name, puppy_desc, puppy_price_details, puppy_delivery_options


def send_whatsapp_notification_twilio(message):
    account_sid = 'AC234f380f9e4b2cec7eaea0de40e037f9'
    auth_token = 'c4f02f48d67e96f155bb416c3f426eff'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=message,
        from_='whatsapp:+14155238886',
        to='whatsapp:+16075426682'
    )
    log.info(f"Message SID : {message.sid}")


def send_sms_notification_twilio(message):
    account_sid = 'AC234f380f9e4b2cec7eaea0de40e037f9'
    auth_token = 'c4f02f48d67e96f155bb416c3f426eff'
    client = Client(account_sid, auth_token)
    message_sujith = client.messages \
        .create(body=message, messaging_service_sid='MG35a3259d692d2c6e0bef107f1fa1b889', to='+16075426682')
    message_sneha = client.messages \
        .create(body=message, messaging_service_sid='MG35a3259d692d2c6e0bef107f1fa1b889', to='+18574987498')
    log.info(f"Message SID : {message_sujith.sid}\nMessage SID : {message_sneha.sid}")


def send_push_notifications_android(message):
    notify = Notify()
    notify.send(message)


def configure_logger():
    logging_config = dict({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {'format': '%(asctime)s [%(levelname)s] <%(processName)s:%(process)s> '
                                 '[%(name)s(%(filename)s:%(lineno)d)] - %(message)s',
                       'datefmt': '%Y-%m-%d %H:%M:%S'
                       },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "simple",
                "stream": "ext://sys.stdout"
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "simple",
                "filename": "/home/sujithg9/Documents/CrookettDoodleWebScraping/CD_WebScrap/cd_puppies.log",
                "maxBytes": 100 * pow(1024, 3),
                "backupCount": 1,
                "encoding": "utf8"
            }
        },
        "loggers": {
            "default": {
                "level": "INFO",
                "handlers": ["console", "file_handler"],
                "propagate": False
            }
        },
        "root": {
            "level": "INFO",
            "handlers": ["console", "file_handler"]
        }
    })
    return logging_config


def initialize_cd_lookup_loop(args):
    logging.config.dictConfig(configure_logger())
    main_event_loop = tornado.ioloop.IOLoop()
    asyncio.set_event_loop_policy(AnyThreadEventLoopPolicy())
    main_event_loop.make_current()
    # Create and start cleaup callback
    lookup_cb = tornado.ioloop.PeriodicCallback(functools.partial(cd_puppies_lookup, args),
                                                AVAILABILITY_CHECK_FREQUENCY)
    lookup_cb.start()
    main_event_loop.start()


def main(argv=None):
    parser = argparse.ArgumentParser(prog="cdlookup-cli", description="CLI for looking up for"
                                                                      " Crockett Doodles puppy posts.")
    subparsers = parser.add_subparsers(help="commands")

    lookup = subparsers.add_parser("lookup", help="CD Lookup sub-commands for looking up for puppies")
    lookup_commands = lookup.add_subparsers(help="lookup operations")

    initialize = lookup_commands.add_parser("initialize", help="Initial puppies lookup loop.")
    initialize.add_argument("--test", action="store_true", help="Use pre-saved CD Site html file.")
    initialize.set_defaults(func=initialize_cd_lookup_loop)

    check = lookup_commands.add_parser("check", help="Check if there are any puppies right now (One-time).")
    check.add_argument("--test", action="store_true", help="Use pre-saved CD Site html file.")
    check.set_defaults(func=cd_puppies_lookup)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    main()
