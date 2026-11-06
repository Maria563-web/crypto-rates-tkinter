from tkinter import *
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

    response = requests.get(url)
    data = response.json()

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

Label(root, text='Криптовалюты к доллару США',
      font=('Arial', 12, 'bold')).pack(pady=15)

tree = ttk.Treeview(root, columns=('name', 'price'), show='headings')
tree.heading('name', text='Монета')
tree.heading('price', text='Цена (USD)')
tree.column('name', width=200, anchor='w')
tree.column('price', width=150, anchor='e')
tree.pack(pady=10)

Button(root, text='Обновить курсы', command=fetch_prices).pack(pady=10)

root.mainloop()
