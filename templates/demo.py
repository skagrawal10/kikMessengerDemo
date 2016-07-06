from flask import Flask, request, Response,render_template
import os
from random import randint
import time
import schedule
from threading import Thread
import datetime
from kik import KikApi, Configuration
from pydblite import Base
import datetime
import json
import csv
from kik.messages import messages_from_json, TextMessage,VideoMessage,SuggestedResponseKeyboard,TextResponse, PictureMessage,CustomAttribution, LinkMessage,Message


#strings
# bot_username = "dailysmokeshows"
bot_username = "dailysmokeshow"
# bot_secret_key = "c705faf0-0083-4f42-9294-6abf7ea8f42a"
bot_secret_key = "e71e8681-239a-47d3-8ace-ca6fbfd9bf48"
webhook_address = "http://107.170.21.148:9999/incoming"
schedule_table_name = 'kik.pdl'
picture_table = 'pic.pdl'
AM8 = '8AM'
PM8 = '8PM'
AM10 = '10AM'
PM10 = '10PM'
DEFAULT_TIME = 18
SET_BAE_TIME = 'SET BAE TIME'
TODAY_BAE = "TODAY'S BAE"
DISABLE_BAE_TIME = 'DISABLE BAE TIME'



app = Flask(__name__)
# kik = KikApi("TwerkBabes","aa3bc886-2ccc-4382-a754-248cdce3b0c8")
# kik = KikApi("TwerkBabes","e3900be8-7cb0-491e-8fa2-95a58719ce3a")
kik = KikApi(bot_username,bot_secret_key)
kik.set_configuration(Configuration(webhook=webhook_address,features= {"manuallySendReadReceipts": True,"receiveReadReceipts": True,"receiveDeliveryReceipts": True,"receiveIsTyping": True}))
db = Base(schedule_table_name)
if db.exists():
	db.open()
#kik.send_messages([TextMessage(to='adertsc3521',body='Test')])
def run_every_10_seconds():
	print 'run_every_10_seconds'
	now = datetime.datetime.now()
	#record = db(user="")
	#now = now.replace(hour=20, minute=0, second=1, microsecond=0)
	print now;
	db = Base(schedule_table_name)
	if db.exists():
		db.open()
	
	records = db.records
	'''
	list_of_records = [];
	for record in records:
		list_of_records.append(records[record]);
		
	db.delete(list_of_records);
	db.commit();
	'''
	for record in records:
		schedule_time = records[record]['schedule_time']
		user = records[record]['user']
		chat_id = records[record]['chat_id']
		enable = records[record]['enable']
		print schedule_time,user,chat_id,enable
		if enable=='no':
			continue
		try:
			if schedule_time==AM8:
				today8am0min = now.replace(hour=8, minute=0, second=0, microsecond=0)
				today8am1min = now.replace(hour=8, minute=1, second=0, microsecond=0)
				if now >= today8am0min and now <= today8am1min:
					kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message 8AM")])
		except:
			pass
		try:
			if schedule_time==PM8:
				print "In 8PM";
				
				today8pm0min = now.replace(hour=20, minute=0, second=0, microsecond=0)
				today8pm1min = now.replace(hour=20, minute=1, second=0, microsecond=0)
				print today8pm0min;
				print today8pm0min;
				if now > today8pm0min and now < today8pm1min:
					print "Condition matched. Sending message to " + str(user);
					kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message 8PM")])
		except Exception as e:
			print (e);
			pass
		try:
			if schedule_time==AM10:
				today10am0min = now.replace(hour=10, minute=0, second=0, microsecond=0)
				today10am1min = now.replace(hour=10, minute=1, second=0, microsecond=0)
				if now > today10am0min and now < today10am1min:
					kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message 10AM")])
		except:
			pass
		try:
			if schedule_time==PM10:
				today10pm0min = now.replace(hour=22, minute=0, second=0, microsecond=0)
				today10pm1min = now.replace(hour=22, minute=1, second=0, microsecond=0)
				if now > today10pm0min and now < today10pm1min:
					kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message 10PM")])
		except:
			pass
		try:
			if schedule_time=='Default':
				todaydefault0 = now.replace(hour=DEFAULT_TIME, minute=0, second=0, microsecond=0)
				todaydefault1 = now.replace(hour=DEFAULT_TIME, minute=1, second=0, microsecond=0)
				if now > todaydefault0 and now < todaydefault1:
					kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message default")])
		except:
			pass
		# else:
			# kik.send_messages([TextMessage(to=user,chat_id=chat_id,body="scheduled message")])

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1) 

video_list = os.listdir('/var/www/html/videos')
pic_list = os.listdir('/var/www/html/pics')
month_map = {};
f = open("input.csv", "rU");

csvreader = csv.reader(f);
count = 1;
for row in csvreader:
	print row;
	try:
		month_map[str(count)] = row[0] + "##" + row[1];
	except:
		pass;
	count += 1;
	
