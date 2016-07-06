from flask import Flask, request, Response
import os
from random import randint
from kik import KikApi, Configuration
from kik.messages import messages_from_json, TextMessage,VideoMessage,SuggestedResponseKeyboard,TextResponse
app = Flask(__name__)
# kik = KikApi("TwerkBabes","aa3bc886-2ccc-4382-a754-248cdce3b0c8")
# kik = KikApi("TwerkBabes","e3900be8-7cb0-491e-8fa2-95a58719ce3a")
kik = KikApi("TwerkBabes","e3900be8-7cb0-491e-8fa2-95a58719ce3a")
kik.set_configuration(Configuration(webhook="http://107.170.21.148:9997/incoming",features= {"manuallySendReadReceipts": True,"receiveReadReceipts": True,"receiveDeliveryReceipts": True,"receiveIsTyping": True}))

#kik.send_messages([TextMessage(to='adertsc3521',body='Test')])

dir_list = os.listdir('/var/www/html/videos')
@app.route('/incoming', methods=['POST'])
def incoming():
	# print 'kuch to hua2'
	if not kik.verify_signature(request.headers.get('X-Kik-Signature'), request.get_data()):
		return Response(status=403)
	messages = messages_from_json(request.json['messages'])
	msg = TextMessage()

	for message in messages:
 		if isinstance(message, TextMessage):
 			# print message.body
 			# kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="thank you for messaging TwerkBabes. Your daily source of Twerkers")])
 			# kik.send_messages([VideoMessage(to=message.from_user,chat_id=message.chat_id,video_url="http://199.217.117.213:9999/static/tt.mp4")])
 			# kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="We hope you enjoyed this twerk babe! See more by going to url.com")])
 			# break
 			random_index = randint(0,len(dir_list)-1)
 			file_name = dir_list[random_index]
 			if message.body == 'more twerk':
 				kik.send_messages([VideoMessage(to=message.from_user,chat_id=message.chat_id,video_url="http://107.170.21.148/videos/"+file_name),TextMessage(to=message.from_user,chat_id=message.chat_id,body="We hope you enjoyed this twerk babe! See more by going to url.com",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse('more twerk')])])])
 			else:
 				kik.send_messages([TextMessage(to=message.from_user,chat_id=message.chat_id,body="thank you for messaging TwerkBabes. Your daily source of Twerkers"),VideoMessage(to=message.from_user,chat_id=message.chat_id,video_url="http://107.170.21.148/videos/"+file_name),TextMessage(to=message.from_user,chat_id=message.chat_id,body="We hope you enjoyed this twerk babe! See more by going to url.com",keyboards=[SuggestedResponseKeyboard(to=None,hidden=False,responses=[TextResponse('more twerk')])])])
 			break
 	# msg.keyboards.append(SuggestedResponseKeyboard(to=message.from_user,hidden=False,responses=[TextResponse('OK')]))


	return Response(status=200)

@app.route('/', methods=['GET'])
def home():
	return "hello"


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True,port=9997)