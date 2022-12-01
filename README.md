1. you need to Register users/register
2. you need to get Token users/get-token
3. now you can use api/messages/ routes to read / delete / send messages

base_url= https://abra-messaging.onrender.com

if not working try: 
    base_url= https://abra-messaging-prod-abra-messages-nlpl12.mo4.mogenius.io

Django DRF, contains one model ->

    Message:
        sender
        receiver 

        message
        subject 

        read 
        sender_deleted 
        receiver_deleted 

        sent_at 