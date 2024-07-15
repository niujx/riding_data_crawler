import json
import requests
import requests.cookies
import argparse


def cralwer_riding_data(cookie_jar, headers, user_id, year: int, month: int):
    res = requests.get(
        url='https://www.imxingzhe.com/api/v4/user_month_info/?user_id=%s&year=%s&month=%s' % (user_id, year, month), cookies=cookie_jar, headers=headers)
    riding_data = json.loads(res.text)
    for riding_d in riding_data['data']['wo_info']:
        title = riding_d['title']
        download_url = 'https://www.imxingzhe.com/xing/%s/gpx/' % riding_d['id']
        data_res = requests.get(
            url=download_url, cookies=cookie_jar, headers=headers)
        file = open(title+".gpx", 'w')
        file.write(data_res.text)
        file.close()
        print('downloading %s file done' % title)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="输入抓取的参数")
    parser.add_argument('--cookie', '-c', type=str,
                        required=True, help="输入cookies json的路径")
    parser.add_argument('--start', '-s', type=int,
                        required=True, help="输入抓取的开始年份")
    parser.add_argument('--end', '-e', type=int,
                        required=True, help="输入抓取的结束年份")

    args = parser.parse_args()
    print('cookie path is %s' % args.cookie)
#   f = open('xingzhe_cookies.json')
    f = open(args.cookie)
    data = json.load(f)
    cookie_jar = requests.cookies.RequestsCookieJar()
    for d in data:
        del d['sameSite']
        del d['session']
        del d['httpOnly']
        del d['firstPartyDomain']
        del d['partitionKey']
        del d['hostOnly']
        del d['storeId']
        if "expirationDate" in d:
            del d['expirationDate']
        cookie_jar.set(**d)
    headers = {
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.imxingzhe.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0'
    }

    res = requests.get(url='https://www.imxingzhe.com/api/v4/account/get_user_info/',
                       cookies=cookie_jar, headers=headers)
    user_info_data = json.loads(res.text)
    if 'userid' not in user_info_data:
        print('登录失败检查传入的cookie是否正确或者过期')
    user_id = user_info_data['userid']

    for year in range(args.start, args.end+1):
        for month in range(1, 13):
            cralwer_riding_data(cookie_jar=cookie_jar, headers=headers, user_id=user_id, year=year, month=month)
