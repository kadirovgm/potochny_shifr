# x^31 + x^6 + 1 - полином обратной связи
# x^m + x^l + 1
# генератор М - последовательности

# зарандомить значения регистра сдвига
# key.txt - хранится начальное состояние регистра сдвига
# возможность вывода первых n двоичных символов М-последоавтельности
#####################################################################################################################

import math
import random


# def rand(start, end, num):
#     res = []
#     for j in range(num):
#         res.append(random.randint(start, end))
#     with open('key.txt', mode='w', encoding="utf-8") as file_reg:  # начальное значение регистра
#         file_reg.write(str(res))
#
#     return res
#
#
# num = 4
# start = 0
# end = 1
#
# begin = rand(start, end, num)
#
#
# def keygen(begin, num):
#     b = begin
#     for i in range(1000):
#         b[num+i] = b[0] ^ b[3]
#     return b
#
# print(keygen(begin, num))


print("Введите число степеней полинома")
chislo = int(input())
pol = []  # полином
print("Введите степени полинома")
for i in range(chislo):
    stepen = int(input())  # вводим степень полинома
    pol.append(stepen)  # вставялем в конец списка значение аргумента
k = int(pol[0])
razr = k

print("pol = " + str(pol))
print("razr = " + str(razr))

# Теперь pol содержит два степеня полинома - 31,3


# def createbi(k):
#     r = random.randint(0, pow(2, k)-1)
#     print(r)
#     r = bin(r)[2:]
#     if (len(r) != k):
#         num = k-len(r)
#     zeros = '0'*num
#     r = zeros+r
#     with open('random_binary.txt', mode='w') as file:
#         file.write(r)
#     # print(pol)

def rand(num):
    res = []
    for i in range(num):
        res.append(random.randint(0, 1))

    x = len(res) - 1  # объединение элементов списка в одно целое число
    res_perevod = 0
    for i, v in enumerate(res):
        res_perevod += v * 10 ** (x - i)

    with open('key.txt', mode='w', encoding="utf-8") as file_reg:  # начальное значение регистра
        file_reg.write(str(res_perevod))

    print("Это регистр после рандома: " + str(res_perevod))
    # print(len(res))
    return res_perevod


def lfsr(taps, n):  # передаем степенИ полинома и разрядность
    k = int(taps[0])  # степень полинома
    rand(k)  # отработала функция генерации регистра
    # createbi(k)
    with open('key.txt') as f:  # считываем регистр
        seed = f.read()
        print("Что считал с key.txt: " + str(seed))


    sr = seed  # исходный регистр
    xor = 0
    m = []  # список для М - последовательности

    for i in range(n):  # n - 4*31 = 124
        m.append(sr[len(sr) - 1])
    print("m - posled: " + str(m))
    for t in taps:
        xor ^= int(sr[len(sr)-t])
    print("xor: " + str(xor))
    sr = str(xor) + sr[:-1]
    xor = 0
    print(sr)
    # if sr == seed:
    # break
    print("м-последовательность")
    return m  # может sr??


m = lfsr(pol, 4*razr)
print(m)







