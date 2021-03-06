# x^31 + x^6 + 1 - полином обратной связи
# x^m + x^l + 1
# генератор М - последовательности

# зарандомить значения регистра сдвига
# key.txt - хранится начальное состояние регистра сдвига
# возможность вывода первых n двоичных символов М-последоавтельности
#####################################################################################################################

import math
import random
import itertools
import re


print("Количество степеней полинома: ")
count = int(input())
polynom = []  # полином
print("Введите степени полинома: ")
for i in range(count):
    power = int(input())  # вводим степень полинома
    polynom.append(power)  # вставялем в конец списка значение аргумента
razr = int(polynom[0])


print("Полином: x^" + str(polynom[0]) + " + x^" + str(polynom[1]))
print("Старший разряд: " + str(razr))

# Теперь pol содержит два степеня полинома - 31,3

# def createbi(k):
#     r = random.randint(0, pow(2, k)-1)
#     print(r)
#     r = bin(r)[2:]
#     if (len(r) != k):
#         num = k-len(r)
#     zeros = '0'*num
#     r = zeros+r
#     with open('key.txt', mode='w') as file:
#         file.write(r)
#     # print(pol)


def rand_key(numeric):
    result = []
    for i in range(numeric):
        result.append(random.randint(0, 1))

    x = len(result) - 1  # объединение элементов списка в одно целое число
    res_perevod = 0
    for i, v in enumerate(result):
        res_perevod += v * 10 ** (x - i)

    with open('key.txt', mode='w', encoding="utf-8") as file_reg:  # начальное значение регистра
        file_reg.write(str(res_perevod))

    print("Сгенерировано начальное значение регистра: " + str(res_perevod))
    # print(len(result))
    return res_perevod


def lfsr_generate(powers, n):  # передаем степенИ полинома и разрядность
    k = int(powers[0])  # высшая степень полинома
    rand_key(k)  # отработала функция генерации регистра
    # createbi(k)
    with open('key.txt') as f:  # считываем регистр
        regist = f.read()
        print("Что считал с key.txt: " + str(regist))
    sr = regist  # исходный регистр
    xor = 0
    m = []  # список для М - последовательности

    for i in range(n):  #
        m.append(sr[len(sr) - 1])  # "выбывший элемент" записываем в m-последовательность

        for j in powers:
            xor ^= int(sr[len(sr)-j])

        sr = str(xor) + sr[:-1]  # результат xor прибавляем в регистр (последний элемент выбывает)
        xor = 0
    # print(len(sr))

    with open('m.txt', mode='w', encoding="utf-8") as file_m:  # начальное значение регистра
        file_m.write(str(m))

    print("M-последовательность сгенерирована в файле m.txt:")
    return m


m = lfsr_generate(polynom, 100000)  # генерация м-последовательности
# print(m)


# CЕРИАЛЬНЫЙ ТЕСТ НА РАВНОМЕРНОСТЬ
print('\n')
print("--- СЕРИАЛЬНЫЙ ТЕСТ ---")
# all_parameters = [['parm1', 'parm2', 'parm3', 'parm4'], ['parm21','parm22','parm23']]

res_m_str = ''  # подготовка м-последовательности для сериального теста, объединяем элементы списка в одно число (убираем пробелы)
for parameters in m:
    res_m_str += '' + ''.join(parameters)
with open('m_stroka.txt', mode='w', encoding="utf-8") as file_m_str:  # начальное значение регистра
    file_m_str.write(str(res_m_str))
# print(res)


def serial_test_generator(m):
    count_povtor = 4  # длина повторений от (к)
    k = 4
    bites = [0, 1]
    series_count = [group for group in set(itertools.permutations(bites * count_povtor, k))] # перестановки длиной k из iterable.

    new_series = [m[x:x + k] for x in range(0, len(m), k)]  # считываем уникальные серии
    # желательно, чтобы каждые k - биты встречались с вероятностью Pj = (1/2^k)
    n_teor = len(new_series) / (2 ** k)
    print("Теоретическая частота каждой комбинации: " + str(n_teor))

    print("Длина серии: " + str(len(new_series)))
    frequencies = []
    for el in series_count:
        el = ''.join(map(str, el))
        print(el)
        frequencies.append(new_series[2 * razr:].count(el))  # n(э) частота (количество серий которая совпадает с j комбинацией)
    print("Количество повторений: " + str(frequencies))  # промежуточное состояние

    hi_squared = [((i - n_teor) ** 2 / n_teor) for i in frequencies]  # основная формула для сериального теста
    print("Промежуточно: " + str(hi_squared))
    hi_squared = sum(hi_squared)
    print('Критерий Пирса X^2 = ', hi_squared)  # мера отклонения
    return hi_squared


result_serial = serial_test_generator(res_m_str)  # вызов функции сериального теста для м-последовательности


# КОРРЕЛЯЦИОННЫЙ ТЕСТ
print('\n')
print("--- КОРРЕЛЯЦИОННЫЙ ТЕСТ ---")


