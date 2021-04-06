import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as tkmb
import math, random, time, json

class Japanese:
    def __init__(self):
        self.Hiragana = {
            # Hiragana Single
            "a":"あ","i":"い","u":"う","e":"え","o":"お",
            "ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
            "ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
            "sa":"さ","shi":"し","su":"す","se":"せ","so":"そ",
            "za":"ざ","ji":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
            "ta":"た","chi":"ち","tsu":"つ","te":"て","to":"と",
            "da":"だ","ji":"ぢ","zu":"づ","de":"で","do":"ど",
            "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
            "ha":"は","hi":"ひ","fu":"ふ","he":"へ","ho":"ほ",
            "ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
            "pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
            "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
            "ya":"や","yu":"ゆ","yo":"よ",
            "ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
            "wa":"わ","wo":"を","n":"ん"
        }

        self.HiraganaDouble = {
            # Hiragana Double
            "kya":"きゃ","kyu":"きゅ","kyo":"きょ",
            "sha":"しゃ","shu":"しゅ","sho":"しょ",
            "cha":"ちゃ","chu":"ちゅ","cho":"ちょ",
            "nya":"にゃ","nyu":"にゅ","nyo":"にょ",
            "hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ",
            "mya":"みゃ","myu":"みゅ","myo":"みょ",
            "rya":"りゃ","ryu":"りゅ","ryo":"りょ",
            "gya":"ぎゃ","gyu":"ぎゅ","gyo":"ぎょ",
            "ja":"じゃ","ju":"じゅ","jo":"じょ",
            "ja":"ぢゃ","ju":"ぢゅ","jo":"ぢょ",
            "bya":"びゃ","byu":"びゅ","byo":"びょ",
            "pya":"ぴゃ","pyu":"ぴゅ","pyo":"ぴょ"
        }

        self.Katakana = {
            # Katakana Single
            "!a":"ア","!i":"イ","!u":"ウ","!e":"エ","!o":"オ",
            "!ka":"カ","!ki":"キ","!ku":"ク","!ke":"ケ","!ko":"コ",
            "!ga":"ガ","!gi":"ギ","!gu":"グ","!ge":"ゲ","!go":"ゴ",
            "!sa":"サ","!shi":"シ","!su":"ス","!se":"セ","!so":"ソ",
            "!za":"ザ","!zi":"ジ","!zu":"ズ","!ze":"ゼ","!zo":"ゾ",
            "!ta":"タ","!chi":"チ","!tsu":"ツ","!te":"テ","!to":"ト",
            "!da":"ダ","!di":"ヂ","!du":"ヅ","!de":"デ","!do":"ド",
            "!na":"ナ","!ni":"ニ","!nu":"ヌ","!ne":"ネ","!no":"ノ",
            "!ha":"ハ","!hi":"ヒ","!fu":"フ","!he":"ヘ","!ho":"ホ",
            "!ba":"バ","!bi":"ビ","!bu":"ブ","!be":"ベ","!bo":"ボ",
            "!pa":"パ","!pi":"ピ","!pu":"プ","!pe":"ペ","!po":"ポ",
            "!ma":"マ","!mi":"ミ","!mu":"ム","!me":"メ","!mo":"モ",
            "!ya":"ヤ","!yu":"ユ","!yo":"ヨ",
            "!ra":"ラ","!ri":"リ","!ru":"ル","!re":"レ","!ro":"ロ",
            "!wa":"ワ","!wo":"ヲ","!n":"ン"
        }

        self.KatakanaDouble = {
            # Katakana Double
            "!kya":"キャ","!kyu":"キュ","!kyo":"キョ",
            "!sha":"シャ","!shu":"シュ","!sho":"ショ",
            "!cha":"チャ","!chu":"チュ","!cho":"チョ",
            "!nya":"ニャ","!nyu":"ニュ","!nyo":"ニョ",
            "!hya":"ヒャ","!hyu":"ヒュ","!hyo":"ヒョ",
            "!mya":"ミャ","!myu":"ミュ","!myo":"ミョ",
            "!rya":"リャ","!ryu":"リュ","!ryo":"リョ",
            "!gya":"ギャ","!gyu":"ギュ","!gyo":"ギョ",
            "!ja":"ジャ","!ju":"ジュ","!jo":"ジョ",
            "!ja":"ヂャ","!ju":"ヂュ","!jo":"ヂョ",
            "!bya":"ビャ","!byu":"ビュ","!byo":"ビョ",
            "!pya":"ピャ","!pyu":"ピュ","!pyo":"ピョ"
        }

Japanese = Japanese()



