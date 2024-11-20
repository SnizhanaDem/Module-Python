import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox, simpledialog

file_path = "data_module.csv"  # Шлях до файлу
data = pd.DataFrame()  

# Функція для завантаження даних із CSV-файлу
def load_data(file_path):
    global data
    # Зчитування даних з обробкою вийнятків
    try:
        data = pd.read_csv(file_path)
        messagebox.showinfo("Успіх", "Дані завантажено успішно!")
        return data
    except FileNotFoundError:
        messagebox.showerror("Помилка", f"Файл '{file_path}' не знайдено.")
    except pd.errors.EmptyDataError:
        messagebox.showerror("Помилка", "Файл порожній.")
    except pd.errors.ParserError:
        messagebox.showerror("Помилка", "Некоректний формат CSV-файлу.")

# Функція для збереження даних у CSV-файл
def save_data(file_path, data):
    if data is None:
        messagebox.showwarning("Попередження", "Немає даних для збереження.")
        return
   
   # Збереження даних з обробкою вийнятків
    try:
        data.to_csv(file_path, index=False)
        messagebox.showinfo("Успіх", "Дані збережено успішно!")
    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка під час збереження даних: {e}")

# Функція для додавання товару
def add_product():
    global data
    
    if data.empty:
        messagebox.showerror("Помилка", "Спочатку завантажте дані з файлу CSV!")
        return
    
    # Присвоєння значень з обробкою вийнятків
    name = simpledialog.askstring("Додати клієнта", "Введіть ім'я клієнта:")
    if not name:
        messagebox.showwarning("Увага", "Ім'я не введено.")
        return
    
    try:
        number = int(simpledialog.askstring("Додати номер замовлення", "Введіть номер:"))
        if not number:
            messagebox.showwarning("Увага", "Номер не введено.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип номеру замовлення.")
        return
    try:
        date = str(simpledialog.askstring("Додати дату", "Введіть дату замовлення:"))
        if not date:
            messagebox.showwarning("Увага", "Дату не введено.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип дати замовлення.")
        return
    
    try:
        price = float(simpledialog.askstring("Додати суму", "Введіть суму замовлення:").replace(',', '.'))
        if price <= 0:
            messagebox.showwarning("Увага", "Сума має бути більше нуля.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип даних суми.")
        return
    
    # Введення статусу
    status_options = ["Виконано", "В процесі"]
    status = simpledialog.askstring("Додати статус", f"Введіть статус замовлення ({', '.join(status_options)}):")
    if not status or status not in status_options:
        messagebox.showwarning("Увага", f"Статус має бути одним із: {', '.join(status_options)}.")
        return
    
    # Встановлення даних
    product = pd.DataFrame({
        "Ім'я клієнта": [name],
        'Номер замовлення': [number],
        'Дата замовлення': [date],
        'Сума замовлення': [price],
        'Статус' : [status_options]
        })
    
    # Об'єднання товару з таблицею
    data = pd.concat([data, product], ignore_index=True)
    messagebox.showinfo("Успіх", "Товар додано!")
    return data

# Функція для редагування інформації про товар
def edit_product():
    global data
    
    if data.empty:
        messagebox.showinfo("Інформація", "Немає товарів для редагування.")
        return
    
    # Якщо існує товар, зміна його даних з обробкою вийнятків
    name = simpledialog.askstring("Редагування товару", "Введіть ім'я для редагування:") 
    if not name:
        messagebox.showwarning("Увага", "Назву ім'я не введено.")
        return

    # Переведення введеної назви та назв у таблиці до нижнього регістру
    # Ігноруваеея регістру
    name = name.strip().lower()
    product = data[data["Ім'я клієнта"].str.lower() == name]
    
    if product.empty:
        messagebox.showerror("Помилка", f"ім'я клієнта '{name}' не знайдено!")
        return
    
    try:
        new_number = int(simpledialog.askstring("Редагування товару", f"Введіть новий номер:", initialvalue=product['Номер замовлення'].values[0]))
        if not new_number:
            messagebox.showwarning("Увага", "Номер  не введено.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип даних номеру.")
        return
    try:
        new_date = str(simpledialog.askstring("Редагування товару", f"Введіть нову дату:", initialvalue=product['Дата замовлення'].values[0]))
        if not new_date:
            messagebox.showwarning("Увага", "Дату не введено.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип дати замовлення.")
        return    
    try:
        new_price = float(simpledialog.askstring("Редагування товару", f"Введіть нову суму:", initialvalue=product['Сума замовлення'].values[0]).replace(',', '.'))
        if new_price <= 0:
            messagebox.showwarning("Увага", "Сума має бути більше нуля.")
            return
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип даних суми.")
        return
    
    # Оновлення статусу
    status_options = ["Виконано", "В процесі"]
    new_status = simpledialog.askstring("Редагування замовлення", f"Введіть новий статус ({', '.join(status_options)}):")
    if not new_status or new_status not in status_options:
        messagebox.showwarning("Увага", f"Статус має бути одним із: {', '.join(status_options)}.")
        return

    # Збереження змін
    data.loc[data["Ім'я клієнта"].str.lower() == name, ['Номер замовлення', 'Дата замовлення', 'Сума замовлення', 'Статус']] = [new_number, new_date, new_price, new_status]
    messagebox.showinfo("Успіх", "Інформацію про замовлення оновлено!")

