import numpy as np
import os
import pickle

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
        money = int(input("Masukkan uang yang ingin didepositkan : "));

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print("Data berhasil disimpan!")

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

# User Management System
def load_users(filename):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return {}

def save_users(users, filename):
    with open(filename, 'wb') as file:
        pickle.dump(users, file)
    print("Users data berhasil disimpan!")

def register_user(users, filename):
    name = input("Masukkan nama anda : ")
    if name in users:
        print("Nama sudah terdaftar. Silahkan login.")
        return

    color_instance = Color()
    client_instance = Client(name, color_instance, "", 0)
    client_instance.define_color()
    client_instance.define_shape()
    client_instance.balance = int(input("Masukkan saldo awal : "))
    users[name] = client_instance
    save_users(users, filename)
    print(f"Registrasi berhasil untuk {name}!")

def login_user(users):
    name = input("Masukkan nama anda : ")
    if name in users:
        print(f"Login berhasil! Selamat datang, {name}.")
        users[name].cek_saldo()
    else:
        print("Nama tidak ditemukan. Silahkan mendaftar.")
        

# Main function
def main():
    users_file = 'users_data.bin'  # Changed the extension to .bin
    users = load_users(users_file)

    while True:
        pilihan = int(input("1. Mendaftar\n2. Login\n3. Keluar\nPilih: "))
        if pilihan == 1:
            register_user(users, users_file)
        elif pilihan == 2:
            login_user(users)
        elif pilihan == 3:
            break
        else:
            print("Pilihan salah! coba lagi!")

if __name__ == "__main__":
    main()
