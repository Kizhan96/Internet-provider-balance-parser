import requests
from bs4 import BeautifulSoup
url_r_line = \
    'https://state.r-line.ru:8443/bgbilling/webexecuter?action=GetBalance&mid=0&module=contract&contractId=172737'


def rline_parser(login, password):
    """
    Used to parse the data from the inet-provider site, especially users current balances.

    :param login: user's R-Line contract login.
    :param password: user's R-Line contract password.
    :return: Function returns str that contains user's current balance.
    """
    try:
        credentials = {'user': login, 'pswd': password}
        req = requests.get(url_r_line, credentials)
        soup = BeautifulSoup(req.text, "html.parser")
        balance = soup.select('.balanceList tbody tr:nth-last-child(2) td:last-child')[0].text
        return balance
    except IndexError:
        return 'Error'
