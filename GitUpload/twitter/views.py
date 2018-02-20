from django.shortcuts import render, get_object_or_404
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from pymongo import MongoClient
from datetime import datetime
from django.core.paginator import Paginator
import codecs

#twitter auth.
ckey = 'HhFK2YvZ1uvUNXeBaX8ChV4XZ'
csecret = 'ypriMsRiiqF3kzBQYf5v7i3Wmnpdrs4441qYyaYQF59gwJQRSw'
atoken = '512070897-m05qwMOj3P9xcrUTWpmGyRMYWBBBxcHo5SH1RVfp'
asecret = 'g1QLZUnaseCFU0XI6Wob7Kh6lKlOXPIXxWS7ygMTP11yI'

uri = 'mongodb://localhost/twitterDB'

client = MongoClient(uri)
db = client.twitterDB




class listener(StreamListener):
    def __init__(self):
        global num
        num=0

    def on_data(self, data):
        global num
        datajson = json.loads(data)

        #Add following fields with null values in case they are absent. For convenient filtering.
        if ('urls' in datajson['entities']) is False:
            datajson['entities'] = {'urls':{'url':' '}}
        elif ('url' in datajson['entities']['urls']) is False:
            datajson['entities']['urls'] = {'url':' '}

        if ('user_mentions' in datajson['entities']) is False:
            datajson['entities'] = {'user_mentions':{'screen_name':' '}}
        elif ('screen_name' in datajson['entities']['user_mentions']) is False:
            datajson['entities']['user_mentions'] = {'screen_name':' '}

        #inserting data into NoSQL DataBase
        db.twitter_search.insert(datajson)
        num+=1
        return True

    def on_error(self, status):
        print (status)

auth = OAuthHandler(ckey , csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())

collection = db['twitter_search']

compares = ['=','<','>']
encode = ['$eq','$lt','$gt']

#used to refresh
def index(request):
    global key, num
    num=0
    key=''
    return render(request, 'twitter/home.html', {})

def stopStream(request):
    global num
    global key
    twitterStream.disconnect()
    msg='Streaming Stopped.'
    stop=1
    return render(request, 'twitter/home.html', {'msg':msg,'stop':stop,'count':num, 'key':key})

def api1(request):
    global key
    global num
    num=0
    key = request.POST['word']
    msg='Streaming Begun!'
    twitterStream.filter(track=[key], async=True)
    start=1
    return render(request, 'twitter/home.html', {'msg':msg,'start':start})

