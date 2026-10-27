import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi >= inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak dapat ditentukan"

def submit_nilai():
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def on_enter(e):
    btn_submit["bg"] = "#1E90FF"
    btn_submit["fg"] = "white"

def on_leave(e):
    btn_submit["bg"] = "#0000FF"
    btn_submit["fg"] = "white"

create_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas Siswa")
root.geometry("450x550")
root.config(bg="#f0f4f8")  

header_frame = tk.Frame(root, bg="#0056b3", pady=15)
header_frame.pack(fill="x")

title_label = tk.Label(header_frame, text="Prediksi Fakultas Siswa", font=("Arial", 16, "bold"), bg="#0056b3", fg="white")
title_label.pack()

main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
main_frame.pack(padx=25, pady=25, fill="both", expand=True)

def create_input_field(parent, label_text):
    lbl = tk.Label(parent, text=label_text, font=("Arial", 10, "bold"), bg="white", fg="#333333")
    lbl.pack(anchor="w", pady=(8, 2))
    ent = tk.Entry(parent, font=("Arial", 11), relief="solid", bd=1)
    ent.pack(fill="x", ipady=4)
    return ent

entry_nama = create_input_field(main_frame, "Nama Siswa:")
entry_bio = create_input_field(main_frame, "Nilai Biologi:")
entry_fis = create_input_field(main_frame, "Nilai Fisika:")
entry_ing = create_input_field(main_frame, "Nilai Bahasa Inggris:")

btn_submit = tk.Button(
    main_frame, 
    text="Submit & Simpan", 
    font=("Arial", 11, "bold"), 
    bg="#0056b3", 
    fg="white", 
    relief="flat", 
    cursor="hand2", 
    command=submit_nilai
)
btn_submit.pack(fill="x", pady=(25, 10), ipady=8)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()