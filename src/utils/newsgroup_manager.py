import nntplib
from typing import *
import yaml
from datetime import datetime


class NewsGroupManager:

    NNTP: nntplib.NNTP = None
    address: str = None
    groups: Dict = None
    encoding: str = None
    delta_time: str = None

    def open_connection(self):
        try:
            self.NNTP = nntplib.NNTP(self.address)
        except Exception as e:
            print("Error when opening nntp connection")
            raise e

    def close_connection(self):
        try:
            self.NNTP.quit()
        except Exception as e:
            print("Error when closing nntp connection")
            raise e

    def get_config(self):
        with open('run/config/newsgroups.yml', 'r') as file:
            config = yaml.safe_load(file)
        self.address = config["address"]
        self.encoding = config["encoding"]
        self.delta_time = config["delta_time"]
