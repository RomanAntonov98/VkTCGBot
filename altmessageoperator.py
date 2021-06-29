import profilereader
import altcardlibfiles
import altdeckeditor
import Dictionaries
import GreatLibrarySorter
import random


def comm(incmsg):  # возвращает тип команды по первому слову строки
    a = ''
    c = 0
    incmsg += ' '
    while a != ' ':
        a = incmsg[c]
        c += 1
        if c > 15:
            return 0
    command = incmsg[:c - 1].lower()
    return Dictionaries.txtcomm.get(command, 0)


def separator(incmsg):  # возвращает всё, кроме первого слова строки
    a = ''
    c = 1
    incmsg += ' '
    while a != ' ':
        a = incmsg[c]
        c += 1
    rest = incmsg[c:-1]
    return str(rest)


def alt_read_msg(incmsg, user_id):
    command = comm(incmsg)          # первое слово строки переводится в номер команды
    incmsg = separator(incmsg)      # остаток строки преобразуется в аргумент команды
    if command == 1:  # выводит данные профиля
        info = profilereader.user_stat(user_id)
        return info, "null"

    elif command == 5:  # выводит определённую карту
        try:
            if ord('0') <= ord(incmsg[0]) <= ord('9'):
                card = altcardlibfiles.card_into_index(incmsg.lower())  # запрашивает внутренний индекс карты по номеру
            else:
                card = altcardlibfiles.name_search(incmsg)  # запрашивает внутренний индекс карты по названию
            if card == "ZZ":                                # дефолтный индекс - карта не найдена
                return "нет такой карты", "null"
            cardtext = altcardlibfiles.name_type(card)      # запрос текста и типа карты
            attachment = altcardlibfiles.deck_pics(card)    # запрос изображения карты
            return cardtext, attachment
        except Exception as error:
            print(error)
            return "нет такой карты", "null"

    elif command == 11:  # выводит случайную карту
        rnd_command = comm(incmsg)
        at = (rnd_command - 11) * 3 - 2  # определяет тип запрашиваемой случайной карты
        a = '0'
        b = '0'
        t = 0
        while t < at or t > at + 2:  # проверка соответствия типа сгенерированной карты
            a = GreatLibrarySorter.numskip(random.randint(1, 58))       # перевод случайной серии во внутренний индекс
            b = GreatLibrarySorter.numskip(random.randint(1, 49))       # перевод случайного номера во внутренний индекс
            try:
                str_cardtype = (altcardlibfiles.card_type((a + b)))     # определяет тип сгенерированной карты
                t = Dictionaries.crdtp_cym_to_int[str_cardtype]         # переводит его в число
            except:
                t = 0
        card = a + b
        cardtext = altcardlibfiles.name_type(card)
        attachment = altcardlibfiles.deck_pics(card)
        return cardtext, attachment

    elif command == 3:  # взаимодействует с обычной колодой
        deck_command = comm(incmsg)
        if deck_command == 2:  # выводит текущую колоду игрока или заменяет её на новую
            pl_deck = separator(incmsg)
            if len(pl_deck) > 1:
                if profilereader.deck_type(pl_deck) != 0:  # проверяет валидность новой колоды
                    success = profilereader.deck_update(user_id, pl_deck)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 010"
                    return result, "null"
                else:
                    return "Указанная колода не подходит для игры", "null"
            else:
                deck = profilereader.deck_def(user_id)
                try:
                    cardtext = altcardlibfiles.card_texts(deck)             # запрашивает текст и тип всез карт
                    attachment = altcardlibfiles.deck_pics(deck)            # запрашивает адреса изображений всех карт
                    deckuse = Dictionaries.dtl[profilereader.deck_type(deck)]   # запрашивает тип текущей колоды
                    totaltext = "Ваша колода:\n" + cardtext + "\n\nКод колоды: " + deck + "\n\n" + deckuse
                    return totaltext, attachment
                except Exception as error:
                    print(error)
                    return "Что-то очень сильно не так, номер ошибки - 002", "null"

        elif deck_command == 6:  # удаление карт из обычной колоды
            try:
                if separator(incmsg) == "всё":  # удаление всех карт из колоды
                    success = profilereader.deck_delete(user_id)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 011"
                    return result, "null"
                else:  # удаление опрелённой карты в колоде по позиции
                    pos = int(separator(incmsg))
                    deck = profilereader.deck_def(user_id)
                    deck = altdeckeditor.remove_card(deck, pos)
                    success = profilereader.deck_update(user_id, deck)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 012"
                    return result, "null"
            except Exception as error:
                print(error)
                return "Что-то пошло не так, номер ошибки - 013", "null"

        elif deck_command == 7:  # добавление карты в колоду
            try:
                pl_card = separator(incmsg)
                card = altcardlibfiles.name_search(pl_card)
                if card == "ZZ":
                    card = altcardlibfiles.card_into_index(pl_card.lower())
                deck = profilereader.deck_def(user_id)
                new_deck = altdeckeditor.add_card(deck, card)
                if new_deck == 0:
                    return "Что-то пошло не так."
                else:
                    success = profilereader.deck_update(user_id, new_deck)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 014"
                    return result, "null"
            except Exception as error:
                print(error)
                return "Нет такой карты", "null"
        else:
            return "Неопознанная команда", "null"

    elif command == 4:  # взаимодействует с особой колодой
        deck_command = comm(incmsg)
        if deck_command == 2:
            pl_deck = separator(incmsg)
            if len(pl_deck) > 1:
                deckuse = profilereader.alt_deck_type(pl_deck)
                if deckuse == 1:
                    success = profilereader.deck_update(user_id, pl_deck, 1)
                    if success == 1:
                        return "Успешно", "null"
                    else:
                        return "Что-то пошло не так", "null"
                else:
                    return Dictionaries.altdeckuse[deckuse], "null"
            else:
                deck = profilereader.deck_def(user_id, 1)
                try:
                    cardtext = altcardlibfiles.card_texts(deck)
                    dectype = profilereader.alt_deck_type(deck)
                    if int(dectype) > 4:
                        deckuse = Dictionaries.altdeckuse[5]
                        i = 0
                        while i < 6:
                            deckuse += Dictionaries.deckuse_type5_response[i] + " карт в колоде: " + dectype[i] + "\n"
                            i += 1
                    else:
                        deckuse = Dictionaries.altdeckuse[dectype]
                    totaltext = "Ваша колода:\n" + cardtext + "\n\nКод колоды: " + deck + "\n\n" + deckuse
                    attachment = altcardlibfiles.deck_pics(deck)
                    return totaltext, attachment
                except Exception as error:
                    print(error)
                    return "Что-то очень сильно не так, номер ошибки - 002", "null"

        elif deck_command == 6:
            try:
                if separator(incmsg) == "всё":
                    success = profilereader.deck_delete(user_id, 1)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 011"
                    return result, "null"
                else:
                    pos = int(separator(incmsg))
                    deck = profilereader.deck_def(user_id, 1)
                    deck = altdeckeditor.remove_card(deck, pos)
                    success = profilereader.deck_update(user_id, deck, 1)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 012"
                    return result, "null"
            except Exception as error:
                print(error)
                return "Что-то пошло не так, номер ошибки - 013", "null"

        elif deck_command == 7:
            try:
                pl_card = separator(incmsg)
                card = altcardlibfiles.name_search(pl_card)
                if card == "ZZ":
                    card = altcardlibfiles.card_into_index(pl_card.lower())
                deck = profilereader.deck_def(user_id, 1)
                new_deck = altdeckeditor.add_card(deck, card, 1)
                if new_deck == 0:
                    return "Что-то пошло не так."
                else:
                    success = profilereader.deck_update(user_id, new_deck, 1)
                    if success == 1:
                        result = "Успешно"
                    else:
                        result = "Что-то пошло не так, номер ошибки - 014"
                    return result, "null"
            except Exception as error:
                print(error)
                return "Нет такой карты", "null"
        else:
            return "Неопознанная команда", "null"

    elif command == 9:  # техническая команда для перевода текстовых файлов на внутреннюю систему индексирования
        #success = GreatLibrarySorter.the_sort()
        success = 0
        if success == 1:
            result = "Успешно"
        else:
            result = "Что-то пошло не так"
        result = "Эта команда недоступна"
        return result, "null"

    elif command == 10:  # техническая команда для создания текстовых файлов с адресами фотографий
        #success = cardlib.textalbums()
        success = 0
        if success == 1:
            result = "Успешно"
        else:
            result = "Что-то пошло не так"
        return result, "null"
    return "Неопознанная команда", "null"
