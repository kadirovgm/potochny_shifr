# x^31 + x^6 + 1 - полином обратной связи
# x^m + x^l + 1
# генератор М - последовательности

# зарандомить значения регистра сдвига
# key.txt - хранится начальное состояние регистра сдвига
# возможность вывода первых n двоичных символов М-последоавтельности
import math
import random

# regist = []
# regist = random.getrandbits(1000)


def regist_gen(N):
    with open('regist.txt', mode='w', encoding="utf-8") as file:
        # regist = []
        regist = random.getrandbits(N)
        file.write(str(regist))
    return regist


regist_gen(10000)


# print(regist)
# spisok = []
#
# for element in range(100):
#     spisok[element] = regist[0] ^ regist[4]
#     print(spisok[element])









