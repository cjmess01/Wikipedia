import Link

import LinkCollector
from collections import deque
import requests
from bs4 import BeautifulSoup as bs
import xlwt


    

mine = LinkCollector.LinkCollector("test1")

mine.findPath("https://en.wikipedia.org/wiki/Baptists","https://en.wikipedia.org/wiki/Mennonites")