import tkinter as tk
from tkinter import ttk
import random

# Глобальные переменные для статистики
total_flips = 0
yes_count = 0
no_count = 0

def flip_coin():
    global total_flips, yes_count, no_count
    
    result = random.choice(["ДА", "НЕТ"])
    total_flips += 1
    
    if result == "ДА":
        yes_count += 1
    else:
        no_count += 1
    
    update_display(result)
    return result  # Возвращаем результат для автоподброса

def auto_flip():
    try:
        num_flips = int(auto_flip_entry.get())
        if num_flips <= 0:
            raise ValueError
    except ValueError:
        result_label.config(text="Ошибка: введите число > 0")
        return
    
    # Сбрасываем статистику перед автоподбросом (опционально)
    reset_stats()  
    
    for _ in range(num_flips):
        flip_coin()
    
    result_label.config(text=f"Автоподброс: {num_flips} раз")

def update_display(result=None):
    if total_flips > 0:
        yes_percent = (yes_count / total_flips) * 100
        no_percent = (no_count / total_flips) * 100
    else:
        yes_percent = no_percent = 0.0
    
    stats_label.config(
        text=f"Всего подбрасываний: {total_flips}\n"
             f"ДА: {yes_count} ({yes_percent:.1f}%)\n"
             f"НЕТ: {no_count} ({no_percent:.1f}%)"
    )

def reset_stats():
    global total_flips, yes_count, no_count
    total_flips = yes_count = no_count = 0
    result_label.config(text="Результат: —")
    update_display()

# Создаем основное окно
root = tk.Tk()
root.title("Монетка - Да/Нет + Автоподброс")
root.geometry("400x300")

# Надпись с инструкцией
instruction_label = tk.Label(root, text="Нажмите кнопку, чтобы подкинуть монетку!")
instruction_label.pack(pady=5)

# Кнопка для подбрасывания монетки
flip_button = tk.Button(root, text="Подкинуть монетку", command=flip_coin)
flip_button.pack(pady=5)

# Метка для вывода результата
result_label = tk.Label(root, text="Результат: —", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

# Метка для статистики
stats_label = tk.Label(
    root,
    text="Всего подбрасываний: 0\nДА: 0 (0.0%)\nНЕТ: 0 (0.0%)",
    justify="left"
)
stats_label.pack(pady=10)

# === Автоматический подброс ===
auto_frame = tk.Frame(root)
auto_frame.pack(pady=10)

auto_flip_label = tk.Label(auto_frame, text="Автоподброс (кол-во):")
auto_flip_label.pack(side="left")

auto_flip_entry = tk.Entry(auto_frame, width=10)
auto_flip_entry.pack(side="left", padx=5)

auto_flip_button = tk.Button(auto_frame, text="Запуск", command=auto_flip)
auto_flip_button.pack(side="left")

# Кнопка сброса статистики
reset_button = tk.Button(root, text="Сбросить статистику", command=reset_stats)
reset_button.pack(pady=10)

# Запуск основного цикла
root.mainloop()