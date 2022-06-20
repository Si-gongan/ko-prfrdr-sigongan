#!/usr/bin/python3

from urllib import parse
from bs4 import BeautifulSoup
import argparse
import sys

import review_crawler


site = "http://www.yes24.com"


def reviewlist(info, csv, order=None, showurl=None):
    return goodsReviewList(info, order, csv) + awordReviewList(info, order, csv)


def main(itemid_list, csv, noheader, order=None, showurl=None):
    review_crawler.mainloop(itemid_list, bookinfo, reviewlist, csv, noheader, order, showurl)


def bookinfo(goodsid, showurl):
    url = site + "/Product/Goods/" + goodsid
    if showurl:
        print(url)

    html = review_crawler.readurl(url)
    soup = BeautifulSoup(html, 'html.parser')

    ebook = soup.select_one("div.gd_titArea > strong.icon_res")
    if ebook:
        title = '[' + ebook.text + '] ' + soup.select_one("h2.gd_name").text
    else:
        title = soup.select_one("h2.gd_name").text

    author = soup.select_one("span.gd_auth").text
    moreAuthArea = soup.select_one("span.moreAuthArea")
    if moreAuthArea:
        author = author.replace(moreAuthArea.text, '')

    return {
        "goodsid": goodsid,
        "title": title,
        "url": url,
        "author": author.strip(),
        "pubdate": soup.select_one("span.gd_date").text
    }


def goodsReviewList(info, order, csv):
    result = []

    sortorder = {
        "최근순": 1,
        "추천순": 2,
        "별점순": 3,
    }

    qrylist = [
        ("type", "ALL"),
        ("sort", sortorder[order]),
        ("PageNumber", 1)
    ]

    qrystr = parse.urlencode(qrylist)
    url = site + "/Product/communityModules/GoodsReviewList/" + info["goodsid"] + '?' + qrystr
    html = review_crawler.readurl(url)
    soup = BeautifulSoup(html, 'html.parser')

    for review in soup.select('div.reviewInfoGrp'):
        buy = review.select_one("span.buy")
        result.append({
            "reviewdate": review.select_one("em.txt_date").text,
            "reviewerid": review.select_one("em.txt_id > a").text,
            "buy": buy.text.strip() if buy else '',
            "rating": "내용 " + review.select_one("span.rating").text.strip() + "  편집/디자인 " + review.select_one("span.rating").text.strip(),
            "content": ' '.join(review.select_one("div.review_cont").text.split())
        })
        
    return result
   

def awordReviewList(info, order, csv):
    result = []

    sortorder = {
        "최근순": 1,
        "추천순": 2,
        "별점순": 3,
    }

    qrylist = [
        ("type", "ALL"),
        ("sort", sortorder[order]),
        ("PageNumber", 1)
    ]

    qrystr = parse.urlencode(qrylist)
    url = site + "/Product/communityModules/AwordReviewList/" + info["goodsid"] + '?' + qrystr
    html = review_crawler.readurl(url)
    soup = BeautifulSoup(html, 'html.parser')

    for review in soup.select('div.cmtInfoGrp'):
        buy = review.select_one("span.buy")
        result.append({
            "reviewdate": review.select_one("em.txt_date").text,
            "reviewerid": review.select_one("em.txt_id > a").text,
            "rating": review.select_one("span.rating").text.strip(),
            "buy": buy.text.strip() if buy else '',
            "content": review.select_one("div.cmt_cont").text.replace('\n', ' ').strip(),
        })
        
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", default="최근순", choices=["최근순", "추천순", "별점순"])
    parser.add_argument("--csv", action=argparse.BooleanOptionalAction)
    parser.add_argument("--noheader", action=argparse.BooleanOptionalAction)
    parser.add_argument("goodsid_list", nargs='?', type=str)
    args = parser.parse_args()
    main(args.goodsid_list, args.csv, args.noheader, args.order)