#api3 also included
def api2(request):
    global n_tweets, nf_tweets


    if request.method == 'POST':
        n_tweets =[]


        #recieve all filter data from user

        user_contains= request.POST.get('user_contains', '')
        user_start = request.POST.get('user_start','')
        user_end = request.POST.get('user_end','')


        mention = request.POST.get('mention','')
        url = request.POST.get('url','')


        start= request.POST.get('start', '')
        end= request.POST.get('end','')

        contains = request.POST.get('contains', '')

        retweetCount = request.POST.get('retweet',-1)
        retweetCompare = request.POST.get('tweetcompare',3)
        retweetCompare=int(retweetCompare)
        retweetCount=int(retweetCount)

        followerCount = request.POST.get('follower',-1)
        followerCompare = request.POST.get('followercompare',3)
        followerCount=int(followerCount)
        followerCompare=int(followerCompare)

        favouriteCount = request.POST.get('favourite',-1)
        favouriteCompare = request.POST.get('favouritecompare',3)
        favouriteCount=int(favouriteCount)
        favouriteCompare=int(favouriteCompare)


        # 0 value is returned in case user wishes to apply no such filter.
        if retweetCount==0:
            retweetCount=-1
        if favouriteCount==0:
            favouriteCount=-1
        if followerCount==0:
            followerCount=-1


        startdate = request.POST.get('startdate','0001-01-01')
        enddate = request.POST.get('enddate','2999-10-02')


        # if user wishes to not filter based on date
        if startdate == '':
            startdate = '0001-01-01'
        if enddate == '':
            enddate = '2999-10-02'

        # change dates to a format we desire
        start_date=datetime.strptime(startdate,'%Y-%m-%d')
        end_date=datetime.strptime(enddate,'%Y-%m-%d')


        #tweet compare
        for i in [1,2,3]:
            if retweetCompare==i:
                retweet=encode[i-1]
                break

        #favourite compare
        for i in [1,2,3]:
            if favouriteCompare==i:
                favourite=encode[i-1]
                break


        #follower compare
        for i in [1,2,3]:
            if followerCompare==i:
                follow=encode[i-1]
                break

        order = request.POST.get('order',-1)
        order = int(order)
        typer = request.POST.get('type',0)
        typer= int(typer)

        if typer==0:
            type = "timestamp_ms"
        else:
            type="text"


        lang = request.POST.get('language','')
        lang = str(lang)


        # applying all filters requested and sorting

        tweets = collection.find(
            {
                "$and":[
                    {"user.name":{"$regex":user_contains}},
                    {"user.name":{"$regex":"^" + user_start}},
                    {"user.name":{"$regex":user_end + "$"}},
                    {"entities.user_mentions.screen_name":{"$regex":mention}},
                    {"entities.urls.url":{"$regex":url}},
                    {"text":{"$regex":contains}},
                    {"text":{"$regex":"^" + start}},
                    {"text":{"$regex":end + "$"}},
                    {"retweet_count":{retweet:retweetCount}},
                    {"user.followers_count":{follow:followerCount}},
                    {"user.favourites_count":{favourite:favouriteCount}},
                    {"user.lang":{"$regex":lang}}
                ]
            },
                {"user.lang":1,"user.time_zone":1,"user.verified":1,"user.friends_count":1,"user.followers_count":1,"created_at":1,"user.name":1,"retweet_count":1,"text":1,"_id":0}
            ).sort(type,order)


        # whether user wishes to export into a csv or not
        imp = request.POST.get('csv',0)
        file_name = request.POST.get('file_name','')
        file_name= str(file_name)
        if file_name == '':
            file_name = 'twitter-data'
        file_name = file_name + '.csv'
        location = request.POST.get('location','')
        location = str(location)
        if location == '':
            location = 'C:/Users/Ideapad/Desktop'
        file = location + '/' + file_name

        # write data into a csv on request

        if imp=='on':
            saveFile = open(file,'a')
            saveFile.write( "User name" + "," + "Time_Zone" + ',' + "Tweet_text" + ',' + "Tweet_time" + ',' + "User_verified" + ',' + "Friends_count" + ',' + "Followers_count" )
            saveFile.write("\n")
            for tweet in tweets:
                try:
                    saveFile = open(file,'a')
                    t=tweet['text']
                    t_new=t.replace('\"','\"\"')
                    saveFile.write( str(tweet['user']['time_zone']) + ',' +  str(tweet['user']['name']) + "," + "\"" + t_new + "\"" + ',' + tweet['created_at'] + ',' + str(tweet['user']['verified']) + ',' + str(tweet['user']['friends_count']) + ',' + str(tweet['user']['followers_count'])   )
                    saveFile.write("\n")
                    saveFile.close()

                except:
                    saveFile = open(file,'a')
                    saveFile.write('ERROR : Couldn\'t import this tweet because of some special characters contained within!')
                    saveFile.write("\n")
                    saveFile.close()

        tweets.rewind()

        for tweet in tweets:
            tweet_date=tweet['created_at']
            date=tweet_date.split(' ')
            formatted_date=datetime.strptime(str(date[1])+'-'+str(date[2])+'-'+str(date[5]),'%b-%d-%Y')
            if formatted_date>=start_date and formatted_date<=end_date:
                n_tweets.append(tweet)

        page = request.GET.get('page',1)
        paginator = Paginator(n_tweets,15)
        nf_tweets= paginator.page(page)

        return render(request, 'twitter/detail.html', {'tweets':nf_tweets})
    else:

        page = request.GET.get('page',1)
        paginator = Paginator(n_tweets,15)
        nf_tweets= paginator.page(page)
        return render(request, 'twitter/detail.html', {'tweets':nf_tweets})


def redirect(request):
    return render(request, 'twitter/filter.html',{'compares':compares})



