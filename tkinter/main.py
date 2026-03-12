import tkinter as tk
from PIL import Image, ImageTk
TEXT = {

    "ru": {
        "title": "МЕТРО: Тени выбора",
        "start": "Начать игру",
        "exit": "Выход",
        "language": "Выберите язык",

        "chapter": "Глава",
        "part": "Часть",
        "health": "Здоровье",
        "bullets": "Патроны",
        "filters": "Фильтры",
        "allies": "Союзники",

        "intro1": "МЕТРО: ТЕНИ ВЫБОРА",
        "intro2": "Без оценок. Без подсказок. Только твои решения."
    },

    "en": {
        "title": "METRO: Shadows of Choice",
        "start": "Start Game",
        "exit": "Exit",
        "language": "Choose language",

        "chapter": "Chapter",
        "part": "Part",
        "health": "Health",
        "bullets": "Bullets",
        "filters": "Filters",
        "allies": "Allies",

        "intro1": "METRO: SHADOWS OF CHOICE",
        "intro2": "No hints. No scores. Only your choices."
    }
}

class Player:
    def __init__(self):
        self.name = "Artyom"
        self.health = 100
        self.bullets = 120
        self.filters = 180
        self.part = 1
        self.chapter = 1
        self.allies = []
        self.has_heart = False

class MainMenu:

    def __init__(self, root):

        self.root = root
        self.lang = "ru"

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        img = Image.open("metro_menu.png")

        img = img.resize((750, 400))

        self.photo = ImageTk.PhotoImage(img)

        self.image_label = tk.Label(self.frame, image=self.photo)
        self.image_label.pack()

        self.title = tk.Label(
            self.frame,
            font=("Arial", 22, "bold")
        )

        self.title.pack(pady=10)

        self.lang_label = tk.Label(self.frame)
        self.lang_label.pack()

        lang_frame = tk.Frame(self.frame)
        lang_frame.pack(pady=5)

        tk.Button(
            lang_frame,
            text="Русский",
            width=12,
            command=lambda: self.set_lang("ru")
        ).pack(side="left", padx=5)

        tk.Button(
            lang_frame,
            text="English",
            width=12,
            command=lambda: self.set_lang("en")
        ).pack(side="left", padx=5)

        self.start_btn = tk.Button(
            self.frame,
            width=20,
            command=self.start_game
        )

        self.start_btn.pack(pady=5)

        self.exit_btn = tk.Button(
            self.frame,
            width=20,
            command=root.quit
        )

        self.exit_btn.pack()

        self.update_text()

    def set_lang(self, lang):

        self.lang = lang
        self.update_text()

    def update_text(self):

        t = TEXT[self.lang]

        self.title.config(text=t["title"])
        self.lang_label.config(text=t["language"])
        self.start_btn.config(text=t["start"])
        self.exit_btn.config(text=t["exit"])

    def start_game(self):
        self.frame.destroy()
        MetroGame(self.root, self.lang)

