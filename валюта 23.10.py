from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests


currencies = {
    'EUR': 'Евро',
    'JPY': 'Японская йена',
    'GBP': 'Фунт стерлингов',
    'AUD': 'Австралийский доллар',
    'RUB': 'Российский рубль',
    'KZT': 'Казахстанский тенге',
    'UZS': 'Узбекский сум',
    'USD': 'Американский доллар'
}


def update_currency_label(event, combobox_widget, label_widget):
    """Обновляет текстовую метку при выборе валюты в комбобоксе"""
    code = combobox_widget.get()
    name = currencies.get(code, 'Неизвестная валюта')
    label_widget.config(text=name)


def exchange():
    """Запрашивает курсы для двух базовых валют относительно целевой"""
    base1 = combo_base1.get()
    base2 = combo_base2.get()
    target = combo_target.get()

    if not (base1 and base2 and target):
        mb.showwarning('Внимание', 'Выберите все валюты')
        return

    try:

        response1 = requests.get(f'https://open.er-api.com/v6/latest/{base1}')
        response1.raise_for_status()
        data1 = response1.json()


        response2 = requests.get(f'https://open.er-api.com/v6/latest/{base2}')
        response2.raise_for_status()
        data2 = response2.json()


        if target in data1['rates'] and target in data2['rates']:
            rate1 = data1['rates'][target]
            rate2 = data2['rates'][target]

            msg = (f"Курс обмена к {target}:\n"
                   f"1 {base1} = {rate1:.2f} {target}\n"
                   f"1 {base2} = {rate2:.2f} {target}")

            mb.showinfo('Курсы обмена', msg)
        else:
            mb.showerror('Ошибка', 'Валюта не найдена в ответе API')

    except Exception as e:
        mb.showerror('Ошибка', f'Не удалось получить данные: {e}')



root = Tk()
root.title('Курсы обмена валют')
root.geometry('350x450')


popular_currencies = list(currencies.keys())

# 1. Первая базовая валюта
Label(root, text='Базовая валюта', font=('Arial', 10, 'bold')).pack(pady=(10, 5))
combo_base1 = ttk.Combobox(root, values=popular_currencies, state='readonly')
combo_base1.set('EUR')  # Значение по умолчанию
combo_base1.pack(pady=5)
label_base1 = ttk.Label(root, text='Евро')
label_base1.pack()
combo_base1.bind('<<ComboboxSelected>>',
                 lambda e: update_currency_label(e, combo_base1, label_base1))

# 2. Вторая базовая валюта
Label(root, text='Вторая базовая валюта', font=('Arial', 10, 'bold')).pack(pady=(15, 5))
combo_base2 = ttk.Combobox(root, values=popular_currencies, state='readonly')
combo_base2.set('USD')  # Значение по умолчанию
combo_base2.pack(pady=5)
label_base2 = ttk.Label(root, text='Американский доллар')
label_base2.pack()
combo_base2.bind('<<ComboboxSelected>>',
                 lambda e: update_currency_label(e, combo_base2, label_base2))

# 3. Целевая валюта
Label(root, text='Целевая валюта', font=('Arial', 10, 'bold')).pack(pady=(15, 5))
combo_target = ttk.Combobox(root, values=popular_currencies, state='readonly')
combo_target.set('RUB')  # Значение по умолчанию
combo_target.pack(pady=5)
label_target = ttk.Label(root, text='Российский рубль')
label_target.pack()
combo_target.bind('<<ComboboxSelected>>',
                  lambda e: update_currency_label(e, combo_target, label_target))


Button(root, text='Получить курс обмена', command=exchange).pack(pady=30)

root.mainloop()