'''
Created on Sep 21, 2013

'''
from collections import deque
import time
import praw
import httplib
import urllib
from UniqueQueue import UniqueQueue

global recentcommentid, tempcommentid, idflag
global recentcommentid
recentcommentid = ''
global dubqueue
dubqueue = deque()
global processedqueue
processedqueue = UniqueQueue()
def processqueue():
    try:
        comment = dubqueue.popleft()
        parent = r.get_info(thing_id=comment.parent_id)
        if not processedqueue.contains(parent.id):
#            comment.reply("test")
            params = urllib.urlencode({'commentText': parent.body})
            f = urllib.urlopen("http://cs4414.cloudapp.net/wubbify/"+parent.id, params)
            processedqueue.append(parent.id)
#            print f.read()
            comment.reply(f.read())
        #if SOUNDCLOUD IS FULLLLL
            #DELETE (processedqueue.popleft)
            
    except IndexError:
        print 'No Processes'
    except IOError:
        print 'No connection'
    
r = praw.Reddit('Dubstep request parser')
r.login('DubstepBot','') # TODO: Need to fix
while 1==1:
    all_comments = r.get_comments('all',limit=1000)
    idflag = 1
    for comment in all_comments:
        if comment.id == recentcommentid: #Checks whether the comment has been processed previously
            print 'Processing'
            processqueue()
            time.sleep(60)
            break;
        if idflag:  #flag maniuplation so that this section only executes for the first comment (most recent) in all_comments
            idflag = 0
            global tempcommentid
            tempcommentid = comment.id
#        print comment.id
        #print comment
        try:
#            print str(comment.body)
            if str(comment.body) == 'wubit':
                if comment.is_root:
                    parent = comment.submission
                else:
#                print parent
                    dubqueue.append(comment)
#                print ("cs4414.cloudapp.net/wubbify/"+comment.parent_id)
                
                #wubparent
                #parent.reply('placeholder')
        except:
            print ''
    recentcommentid = tempcommentid
