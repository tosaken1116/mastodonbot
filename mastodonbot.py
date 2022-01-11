from mastodon import Mastodon, StreamListener
from datetime import datetime
from dotenv import load_dotenv
import time
import bs4
import threading
import os
import random
import numpy

load_dotenv()
acsess_key = os.environ.get('ACCESS_TOKEN')
def Login():
    mastodon = Mastodon(
                access_token = acsess_key,
                api_base_url = "https://mastodon.compositecomputer.club"
                )
    return mastodon

mastodon = Login()
bot_sourth = mastodon.account_verify_credentials()
bot_timeline = mastodon.account_statuses(bot_sourth['id'])

class Stream(StreamListener):
    def __init__(self):
        super(Stream, self)
    def on_notification(self,notif):
        print("on_notification")
        if notif['type'] == 'mention': 
            content = notif['status']['content'] 
            id = notif['status']['account']['username']
            st = notif['status']
            if '御籤' in content or 'みくじ' in content:
                mikuji(content, st, id)
            else:
                main2(content, st, id)
          
            
def rewrite(text: str, doRet: bool = True):
    if doRet:
        text = text.replace('</p><p>', '\n\n')
        text = text.replace('<br />','\n')
    else:
        text = text.replace('</p><p>', ' ')
        text = text.replace('<br />',' ')
    text = bs4.BeautifulSoup(text, 'html.parser').get_text()
    text = text.replace('&apos;', '\'')
    text = text.replace('&amp;', '&')
    text = text.replace('&quot;', '\"')
    return text

def main():
    max_id = None
    while(True):
        toots = mastodon.timeline_hashtag('blender便利機能', max_id=max_id)
        if len(toots) == 0:
            break
        for toot in toots:
            if not toot['reblogged']:
                mastodon.status_reblog(toot['id'])
            else:
                return
            time.sleep(10)
        max_id = toots[-1]['id']
        
        
def main2(content, st, id):
    candidate = []
    candidateurl = []
    replycontent = []
    replyconrenturl = []
    i = 0
    t = 0
    max_id = None
    if st['in_reply_to_account_id'] !=bot_sourth['id'] and st['in_reply_to_id'] == None:
        x = rewrite(content)
        keys = x.replace('@blender ','').split()
        keynumber = len(keys) #検索ワードの数の取得
        while(True):
            toots = mastodon.account_statuses(bot_sourth['id'], max_id=max_id)
            if len(toots) == 0:
                break
            for toot in toots:
                rewritecontent = rewrite(toot['content']).replace('#blender便利機能','')
                if toot['reblog']:
                    candidate = candidate + [rewritecontent]
                    candidateurl = candidateurl + [toot['reblog']['url']]
                
            counttoot = len(candidate)

            for word in keys:
                maxloop = counttoot
                counttoot = 0
                t = 0
                replycontent = []
                replyconrenturl = []
                for t in range(maxloop):
                    if word in candidate[t]:
                        replycontent.append(candidate[t])
                        replyconrenturl.append(candidateurl[t])
                        counttoot += 1
                    else:
                        t -= 1
                candidate = replycontent[:]
                candidateurl = replyconrenturl[:]
            
            for url in replyconrenturl:#返信
                text = url
                mastodon.status_reply(st, text)
                time.sleep(2)
            max_id = toots[-1]['id']

def mikuji(content, st, id):
    print('test')
    k = 1
    t = 1
    if 'みくじ' in content or '御籤' in content:
        print('text')
        p = [0.05,0.1,0.2,0.3,0.2,0.1,0.05]
        word = ['大吉','中吉','小吉','吉','末吉','凶','大凶']
        achivement = ['秀','優','良','可','不可']
        text = random.choices(word, k = 1, weights = p)[0]
        if text == '大吉':
            p = [0.5,0.3,0.1,0.05,0.05]
        if text == '中吉':
            p = [0.4,0.4,0.1,0.05,0.05]
        if text == '小吉':
            p = [0.3,0.4,0.2,0.05,0.05]
        if text == '吉':
            p = [0.2,0.3,0.4,0.05,0.05]
        if text == '末吉':
            p = [0.1,0.3,0.5,0.05,0.05]
        if text == '凶':
            p = [0.1,0.1,0.5,0.2,0.1]
        if text == '大凶':
            p = [0.05,0.05,0.4,0.2,0.3]
        heartluck = random.choices(achivement, k = 1,weights = p)
        studyluck = random.choices(achivement,k = 1,weights = p)
        hopeluck = random.choices(achivement,k = 1,weights = p)
        friendluck = random.choices(achivement,k = 1,weights = p)
        result = text + '\n勉学:' + studyluck[0] + '\n恋愛:' + heartluck[0] + '\n探し物:' + hopeluck[0] + '\n友情:' + friendluck[0] + '\nこの御籤はフィクションです。\n実在の人物や団体とは関係ありません。\n仮に損害を与えられたとしても当方は一切の責任を負いません'
        mastodon.status_reply(st,result)
        ability()
    
def ability():
    print ('main1')
    count = [0,0,0,0,0,0,0]
    flag = False
    max_id = None
    while(True):
        toots = mastodon.account_statuses(bot_sourth['id'], max_id = max_id)
        if len(toots) == 0:
            break
        for toot in toots:
            date = datetime.strptime(toot['created_at'], '%Y-%m-%d %H:%M:%S')
            considerdate = datetime.strptime('2021-12-31','%Y-%m-%d %H:%M:%S')
            if date == considerdate:
                flag = True
                break
            if '吉' in toot['content'] or '凶' in toot['content']:
                if '@' in toot['content'] and toot['reblogs_count'] == 0:
                    es = 0
                    if '大吉' in toot['content']:
                        print('大吉')
                        count[0] +=1
                    if '中吉' in toot['content']:
                        count[1] +=1
                    if '小吉' in toot['content']:
                        count[2] +=1
                    if '吉' in toot['content']:
                        count[3] +=1
                    if '末吉' in toot['content']:
                        count[4] +=1
                    if '凶' in toot['content']:
                        count[5] +=1
                    if '大凶' in toot['content']:
                        count[6] +=1
                    else:
                        pass
        if flag:
            break
        max_id = toots[-1]['id']
    content = '現在の御籤の排出率は以下の通りです' '\n大吉:' + str(count[0]) + '\n中吉:' +  str(count[1]) + '\n小吉:' +  str(count[2]) + '\n吉:' +  str(count[3]) + '\n末吉:' +  str(count[4]) + '\n凶:' +  str(count[5]) + '\n大凶:' +  str(count[6]) 
    mastodon.toot(content)
    time.sleep(2)

def hoge():
    mastodon.stream_user(Stream())

threading.Thread(target = hoge).start()
while(True):
    date = datetime.now()
    if date.hour == 0 or date.hour == 12:
        main()
    time.sleep(3600)