class MetroGame:
    def __init__(self, root, lang):
        self.root = root
        self.lang = lang
        self.t = TEXT[lang]

        self.player = Player()

        self.status = tk.Label(root, font=("Arial", 12), justify="left")
        self.status.pack(anchor="w", padx=10)

        self.text = tk.Text(root, height=18, wrap="word", state="disabled")
        self.text.pack(fill="both", expand=True, padx=10)

        self.buttons = tk.Frame(root)
        self.buttons.pack(pady=10)

        self.update_status()

        self.start()

    def write(self, text):
        self.text.config(state="normal")
        self.text.insert("end", text + "\n\n")
        self.text.config(state="disabled")
        self.text.see("end")

    def clear_buttons(self):
        for w in self.buttons.winfo_children():
            w.destroy()

    def choice(self, question, options):
        self.write(question)
        self.clear_buttons()

        for text, func in options:
            tk.Button(self.buttons,
                      text=text,
                      width=40,
                      command=func).pack(pady=3)

    def update_status(self):
        p = self.player
        status = (
            f"{self.t['part']} {p.part}/7   {self.t['chapter']} {p.chapter}/17\n"
            f"{self.t['health']}: {p.health}%   {self.t['bullets']}: {p.bullets}\n"
            f"{self.t['filters']}: {p.filters//60}h   {self.t['allies']}: {len(p.allies)}"
        )

        self.status.config(text=status)

    def damage(self, amount):
        self.player.health -= amount
        if self.player.health <= 0:
            self.player.health = 0
            self.game_over()

    def spend_bullets(self, amount):
        if self.player.bullets >= amount:
            self.player.bullets -= amount
            return True
        return False

    def spend_filters(self, amount):
        if self.player.filters >= amount:
            self.player.filters -= amount
            return True
        return False

    def start(self):
        self.write(self.t["intro1"])
        self.write(self.t["intro2"])
        self.ch1()

    def ch1(self):
        self.player.chapter = 1
        self.update_status()
        self.choice("Обычное утро на ВДНХ. Что делаешь?", [
            ("Помочь починить генератор", self.ch2),
            ("Сказать что занят", self.ch2),
            ("Поговорить о странных снах", self.ch2)
        ])

    def ch2(self):
        self.player.chapter = 2
        self.update_status()
        self.choice("В туннеле слышится крик.", [
            ("Бежать на помощь", self.ch2_a),
            ("Спрятаться", self.ch3),
            ("Подождать", self.ch2_b)
        ])

    def ch2_a(self):
        self.damage(12)
        self.ch3()

    def ch2_b(self):
        self.player.bullets += 15
        self.ch3()

    def ch3(self):
        self.player.chapter = 3
        self.player.part = 2
        self.update_status()
        self.choice("Пора уходить.", [
            ("Взять припасы", self.ch3_a),
            ("Оставить патроны", self.ch4)
        ])

    def ch3_a(self):
        self.player.bullets += 40
        self.ch4()

    def ch4(self):
        self.player.chapter = 4
        self.update_status()
        self.choice("Рижская. Рейдеры требуют плату.", [
            ("Отдать патроны", self.ch4_a),
            ("Прорваться", self.ch4_b),
            ("Обход", self.ch5)
        ])

    def ch4_a(self):
        self.spend_bullets(60)
        self.ch5()

    def ch4_b(self):
        self.damage(25)
        self.ch5()

    def ch5(self):
        self.player.chapter = 5
        self.update_status()
        self.choice("Алексеевская заброшена.", [
            ("Пройти тихо", self.ch6),
            ("Осмотреть", self.ch5_a),
            ("Ловушка", self.ch6)
        ])

    def ch5_a(self):
        self.damage(18)
        self.player.allies.append("survivor")
        self.ch6()

    def ch6(self):
        self.player.chapter = 6
        self.update_status()
        self.choice("Проспект Мира.", [
            ("Купить фильтры", self.ch6_a),
            ("Поговорить", self.ch7),
            ("Уйти", self.ch7)
        ])

    def ch6_a(self):
        if self.spend_bullets(45):
            self.player.filters += 90
        self.ch7()

    def ch7(self):
        self.player.chapter = 7
        self.player.part = 3
        self.update_status()
        self.choice("Тургеневская — лабиринт.", [
            ("Основной туннель", self.ch7_a),
            ("Обход", self.ch8),
            ("Осторожно", self.ch8)
        ])

    def ch7_a(self):
        self.damage(15)
        self.ch8()

    def ch8(self):
        self.player.chapter = 8
        self.update_status()
        self.choice("Китай-город.", [
            ("Договориться", self.ch8_a),
            ("Пройти молча", self.ch9)
        ])

    def ch8_a(self):
        if self.player.health > 40:
            self.player.allies.append("trader")
        self.ch9()

    def ch9(self):
        self.player.chapter = 9
        self.update_status()
        self.choice("Театральная.", [
            ("Поддержать сторону", self.ch9_a),
            ("Нейтралитет", self.ch10)
        ])

    def ch9_a(self):
        self.player.allies.append("fighter")
        self.ch10()

    def ch10(self):
        self.player.chapter = 10
        self.player.part = 4
        self.update_status()
        self.choice("Ворота Полиса.", [
            ("Заплатить", self.ch10_a),
            ("Прорваться", self.ch10_b)
        ])

    def ch10_a(self):
        self.spend_bullets(70)
        self.ch11()

    def ch10_b(self):
        self.damage(30)
        self.ch11()

    def ch11(self):
        self.player.chapter = 11
        self.update_status()
        self.choice("Библиотека.", [
            ("Искать артефакт", self.ch11_a),
            ("Уйти", self.ch12)
        ])

    def ch11_a(self):
        if self.player.health > 30:
            self.player.has_heart = True
        self.ch12()

    def ch12(self):
        self.player.chapter = 12
        self.player.part = 5
        self.update_status()
        self.choice("Поверхность.", [
            ("Использовать противогаз", self.ch12_a),
            ("Бежать", self.ch13)
        ])

    def ch12_a(self):
        self.spend_filters(70)
        self.ch13()

    def ch13(self):
        self.player.chapter = 13
        self.update_status()
        self.choice("Ботанический сад.", [
            ("С боем", self.ch13_a),
            ("Обойти", self.ch14)
        ])

    def ch13_a(self):
        self.spend_bullets(40)
        self.ch14()

    def ch14(self):
        self.player.chapter = 14
        self.player.part = 6
        self.update_status()
        self.choice("ВДНХ в беде.", [
            ("Спасать станцию", self.ch14_a),
            ("Идти к цели", self.ch15)
        ])

    def ch14_a(self):
        self.damage(35)
        self.ch15()

    def ch15(self):
        self.player.chapter = 15
        self.update_status()
        self.choice("Последние приготовления.", [
            ("Взять союзников", self.ch16),
            ("Идти одному", self.ch16)
        ])

    def ch16(self):
        self.player.chapter = 16
        self.player.part = 7
        self.update_status()
        self.choice("Сердце тьмы.", [
            ("Использовать артефакт", self.end),
            ("Сражаться", self.end)
        ])

    def end(self):
        self.player.chapter = 17
        self.update_status()
        self.show_ending()

    def show_ending(self):
        self.clear_buttons()
        p = self.player
        if p.has_heart and p.health > 20 and len(p.allies) >= 2:
            txt = "КОНЕЦ: Странный свет в темноте"
        elif p.has_heart:
            txt = "КОНЕЦ: Цена надежды"
        elif p.health > 40 and len(p.allies) >= 3:
            txt = "КОНЕЦ: Последний патруль"
        elif p.health <= 0:
            txt = "КОНЕЦ: Тишина"
        else:
            txt = "КОНЕЦ: Неизвестность"
        self.write(txt)
        tk.Button(self.buttons,
                  text=self.t["exit"],
                  command=self.root.quit).pack()

    def game_over(self):
        self.clear_buttons()
        self.write("Ты погиб.")
        tk.Button(self.buttons,
                  text=self.t["exit"],
                  command=self.root.quit).pack()


root = tk.Tk()
root.geometry("750x550")
MainMenu(root)
root.mainloop()