from tkinter import Tk, Label, Menu, Scrollbar, Canvas, Frame, messagebox, Toplevel
from tkinter.ttk import Progressbar
from ellco_balance_parser import ellco_parser
from rline_balance_parser import rline_parser
from pandas import read_csv
import threading
import csv
import datetime
import os


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


def create_invoice(provider):
    """
    Used to create an invoice csv file, that contains the login and the amount of money to transfer.
    It calculates the amount of money that needs to be transferred to the account so that the balance allows you to
    use the Internet for 2 full months.
    """
    current_date = datetime.date.today()

    if provider == 1:
        if os.path.exists('invoice/Rline_' + str(current_date) + '.csv'):
            os.remove('invoice/Rline_' + str(current_date) + '.csv')
        for row in range(1, return_row_num('data/internet.csv')):
            if read_from_csv(4, row) == '1':
                try:
                    invoice = [read_from_csv(2, row), int((float(read_from_csv(6, row)) - float(rline_parser(read_from_csv(2, row), read_from_csv(3, row)))) + float(read_from_csv(6, row)))]
                    if invoice[1] > 0:
                        write_row_to_csv('invoice/Rline_' + str(current_date) + '.csv', invoice)
                except ValueError:
                    write_row_to_csv('invoice/Rline_' + str(current_date) + '.csv', [read_from_csv(2, row), 'Error'])
        messagebox.showinfo('Status', 'Invoice created, and written to a file: \n' + 'invoice/Rline_' + str(current_date) + '.csv')

    if provider == 2:
        if os.path.exists('invoice/Ellco_' + str(current_date) + '.csv'):
            os.remove('invoice/Ellco_' + str(current_date) + '.csv')
        for row in range(1, return_row_num('data/internet.csv')):
            if read_from_csv(4, row) == '2':
                try:
                    invoice = [read_from_csv(2, row), int((float(read_from_csv(6, row)) - float(ellco_parser(read_from_csv(2, row), read_from_csv(3, row)))) + float(read_from_csv(6, row)))]
                    if invoice[1] > 0:
                        write_row_to_csv('invoice/Ellco_' + str(current_date) + '.csv', invoice)
                except ValueError:
                    write_row_to_csv('invoice/Ellco_' + str(current_date) + '.csv', [read_from_csv(2, row), 'Error'])
        messagebox.showinfo('Status', 'Invoice created, and written to a file: \n' + 'invoice/Ellco_' + str(current_date) + '.csv')

    if provider == 3:
        if os.path.exists('invoice/KASPNet_' + str(current_date) + '.csv'):
            os.remove('invoice/KASPNet_' + str(current_date) + '.csv')
        for row in range(1, return_row_num('data/internet.csv')):
            if read_from_csv(4, row) == '3':
                try:
                    invoice = [read_from_csv(2, row), int((float(read_from_csv(6, row)) - float(rline_parser(read_from_csv(2, row), read_from_csv(3, row)))) + float(read_from_csv(6, row)))]
                    if invoice[1] > 0:
                        write_row_to_csv('invoice/KASPNet_' + str(current_date) + '.csv', invoice)
                except ValueError:
                    write_row_to_csv('invoice/KASPNet_' + str(current_date) + '.csv', [read_from_csv(2, row), 'Error'])
        messagebox.showinfo('Status', 'Invoice created, and written to a file: \n' + 'invoice/KASPNet_' + str(current_date) + '.csv')

    if provider == 4:
        messagebox.showinfo('Status', 'Parser for this provider is not ready yet')


