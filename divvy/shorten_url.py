# Larry Wells
# 02/20/2016

# Input long URL, return short URL

import bitly_api
from pyshorteners import Shortener

BITLY_ACCESS_TOKEN = '69574891f99870cd0a79c4864cbb1f01ca5e9313'

def shortenURL(url):
    shortener = Shortener('BitlyShortener', bitly_token=BITLY_ACCESS_TOKEN)
    return shortener.short(url)