class Stylesheet:
    def __init__(self, style):
        if style == "light":
            self.WindowBackground = "#ffffff"
            self.WindowSubground = "#eeeeee"
            self.InputBorder = "#333333"
            self.Highlight = "#da3b01"
            self.Foreground = "#000000"

        if style == "dark":
            self.WindowBackground = "#000000"
            self.WindowSubground = "#333333"
            self.InputBorder = "#333333"
            self.Highlight = "#da3b01"
            self.Foreground = "#eeeeee"

class WindowSpacer:
    def __init__(self, master, size, stylesheet, side=tk.TOP):
        tk.Label(master, text = " ", font=("Nunito", 1), pady=math.floor(size/2), bg=stylesheet).pack(side=side)

class Window:
    def __init__(self, master, scheme):
        self.master = master
        self.Scheme = scheme
        self.testStarted = False
        self.cardsCorrect = 0
        self.cardsTested = 0
        self.percentage = 0
        self.setPacket = {}
        self.testedCorrect = []
        self.fetchValue = []
        self.outOf = 0
        self.mode = 0 # 0 = HS, 1 = HD, 2 = KS, 3 = KD, 4 = H, 5 = K, 6 = A
        self.cat = ""
        self.timerFirst = 0
        self.timerLast = 0

        self.scores = {}

        self.__loadscores__()
        self.__winconfig__()
        self.__widgets__()
        self.__widgetconfg__()
        self.__grid__()
        self.__func__()

    def __loadscores__(self):
        with open('scores.jap') as json_file:
            self.scores = json.load(json_file)

    def __widgets__(self):
        self.FlashcardFrame = tk.Frame(self.master)
        self.Flashcard = tk.Label(self.FlashcardFrame, text = "あ")
        self.AnswerInput = tk.Entry(self.FlashcardFrame)

        self.StatFrame = tk.Frame(self.master)
        self.ModeOptions = ttk.Combobox(self.StatFrame, values=["Hiragana Single", "Hiragana Double", "Katakana Single", "Katakana Double", "Hiragana", "Katakana", "All"])
        self.ModeOptions.current(6)
        self.FlashcardAnswer = tk.Label(self.StatFrame, text = "a")
        self.ScoresBox = tk.Listbox(self.StatFrame)
        for stat in self.scores['scores']:
            totaltext = stat['category'] + ": " + stat['score'] + " or " + stat['percentage'] + " in " + stat['time']
            self.ScoresBox.insert(tk.END, totaltext)

        self.Timer = tk.Label(self.StatFrame, text="0.00")
        self.LabelText = tk.Label(self.StatFrame, text = "score")
        self.PercentageCorrect = tk.Label(self.StatFrame, text = str(self.percentage) + "%")
        self.ScoreFraction = tk.Label(self.StatFrame, text = str(self.cardsCorrect) + "/" + str(self.cardsTested) + " (" + str(self.outOf) + ")")

    def __widgetconfg__(self):
        self.Flashcard.config(font=("Noto Sans JP", 128), justify=tk.CENTER, background=self.Scheme.WindowBackground, fg=self.Scheme.Foreground)
        self.AnswerInput.config(font=("Nunito", 10), justify=tk.CENTER, relief=tk.FLAT, highlightthickness=1, highlightbackground=self.Scheme.InputBorder, bg=self.Scheme.WindowBackground, fg=self.Scheme.Foreground, insertbackground=self.Scheme.Highlight)

        self.StatFrame.config(bg=self.Scheme.WindowSubground, padx=32, pady=8)
        self.ModeOptions.config(font=("Nunito", 10), justify=tk.CENTER, state="readonly")
        self.FlashcardAnswer.config(font=("Nunito ExtraBold", 48),fg=self.Scheme.Foreground,bg=self.Scheme.WindowSubground)
        self.ScoresBox.config(height=6, relief=tk.FLAT,bg=self.Scheme.WindowSubground,fg=self.Scheme.Foreground,highlightcolor=self.Scheme.Highlight,highlightbackground=self.Scheme.Highlight,selectbackground=self.Scheme.Highlight,font=("Nunito", 10),justify=tk.CENTER)
        self.Timer.config(font=("Nunito Italic", 24), justify=tk.CENTER, fg=self.Scheme.Highlight, height=1,bg=self.Scheme.WindowSubground)
        self.LabelText.config(font=("Nunito Bold", 16), justify=tk.CENTER, height=1,fg=self.Scheme.Foreground,bg=self.Scheme.WindowSubground)
        self.PercentageCorrect.config(font=("Nunito ExtraBold", 32), justify=tk.CENTER, height=1,fg=self.Scheme.Foreground,bg=self.Scheme.WindowSubground)
        self.ScoreFraction.config(font=("Nunito", 14), justify=tk.CENTER, fg=self.Scheme.Highlight, height=1,bg=self.Scheme.WindowSubground)

    def __grid__(self):
        self.FlashcardFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.AnswerInput.pack(side=tk.BOTTOM, fill=tk.X)
        self.Flashcard.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.StatFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)
        WindowSpacer(self.StatFrame, 10, self.Scheme.WindowSubground)
        self.ModeOptions.pack(fill=tk.X)
        self.FlashcardAnswer.pack()
        self.ScoresBox.pack(side=tk.BOTTOM,fill=tk.X)
        WindowSpacer(self.StatFrame, 20, self.Scheme.WindowSubground, side=tk.BOTTOM)
        self.ScoreFraction.pack(side=tk.BOTTOM)
        self.PercentageCorrect.pack(side=tk.BOTTOM)
        self.Timer.pack(side=tk.BOTTOM)
        self.LabelText.pack(side=tk.BOTTOM)


        # Text Spacer

    def __reset__(self):
        confirm = tkmb.askokcancel("Reset progress", "Are you sure you want to reset your score?")
        if confirm:
            self.cardsCorrect = 0
            self.cardsTested = 0
            self.testStarted = False
            self.percentage = 0
            self.setPacket = {}
            self.testedCorrect = []
            self.fetchValue = []
            self.outOf = 0


            tkmb.showwarning("Complete", "Flashcard score successfully reset.")
        if not confirm:
            return confirm

    def __generate__question__(self):
        if len(self.fetchValue) == len(self.testedCorrect):
            self.timerLast = time.perf_counter()
            seconds = round(self.timerLast-self.timerFirst)
            seconds = seconds % (24 * 3600)
            seconds %= 3600
            minutes = seconds // 60
            seconds %= 60
            timeFormatted = "%02d:%02d" % (minutes, seconds) #formatting
            message = "You finished a whole set of " + str(len(self.testedCorrect)) + " characters.\nYou finished with a score of " + str(self.percentage) + "% or " + str(self.cardsCorrect) + "/" + str(self.cardsTested) + " (" + str(self.outOf) + ")" + "\nAnd a time of " + timeFormatted + " \nYou answered " + str(self.cardsTested - len(self.fetchValue)) + " questions wrong.\nThe window will reset once you exit this dialog."

            self.scores['scores'].append({
                "category":self.cat,
                "score":str(self.cardsCorrect) + "/" + str(self.cardsTested),
                "percentage":str(self.percentage) + "%",
                "time":timeFormatted
            })

            with open("scores.jap", 'w') as savefile:
                json.dump(self.scores, savefile)

            self.ScoresBox.delete(0, tk.END)
            for stat in self.scores['scores']:
                totaltext = stat['category'] + ": " + stat['score'] + " or " + stat['percentage'] + " in " + stat['time']
                self.ScoresBox.insert(tk.END, totaltext)

            tkmb.showinfo("Congratulations!", message)
            self.__reset__()
            return 0

        q = random.randint(0,self.outOf-1) # Generate character
        for item in self.testedCorrect:
            if self.fetchValue[q] == item:
                self.__generate__question__()
                return 0
        self.cardsTested += 1
        self.Flashcard.config(text = self.setPacket[self.fetchValue[q]])
        self.FlashcardAnswer.config(text = self.fetchValue[q].replace("!",""))
        self.rawCorrectAnswer = self.fetchValue[q]
        self.correctAnswer = self.fetchValue[q].replace("!","")

        #print("Cards out of: " + str(self.cardsTested))


    def __event__check__(self):
        if self.testStarted:
            wrong = 0
            if self.FlashcardAnswer['fg'] == self.Scheme.Foreground:
                self.FlashcardAnswer.config(fg=self.Scheme.WindowSubground)
                wrong = 1

            #print(wrong)
            #print("Your input", self.AnswerInput.get().strip())

            if self.AnswerInput.get().strip() == self.correctAnswer and not wrong:
                self.cardsCorrect += 1
                self.testedCorrect.append(self.rawCorrectAnswer)
                self.AnswerInput.config(highlightthickness=1, highlightbackground="#43a047", highlightcolor="#43a047")

                #print("Cards correct: " + str(self.cardsCorrect))
                #print("CORRECT -->")
                #print(self.testedCorrect)

            if self.AnswerInput.get().strip() != self.correctAnswer or wrong:
                self.AnswerInput.config(highlightthickness=1, highlightbackground="#ff1744", highlightcolor="#ff1744")

            self.percentage = round((self.cardsCorrect / self.cardsTested)*100, 1)
            self.PercentageCorrect.config(text = str(self.percentage) + "%")
            self.ScoreFraction.config(text = str(self.cardsCorrect) + "/" + str(self.cardsTested) + " (" + str(self.outOf) + ")")

            self.__generate__question__()

        if not self.testStarted:
            # Hide answer
            self.FlashcardAnswer.config(fg=self.Scheme.WindowSubground)

            # Display Info
            self.testStarted = True
            tkmb.showinfo("Information", "Flashcard testing started.\nInput the answer and press [ENTER] to begin.\nPress [F1] to reset.\n*You cannot change mode during play.")

            # Create testing dictionary
            self.mode = self.ModeOptions.current()
            self.setPacker = {}
            if self.mode == 0:
                self.setPacket = Japanese.Hiragana
                self.cat = "Hiragana Single"
            if self.mode == 1:
                self.setPacket = Japanese.HiraganaDouble
                self.cat = "Hiragana Double"
            if self.mode == 2:
                self.setPacket = Japanese.Katakana
                self.cat = "Katakana Single"
            if self.mode == 3:
                self.setPacket = Japanese.KatakanaDouble
                self.cat = "Katakana Double"
            if self.mode == 4:
                self.setPacket = {**Japanese.Hiragana, **Japanese.HiraganaDouble}
                self.cat = "Hiragana*"
            if self.mode == 5:
                self.setPacket = {**Japanese.Katakana, **Japanese.KatakanaDouble}
                self.cat = "Katakana*"
            if self.mode == 6:
                self.setPacket = {**Japanese.Hiragana, **Japanese.HiraganaDouble, **Japanese.Katakana, **Japanese.KatakanaDouble}
                self.cat = "All"

            # Initialize scores
            self.outOf = len(self.setPacket)
            self.ScoreFraction.config(text = str(self.cardsCorrect) + "/" + str(self.cardsTested) + " (" + str(self.outOf) + ")")

            # Create fetching list (for dict)
            self.fetchValue.clear()
            for pro in self.setPacket:
                self.fetchValue.append(pro)

            # First question and start timer
            self.timerFirst = time.perf_counter()
            self.__generate__question__()

        self.AnswerInput.delete(0, 'end')

    def __toggle__answer__(self): ############ DEAL WITH THIS
        self.FlashcardAnswer.config(fg=self.Scheme.Foreground)

    def __upd__timer__(self):
        seconds = round(self.timerLast-self.timerFirst)
        seconds = seconds % (24 * 3600)
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        timeFormatted = "%02d:%02d" % (minutes, seconds) #formatting
        self.timerLast = time.perf_counter()
        self.Timer.config(text=timeFormatted)

    def __delete__score__(self):
        self.scores['scores'].pop(self.ScoresBox.curselection()[0])

        with open("scores.jap", 'w') as savefile:
            json.dump(self.scores, savefile)

        self.ScoresBox.delete(0, tk.END)
        for stat in self.scores['scores']:
            totaltext = stat['category'] + ": " + stat['score'] + " or " + stat['percentage'] + " in " + stat['time']
            self.ScoresBox.insert(tk.END, totaltext)


    def __func__(self):
        self.master.bind("<Return>", lambda e: self.__event__check__())
        self.master.bind("<F1>", lambda e: self.__reset__())
        self.master.bind("<space>", lambda e: self.__toggle__answer__())
        self.master.bind("<Key>", lambda e: self.__upd__timer__())

        self.ScoresBox.bind("<Delete>", lambda e: self.__delete__score__())


    def __winconfig__(self):
        self.master.title("Japanese Practice")
        self.master.geometry("900x600")
        self.master.iconphoto(False, tk.PhotoImage(file="windowicon.png"))
        self.master.config(bg=self.Scheme.WindowSubground)

##### SELECT THEME

#theme = "light"

optionWindow = tk.Tk()
optionWindow.title("Start-up")
optionWindow.iconphoto(False, tk.PhotoImage(file="windowicon.png"))
optionWindow.geometry("400x70")
optionWindow.resizable(0,0)

listbox = tk.Listbox(optionWindow, justify=tk.CENTER, height=2, relief=tk.FLAT,selectmode=tk.SINGLE)
button = tk.Button(optionWindow, justify=tk.CENTER, relief=tk.FLAT, bd=0, bg="#da3b01", fg="#eee", text="Select", command=lambda:updateTheme(listbox.curselection()))
listbox.pack(fill=tk.BOTH, expand=1)
button.pack(fill=tk.BOTH, expand=1)

def updateTheme(s):
    global listbox, theme
    if s[0] == 1: theme = "dark"
    elif s[0] == 0: theme = "light"
    optionWindow.destroy()



for item in ["Light","Dark"]:
    listbox.insert(tk.END, item)

optionWindow.mainloop()



root = tk.Tk()
stylesheet = Stylesheet(theme)
window = Window(root, stylesheet)
window.master.mainloop()