class Main(Tk):

    def __init__(self):

        super().__init__()
        self.loading_window = Toplevel(self)
        self.progress = Progressbar(self.loading_window, orient="horizontal", mode="indeterminate", maximum=100,
                                    value=0)

        self.ws = self.winfo_screenwidth()  # width of the screen
        self.hs = self.winfo_screenheight()  # height of the screen
        w = 750  # width for the window
        h = 805  # height for the window
        # calculate x and y coordinates for the window
        x = (self.ws / 2) - (w / 2)
        y = (self.hs / 2) - (h / 2)

        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Labels lists initialisation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        self.Address_lb = []
        self.Login_lb = []
        self.Password_lb = []
        self.Balance_lb = []
        self.Tariff_lb = []
        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Labels lists initialisation~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.title('Balance')
        self.canvas = Canvas(self, borderwidth=0)
        self.frame = Frame(self.canvas)
        self.vsb = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.iconbitmap('assets/icon.ico')

        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Scroll bar configuring start~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)
        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Scroll bar configuring finish~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

        self.menu_config()
        self.table_header()

    def table_header(self):
        """ Function to create table header in main window.

        """
        Label(self.frame, text='Address', borderwidth=1, relief='solid', width=50, anchor='w').grid(row=0, column=0)
        Label(self.frame, text='Login', borderwidth=1, relief='solid', width=20, anchor='w').grid(row=0, column=1)
        Label(self.frame, text='Password', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=2)
        Label(self.frame, text='Balance', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=3)
        Label(self.frame, text='Tariff', borderwidth=1, relief='solid', width=10, anchor='w').grid(row=0, column=4)

    def menu_config(self):
        """ Main window menu configuration function

        """
        self.menu = Menu(self)

        self.file_menu = Menu(self.menu, tearoff=0)
        self.file_menu.add_command(label="Show R-line balances", command=lambda: self.grid_up(1))
        self.file_menu.add_command(label="Show Ellco balances", command=lambda: self.grid_up(2))
        self.file_menu.add_command(label="Show Kaspnet balances", command=lambda: self.grid_up(3))
        self.file_menu.add_command(label="Show Паутина05 balances", command=lambda: self.grid_up(4))
        self.file_menu.add_separator()  # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.action_menu = Menu(self.menu, tearoff=0)
        self.action_menu.add_command(label='Create Rline invoice', command=lambda: create_invoice(1))
        self.action_menu.add_command(label='Create Ellco invoice', command=lambda: create_invoice(2))
        self.action_menu.add_command(label='Create KASPNet invoice', command=lambda: create_invoice(3))
        self.action_menu.add_command(label='Create Паутина05 invoice', command=lambda: create_invoice(4))

        self.menu.add_cascade(label="Balances", menu=self.file_menu)
        self.menu.add_cascade(label="Actions", menu=self.action_menu)
        self.config(menu=self.menu)

    def filler(self):
        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~START filling lists with data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
        for row in range(1, return_row_num('data/internet.csv')):
            if row == return_row_num('data/internet.csv') - 1:
                self.loading_window.destroy()
            self.Address_lb.append(Label(self.frame,
                                         text=read_from_csv(1, row),
                                         borderwidth=1, relief='solid', width=50, anchor='w'))  # Address
            self.Login_lb.append(Label(self.frame,
                                       text=read_from_csv(2, row),
                                       borderwidth=1, relief='solid', width=20, anchor='w'))  # Login
            self.Password_lb.append(Label(self.frame,
                                          text=read_from_csv(3, row),
                                          borderwidth=1, relief='solid', width=10, anchor='w'))  # Password

            """~~~~~~~~~~~~~~~~~~~~~~~~~~START filling balance list with data from parsers~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
            if read_from_csv(4, row) == '1':
                self.Balance_lb.append(Label(self.frame,
                                             text=rline_parser(read_from_csv(2, row), read_from_csv(3, row)),
                                             borderwidth=1, relief='solid', width=10, anchor='w'))
            elif read_from_csv(4, row) == '2':
                self.Balance_lb.append(Label(self.frame,
                                             text=ellco_parser(read_from_csv(2, row), read_from_csv(3, row)),
                                             borderwidth=1, relief='solid', width=10, anchor='w'))
            elif read_from_csv(4, row) == '3':
                self.Balance_lb.append(Label(self.frame,
                                             text='404', borderwidth=1, relief='solid', width=10, anchor='w'))
            elif read_from_csv(4, row) == '4':
                self.Balance_lb.append(Label(self.frame, text='404',
                                             borderwidth=1, relief='solid', width=10, anchor='w'))
            else:
                self.Balance_lb.append(Label(self.frame, text='404',
                                             borderwidth=1, relief='solid', width=10, anchor='w'))
            """~~~~~~~~~~~~~~~~~~~~~~~~~~FINISH filling balance list with data from parsers~~~~~~~~~~~~~~~~~~~~~~~~~~"""

            self.Tariff_lb.append(Label(self.frame, text=read_from_csv(6, row), borderwidth=1, relief='solid', width=10,
                                        anchor='w'))  # Tariff
        """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FINISH filling lists with data~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""

    def top_level(self):
        self.loading_window.overrideredirect(True)
        Label(self.loading_window, text='Loading data').pack()
        self.loading_window.geometry('%dx%d+%d+%d' % (100, 42, (self.ws / 2) - 100 / 2, (self.hs / 2)))
        self.loading_window.grab_set()
        self.progress.start(10)
        self.progress.pack()

    def grid_down(self):
        """Function for hiding all the labels from main window canvas
        """
        for row in range(0, len(self.Address_lb)):
            self.Address_lb[row].grid_forget()
            self.Login_lb[row].grid_forget()
            self.Password_lb[row].grid_forget()
            self.Balance_lb[row].grid_forget()
            self.Tariff_lb[row].grid_forget()

    def grid_up(self, provider):
        """Function for showing up only certain provider labels.

        :param int provider:
            A parameter that contains an integer to determine the provider. (1 - for the R-line provider, 2 - for the
            Ellco provider, 3 - for the KASPNet provider, 4 - for the Паутина05 provider).
        """
        self.grid_down()
        for row in range(0, len(self.Address_lb)):
            if read_from_csv(4, row + 1) == str(provider):
                if float(self.Balance_lb[row].cget('text')) < 300:
                    self.Address_lb[row].grid(row=row + 1, column=0, sticky='w')
                    self.Login_lb[row].grid(row=row + 1, column=1, sticky='w')
                    self.Password_lb[row].grid(row=row + 1, column=2, sticky='w')
                    self.Balance_lb[row].config(bg='red')
                    self.Balance_lb[row].grid(row=row + 1, column=3, sticky='w')
                    self.Tariff_lb[row].grid(row=row + 1, column=4, sticky='w')
                elif 300 < float(self.Balance_lb[row].cget('text')) < 600:
                    self.Address_lb[row].grid(row=row + 1, column=0, sticky='w')
                    self.Login_lb[row].grid(row=row + 1, column=1, sticky='w')
                    self.Password_lb[row].grid(row=row + 1, column=2, sticky='w')
                    self.Balance_lb[row].config(bg='yellow')
                    self.Balance_lb[row].grid(row=row + 1, column=3, sticky='w')
                    self.Tariff_lb[row].grid(row=row + 1, column=4, sticky='w')
                elif float(self.Balance_lb[row].cget('text')) > 600:
                    self.Address_lb[row].grid(row=row + 1, column=0, sticky='w')
                    self.Login_lb[row].grid(row=row + 1, column=1, sticky='w')
                    self.Password_lb[row].grid(row=row + 1, column=2, sticky='w')
                    self.Balance_lb[row].config(bg='green')
                    self.Balance_lb[row].grid(row=row + 1, column=3, sticky='w')
                    self.Tariff_lb[row].grid(row=row + 1, column=4, sticky='w')
                else:
                    self.Address_lb[row].grid(row=row + 1, column=0, sticky='w')
                    self.Login_lb[row].grid(row=row + 1, column=1, sticky='w')
                    self.Password_lb[row].grid(row=row + 1, column=2, sticky='w')
                    self.Balance_lb[row].config(bg='blue')
                    self.Balance_lb[row].grid(row=row + 1, column=3, sticky='w')
                    self.Tariff_lb[row].grid(row=row + 1, column=4, sticky='w')

    def on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = Main()

    t1 = threading.Thread(target=root.filler)
    t2 = threading.Thread(target=root.top_level)
    t1.start()
    t2.start()

    root.mainloop()
