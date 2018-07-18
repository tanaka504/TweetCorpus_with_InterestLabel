# -*- coding:utf-8 -*-

import re, sys, json, config, time
from requests_oauthlib import OAuth1Session
from pprint import pprint


CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET

repid = re.compile(r'@[a-zA-Z0-9_]+[\s|\n]')
url = re.compile(r'http(s)?://[\x20-\x7E]+')
emoji = re.compile(r'[^a-zA-Zａ-ｚＡ-Ｚぁ-んァ-ンｧ-ﾝ0-9一-龥？!！ー]')
kaomoji = re.compile \
    (r'(!<[^\w\s\])\s?(.?[（(].{0,8}[）)](.{0,4})?)')  # http://d.hatena.ne.jp/tochikuji/20111123/1322056418
haihun = re.compile(r'[-‐‑–—−ｰ]')
retweet = re.compile(r'RT[a-zA-Z0-9]+')
qt = re.compile(r'QT')

oath = OAuth1Session(CK, CS, AT, ATS)

def sub_processor(sentence):
    sentence = repid.sub('', sentence)  #リプライのユーザID(@hogehoge)を削除
    sentence = url.sub('', sentence)    #URLを削除
    sentence = sentence.replace('\n', '')   #ツイート内の改行を削除
    sentence = kaomoji.sub('', sentence)    #顔文字を削除　うまく消えてくれずに'm(_ _)m'が'mm'になったりします
    sentence = haihun.sub('ー', sentence)    #ハイフンを統一
    sentence = emoji.sub('', sentence)    #絵文字を削除
    sentence = retweet.sub('', sentence)    #リツイートIDを削除
    sentence = qt.sub('', sentence) #引用リツイートIDを削除
    sentence = re.sub(r'o+', '', sentence)  #顔文字の残りのoが名詞判定されるのをなくすためですがiPhoneのoも消えてしまうので入れたのは失敗
    sentence = re.sub(r'^!+', '', sentence) #!から始まるツイートがあったので

    return sentence

def get_tweet(id):
    url = 'https://api.twitter.com/1.1/statuses/show.json'
    params = {'id': id}
    res = oath.get(url, params=params)
    while 1:
        if res.status_code == 200:
            timelines = json.loads(res.text)
            return timelines['text']
        elif res.status_code == 429:
            time.sleep(900)
        else:
            print('Failed: %d' % res.status_code)
            print(id)
            return 'ツイートの取得に失敗しました'

def main():
    with open('Annotated_Users_Interest.json', 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)

        for id, tweet in data.items():
            sentence = get_tweet(tweet['TweetID'])
            sentence = sub_processor(sentence)
            tweet['text'] = sentence
            data[id] = tweet

    with open('Annotated_Users_Interest_Preprocessed.json', 'w') as out_f:
        json.dump(data, out_f, ensure_ascii=False, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    main()