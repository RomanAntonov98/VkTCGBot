from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import altmessageoperator

login, password = "Login", "Password"  # логин и пароль
vk_session = vk_api.VkApi(login=login, password=password, app_id=2685278)
vk_session.auth(token_only=True)

token = "Token"  # токен для группы, которая будет отправлять сообщения
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and not event.from_me:
                incmsg = event.text

                if event.from_user and not event.from_me:
                    chat_id = 0
                    text, attachment = altmessageoperator.alt_read_msg(incmsg, event.user_id)
                    attachment_2 = "null"
                    if attachment == "null":
                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': text, 'random_id': 0})
                    else:
                        if len(attachment) > 260:  # по длине строки проверяет количество изображений
                            attachment_2 = attachment[260:]
                            attachment = attachment[:260]
                        vk_session.method('messages.send', {'user_id': event.user_id, 'message': text, 'random_id': 0,
                                                            'attachment': attachment})
                        if attachment_2 != "null":  # остальные изображения отправляет во втором сообщинии
                            vk_session.method('messages.send',
                                              {'user_id': event.user_id, 'message': "Остальные карты:",
                                               'random_id': 0, 'attachment': attachment_2})
                elif event.from_chat and incmsg[:5] == "баку " and not event.from_me:  # реагирует только на обращение
                    try:
                        text, attachment = altmessageoperator.alt_read_msg(incmsg[5:], event.user_id)
                        attachment_2 = "null"
                        if attachment == "null":
                            vk_session.method('messages.send',
                                              {'chat_id': event.chat_id, 'message': text, 'random_id': 0})
                        else:
                            if len(attachment) > 260:
                                attachment_2 = attachment[260:]
                                attachment = attachment[:260]
                            vk_session.method('messages.send',
                                              {'chat_id': event.chat_id, 'message': text, 'random_id': 0,
                                               'attachment': attachment})
                            if attachment_2 != "null":
                                vk_session.method('messages.send',
                                                  {'chat_id': event.chat_id, 'message': "Остальные карты:",
                                                   'random_id': 0, 'attachment': attachment_2})
                    except:
                        vk_session.method('messages.send',
                                          {'chat_id': event.chat_id, 'message': 'Команда не распознана',
                                           'random_id': 0})
    except Exception as error:
        print(error)
