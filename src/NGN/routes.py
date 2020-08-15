from . import app, request, bot, VERIFY_TOKEN, Session, User, handles

@app.route("/ngn_bot", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    if request.method == 'POST':
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    recipient_id = message['sender']['id']
                    message = message['message'].get('text')
                    if message:
                        handle_message(recipient_id, message)
    return "Message Processed"


def handle_message(recipient_id, user_input):
    # User gathering and integrity check
    session = Session()
    user = session.query(User).filter(User.fb_id == recipient_id).scalar()
    if not user:
        user = User(fb_id=recipient_id, state='home')
        session.add(user)

    if user.state == 'home':
        if user_input in ('help', 'name'):
            user.change_state(user_input)

    handles[user.state](user, user_input)

    session.commit()
    session.close()


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'
