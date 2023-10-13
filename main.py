import sqlite3
import tkinter as tk

from tkinter import ttk, messagebox

# Создание базы данных и таблицы
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary INTEGER)""")
conn.commit()


# Функция обновления treeview
def update_treeview(tree):
    # Очищаем Treeview от предыдущих записей
    records = tree.get_children()
    for record in records:
        tree.delete(record)

    cursor.execute("SELECT * FROM employees")
    data = cursor.fetchall()
    # Добавляем данные в Treeview
    for employee_info in data:
        tree.insert("", "end", values=employee_info)

    search_entry.delete(0, 'end')


# Функция, вызываемая при нажатии на кнопку для открытия окна
def insert_employee(tree, editing=False):
    item = tree.focus()
    if not item and editing:
        messagebox.showerror("Ошибка", "Ни один сотрудник не выбран.")
        return
        # Создание нового окна
    new_window = tk.Toplevel(window)

    # Создание 4 меток и полей для ввода
    label1 = tk.Label(new_window, text="ФИО:")
    name = tk.Entry(new_window)
    label2 = tk.Label(new_window, text="Телефон:")
    phone = tk.Entry(new_window)
    label3 = tk.Label(new_window, text="Email:")
    email = tk.Entry(new_window)
    label4 = tk.Label(new_window, text="Зарплата:")
    salary = tk.Entry(new_window)

    # Установка позиций и отступов
    label1.pack(side="left", padx=(10, 0))
    name.pack(side="left")
    label2.pack(side="left", padx=(10, 0))
    phone.pack(side="left")
    label3.pack(side="left", padx=(10, 0))
    email.pack(side="left")
    label4.pack(side="left", padx=(10, 0))
    salary.pack(side="left", padx=(0, 10))

    if editing:
        # Вставка в поля для ввода данных из выбранного treeview
        selected_id = tree.item(item)["values"][0]
        name.insert(0, tree.item(item)["values"][1])
        phone.insert(0, tree.item(item)["values"][2])
        email.insert(0, tree.item(item)["values"][3])
        salary.insert(0, tree.item(item)["values"][4])

        def submit():
            # Добавление нового сотрудника
            cursor.execute("UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?",
                           (name.get(), phone.get(), email.get(), salary.get(), selected_id))
            conn.commit()

            # Обновление treeview
            update_treeview(tree)

            # Закрытие нового окна
            new_window.destroy()
            # Создание кнопки "Подтвердить"

        # Создание кнопки "Подтвердить"
        button_submit = tk.Button(new_window, text="Подтвердить", command=submit)
        button_submit.pack()
    else:
        # Функция, вызываемая при нажатии на кнопку "Подтвердить"
        def submit():
            # Добавление нового сотрудника
            cursor.execute("INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)",
                           (name.get(), phone.get(), email.get(), salary.get()))
            conn.commit()

            # Обновление treeview
            update_treeview(tree)

            # Закрытие нового окна
            new_window.destroy()

        # Создание кнопки "Подтвердить"
        button_submit = tk.Button(new_window, text="Подтвердить", command=submit)
        button_submit.pack()


# Функция удаление сотрудника
def delete_employee(tree):
    # Удаление сотрудника
    item = tree.focus()
    tree_selected_id = tree.item(item)["values"][0]
    cursor.execute("DELETE FROM employees WHERE id=?", (tree_selected_id,))
    conn.commit()

    # Обновление виджета Treeview после удаления
    update_treeview(tree)


# Функция поиска сотрудника по ФИО
def search_employee(name, tree):
    # Вывод всех сотрудников в виджете Treeview
    records = tree.get_children()
    for record in records:
        tree.delete(record)
    # Поиск сотрудника по ФИО
    cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
    data = cursor.fetchall()
    for row in data:
        tree.insert("", "end", values=row)


# Инициализация главного окна
window = tk.Tk()
window.title("Список сотрудников компании")

# Создаем Treeview с заголовками столбцов
treeview = ttk.Treeview(window, columns=("ID", "ФИО", "Телефон", "E-mail", "Зарплата"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("ФИО", text="ФИО")
treeview.heading("Телефон", text="Телефон")
treeview.heading("E-mail", text="E-mail")
treeview.heading("Зарплата", text="Зарплата")
treeview.column("ID", width=50)
treeview.column("ФИО", width=270)
treeview.column("Телефон", width=120)
treeview.column("Зарплата", width=130)
treeview.pack()

# Создаем контейнер для кнопок
button_frame = tk.Frame(window)
button_frame.pack()

# Создаем пустую рамку для создания расстояния
spacer_frame = tk.Frame(button_frame)
spacer_frame.pack(side="left")

# Создаем кнопку для добавления нового сотрудника
add_button = tk.Button(button_frame, text="Добавить сотрудника", command=lambda: insert_employee(treeview))
add_button.pack(side="left")

# Создаем пустую рамку для создания расстояния
spacer_frame2 = tk.Frame(button_frame, width=35)
spacer_frame2.pack(side="left")

# Создаем кнопку для изменения текущего сотрудника
edit_button = tk.Button(button_frame, text="Изменить сотрудника", command=lambda: insert_employee(treeview, True))
edit_button.pack(side="left")

# Создаем пустую рамку для создания расстояния
spacer_frame3 = tk.Frame(button_frame, width=35)
spacer_frame3.pack(side="left")

# Создаем кнопку для удаления сотрудника
delete_button = tk.Button(button_frame, text="Удалить сотрудника", command=lambda: delete_employee(treeview))
delete_button.pack(side="left")

# Создаем пустую рамку для создания расстояния
spacer_frame4 = tk.Frame(button_frame, width=35)
spacer_frame4.pack(side="left")

# Создаем поле ввода для поиска по ФИО
search_entry = tk.Entry(button_frame)
search_entry.pack(side="left")

# Создаем пустую рамку для создания расстояния
spacer_frame5 = tk.Frame(button_frame)
spacer_frame5.pack(side="left")

# Создаем кнопку для поиска по ФИО
search_button = tk.Button(button_frame, text="Найти", command=lambda: search_employee(search_entry.get(), treeview))
search_button.pack(side="left")

# Создаем пустую рамку для создания расстояния
spacer_frame6 = tk.Frame(button_frame, width=35)
spacer_frame6.pack(side="left")

# Создаем кнопку для поиска по ФИО
search_button = tk.Button(button_frame, text="Обновить", command=lambda: update_treeview(treeview))
search_button.pack(side="left")

# Обновление treeview и запуск окно
update_treeview(treeview)
window.mainloop()