@app.route('/incoming', methods=['POST'])
def incoming():
	if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
		return Response(status=403)
	messages = messages_from_json(request.json['messages'])
	for message in messages:
 		if isinstance(message, TextMessage):
 			random_index_video = randint(0,len(video_list)-1)
 			video_file = "n.mp4"; #video_list[random_index_video]
 			print 'video_file: ',video_file
 			random_index_pic = randint(0,len(pic_list)-1)
 			pic_file = pic_list[random_index_pic]
			now = datetime.datetime.now();
			daily_smoke_show_pic =  month_map[str(now.day)].split("##")[0];
			daily_smoke_show_message =  month_map[str(now.day)].split("##")[1];
			print daily_smoke_show_pic , " " , daily_smoke_show_message;
 			if(message.body=='SETTINGS'):
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="change settings from here",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(SET_BAE_TIME),TextResponse(DISABLE_BAE_TIME)])])])
 			elif message.body==SET_BAE_TIME:
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="plesae select schedule time",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse('8AM'),TextResponse('8PM'),TextResponse('10AM'),TextResponse('10PM'),TextResponse('BACK')])])])
 			elif message.body=='BACK':
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="please choose an option",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse(SET_BAE_TIME),TextResponse('SETTINGS')])])])
 			elif message.body=='8AM' or message.body=='8PM' or message.body=='10AM' or message.body=='10PM':
 				record = db(user=message.from_user)
 				if len(record)>0:
 					record[0].update(schedule_time=message.body,enable='yes')
 					kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="BAE TIME SET TO "+message.body,keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse(SET_BAE_TIME),TextResponse('SETTINGS')])])])
 				else:
 					db.insert(message.from_user,message.chat_id,message.body,'yes')
 					kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="BAE TIME SET TO "+message.body,keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse(SET_BAE_TIME),TextResponse('SETTINGS')])])])
 				db.commit()
 			elif message.body==DISABLE_BAE_TIME:
 				record = db(user=message.from_user)
 				if len(record)>0:
 					record[0].update(enable="no")
 					kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="schedule disabled",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(SET_BAE_TIME),TextResponse(DISABLE_BAE_TIME)])])])
 				else:
 					kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="you have not set any BAE TIME! set now..",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(SET_BAE_TIME),TextResponse(DISABLE_BAE_TIME)])])])
 				db.commit()
 			elif message.body==TODAY_BAE:
 				csv_file = csv.reader(open('input.csv','rU'))
 				todays_day = datetime.datetime.now().day
 				counter = 1
 				media_file_location = ""
 				for row in csv_file:
 					if counter==todays_day:
 						print 'counter: ',counter
 						print 'todays_day: ',todays_day
 						print 'row: ',row
 						media_file = row[0].strip()
 						text_message = row[1].strip()
 						if '.jpg' in media_file:
 							media_file_location = "http://107.170.21.148/pics/"+media_file
 							kik.send_messages([PictureMessage(to=message.from_user,chat_id=message.chat_id,pic_url=media_file_location),TextMessage(to=message.from_user,chat_id=message.chat_id,body=daily_smoke_show_message,keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse('MEET LOCALS'),TextResponse('SETTINGS'),TextResponse('SHARE THIS BAE')])])])
 						elif '.mp4' in media_file:
 							media_file_location = "http://107.170.21.148/videos/"+media_file
 							kik.send_messages([VideoMessage(to=message.from_user,chat_id=message.chat_id,video_url=media_file_location),TextMessage(to=message.from_user,chat_id=message.chat_id,body=daily_smoke_show_message,keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse('MEET LOCALS'),TextResponse('SETTINGS'),TextResponse('SHARE THIS BAE')])])])
 						break
 					else:
 						counter+=1
 			elif message.body=='MEET LOCALS':
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="Are you interested in meeting local girls? Its super easy! Simply go to http://SwipeSmash.com, create a profile and start swiping girls. These girls are local and looking for guys with the same hookup interest! Its the easiest dating app out there! Go to http://SwipeSmash.com",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse('SHARE'),TextResponse('SETTINGS')])])])
 			elif message.body in ['SHARE','SHARE THIS BAE']:
 				print 'in link message'
 				msg = LinkMessage(to=message.from_user,text="CLICK HERE to share with your friends", chat_id=message.chat_id,url='http://107.170.21.148:9999/users',pic_url='http://107.170.21.148/share.png',keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse('MEET LOCALS'),TextResponse('SETTINGS')])])
 				kik.send_messages([msg])
				
 			else:
 				record = db(user=message.from_user)
 				if len(record)==0:
 					db.insert(message.from_user,message.chat_id,'Default','yes')
 					db.commit()
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=None,body="Welcome to BAE'S DAILY! We will send you daily hot babes with there usernames!"),VideoMessage(to=message.from_user,chat_id=message.chat_id,video_url="http://107.170.21.148/welcome/"+video_file),TextMessage(to=message.from_user,chat_id=message.chat_id,body="Click TODAY'S BAE to get started!",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse(TODAY_BAE),TextResponse(SET_BAE_TIME),TextResponse('SETTINGS')])])])
 			break
 	# msg.keyboards.append(SuggestedResponseKeyboard(to=message.from_user,hidden=False,responses=[TextResponse('OK')]))


	return Response(status=200)

@app.route('/users', methods = ['GET', 'POST'])
def delete_cat():
	if request.method == 'GET':
		return render_template('pickusers.html')
		
@app.route('/users/', methods = ['GET', 'POST'])
def delete_cat1():
	if request.method == 'GET':
		return render_template('index.html')		

@app.route('/', methods = ['GET', 'POST'])
def home():
	if request.method == 'GET':
		return 'hello'



if __name__ == "__main__":
	schedule.every(15).seconds.do(run_every_10_seconds)
	t = Thread(target=run_schedule)
	t.start()
	app.run(host='0.0.0.0',debug=True,port=9999,use_reloader=False)
	# app.run(host='0.0.0.0',debug=True,port=9999)

