from bs4 import BeautifulSoup
from pandas import read_csv
from tkinter import Tk, Label, Menu, Scrollbar, Canvas, Frame, messagebox
import requests
import csv
import datetime
import os
r_line_url =\
    "https://state.r-line.ru:8443/bgbilling/webexecuter?action=GetBalance&mid=0&module=contract&contractId=172737"


def write_row_to_csv(path, w_list):
    """
    Used to write a row to csv file

    :param path: the path to the file to which the sheet will be written in
    :param w_list: the list of data to write
    """
    with open(path, mode="a", encoding='utf-8') as w_file:
        # Создаем объект writer, указываем символ-разделитель ";"
        file_writer = csv.writer(w_file, delimiter="\t", lineterminator="\r")
        # Записываем строку в CSV файл
        file_writer.writerow(w_list)


def get_balance(login, password):
    """
    Used to parse the data from the inet-provider site, especially users current balances.

    :param login: user's R-Line contract login.
    :param password: user's R-Line contract password.
    :return: Function returns str that contains user's current balance.
    """
    try:
        credentials = {'user': login, 'pswd': password}
        req = requests.get(r_line_url, credentials)
        soup = BeautifulSoup(req.text, "html.parser")
        balance = soup.select('.balanceList tbody tr:nth-last-child(2) td:last-child')[0].text
        return balance
    except IndexError:
        return 'Error'


def return_row_num(path_to_csv):
    """
    Used to retrieve the total amount of rows in csv file.

    :param path_to_csv: path to a csv file.
    :return: Amount of rows in the file.
    """
    file = open(path_to_csv, encoding='utf-8')
    return len(file.readlines())


def read_from_csv(col, row):
    """
    Used to retrieve data from exact row and column in csv file.

    :param col: column number.
    :param row: row number.
    :return: Returns the data from csv, using rows and column numbers as an indexes.
    """
    out = read_csv('data/internet.csv', sep=';', header=None, comment='#')
    return out[col][row]


def create_invoice():
    """
    Used to create an invoice csv file, that contains the login and the amount of money to transfer.
    It calculates the amount of money that needs to be transferred to the account so that the balance allows you to
    use the Internet for 2 full months.
    """
    now = datetime.date.today()
    if os.path.exists('invoice/' + str(now) + '.csv'):
        os.remove('invoice/' + str(now) + '.csv')
    try:
        for row in range(1, return_row_num('data/internet.csv')):
            invoice = [read_from_csv(2, row), int((float(read_from_csv(6, row)) - float(
                get_balance(read_from_csv(2, row), read_from_csv(3, row)))) + float(read_from_csv(6, row)))]
            if invoice[1] > 0:
                write_row_to_csv('invoice/' + str(now) + '.csv', invoice)
        messagebox.showinfo('Status', 'Invoice created, and written to a file: \n' + 'invoice/' + str(now) + '.csv')
    except ValueError:
        write_row_to_csv('invoice/' + str(now) + '.csv', ['Error', 'Error'])


class Main(Tk):

    def __init__(self):
        super().__init__()
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        w = 750  # width for the window
        h = 805  # height for the window
        # calculate x and y coordinates for the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title('Balance')
        self.canvas = Canvas(self, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.iconbitmap('assets/icon.ico')

        """Menu configuring start"""
        self.menu = Menu(self)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Create an invoice", command=lambda: create_invoice())
        self.file_menu.add_separator()

        self.menu.add_cascade(label="Actions", menu=self.file_menu)
        self.config(menu=self.menu)
        """Menu configuring finish"""

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)
        self.populate()

        Label(self.frame, text='Address', borderwidth=1, relief='solid', width=50, anchor='w').grid(row=0, column=0)
        Label(self.frame, text='Login', borderwidth=1, relief='solid', width=20, anchor='w').grid(row=0, column=1)
        Label(self.frame, text='Password', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=2)
        Label(self.frame, text='Balance', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=3)
        Label(self.frame, text='Tariff', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=4)

    def populate(self):
        """Fill the table with data"""
        for row in range(1, return_row_num('data/internet.csv')):
            Label(self.frame, text=read_from_csv(1, row), borderwidth=1, relief='solid', width=50, anchor='w').grid(
                row=row, column=0, sticky='w')  # Address
            Label(self.frame, text=read_from_csv(2, row), borderwidth=1, relief='solid', width=20, anchor='w').grid(
                # Login
                row=row, column=1)
            Label(self.frame, text=read_from_csv(3, row), borderwidth=1, relief='solid', width=10, anchor='w').grid(
                # Password
                row=row, column=2)
            Label(self.frame, text=(get_balance(read_from_csv(2, row), read_from_csv(3, row))), borderwidth=1,
                  # Balance
                  relief='solid', width=10, anchor='w').grid(row=row, column=3)
            Label(self.frame, text=read_from_csv(6, row), borderwidth=1, relief='solid', width=10, anchor='w').grid(
                # Tariff
                row=row, column=4)

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = Main()
    root.mainloop()
