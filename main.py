import datetime
import glob
import os
import sqlite3
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb

import board
import game


class Main:
    def __init__(self):
        self.self_turn = False
        self.give_up = False

        self.color_list = {1: "黒", -1: "白"}
        self.level_list = {1: "レベル1", 2: "レベル2"}
        self.result_list = {0: "勝ち", 1: "負け", 2: "引き分け"}

        # メインウィンドウ
        self.window = tk.Tk()
        self.window.geometry("1000x650+200+0")
        self.window.resizable(False, False)
        self.window.title("Reversi")

        # スタイルの設定
        style = ttk.Style()

        # 対局履歴のスタイル
        style.configure(
            "Custom.Treeview",
            background="white",
            foreground="black",
            rowheight=25,
            fieldbackground="white",
            font=("游明朝", 14),
        )
        style.map("Custom.Treeview", background=[("selected", "lightgray")], foreground=[("selected", "black")])

        # buttonのスタイル
        style.configure("Custom.TButton", background="white", foreground="black", font=("游明朝", 14))

        # labelのスタイル
        style.configure("Custom.TLabel", foreground="black", font=("游明朝", 14))

        # labelframeのスタイル
        style.configure("Custom.TLabelframe", borderwidth=5, relief="ridge")
        style.configure("Custom.TLabelframe.Label", font=("游明朝", 14, "bold"))

        # radiobuttonのスタイル
        style.configure("Custom.TRadiobutton", foreground="black", font=("游明朝", 14))

        # リバーシ盤
        self.b = board.Board()
        self.g = None
        self.main_frame = tk.Frame(self.window, width=600, height=600, padx=25, pady=50)
        self.b_picture = tk.Canvas(self.main_frame, width=self.b.b_size, height=self.b.b_size)
        self.b.drawBoard(self.b_picture)
        self.b_picture.bind("<Button-1>", self.playerMove)

        # 対局履歴
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=(
                "date",
                "time",
                "stone_color",
                "enemy_level",
                "black_count",
                "white_count",
                "result",
            ),
            show="headings",
            height=20,
            style="Custom.Treeview",
        )

        self.tree.column("date", width=120)
        self.tree.column("time", width=100)
        self.tree.column("stone_color", width=75)
        self.tree.column("enemy_level", width=100)
        self.tree.column("black_count", width=75)
        self.tree.column("white_count", width=75)
        self.tree.column("result", width=75)

        self.tree.heading("date", text="日付")
        self.tree.heading("time", text="時刻")
        self.tree.heading("stone_color", text="自分の石")
        self.tree.heading("enemy_level", text="相手の強さ")
        self.tree.heading("black_count", text="黒の数")
        self.tree.heading("white_count", text="白の数")
        self.tree.heading("result", text="勝敗")

        # 対局履歴のスクロールバー
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # スタートメニュー
        self.start_menu = ttk.Frame(self.window, width=400, height=600)

        self.game_options = ttk.Labelframe(self.start_menu, text="対局設定", style="Custom.TLabelframe")
        self.choose_color = ttk.Labelframe(
            self.game_options, text="石の色(先手/後手)を選択して下さい", style="Custom.TLabelframe"
        )
        self.stone_color = tk.IntVar()
        self.radio_black = ttk.Radiobutton(
            self.choose_color, text="黒(先手)", value=1, variable=self.stone_color, style="Custom.TRadiobutton"
        )
        self.radio_white = ttk.Radiobutton(
            self.choose_color, text="白(後手)", value=-1, variable=self.stone_color, style="Custom.TRadiobutton"
        )

        self.choose_level = ttk.Labelframe(
            self.game_options, text="相手の強さを選択して下さい", style="Custom.TLabelframe"
        )
        self.enemy_level = tk.IntVar()
        self.radio_level1 = ttk.Radiobutton(
            self.choose_level, text="レベル1", value=1, variable=self.enemy_level, style="Custom.TRadiobutton"
        )
        self.radio_level2 = ttk.Radiobutton(
            self.choose_level, text="レベル2", value=2, variable=self.enemy_level, style="Custom.TRadiobutton"
        )

        self.start_button = ttk.Button(
            self.game_options,
            text="対局開始",
            command=lambda: self.start(self.stone_color.get(), self.enemy_level.get()),
            style="Custom.TButton",
        )
        self.log_button = ttk.Button(self.start_menu, text="対局履歴", command=self.showLog, style="Custom.TButton")

        self.quit_button = ttk.Button(self.start_menu, text="終了", command=self.quitApp, style="Custom.TButton")

        # 対局中メニュー
        self.game_menu = ttk.Frame(self.window, width=400, height=600)

        self.turn = ttk.Labelframe(self.game_menu, text="現在の手番", style="Custom.TLabelframe")
        self.turn_texts = ("貴方の番です", "相手の番です", "パスします")
        self.turn_text = tk.StringVar()
        self.current_turn = ttk.Label(self.turn, textvariable=self.turn_text, style="Custom.TLabel")

        self.count_frame = ttk.Labelframe(self.game_menu, text="石の数", style="Custom.TLabelframe")
        self.stone_count = tk.StringVar()
        self.display_stone = ttk.Label(self.count_frame, textvariable=self.stone_count, style="Custom.TLabel")

        self.giveup_button = ttk.Button(self.game_menu, text="投了", command=self.confirmGiveUp, style="Custom.TButton")

        # 対局結果メニュー
        self.result_menu = ttk.Frame(self.window, width=400, height=600)

        self.final_count_frame = ttk.Labelframe(self.result_menu, text="石の数", style="Custom.TLabelframe")
        self.final_count = ttk.Label(self.final_count_frame, textvariable=self.stone_count, style="Custom.TLabel")

        self.result_texts = ("貴方の勝ち", "貴方の負け", "引き分け")
        self.result_text = tk.StringVar()
        self.result_display = ttk.Label(self.result_menu, textvariable=self.result_text, style="Custom.TLabel")
        self.replay_button = ttk.Button(self.result_menu, text="もう1局", command=self.replay, style="Custom.TButton")
        self.back_button = ttk.Button(
            self.result_menu, text="始めに戻る", command=self.backMenu, style="Custom.TButton"
        )

        # 対局履歴メニュー
        self.log_menu = ttk.Frame(self.window, width=400, height=600)

        self.select_date_frame = ttk.Labelframe(self.log_menu, text="日付検索", style="Custom.TLabelframe")
        self.select_date = ttk.Combobox(self.select_date_frame, state="readonly")
        self.select_date.bind("<<ComboboxSelected>>", self.searchLog)
        self.delete_button = ttk.Button(self.log_menu, text="削除", command=self.confirmDelete, style="Custom.TButton")
        self.back_button2 = ttk.Button(self.log_menu, text="始めに戻る", command=self.backMenu, style="Custom.TButton")

        # 盤の配置
        self.main_frame.grid(row=0, column=0)

        self.switchMain(self.b_picture, self.tree)

        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # メニュー画面の配置
        self.switchMenu(self.start_menu, self.game_menu, self.result_menu, self.log_menu)

        # スタートメニューの配置
        self.game_options.grid(row=0, column=0, pady=15)
        self.log_button.grid(row=1, column=0, pady=15)
        self.quit_button.grid(row=2, column=0, pady=15)

        self.choose_color.grid(row=0, column=0, pady=15)
        self.choose_level.grid(row=1, column=0, pady=15)
        self.start_button.grid(row=2, column=0, pady=15)

        self.radio_black.grid(row=0, column=0, pady=15)
        self.radio_white.grid(row=0, column=1, pady=15)

        self.radio_level1.grid(row=0, column=0, pady=15)
        self.radio_level2.grid(row=0, column=1, pady=15)

        # 対局中メニューの配置
        self.turn.grid(row=0, column=0, pady=15)
        self.count_frame.grid(row=1, column=0, pady=15)
        self.giveup_button.grid(row=2, column=0, pady=15)

        self.current_turn.grid(row=0, column=0, pady=15)

        self.display_stone.grid(row=0, column=0, pady=15)

        # 対局結果メニューの配置
        self.final_count_frame.grid(row=0, column=0, pady=15)
        self.result_display.grid(row=1, column=0, pady=15)
        self.replay_button.grid(row=2, column=0, pady=15)
        self.back_button.grid(row=3, column=0, pady=15)

        self.final_count.grid(row=0, column=0, pady=15)

        self.select_date_frame.grid(row=0, column=0, pady=15)
        self.delete_button.grid(row=1, column=0, pady=15)
        self.back_button2.grid(row=2, column=0, pady=15)

        self.select_date.grid(row=0, column=0, pady=15)

    def start(self, sc, el):
        """
        対局開始
        """
        if sc == 0 or el == 0:
            mb.showwarning("必須項目未選択", "必要な項目を選択して下さい")
        else:
            self.g = game.Game(sc, el)

            self.b.resetStones()
            self.b.drawStones(self.b_picture)
            self.stone_count.set(f"黒:{self.b.black_count} 白:{self.b.white_count}")

            self.switchMain(self.b_picture, self.tree)
            self.switchMenu(self.game_menu, self.start_menu, self.result_menu, self.log_menu)

            if self.g.checkSquares(self.b):
                match sc:
                    case 1:
                        self.self_turn = True
                        self.turn_text.set(self.turn_texts[0])
                    case -1:
                        self.turn_text.set(self.turn_texts[1])
                        threading.Thread(target=self.delayedEnemyMove).start()
            else:
                self.passMessage()

    def switchMain(self, raise_main, forget_main, scroll=False):
        """
        盤と対局履歴の切り替え
        """
        raise_main.grid(row=0, column=0, sticky="nsew")
        forget_main.grid_forget()

        if scroll:
            self.scrollbar.grid(row=0, column=1, sticky="ns")
        else:
            self.scrollbar.grid_forget()

    def switchMenu(self, raise_menu, forget_menu1, forget_menu2, forget_menu3):
        """
        メニューの切り替え
        """
        raise_menu.grid(row=0, column=1, padx=50)
        forget_menu1.grid_forget()
        forget_menu2.grid_forget()
        forget_menu3.grid_forget()

    def playerMove(self, event):
        """
        プレイヤーの着手
        """
        if self.g != None:
            if self.self_turn:
                if self.g.current_turn == self.g.player_stone:
                    x = event.x
                    y = event.y

                    is_ok = self.g.checkMove(x, y, self.b)
                    if is_ok:
                        self.g.reverseStones(self.b)
                        self.b.drawStones(self.b_picture)
                        self.self_turn = False
                        self.changeTurn()

    def delayedEnemyMove(self):
        self.window.after(1000, self.enemyMove)

    def enemyMove(self):
        """
        相手(コンピュータ)の着手
        """
        match self.g.enemy_level:
            case 1:
                self.g.level1Move()
            case 2:
                self.g.level2Move()

        self.g.reverseStones(self.b)
        self.b.drawStones(self.b_picture)
        self.changeTurn()

    def passMessage(self):
        """
        打てるマスが無い場合にメッセージを表示
        """
        self.turn_text.set(self.turn_texts[2])
        self.g.pass_count += 1

        if self.g.pass_count == 2:
            mb.showinfo("終局", "互いに打てるマスが無くなりました。終了します。")
            self.endGame()
        else:
            threading.Thread(target=self.delayedChangeTurn).start()

    def delayedChangeTurn(self):
        self.window.after(1000, self.changeTurn)

    def changeTurn(self):
        """
        手番の交代
        """
        self.stone_count.set(f"黒:{self.b.black_count} 白:{self.b.white_count}")

        if self.g.pass_count == 0:
            self.g.turn_count += 1
        self.g.current_turn *= -1

        if self.g.turn_count == 60:
            mb.showinfo("終局", "終了です。")
            self.endGame()
        elif self.b.black_count == 0 or self.b.white_count == 0:
            mb.showinfo("終局", "片方の数が0になりました。終了します。")
            self.endGame()
        else:
            if self.g.checkSquares(self.b):
                match self.g.current_turn:
                    case self.g.player_stone:
                        self.self_turn = True
                        self.turn_text.set(self.turn_texts[0])
                    case self.g.enemy_stone:
                        self.self_turn = False
                        self.turn_text.set(self.turn_texts[1])
                        threading.Thread(target=self.delayedEnemyMove).start()
            else:
                self.passMessage()

    def confirmGiveUp(self):
        """
        投了確認
        """
        answer = mb.askokcancel("確認", "投了しますか?")

        if answer:
            self.give_up = True
            self.endGame()

    def endGame(self):
        """
        勝敗判定と結果の記録
        """
        self.self_turn = False
        result_number = self.g.judge(self.b.black_count, self.b.white_count, self.b.black, self.b.white, self.give_up)

        match result_number:
            case 0:
                self.result_text.set(self.result_texts[result_number])
            case 1:
                self.result_text.set(self.result_texts[result_number])
            case 2:
                self.result_text.set(self.result_texts[result_number])

        self.saveResult(result_number)
        self.switchMenu(self.result_menu, self.start_menu, self.game_menu, self.log_menu)

        self.give_up = False

    def saveResult(self, result_number):
        """
        対局結果の記録
        """
        cur = self.openLog()
        current_datetime = datetime.datetime.now()
        today = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M:%S")

        cur.execute(
            "insert into reversi_log values(?,?,?,?,?,?,?)",
            (
                today,
                current_time,
                self.color_list[self.stone_color.get()],
                self.level_list[self.enemy_level.get()],
                self.b.black_count,
                self.b.white_count,
                self.result_list[result_number],
            ),
        )

        self.log.commit()
        self.log.close()

    def replay(self):
        """
        再対局するか確認
        """
        answer = mb.askokcancel("確認", "同じ設定でもう1局打ちますか?")

        if answer:
            self.switchMenu(self.game_menu, self.start_menu, self.result_menu, self.log_menu)
            self.start(self.stone_color.get(), self.enemy_level.get())

    def backMenu(self):
        """
        スタートメニューに戻る
        """
        answer = mb.askokcancel("確認", "メニュー画面に戻りますか?")

        if answer:
            for i in self.tree.get_children():
                self.tree.delete(i)

            self.switchMain(self.b_picture, self.tree)
            self.switchMenu(self.start_menu, self.game_menu, self.result_menu, self.log_menu)

    def openLog(self):
        """
        データベースを開く
        """
        directory = glob.glob("game_log")
        if directory:
            pass
        else:
            os.mkdir("game_log")

        self.log = sqlite3.connect("game_log/game_log.db")
        cur = self.log.cursor()
        cur.execute('SELECT COUNT(*) FROM sqlite_master WHERE TYPE="table" AND NAME="reversi_log"')

        if cur.fetchone() == (0,):
            cur.execute(
                "create table reversi_log(date date,time time,stone_color nchar(2),enemy_level nchar(7),black_count integer,white_count integer,result nvarchar(4,8))"
            )

        return cur

    def showLog(self):
        """
        対局履歴を表示
        """
        cur = self.openLog()
        self.loadLog(cur)
        self.switchMain(self.tree, self.b_picture, True)
        self.switchMenu(self.log_menu, self.start_menu, self.game_menu, self.result_menu)
        self.log.close()

    def loadLog(self, cur):
        """
        データベースから対局履歴を読み込み
        """
        cur.execute("select * from reversi_log")

        rows = cur.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

        dates = set()
        for row in self.tree.get_children():
            item = self.tree.item(row)
            date = item["values"][0]
            dates.add(date)

        self.select_date["values"] = sorted(list(dates))

    def searchLog(self, event):
        """
        対局履歴を日付検索
        """
        selected_date = self.select_date.get()
        cur = self.openLog()
        cur.execute("select * from reversi_log where date=?", (selected_date,))
        rows = cur.fetchall()

        for i in self.tree.get_children():
            self.tree.delete(i)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

        self.log.close()

    def confirmDelete(self):
        """
        対局履歴を削除するか確認
        """
        answer = mb.askokcancel("確認", "表示中の対局履歴を削除しますか?")

        if answer:
            self.deleteSelectedLog()

    def deleteSelectedLog(self):
        """
        表示中の対局履歴を削除
        """
        selected_date = self.select_date.get()
        cur = self.openLog()

        if selected_date == "":
            cur.execute("delete from reversi_log")
        else:
            cur.execute("delete from reversi_log where date=?", (selected_date,))

        for i in self.tree.get_children():
            self.tree.delete(i)

        self.log.commit()

        self.log.close()

    def quitApp(self):
        """
        アプリの終了
        """
        answer = mb.askokcancel("確認", "終了しますか?")

        if answer:
            self.window.destroy()


if __name__ == "__main__":
    main = Main()

    main.window.mainloop()
