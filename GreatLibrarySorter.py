import Dictionaries


def the_sort():  # создаёт текстовые файлы с использованием внутренних индексов на основе текущих текстовых файлов
    f = open('cards/SeriesIndexes.txt', 'r')
    target = f.readline()[:-1]
    while target[0] != '/':
        in_txt = open('cards/' + target[:-1] + '.txt', 'r')
        if ord('A') <= ord(target[-1]) <= ord('Z'):
            out_txt = open('altcards/' + target[-1].lower() + '1.txt', 'w')
        else:
            out_txt = open('altcards/' + target[-1] + '0.txt', 'w')
        line = in_txt.readline()
        out_txt.writelines(line)
        line = in_txt.readline()
        out_txt.writelines(line)
        cardnum = 0
        line = in_txt.readline()
        while line[0] != '/':
            altlib = open('searchcards/' + line[2] + '.txt', 'a')
            altlib.writelines(line[3:-2] + target[-1] + numskip(cardnum) + "\n")
            altlib.close()
            out_txt.writelines(Dictionaries.crdtp_num_to_cym[line[1]] + line[2:-2] + '\n')
            cardnum += 1
            line = in_txt.readline()
        out_txt.writelines("/\n")
        in_txt.close()
        out_txt.close()
        print(target[:-1] + " => " + target[-1] + " Done")
        target = f.readline()[:-1]
    f.close()
    return 0


def numskip(int_input):  # переводит число в букву, соответствующую внутреннему индексу
    int_input -= 1
    result = '!'
    if 0 <= int_input <= 9:
        result = str(int_input)
    if 10 <= int_input <= 35:
        result = chr(ord('a') + int_input - 10)
    if 36 <= int_input <= 61:
        result = chr(ord('A') + int_input - 36)
    return result


def numskipre(str_input):  # переводит букву в число
    result = 0
    if ord('0') <= ord(str_input) <= ord('9'):
        result = ord(str_input) - ord('0')
    if ord('a') <= ord(str_input) <= ord('z'):
        result = ord(str_input) - ord('a') + 10
    if ord('A') <= ord(str_input) <= ord('Z'):
        result = ord(str_input) - ord('A') + 36
    return result

