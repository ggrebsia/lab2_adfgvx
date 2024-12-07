import tkinter as tk
from tkinter import messagebox
from collections import OrderedDict

# Таблица ADFGVX
adfgvx_table = [
    ['p', 'h', '0', 'q', 'g', '6'],
    ['4', 'm', 'e', 'a', '1', 'y'],
    ['l', '2', 'n', 'o', 'f', 'd'],
    ['x', 'k', 'r', '3', 'c', 'v'],
    ['s', '5', 'z', 'w', '7', 'b'],
    ['j', '9', 'u', 't', 'i', '8']
]

adfgvx_letters = "ADFGVX"

def adfgvx_encrypt(plaintext, key):
    # Преобразуем текст в последовательность ADFGVX
    adfgvx_text = ''
    for char in plaintext:
        found = False
        for i in range(6):
            for j in range(6):
                if adfgvx_table[i][j] == char:
                    adfgvx_text += adfgvx_letters[i] + adfgvx_letters[j]
                    found = True
                    break
            if found:
                break
        if not found:
            messagebox.showwarning("Ошибка", f"Символ '{char}' отсутствует в таблице ADFGVX.")
            return ""

    # Создаем матрицу по ключу
    key_len = len(key)
    matrix = [adfgvx_text[i:i + key_len] for i in range(0, len(adfgvx_text), key_len)]

    if len(matrix[-1]) < key_len:
        matrix[-1] = matrix[-1]

    # Сортируем столбцы по ключу
    sort_key_indx = sorted(range(len(key)), key=lambda x: key[x])
    ciphertext = ""
    for indx in sort_key_indx:
        for row in matrix:
            if indx < len(row):
                ciphertext += row[indx]

    return ciphertext
    
def adfgvx_decrypt(ciphertext, key):
    key_len = len(key)
    total = len(ciphertext)
    rows = total // key_len
    excees = total % key_len

    # Сортируем индексы ключа
    key_indx = list(range(len(key)))
    sort_key_indx = sorted(key_indx, key=lambda x: key[x])

    # Разделяем ciphertext на столбцы
    col_lengths = [rows + (1 if i < excees else 0) for i in range(key_len)]
    ciphertext_col = {}
    indx = 0
    for sort_indx in sort_key_indx:
        ciphertext_col[sort_indx] = ciphertext[indx:indx + col_lengths[sort_indx]]
        indx += col_lengths[sort_indx]

    # Восстанавливаем исходный порядок столбцов
    orig_col = [ciphertext_col[i] for i in key_indx]
    adfgvx_text = ""
    for i in range(rows + 1):
        for col in orig_col:
            if i < len(col):
                adfgvx_text += col[i]

    # Декодировка ADFGVX в исходный текст
    plaintext = ""
    for i in range(0, len(adfgvx_text), 2):
        row = adfgvx_letters.index(adfgvx_text[i])
        col = adfgvx_letters.index(adfgvx_text[i + 1])
        plaintext += adfgvx_table[row][col]

    return plaintext

def encrypt_button_click():
    plaintext = plaintext_entry.get()
    key = key_entry.get()
    if plaintext and key:
        ciphertext = adfgvx_encrypt(plaintext, key)
        if ciphertext:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Зашифрованный текст: {ciphertext}")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст и ключ.")

def decrypt_button_click():
    ciphertext = ciphertext_entry.get()
    key = key_entry.get()
    if ciphertext and key:
        plaintext = adfgvx_decrypt(ciphertext, key)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Расшифрованный текст: {plaintext}")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, введите текст и ключ.")

# Создаем интерфейс
root = tk.Tk()
root.title("ADFGVX Шифр")

tk.Label(root, text="Исходный текст:").grid(row=0, column=0, padx=10, pady=10)
plaintext_entry = tk.Entry(root, width=40)
plaintext_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Ключ:").grid(row=1, column=0, padx=10, pady=10)
key_entry = tk.Entry(root, width=40)
key_entry.grid(row=1, column=1, padx=10, pady=10)

encrypt_button = tk.Button(root, text="Зашифровать", command=encrypt_button_click)
encrypt_button.grid(row=2, column=0, padx=10, pady=10)

tk.Label(root, text="Зашифрованный текст:").grid(row=3, column=0, padx=10, pady=10)
ciphertext_entry = tk.Entry(root, width=40)
ciphertext_entry.grid(row=3, column=1, padx=10, pady=10)

decrypt_button = tk.Button(root, text="Расшифровать", command=decrypt_button_click)
decrypt_button.grid(row=4, column=0, padx=10, pady=10)

tk.Label(root, text="Результат:").grid(row=5, column=0, padx=10, pady=10)
result_text = tk.Text(root, height=5, width=40)
result_text.grid(row=5, column=1, padx=10, pady=10)

root.mainloop()
