import os
from dotenv import load_dotenv

load_dotenv()


class NbaHotNewsConfig(object):
    NBA_HOT_NEWS_FIREST_PAGE = os.environ["NBA_HOT_NEWS_FIREST_PAGE"]