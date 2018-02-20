# Twitter-Stream-API

This is an API to stream tweets based on a key word entered by the user and to store those tweets into a NoSQL DB. This is done with the help of the Twitter API.

The database used is MongoDB.

Various filters are provided which lets the user filter the tweet data based on tweet text, user name, date of tweet, retweet count follower count etc.

Sorting options have also been provided based on text and time.

Then, this data can be exported into a .csv file with a name and location specified by the user. However, few special characters can't be encoded and hence those tweets are omitted.


## Mongo DB

Mongo DB has to be downloaded and installed for this code to run. You would have to start the mongod server and keep it running behind.
NoSQL databases are know to store large volumes of structured, semi-structured, and unstructured data. All the meta data that comes with the stream has, thus,  been stored in the Data Base with no bias. 

## Django

This code was written using Django.Tweepy and pymongo were additionally used.
Download and install necessary files.

# API 1
The first page lets the user stream tweets based on a key word input, into a Data Base. A button is provided just below to stop stream and a count of the number of tweets imported is displayed to the user. Now the user may choose to either stream again or stream with a new key word input or to o to the filters page.

# API 2
This API provides different filters for the user to select. The user may select to apply, one or many filters based on requirements. The user may also sort the returned tweets by text or time in any order preferred.

# API 3
This part of the code lets the user to export the tweet data 'after applying the filters' into a .csv file. The user is expected to give a name to the file and the location it is to be saved. The default location given would probably not work on your system.
Since this is a backend program at it's core, no JavaScript has been written for validations.

### Note:
An empty table is returned if no data exists satisfying all the applied filter criteria.

Various fields have been selected by me to be exported into the .csv file. Some of them include : User name, tweet text, tweet time, User Verification Report, Followers count, Favourites count. Any more fileds could have been added.

The displayed tweets have been paginated and limited to 15 tweets per page.
