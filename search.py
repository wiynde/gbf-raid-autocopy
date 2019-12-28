# -*- coding: utf-8 -*-

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'site-packages'))

import json
import re
import subprocess
import time
from requests_oauthlib import OAuth1Session
from argparse import  ArgumentParser

with open("token.json", "r", encoding="utf-8") as tf:
    tokens = json.load(tf)

CK = tokens["consumer_key"]
CS = tokens["consumer_secret"]
AT = tokens["access_token"]
AS = tokens["access_token_secret"]

with open("search_ext.json", "r", encoding="utf-8") as sef:
    search_exts = json.load(sef)

FILTER_URL = 'https://stream.twitter.com/1.1/statuses/filter.json'

def parse_command():
    usage = 'python {0} target [--short] [--exclude] [--help]'\
            'Example: python {0} 120-ゴッドガード・ブローディア'\
            '         python {0} goburo -s -e'\
            .format(__file__)

    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('target', type=str,
                           help='default:level-name, -s:shortname')
    argparser.add_argument('-e', '--exclude', action='store_true',
                           help='exclude specific backup(救援) written in "excludes" of search_ext.json')
    argparser.add_argument('-s', '--shorts', action='store_true',
                           help='exclude specific backup(救援) written in "excludes" of search_ext.json')
    return argparser.parse_args()

def parse_boss(shorts, target):
    if shorts:
        if target in search_exts['shorts']:
            boss_level = search_exts['shorts'][target]['level']
            boss_name = search_exts['shorts'][target]['name']
        else:
            print('target="{}" is not registered in search_ext.json'.format(target))
            sys.exit()
    else:
        target_split = target.split('-')
        boss_level = target_split[0]
        boss_name = target_split[1]
    return (boss_level, boss_name)

def unsupported_os():
    print('This app only support Windows/Mac.')
    sys.exit()

# 文字列から参戦IDを抽出
def parse_raid_id(string):
    pattern = r'[0-9A-F]{8}\s:参戦ID'
    matchOB = re.findall(pattern, string)   # 一致する文字列を全て取得
    if matchOB:
        return matchOB[-1][0:8]     # 一致する文字列のうち最後のものをreturnすることによってダミーのIDを回避
    else:
        return None

# stringをクリップボードにコピー
def set_clipboard(string, os_name):
    if os_name == 'win32':
        process = subprocess.Popen('clip', stdin = subprocess.PIPE, shell=True)
    elif os_name == 'darwin':
        process = subprocess.Popen('pbcopy', stdin = subprocess.PIPE, shell=False)
    else:
        unsupported_os()
    process.communicate(string.encode("utf-8", "ignore")) # str型をbyte型に変換

def parse_tweet(tweet, os_name, exclude):
    if exclude:
        name = tweet.get('user').get('name')
        screen_name = tweet.get('user').get('screen_name')
        for exc in search_exts['excludes']:
            if 'name' in exc and name == exc['name']:
                return
            if 'screen_name' in exc and screen_name == exc['screen_name']:
                return
    raid_id = parse_raid_id(tweet.get('text'))
    if raid_id:
        set_clipboard(raid_id, os_name)

def print_tweet(tweet):
    tm = time.localtime()
    screen_name = tweet.get('user').get('screen_name')

    print('[%02d:%02d:%02d] @%s' % (tm.tm_hour, tm.tm_min, tm.tm_sec, screen_name))
    # TODO: 文字コード周りの処理をする
    print(tweet.get('text') + '\n', flush=True)

def main():
    os_name = sys.platform
    if os_name != 'win32' and os_name != 'darwin':
        unsupported_os()

    args = parse_command()
    boss_level, boss_name = parse_boss(args.shorts, args.target)

    try:
        oauth_session = OAuth1Session(CK, CS, AT, AS)
        params = {'track': 'Lv%s %s' % (boss_level, boss_name)}
        req = oauth_session.post(FILTER_URL, params=params, stream=True)
        
        for line in req.iter_lines():
            line_decode = line.decode('utf-8')
            if line_decode != '':
                tweet = json.loads(line_decode)
                # ゲームからツイートされたものを取得
                if tweet.get('source') == '<a href="http://granbluefantasy.jp/" rel="nofollow">グランブルー ファンタジー</a>':
                    parse_tweet(tweet, os_name, args.exclude)
                    print_tweet(tweet)

    except KeyboardInterrupt:
        print()
        sys.exit()

if __name__ == "__main__":
    main()
