import numpy as np
import os

def load_color_ranges():
    color_ranges = {}
    colors = {'red', 'yellow', 'blue'}
    for color in colors:
        try:
            lower = np.load(os.path.join('saved_colors', f'{color}_lower.npy'))
            upper = np.load(os.path.join('saved_colors', f'{color}_upper.npy'))
            color_ranges[color] = (lower, upper)
        except FileNotFoundError:
            print(f"Files for {color} not found")
    return color_ranges

class Color:
    def __init__(self, low=None, hi=None):
        self.low = low
        self.hi = hi

class Client:
    def __init__(self, name, color, shape, balance):
        self.name = name
        self.color = color
        self.shape = shape
        self.balance = balance

    def define_name(self):
        self.name = input("Masukkan nama anda : ")

    def define_color(self):
        color_ranges = load_color_ranges()
        pilihan = {
            1: "red",
            2: "yellow",
            3: "blue"
        }
        pilih = int(input("Silahkan pilih warna untuk mendaftar :\n1. Merah\n2. Kuning\n3. Biru\nPilih : "))
        selected_color = pilihan.get(pilih, None)
        if selected_color and selected_color in color_ranges:
            self.color.low, self.color.hi = color_ranges[selected_color]
            print(f"Warna berhasil disimpan")
        else:
            print("Pilihan salah!")

    def define_shape(self):
        shapes = ['segitiga', 'persegi', 'persegi panjang', 'lingkaran']
        ulang = True
        while(ulang):
            pilih = int(input("Silahkan pilih shape untuk mendaftar :\n1. segitiga\n2. persegi\n3. persegi panjang\n4. lingkaran\nPilih : "))
            if pilih in {1, 2, 3, 4}:
                self.shape = shapes[pilih - 1]
                ulang = False
            else:
                print("Pilihan salah! coba lagi!")

        print("Shape berhasil disimpan!")

    def cek_saldo(self):
        print(f"Saldo untuk pengguna {self.name} adalah : Rp{self.balance}")

    def deposit(self):
        money = int(input("Masukkan uang yang ingin didepositkan : "))
        self.balance += money
        print(f"Saldo berhasil ditambahkan! Sekarang, saldo ada Rp{self.balance}")

    def tarik_tunai(self):
        money = int(input("Masukkan uang yang ingin ditarik : "))
        if money > self.balance:
            print("Maaf, dana tidak mencukupi!\nKembali ke menu utama...")
        else:
            self.balance -= money
            print(f"Saldo berhasil ditarik! Sekarang, saldo ada Rp{self.balance}")

    def update_info(self):
        self.name = input("Masukkan nama baru : ")
        self.define_color()
        self.define_shape()
        self.balance = int(input("Masukkan saldo baru : "))
        print("Informasi berhasil diperbarui!")

def login_user(users):
    name = input("Masukkan nama anda : ")
    if name in users:
        print(f"Login berhasil! Selamat datang, {name}.")
        users[name].cek_saldo()
        action = input("Pilih tindakan: deposit, tarik, update_info, atau cek_saldo: ").strip().lower()
        if action == "deposit":
            users[name].deposit()
        elif action == "tarik":
            users[name].tarik_tunai()
        elif action == "update_info":
            users[name].update_info()
        elif action == "cek_saldo":
            users[name].cek_saldo()
        else:
            print("Tindakan tidak dikenal.")
    else:
        print("Nama tidak ditemukan. Silahkan mendaftar.")

def main():
    users = {}

    while True:
        pilihan = int(input("1. Mendaftar\n2. Login\n3. Keluar\nPilih: "))
        if pilihan == 1:
            name = input("Masukkan nama anda : ")
            if name in users:
                print("Nama sudah terdaftar. Silahkan login.")
                continue

            color_instance = Color()
            client_instance = Client(name, color_instance, "", 0)
            client_instance.define_color()
            client_instance.define_shape()
            users[name] = client_instance
            print(f"Registrasi berhasil untuk {name}!")
        elif pilihan == 2:
            login_user(users)
        elif pilihan == 3:
            break
        else:
            print("Pilihan salah! coba lagi!")

if __name__ == "__main__":
    main()
