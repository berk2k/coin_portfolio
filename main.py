import tkinter as tk
from tkinter import ttk
import json


data_file = "portfolio_data.json"


def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'total': 0, 'coins': {}}

def save_data():
    data = {
        'total': float(entry_total.get()),
        'coins': coin_dict
    }
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)


def calculate_distribution():
    total = float(entry_total.get())
    result_text = ""
    

    for coin, amount in coin_dict.items():
        percentage = (amount / total) * 100
        result_text += f"{coin}: {percentage:.2f}%\n"
    
    result_label.config(text=result_text)


def add_coin():
    coin_name = entry_coin_name.get()
    coin_value = float(entry_coin_value.get())

    
    if coin_name and coin_value > 0:
        coin_dict[coin_name] = coin_value

        
        entry_coin_name.delete(0, tk.END)
        entry_coin_value.delete(0, tk.END)

        update_coin_list()
        calculate_distribution()
        save_data()


def update_coin_list():
    listbox_coins.delete(0, tk.END)
    for coin, value in coin_dict.items():
        listbox_coins.insert(tk.END, f"{coin}: ${value:.2f}")


def update_coin():
    try:
        selected_coin_index = listbox_coins.curselection()[0]
        selected_coin = listbox_coins.get(selected_coin_index).split(":")[0].strip()

        new_value = float(entry_coin_value.get())
        coin_dict[selected_coin] = new_value
        
        
        entry_coin_name.delete(0, tk.END)
        entry_coin_value.delete(0, tk.END)
        update_coin_list()
        calculate_distribution()
        save_data()
    except IndexError:
        result_label.config(text="Please select a coin to update.")


def delete_coin():
    try:
        selected_coin_index = listbox_coins.curselection()[0]
        selected_coin = listbox_coins.get(selected_coin_index).split(":")[0].strip()
        
        del coin_dict[selected_coin]
        
        
        update_coin_list()
        calculate_distribution()
        save_data()
    except IndexError:
        result_label.config(text="Please select a coin to delete.")


root = tk.Tk()
root.title("Crypto Portfolio Distribution")


data = load_data()
coin_dict = data['coins']
entry_total = ttk.Entry(root)
entry_total.insert(0, str(data['total']))  
entry_total.grid(row=0, column=1)
ttk.Label(root, text="Total Portfolio Value ($):").grid(row=0, column=0)


ttk.Label(root, text="Coin Name:").grid(row=1, column=0)
entry_coin_name = ttk.Entry(root)
entry_coin_name.grid(row=1, column=1)

ttk.Label(root, text="Coin Value ($):").grid(row=2, column=0)
entry_coin_value = ttk.Entry(root)
entry_coin_value.grid(row=2, column=1)


add_coin_btn = ttk.Button(root, text="Add Coin", command=add_coin)
add_coin_btn.grid(row=3, column=1)


update_coin_btn = ttk.Button(root, text="Update Coin", command=update_coin)
update_coin_btn.grid(row=4, column=1)


delete_coin_btn = ttk.Button(root, text="Delete Coin", command=delete_coin)
delete_coin_btn.grid(row=5, column=1)


listbox_coins = tk.Listbox(root, height=6, width=30)
listbox_coins.grid(row=6, column=0, columnspan=2)
update_coin_list()


calculate_btn = ttk.Button(root, text="Calculate", command=calculate_distribution)
calculate_btn.grid(row=7, column=1)


result_label = ttk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=2)


root.mainloop()
