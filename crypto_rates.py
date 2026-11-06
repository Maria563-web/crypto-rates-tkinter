from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

# Список популярных криптовалют (id для CoinGecko)
CRYPTO = {
    'bitcoin': 'Bitcoin (BTC)',
    'ethereum': 'Ethereum (ETH)',
    'tether': 'Tether (USDT)',
    'binancecoin': 'BNB',
    'solana': 'Solana (SOL)',
    'ripple': 'XRP',
    'cardano': 'Cardano (ADA)',
    'dogecoin': 'Dogecoin (DOGE)'
}


def fetch_prices():
    """Запрашивает курсы выбранных криптовалют к USD через CoinGecko."""
    ids = ','.join(CRYPTO.keys())
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd'

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        mb.showerror('Ошибка', f'Не удалось получить данные: {e}')
        return

    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)

    # Заполняем данными
    for coin_id, name in CRYPTO.items():
        if coin_id in data and 'usd' in data[coin_id]:
            price = data[coin_id]['usd']
            tree.insert('', 'end', values=(name, f'${price:,.2f}'))
        else:
            tree.insert('', 'end', values=(name, 'Н/Д'))


# --- Интерфейс ---
root = Tk()
root.title('Курсы криптовалют к USD')
root.geometry('420x380')
root.resizable(False, False)

Label(root, text='Криптовалюты к доллару США',
      font=('Arial', 12, 'bold')).pack(pady=(15, 5))
Label(root, text='Источник: CoinGecko API',
      font=('Arial', 8), fg='gray').pack()

frame = Frame(root)
frame.pack(pady=10, padx=20, fill='both', expand=True)

tree = ttk.Treeview(frame, columns=('name', 'price'),
                    show='headings', height=8)
tree.heading('name', text='Монета')
tree.heading('price', text='Цена (USD)')
tree.column('name', width=200, anchor='w')
tree.column('price', width=150, anchor='e')

scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

Button(root, text='Обновить курсы', command=fetch_prices,
       font=('Arial', 10), width=20).pack(pady=(5, 15))

# Автозагрузка курсов при старте
fetch_prices()

root.mainloop()