# Функція для видалення замовлення за номером
def delete_product():
    global data

    if data.empty:
        messagebox.showinfo("Інформація", "Немає замовлень для видалення.")
        return

    try:
        order_number = int(simpledialog.askstring("Видалити замовлення", "Введіть номер замовлення для видалення:"))
    except ValueError:
        messagebox.showerror("Помилка", "Некоректний тип номеру замовлення.")
        return

    # Пошук замовлення за номером
    product = data[data["Номер замовлення"] == order_number]

    if product.empty:
        messagebox.showwarning("Увага", f"Замовлення з номером '{order_number}' не знайдено!")
        return

    # Видалення замовлення
    data = data[data["Номер замовлення"] != order_number]
    messagebox.showinfo("Успіх", f"Замовлення з номером '{order_number}' видалено!")


# Функція виведення таблиці з даними товарів
def show_products():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає товарів для відображення.")
        return
    
    # Створення вікна для показу таблиці
    top = tk.Toplevel(root)
    top.title("Всі товари")
    
    # Створення таблиці
    text = tk.Text(top, width=80, height=20)
    text.pack(padx=10, pady=10)
    
    # Перетворення даних на текст для виведення
    table_str = data.to_string(index=False)
    text.insert(tk.END, table_str)

import matplotlib.pyplot as plt
from tkinter import Button

# Підрахунок загальної кількості замовлень і їх сумарної вартості
def analyze_total():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає даних для аналізу.")
        return

    total_orders = len(data)
    total_value = data['Сума замовлення'].sum()
    messagebox.showinfo("Аналіз замовлень", f"Загальна кількість замовлень: {total_orders}\nСумарна вартість: {total_value:.2f}")

# Аналіз замовлень за статусом
def analyze_status():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає даних для аналізу.")
        return

    status_counts = data['Статус'].value_counts()
    result = "\n".join([f"{status}: {count}" for status, count in status_counts.items()])
    messagebox.showinfo("Аналіз за статусом", f"Розподіл замовлень за статусами:\n{result}")

# Пошук замовлення з найбільшою сумою
def find_max_order():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає даних для аналізу.")
        return

    max_order = data.loc[data['Сума замовлення'].idxmax()]
    result = f"Найбільше замовлення:\nІм'я клієнта: {max_order["Ім'я клієнта"]}\nНомер замовлення: {max_order['Номер замовлення']}\nСума: {max_order['Сума замовлення']:.2f}"
    messagebox.showinfo("Максимальне замовлення", result)

# Побудова кругової діаграми частки виконаних і невиконаних замовлень
def visualize_status_pie():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає даних для візуалізації.")
        return

    status_counts = data['Статус'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title("Частка замовлень за статусом")
    plt.show()

# Побудова гістограми кількості замовлень за датами
def visualize_orders_histogram():
    global data
    if data.empty:
        messagebox.showinfo("Інформація", "Немає даних для візуалізації.")
        return

    plt.figure(figsize=(10, 6))
    data['Дата замовлення'] = pd.to_datetime(data['Дата замовлення'], errors='coerce')
    date_counts = data['Дата замовлення'].value_counts().sort_index()
    plt.bar(date_counts.index.strftime('%Y-%m-%d'), date_counts.values)
    plt.xlabel("Дата замовлення")
    plt.ylabel("Кількість замовлень")
    plt.title("Кількість замовлень за датами")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

root = tk.Tk()
root.title("Управління замовленнями (CSV)")
root.geometry("300x400")

# Кнопка для завантаження файлу
load_button = tk.Button(root, text="Завантажити CSV", command=lambda: load_data(file_path))
load_button.pack(pady=10)

# Кнопка для додавання замовлення
add_button = tk.Button(root, text="Додати товар", command=add_product)
add_button.pack(pady=5)

# Кнопка для редагування інформації про замовленн
edit_button = tk.Button(root, text="Редагувати товар", command=edit_product)
edit_button.pack(pady=5)

# Кнопка для видалення замовлення
delete_button = tk.Button(root, text="Видалити товар", command=delete_product)
delete_button.pack(pady=5)

# Кнопка для збереження оновлених даних
save_button = tk.Button(root, text="Зберегти CSV", command=lambda: save_data(file_path, data))
save_button.pack(pady=5)

# Кнопка для виведення всіх тзамовлень
show_button = tk.Button(root, text="Показати всі товари", command=show_products)
show_button.pack(pady=5)

# Створення кнопок для функцій аналізу
Button(root, text="Загальна кількість і вартість замовлень", command=analyze_total).pack(pady=5)
Button(root, text="Аналіз замовлень за статусом", command=analyze_status).pack(pady=5)
Button(root, text="Найбільше замовлення", command=find_max_order).pack(pady=5)
Button(root, text="Діаграма частки замовлень за статусом", command=visualize_status_pie).pack(pady=5)
Button(root, text="Гістограма замовлень за датами", command=visualize_orders_histogram).pack(pady=5)

root.mainloop()