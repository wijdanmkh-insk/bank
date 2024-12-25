import numpy as np
import os
import cv2

def load_color_ranges():
    colors = {'red', 'yellow', 'blue'}
    color_ranges = {}
    for color in colors:
        try:
            lower = np.load(os.path.join('saved_colors', f'{color}_lower.npy'))
            upper = np.load(os.path.join('saved_colors', f'{color}_upper.npy'))
            color_ranges[color] = (lower, upper)
            print(f"{color.capitalize()} range loaded: lower={lower}, upper={upper}")
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
            print(f"Warna {selected_color.capitalize()} berhasil disimpan dengan rentang: lower={self.color.low}, upper={self.color.hi}")
        else:
            print("Pilihan salah!")

    def define_shape(self):
        shapes = ['segitiga', 'persegi', 'persegi panjang', 'lingkaran']
        ulang = True
        while ulang:
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

    def detect_shapes_and_colors(self, frame, users):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        contour = frame.copy()
        blur = cv2.GaussianBlur(frame, (7,7),1)
        canny = cv2.Canny(blur, 50,70)

        for user in users.values():
            mask = cv2.inRange(hsv, user.color.low, user.color.hi)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 300:
                    peri = cv2.arcLength(cnt, True)
                    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
                    corner = len(approx)

                    x, y, w, h = cv2.boundingRect(approx)
                    shape = 'lainnya'
                    if corner == 3:
                        shape = 'segitiga'
                    elif corner == 4:
                        ratio = w / float(h)
                        if ratio >= 0.95 and ratio <= 1.05:
                            shape = 'persegi'
                        else:
                            shape = 'persegi panjang'
                    else:
                        (x_circle, y_circle), radius = cv2.minEnclosingCircle(cnt)
                        circularity = area / (np.pi * radius * radius)
                        if 0.85 <= circularity <= 1.15:
                            shape = 'lingkaran'
                        else:
                            shape = 'lainnya'

                    if shape == user.shape:
                        print(f"Detected color: {list(users.keys())[list(users.values()).index(user)]}, Shape: {shape}")
                        menu(user)

        return hsv, canny

    def start_video(self, users):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Gagal membuka kamera.")
                break

            hsv, canny = self.detect_shapes_and_colors(frame, users)

            cv2.imshow('Original Frame', frame)
            cv2.imshow('HSV Frame', hsv)
            cv2.imshow('Canny Frame', canny)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

def login(users):
    if users:
        client = next(iter(users.values()))
        client.start_video(users)
    else:
        print("Tidak ada pengguna terdaftar. Silahkan mendaftar terlebih dahulu.")

def menu(client):
    print(f"Selamat datang, {client.name}")
    ulang = True

    while ulang:
        pilih = int(input("Menu tersedia :\n1. Lihat saldo\n2. Deposit\n3. Tarik saldo\nPilih : "))
        if pilih == 1:
            client.cek_saldo()
        elif pilih == 2:
            client.deposit()
        elif pilih == 3:
            client.tarik_tunai()
        else:
            print("Pilihan salah! coba lagi.")

def daftar(users):
    name = input("Masukkan nama anda : ")

    if name in users:
        print("Nama sudah terdaftar. Silahkan login.")
        return

    color_instance = Color()
    client_instance = Client(name, color_instance, "", 0)
    client_instance.define_color()
    client_instance.define_shape()
    users[name] = client_instance
    print(f"Registrasi berhasil untuk {name}!")

def main():
    users = {}

    while True:
        pilihan = int(input("1. Mendaftar\n2. Login\n3. Keluar\nPilih: "))
        if pilihan == 1:
            daftar(users)
        elif pilihan == 2:
            login(users)
        elif pilihan == 3:
            break
        else:
            print("Pilihan salah! coba lagi.")

if __name__ == "__main__":
    main()
