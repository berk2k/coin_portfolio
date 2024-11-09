import tkinter as tk
from tkinter import ttk
import json



# Dosya yolu
data_file = "portfolio_data.json"

# JSON dosyasını okuma ve veriyi geri yükleme fonksiyonu
def load_data():
    try:
        with open(data_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'total': 0, 'coins': {}}

# Dosyaya kaydetme fonksiyonu
def save_data():
    data = {
        'total': float(entry_total.get()),
        'coins': coin_dict
    }
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

# Yüzdelik hesaplama ve UI'yi güncelleme
def calculate_distribution():
    total = float(entry_total.get())
    
    # Yüzde hesaplama
    for item in treeview_coins.get_children():
        treeview_coins.delete(item)
    
    for coin, amount in coin_dict.items():
        percentage = (amount / total) * 100
        treeview_coins.insert('', 'end', values=(coin, f"${amount:.2f}", f"{percentage:.2f}%"))
    
    save_data()

# Yeni coin ekleme
def add_coin():
    coin_name = entry_coin_name.get()
    coin_value = float(entry_coin_value.get())

    # Coin ekleme işlemi
    if coin_name and coin_value > 0:
        coin_dict[coin_name] = coin_value

        # Entry temizleme
        entry_coin_name.delete(0, tk.END)
        entry_coin_value.delete(0, tk.END)

        calculate_distribution()

# Coin güncelleme
def update_coin():
    try:
        selected_coin_index = treeview_coins.selection()[0]
        selected_coin_name = treeview_coins.item(selected_coin_index)['values'][0]

        new_value = float(entry_coin_value.get())
        coin_dict[selected_coin_name] = new_value
        
        # Güncelleme işleminden sonra
        entry_coin_name.delete(0, tk.END)
        entry_coin_value.delete(0, tk.END)
        calculate_distribution()
    except IndexError:
        result_label.config(text="Please select a coin to update.")

# Coin silme
def delete_coin():
    try:
        selected_coin_index = treeview_coins.selection()[0]
        selected_coin_name = treeview_coins.item(selected_coin_index)['values'][0]
        
        del coin_dict[selected_coin_name]
        
        # Silme işleminden sonra
        calculate_distribution()
    except IndexError:
        result_label.config(text="Please select a coin to delete.")

# UI setup
root = tk.Tk()
root.title("Crypto Portfolio Distribution")
root.configure(bg="#f0f0f0")  # Arka plan rengini açık gri yapıyoruz

# Veriyi yükle
data = load_data()
coin_dict = data['coins']
entry_total = ttk.Entry(root, width=20, font=("Arial", 14))
entry_total.insert(0, str(data['total']))  # Toplam değerini yükle
entry_total.grid(row=0, column=1, pady=10)
ttk.Label(root, text="Total Portfolio Value ($):", font=("Arial", 12), background="#f0f0f0").grid(row=0, column=0)

# Yeni coin eklemek için entry alanları
ttk.Label(root, text="Coin Name:", font=("Arial", 12), background="#f0f0f0").grid(row=1, column=0, pady=5)
entry_coin_name = ttk.Entry(root, width=20, font=("Arial", 14))
entry_coin_name.grid(row=1, column=1, pady=5)

ttk.Label(root, text="Coin Value ($):", font=("Arial", 12), background="#f0f0f0").grid(row=2, column=0, pady=5)
entry_coin_value = ttk.Entry(root, width=20, font=("Arial", 14))
entry_coin_value.grid(row=2, column=1, pady=5)

# Coin ekleme butonu
add_coin_btn = ttk.Button(root, text="Add Coin", command=add_coin, width=20, style="TButton")
add_coin_btn.grid(row=3, column=1, pady=10)

# Coin güncelleme butonu
update_coin_btn = ttk.Button(root, text="Update Coin", command=update_coin, width=20, style="TButton")
update_coin_btn.grid(row=4, column=1, pady=10)

# Coin silme butonu
delete_coin_btn = ttk.Button(root, text="Delete Coin", command=delete_coin, width=20, style="TButton")
delete_coin_btn.grid(row=5, column=1, pady=10)

# Coin listesi (Treeview kullanarak tablo oluşturuyoruz)
treeview_coins = ttk.Treeview(root, columns=("Coin", "Value", "Percentage"), show="headings", height=6)
treeview_coins.grid(row=6, column=0, columnspan=2, pady=10)

# Tablo başlıkları
treeview_coins.heading("Coin", text="Coin Name")
treeview_coins.heading("Value", text="Coin Value ($)")
treeview_coins.heading("Percentage", text="Percentage")

# Yüzde hesaplama butonu
calculate_btn = ttk.Button(root, text="Calculate", command=calculate_distribution, width=20, style="TButton")
calculate_btn.grid(row=7, column=1, pady=10)

# Yüzdelik dağılımı gösteren label
result_label = ttk.Label(root, text="", font=("Arial", 14), background="#f0f0f0", anchor="w")
result_label.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

# Button style customization
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6, relief="flat", background="#4CAF50", foreground="white")
style.map("TButton", background=[('active', '#45a049')])

# Verileri güncelleme
calculate_distribution()

# Start the UI loop
root.mainloop()
