# x^31 + x^6 + 1 - полином обратной связи
# x^m + x^l + 1
# генератор М - последовательности

# зарандомить значения регистра сдвига
# key.txt - хранится начальное состояние регистра сдвига
# возможность вывода первых n двоичных символов М-последоавтельности
import math
import random


def Rand(start, end, num):
    res = []
    for j in range(num):
        res.append(random.randint(start, end))
    with open('key.txt', mode='w', encoding="utf-8") as file_reg:  # начальное значение регистра
        file_reg.write(str(res))
    return res


num = 10000
start = 0
end = 1

Rand(start, end, num)
# def regist_gen(N):
#     with open('regist.txt', mode='w', encoding="utf-8") as file:
#         # regist = []
#         regist = random.getrandbits(N)
#         file.write(str(regist))
#     return regist
#

# regist_gen(10000)


# print(regist)
# spisok = []
#
# for element in range(100):
#     spisok[element] = regist[0] ^ regist[4]
#     print(spisok[element])









