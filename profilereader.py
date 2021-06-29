import altdeckeditor


def user_stat(user_id):  # возвращает информацию по профилю пользователя
    try:
        f = open('profiles/' + str(user_id) + '.txt', 'r')
    except:  # если профиля нет, то создаётся новый
        print("Создан новый профиль: " + str(user_id))
        f = open('profiles/' + str(user_id) + '.txt', 'w+')
        f.writelines(["00\n", "0000\n", "0100\n"])
        f.writelines(["z5AedlzogDaL#########\n"])
        f.writelines(["#" * 44 + "\n"])
        f.seek(0)
    status = str(int(f.readline()[:-1]))
    wins = str(int(f.readline()[:-1]))
    rating = str(int(f.readline()[:-1]))
    f.close()
    return str('Победы: ' + wins + '\n' + 'Рейтинг: ' + rating)


def deck_def(user_id, decktype=0):  # возвращает колоду пользователя
    try:
        f = open('profiles/' + str(user_id) + '.txt', 'r')
    except:
        print("Создан новый профиль: " + str(user_id))
        f = open('profiles/' + str(user_id) + '.txt', 'w+')
        f.writelines(["00\n", "0000\n", "0100\n"])
        f.writelines(["z5AedlzogDaL#########\n"])
        f.writelines(["#" * 44 + "\n"])
    f.seek(16 + 23 * decktype)
    deck_line = f.readline()
    f.close()
    a = ""
    c = 0
    while a != "#" and c < len(deck_line):  # отделяет колоду от прочих символов в строке
        a = deck_line[c]
        c += 1
    deck = deck_line[:c - 1]
    return str(deck)


def deck_type(deck):  # возвращает состояние обычной колоды
    try:
        decoded_deck = altdeckeditor.deck_decoder(deck)  # переводит колоду из строки в список
        deck_comp = altdeckeditor.type_decoder(decoded_deck)  # переводит список карт в список типов этих карт
        deck_cntr = 1
        i = 1
        if deck_comp.count(0) + deck_comp.count(9) == 0:  # определяет, для какого формата игры подходит колода
            while i < 7:
                deck_cntr *= deck_comp.count(i)
                i += 1
            if i == 7 and deck_cntr == 1:
                return 1  # колода подходит для европейских правил
            deck_cntr = 0
            i = 1
            while i < 4:
                deck_cntr += deck_comp.count(i)
                i += 1
            if deck_cntr == 3:
                while i < 7:
                    deck_cntr += deck_comp.count(i)
                    i += 1
            if 6 <= len(deck_comp) <= 9 and len(deck_comp) == deck_cntr and deck_comp.count(7) + deck_comp.count(8) == 0:
                return 2  # колода подходит для японских правил
            return 0  # колода не подходит для игры
        else:
            return 0
    except:
        return 0


def alt_deck_type(deck):  # возвращает тип особой колоды - считает сколько карт каждого типа
    try:
        decoded_deck = altdeckeditor.deck_decoder(deck)
        deck_comp = altdeckeditor.type_decoder(decoded_deck)
        if len(deck_comp) != 16:
            i = 1
            txt_out = ""
            while i < 7:
                txt_out += str(deck_comp.count(i))
                i += 1
            return txt_out
        dcm = 1
        dca = 0
        i = 1
        while i < 4:
            dcm *= deck_comp.count(i)
            dca += deck_comp.count(i)
            i += 1
        if dcm != 8 or dca != 6:
            return 2  # см. Dictionaries.altdeckuse
        while i < 7:
            dca += deck_comp.count(i)
            i += 1
        if dca != 16:
            return 3  # см. Dictionaries.altdeckuse
        dca = 0
        while i < 10:
            dca += deck_comp.count(i)
            i += 1
        if dca + deck_comp.count(0) != 0:
            return 4  # см. Dictionaries.altdeckuse
        return 1  # см. Dictionaries.altdeckuse
    except:
        return 0  # см. Dictionaries.altdeckuse


def deck_update(user_id, deck, decktype=0):  # заменяет текущую колоду на новую
    try:
        f = open('profiles/' + str(user_id) + '.txt', 'r+')
    except:
        print("Создан новый профиль: " + str(user_id))
        f = open('profiles/' + str(user_id) + '.txt', 'w+')
        f.writelines(["00\n", "0000\n", "0100\n"])
        f.writelines(["z5AedlzogDaL#########\n"])
        f.writelines(["#" * 44 + "\n"])
    f.seek(16 + 23 * decktype)
    f.write(deck + "#" * ((21 + 23 * decktype) - len(deck)) + "\n")
    f.close()
    return 1


def deck_delete(user_id, decktype=0):  # удаляет колоду
    try:
        f = open('profiles/' + str(user_id) + '.txt', 'r+')
    except:
        print("Создан новый профиль: " + str(user_id))
        f = open('profiles/' + str(user_id) + '.txt', 'w+')
        f.writelines(["00\n", "0000\n", "0100\n"])
        f.writelines(["z5AedlzogDaL#########\n"])
        f.writelines(["#" * 44 + "\n"])
    f.seek(16 + 23 * decktype)
    f.write("#" * (21 + 23 * decktype) + "\n")
    f.close()
    return 1
