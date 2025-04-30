import pandas as pd
import namesutil as nu
import sys
import datetime
import glob
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

tk.Tk().withdraw()
dirpath = filedialog.askdirectory()
print(dirpath)
if dirpath == '' :
    sys.exit()
else :
    files = glob.glob(''+dirpath+'/*.csv')
    print('files:',files)

tk.Tk().withdraw()
result = pd.DataFrame(index=[],columns=nu.defaultcols)
for i in files:
    df = pd.read_csv(i,skipinitialspace=True, encoding='utf_8')
    print(len(df))
    if len(df)==21    :
        df['t'] = [10,10,10,7,7,7,5,5,5,4,4,4,3,3,3,2,2,2,1,1,1]
    else    :
        df['t'] = [10,10,10,7,7,7,5,5,5,4,4,4,3,3,3,2,2,2,1,1,1,0,0,0]

    result = pd.concat([result,df])

teamsize = 3
now = datetime.datetime.now()
date = now.strftime('%m%d')
result['nickname'] = result['nickname'].str.strip()
result['best weapon mastery'] = result['best weapon mastery'].str.strip()
result['character'] = result['character'].str.strip()
result['best weapon mastery jp'] = result['best weapon mastery'].replace(nu.weapons)
result['character jp'] = result['character'].replace(nu.characters)
print(result['t'])

#プレイヤー統計
player_statistics = pd.DataFrame(index=[])
players = result['nickname'].unique()
for i in players:
    ii = result[result['nickname'] == i]
    picklist = ii['character'].unique()
    played = int(len(ii))
    win = 0
    for iii in ii.itertuples():
        if int(iii[1]) == 1 :
            win = win + 1
    winper = round( win / played * 100 , 1 )
    fieldkills = int(ii['total field kill'].sum())
    avgkill = round(fieldkills / played,2)
    avgrank = round(( ii['rank'].sum() ) / played,2)
    weaponmastery = round( ( ii['best weapon mastery level'].sum() ) / played, 2)
    avghunt = round( (ii['hunting'].sum()) / played, 2)
    add = pd.DataFrame({'Player name':i,'Character Pick':' / '.join(picklist),'Played Rounds':played,'Win Percent':winper,'Total Kills':fieldkills,'Avg. Kills':avgkill,'Avg. Rank':avgrank,'Avg Hunting':avghunt,'Avg Weapon Mastery':weaponmastery,},index=[0])
    player_statistics = pd.concat([player_statistics,add])

#チーム統計(チームサイズ2以上のみ)
team_statistics = pd.DataFrame(index=[])
teams = result['teamName'].unique()
for i in teams:
    ii = result[result['teamName'] == i]
    played = int(int(len(ii)) / teamsize)
    cnt = teamsize
    win = 0
    for iii in ii.itertuples():
        if cnt % teamsize == 0 :
            if int(iii[1]) == 1 :
                win = win + 1
        cnt = cnt + 1
    winper = round( win / played * 100 , 1)
    kills = int(int(ii['total field kill'].sum()) / teamsize)
    avgkill = round(kills / played,2)
    avgrank = round(( ii['rank'].sum() / teamsize ) / played,2)
    totalpts = int(int(ii['t'].sum()) / teamsize)  + kills
    avgpts = round( totalpts/ played,2)
    add = pd.DataFrame({'Team name':i,'Played Rounds':played,'Win Percent':winper,'Total Kills':kills,'Avg Kills':avgkill,'Avg Rank':avgrank,'Total points':totalpts,'Avg Points':avgpts},index=[0])
    team_statistics = pd.concat([team_statistics,add])

# csvの保存

player_statistics.to_csv('P'+date+'.csv',index = False)
team_statistics.to_csv('T'+date+'.csv',index = False)
    
a = input('Enter something to exit:')
sys.exit()