def correlation_test(m_psld, k):
    N = len(m_psld)  # считываем длину м-последовательности
    m_psld = list(map(int, m_psld))  # переводим в список м-последовательность

    m1 = m2 = m1_sqr = m2_sqr = M = 0

    for i in range(N - k):
        m1 += 1 / (N - k) * m_psld[i]  # промеж первой пслдв начиная от 0 до к
        m2 += 1 / (N - k) * m_psld[k + i]  # промеж первой пслдв начиная от k до N
        m1_sqr += 1 / (N - k) * m_psld[i] ** 2
        m2_sqr += 1 / (N - k) * m_psld[k + i] ** 2

    for i in range(N - k):
        M += 1 / (N + k) * (m_psld[i] - m1) * (m_psld[k + i] - m2)

    D1 = m1_sqr - m1 ** 2
    D2 = m2_sqr - m2 ** 2

    R = M / (math.sqrt(D1 * D2))

    print('R = ', R)

    Rcrit = 1 / (N - 1) + 2 / (N - 2) * math.sqrt(N * (N - 3) / (N + 1))  # расчитываем критическое
    print('R (критичный) = ', Rcrit)

    if abs(Rcrit) > abs(R):
        print('Корреляционный тест пройден!')
    else:
        print('R должен быть меньше, корреляционный тест не пройден!')

    return R


correlation_test(m, 1)  # вызов для м-последовательности


# Начинаем шифрование!!!!
print('\n')
print("--- ШИФРОВАНИЕ ---")


def encrypt(key):
    with open("text.txt") as file_text:
        input_text = file_text.readline()
        binary_code = bin(int.from_bytes(input_text.encode(), 'big'))[2:] # переводим текст в бинарный вид


    with open('binary_text.txt', mode='w') as file_binary:  # записываем бинарный текст для последующих тестов
        file_binary.write(str(binary_code))

    key = list(map(int, key))  # переводим м-последовательность в список
    binary_code = list(map(int, binary_code))  # переводим исходный текст в бинарном виде в список

    encrypted_text = []  # список для записи зашифрованного текста (в бинарном виде)

    for litter, code in zip(binary_code, key):
        encrypted_text.append(litter ^ code)  # шифрование

    x = len(encrypted_text) - 1  # объединение элементов списка в одно целое число
    res_perevod_encrypted_text = 0
    for i, v in enumerate(encrypted_text):
        res_perevod_encrypted_text += v * 10 ** (x - i)

    with open('encrypted_text_str', mode='w') as file_encrypt_str:  # записываем зашифрованное сообщение в бинарном виде для последующих тестов
        file_encrypt_str.write(str(res_perevod_encrypted_text))
    # print(encrypted_text)

############################### Осталось показать (зашифрованное сообщение в виде иероглифов)

    encrypted_text_a = ''.join(map(str, encrypted_text))
    decrypt_a = []  # зашифрованное сообщение в бинарном переводим в текст
    for i in range(len(encrypted_text_a)):
        s = encrypted_text_a[i:i + 16] # разбиваем на блоки по 16 бит
        # print(''.join([chr(int(x, 2)) for x in re.split('(........)', s) if x]))
        decrypt_a.append(''.join([chr(int(x, 2)) for x in re.split('(........)', s) if x])) # сплит разделяет строку по 8 бит каждые 16 бит (s)
        # print(decrypt_a)
    decrypt_aa = ''.join(map(str, decrypt_a))
    with open('encrypted_text_text', mode='w') as file_encrypt_text:
        file_encrypt_text.write(str(decrypt_aa))
    print("Файл зашифрован в encrypted_text_text.txt")
    print("++" + str(decrypt_aa))
##############################
    with open('encrypted_text', mode='w') as file_encrypt:
        file_encrypt.write(str(encrypted_text))

    return encrypted_text


result_encrypt = encrypt(m)  # вызов функции шифрования


# РАСШИФРОВКА
def decrypt(key, encrypted_text):
    decrypted_text = []
    key = list(map(int, key))
    for litter, code in zip(encrypted_text, key):
        decrypted_text.append(litter ^ code)
    # print(decrypted_text)
    decrypted_text = ''.join(map(str, decrypted_text))
    n = int(decrypted_text, 2)
    decrypt_bits = ' '.join(format(ord(x), 'b') for x in ' '.join(map(str, decrypted_text)))
    # print("  <Расшифрованные биты> \n" + str(decrypt_bits))
    decrypt = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding='utf-8')
    print("  <Сообщение после расшифровки> \n" + str(decrypt))
    with open('decrypted_text.txt', mode='w') as file:
        file.write(decrypt)

    return str(decrypt)


result_decrypt = decrypt(m, result_encrypt)  # вызов функции расшифровки


# TASK 5 !!!!!!!

# Сериальный тест для исходного сообщеения
print("\n\n")
print("--- СЕРИАЛЬНЫЙ ТЕСТ ДЛЯ ИСХОДНОГО ТЕКСТА ---")
with open('binary_text.txt') as file_binary:  # считываем регистр
    binary_text = file_binary.read()

serial_test_result_text = serial_test_generator(binary_text)


# Сериальный тест для зашифрованного сообщения
print("\n\n")
print("--- СЕРИАЛЬНЫЙ ТЕСТ ДЛЯ ЗАШИФРОВАННОГО ТЕКСТА ---")
with open('encrypted_text_str') as encrypted_text_str:  # считываем регистр
    encrypted_text = encrypted_text_str.read()

serial_test_result_encrypt = serial_test_generator(encrypted_text)


# Корреляционный тест для исходного сообщеения
print("\n\n")
print("--- КОРРЕЛЯЦИОННЫЙ ТЕСТ ДЛЯ ИСХОДНОГО ТЕКСТА ---")
# нужно передавать список, возможно

correlation_test_result_text = correlation_test(binary_text, 16)


# Корреляционный тест для зашифрованного сообщеения
print("\n\n")
print("--- КОРРЕЛЯЦИОННЫЙ ТЕСТ ДЛЯ ЗАШИФРОВАННОГО ТЕКСТА ---")

correlation_test_result_encrypt = correlation_test(result_encrypt, 1)



