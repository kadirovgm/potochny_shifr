from collections import deque
import itertools
import random
import math

# start_list = input().split()

polynom_koef = input().split()

with open('key_2.txt', mode='w') as file:
    bitString = ''.join(random.choice('01') for i in range(31))
    file.write(bitString)
lenght = len(bitString)


def mseries(start_list, polynom_koef) -> str:
    start_list = deque(map(int, bitString))  # создаем очередь FIFO для удобства работы с битами
    polynom_koef = deque(map(int, polynom_koef))  # тож самое
    output = []
    period = 2 ** len(start_list) - 1  # период - максимальная длительность неповторяющейся последователности
    for _ in range(100000):
        temp = 0
        for i in polynom_koef:  # проходим по полиному
            temp ^= start_list[i - 1]  # выбираем из битовой пслдв-ти соответствующие полиному биты
        output.append(start_list[-1])  # в выходной поток записываем "правый бит"
        start_list.appendleft(temp)  # в битовую последовательность добавляем результат сложения полинома
        start_list.pop()  # из битовой последовательности удаляем правый элемент, который ушел на выход
    # print(output)
    output = ''.join(map(str, output))
    with open('key_2.txt', mode='w') as file:
        file.write(''.join((map(str, start_list))))
    print(output)
    return output


def serial_test(m_posledov: str) -> int:
    n_repeats = 1
    k = 1
    bit = [0, 1]
    series = [group for group in set(itertools.permutations(bit * n_repeats, k))]

    new_series = [m_posledov[x:x + k] for x in range(0, len(m_posledov), k)]
    nt = len(new_series) / (2 ** k)
    print(nt)

    print(len(new_series))
    frequencies = []
    for el in series:
        el = ''.join(map(str, el))
        print(el)
        frequencies.append(new_series[2 * lenght:].count(el))
    print(frequencies)

    hi_squared = [((i - nt) ** 2 / nt) for i in frequencies]
    print(hi_squared)
    hi_squared = sum(hi_squared)
    print('Критерий Пирса Хи квадрат = ', hi_squared)
    return hi_squared


def correlation_test(m_posled: str, k: int) -> float:
    N = len(m_posled)
    m_posled = list(map(int, m_posled))

    m1 = m2 = m1_sqr = m2_sqr = M = 0

    for i in range(N - k):
        m1 += 1 / (N - k) * m_posled[i]  # мат ожидание первой пслдв начиная от 0 до к
        m2 += 1 / (N - k) * m_posled[k + i]  # мат ожидание первой пслдв начиная от k до N
        m1_sqr += 1 / (N - k) * m_posled[i] ** 2
        m2_sqr += 1 / (N - k) * m_posled[k + i] ** 2

    for i in range(N - k):
        M += 1 / (N + k) * (m_posled[i] - m1) * (m_posled[k + i] - m2)

    D1 = m1_sqr - m1 ** 2
    D2 = m2_sqr - m2 ** 2

    R = M / (math.sqrt(D1 * D2))

    print('R = ', R)

    Rcrit = 1 / (N - 1) + 2 / (N - 2) * math.sqrt(N * (N - 3) / (N + 1))
    print('R critical = ', Rcrit)

    if abs(Rcrit) > abs(R):
        print('OK')
    else:
        print('R should be smaller')

    return R


def encrypt(key: str) -> list:
    with open('test_input_2.txt') as file:
        input_text = file.readline()
        binary_code = bin(int.from_bytes(input_text.encode(), 'big'))[2:]
    key = list(map(int, key))
    binary_code = list(map(int, binary_code))
    encrypted_text = []
    for liter, code in zip(binary_code, key):
        encrypted_text.append(liter ^ code)
    print(encrypted_text)

    return encrypted_text


def decrypt(key: str, encrypted_text: list) -> str:
    decrypted_text = []
    key = list(map(int, key))
    for liter, code in zip(encrypted_text, key):
        decrypted_text.append(liter ^ code)
    decrypted_text = ''.join(map(str, decrypted_text))
    n = int(decrypted_text, 2)
    decrypt_bits = ' '.join(format(ord(x), 'b') for x in ' '.join(map(str, decrypted_text)))
    print(decrypt_bits)
    decrypt = n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding='utf-8')
    print(decrypt)
    with open('decrypted_2.txt', mode='w') as file:
        file.write(decrypt)

    return str(decrypt)


if __name__ == '__main__':
    output = mseries(bitString, polynom_koef)
    output2 = mseries(bitString, polynom_koef)
    serial_test(output)
    correlation_test(output, 1)
    encrypted_text = encrypt(output)
    decrypt(output, encrypted_text)

    print('\n\nСтатистические тесты для зашифрованного текста:\n')
    correlation_test(''.join(map(str, encrypted_text)), 1)
    serial_test(''.join(map(str, encrypted_text)))
