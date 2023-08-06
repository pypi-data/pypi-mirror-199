import argparse

import requests


def get_url_info(url):
    res = requests.get(url)
    return res.text[:500]


parser = argparse.ArgumentParser(prog='Dummy Package')
parser.add_argument('-u', '--url', required=True)
args = parser.parse_args()

get_url_info(args.url)

if __name__ == '__main__':
    print(get_url_info("https://en.wikipedia.org/wiki/Main_Page"))
