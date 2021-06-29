import vk_api
import altcardlibfiles
import altdeckeditor
import GreatLibrarySorter
import Dictionaries

vk_session = vk_api.VkApi(token='token')
session_api = vk_session.get_api()
id_group = 'group'  # id группы с изображениями


def alt_card_pic(card):  # возвращает адрес изображения по индексу карты
    picn = GreatLibrarySorter.numskipre(card[1])
    album = altcardlibfiles.album(card[0])
    maxpicnum = session_api.photos.get(owner_id=id_group, album_id=album, count=0)['count']
    if 0 <= picn < maxpicnum:
        pictures = session_api.photos.get(owner_id=id_group, album_id=album, count=1, offset=picn)['items']
        buf = []
        for element in pictures:
            buf.append('photo' + str(id_group) + '_' + str(element['id']))
        attachment = ','.join(buf)
        return attachment
    return 0


def deck_pics(deck):  # возвращает строку с адресами изображений карт
    buf = []
    decoded_deck = altdeckeditor.deck_decoder(deck)
    for element in decoded_deck:
        card = element
        attpic = alt_card_pic(card)  # запрашивает адрес изображения по индексу карты
        buf.append(attpic)
    attachment = ','.join(buf)
    return attachment


def textalbums():  # техническая команда для создания текстовых файлов с адресами фотографий
    try:
        f = open('cards/SeriesIndexes.txt', 'r')
        cset = f.readline()[-2]
        while cset != '/':
            album = altcardlibfiles.album(cset)
            a = open('vkalbums/' + str(album) + '.txt', 'w')
            print(1)
            maxpicnum = session_api.photos.get(owner_id=id_group, album_id=album, count=0)['count']
            print(maxpicnum)
            i = 0
            while i < maxpicnum:
                pic = session_api.photos.get(owner_id=id_group, album_id=album, count=1, offset=i)['items']
                buf = []
                for element in pic:
                    buf.append('photo' + str(id_group) + '_' + str(element['id']))
                attachment = ','.join(buf)
                print("pic " + str(i + 1) + " in " + Dictionaries.indexes_to_series[cset] + " done")
                a.writelines(attachment + "\n")
                i += 1
            a.writelines("/\n")
            a.close()
            print(Dictionaries.indexes_to_series[cset] + " done\n")
            cset = f.readline()[-2]
        f.close()
        print("\nALL DONE")
        return 1
    except:
        return 0
