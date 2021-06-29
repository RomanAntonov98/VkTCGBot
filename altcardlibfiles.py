import GreatLibrarySorter
import altdeckeditor
import Dictionaries


def cardnum(card):  # возвращает номер карты в сете по индексу
    a = card[1]
    b = GreatLibrarySorter.numskipre(a) + 1
    return b


def cardset(card):  # возвращает индекс набора по индексу карты
    a = card[0]
    if ord('A') <= ord(a) <= ord('Z'):      # во внутренних индексах используются заглавные и строчные буквы,
        return str(a + '1').lower()         # но ос не видит между ними разницы при наименовании файлов, поэтому
    else:                                   # в названиях используются 0 и 1 для того, чтобы различать их между собой
        return str(a + '0')


def album(cset_letter):  # возвращает альбом во вконтакте по индексу набора карты
    if ord('A') <= ord(cset_letter) <= ord('Z'):
        f = open('altcards/' + cset_letter + '1.txt', 'r')
    else:
        f = open('altcards/' + cset_letter + '0.txt', 'r')
    f.seek(4)
    vk_album = f.readline()
    return int(vk_album[:-1])


def card_type(card):  # возвращает тип карты по индексу
    cset = cardset(card)
    n = cardnum(card)
    f = open('altcards/' + cset + '.txt', 'r')
    a = '0'
    maxnum = int(f.read(2))
    if 0 < n <= maxnum:
        f.seek(15)
        while n > 0:
            line = f.readline()
            if line[0] == '/':
                return 0
            else:
                a = line[0]
            n -= 1
        f.close()
        return a
    f.close()
    return 0


def name_search(pl_card):  # ищет карту по названию
    if ord('0') <= ord(pl_card[0]) <= ord('9'):
        return "ZZ"
    f = open("searchcards/" + pl_card[0].upper() + ".txt")  # для упрощения поска на каждый первый символ названий есть
    line = f.readline()                                     # свой тескстовый файл, в котором по оставшейся части
    while line[0] != "/":                                   # названия ищется индекс карты
        if line[:-3].lower() == pl_card[1:].lower():
            f.close()
            return line[-3:-1]
        line = f.readline()
    f.close()
    return "ZZ"  # если карта с укаанным названием не найдена, то возвращает дефотлтный индекс


def name_type(card):  # возвращает название и тип карты
    cset = cardset(card)
    n = cardnum(card)
    f = open('altcards/' + cset + '.txt', 'r')
    a = '0'
    str_index = str(n) + "/" + Dictionaries.indexes_to_series[card[0]]
    maxnum = int(f.read(2))
    if 0 < n <= maxnum:
        f.seek(15)
        line = ""
        while n > 0:
            line = f.readline()
            if line[0] == '/':
                f.close()
                return str("если вы видите этот текст, то где-то произошла ошибочка")
            else:
                a = line[0]
            n -= 1
        f.close()
        return str(Dictionaries.crdtp_cym_to_txt[a] + " карта:\n" + line[1:-1] + " (" + str_index + ")")
    f.close()
    return str("если вы видите этот текст, то где-то произошла ошибочка")


def card_texts(deck):  # возвращает названия и типы карт в колоде
    totaltext = ""
    decoded_deck = altdeckeditor.deck_decoder(deck)
    for element in decoded_deck:
        card = element
        crdtxt = name_type(card) + "\n"
        totaltext += crdtxt
    return totaltext


def card_into_index(str_card):  # переводит индекс карты во внутренний индекс, с которым проще работать
    try:
        a = ''
        c = 0
        while a != "/":
            a = str_card[c]
            c += 1
        num = str_card[:c - 1]
        cset = str_card[c:]
        alt_num = GreatLibrarySorter.numskip(int(num))
        alt_cset = Dictionaries.series_to_indexes[cset]
        alt_card = alt_cset + alt_num
        return alt_card
    except:
        return "ZZ"


def alt_card_pic(card):  # возвращает адрес изображения по индексу карты используя текстовые библиотеки
    picn = GreatLibrarySorter.numskipre(card[1])
    alb = album(card[0])
    f = open('vkalbums/' + str(alb) + '.txt')   # текстовые библиотеки используются вместо поиска изображений через
    f.seek(27 * picn)                           # vk_api по двум причинам: это не требует прогрузки альбомов,
    pic = f.readline()[:-1]                     # что занимет некоторое время, а так же число запросов изображений
    f.close()                                   # от ботов во ВКонтакте ограничено, что очень неприятно.
    buf = []
    buf.append(pic)
    attachment = ','.join(buf)
    return attachment


def deck_pics(deck):  # возвращает строку с адресами изображений карт
    buf = []
    decoded_deck = altdeckeditor.deck_decoder(deck)
    for element in decoded_deck:
        card = element
        attpic = alt_card_pic(card)  # запрашивает адрес изображения по индексу карты
        buf.append(attpic)
    attachment = ','.join(buf)
    return attachment
