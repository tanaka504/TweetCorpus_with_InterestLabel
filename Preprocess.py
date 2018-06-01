import re
import sys

repid = re.compile(r'@[a-zA-Z0-9_]+[\s|\n]')
url = re.compile(r'http(s)?://[\x20-\x7E]+')
emoji = re.compile(r'[^a-zA-Zａ-ｚＡ-Ｚぁ-んァ-ンｧ-ﾝ0-9一-龥？!！ー]')
kaomoji = re.compile \
    (r'(!<[^\w\s\])\s?(.?[（(].{0,8}[）)](.{0,4})?)')  # http://d.hatena.ne.jp/tochikuji/20111123/1322056418
haihun = re.compile(r'[-‐‑–—−ｰ]')
retweet = re.compile(r'RT[a-zA-Z0-9]+')
qt = re.compile(r'QT')

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

if __name__ == '__main__':
    sentence = sys.argv[1]
    print(sub_processor(sentence))