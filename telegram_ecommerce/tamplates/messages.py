from .buttons import boolean_question

def reply(update, context, text):
    update.message.reply_text(text)


def ask_a_boolean_question(
    update, 
    context, 
    pattern_identifier="", 
    question=None):


    if question:
        text = question
    else:
        text = TEXT["ask_if_its_all_ok"]


    user_id = query.from_user.id
    markup = boolean_question(pattern_identifier)
    query.edit_message_text(text, reply_markup=markup)


