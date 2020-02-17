import nntplib
from typing import *
import yaml
from datetime import datetime


class NewsGroupManager:

    NNTP:nntplib.NNTP = None
    address: str = None
    groups: Dict = None

    def init_connection(self):
        try:
            self.NNTP = nntplib.NNTP(self.address)
        except:
            print("Error when opening nntp connection")

    def get_config(self):
        with open('run/config/newsgroups.yml', 'r') as file:
            config = yaml.safe_load(file)
        self.address =  config["address"]
        self.groups = config["groups"]
