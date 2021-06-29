import altcardlibfiles
import Dictionaries


def deck_decoder(deck):  # переводит строку в список из элементов по два символа
    decoded_deck = []
    while len(deck) > 1:
        card = deck[:2]
        decoded_deck.append(card)
        deck = deck[2:]
    return decoded_deck


def type_decoder(deck_list):  # переводит список индексов карт в список типов карт
    deck_list_types = []
    for element in deck_list:
        t = altcardlibfiles.card_type(element)
        tint = Dictionaries.crdtp_cym_to_int[t]
        deck_list_types.append(tint)
    return deck_list_types


def deck_sorter(decoded_deck):  # сортирует карты в колоде по типам
    sorted_deck = []
    sorted_list = []
    deck_list_types = type_decoder(decoded_deck)

    c = 1
    for element in deck_list_types:
        t = 0
        while deck_list_types.count(c) == 0:
            c += 1
            t += 1
            if t > 10:
                return 0
        sorted_list.append(deck_list_types.index(c))
        deck_list_types[deck_list_types.index(c)] = 0

    for element in sorted_list:
        sorted_deck.append(decoded_deck[element])  # собирает колоду обратно в список индексов
    return sorted_deck


def deck_encoder(decoded_deck):  # переводит список индексов строку
    encodeddeck = ""
    for element in decoded_deck:
        encodeddeck += element
    return str(encodeddeck)


def remove_card(deck, pos):  # убирает карту по номеру позиции
    decoded_deck = deck_decoder(deck)
    decoded_deck.pop(pos - 1)
    organized_deck = deck_sorter(decoded_deck)
    encodeddeck = deck_encoder(organized_deck)
    return encodeddeck


def add_card(deck, card, decktype=0):  # добавляет карту в колоду
    if len(deck) <= (8 + 16 * decktype) * 2:
        deck = deck + card
    decoded_deck = deck_decoder(deck)
    try:
        card_type = Dictionaries.crdtp_cym_to_int[altcardlibfiles.card_type(card)]
    except:
        card_type = 0
    if card_type != 0 and card_type < 7 and decoded_deck.count(card) == 1 and len(decoded_deck) <= 10 + 16 * decktype:
        organized_deck = deck_sorter(decoded_deck)  # карта добавляется в конец, поэтому колоду приходится сортировать
        encoded_deck = deck_encoder(organized_deck)
        return encoded_deck
    return 0
