from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
ellco_url = 'https://bill.ellcom.ru/my/index.xhtml'


def ellco_parser(login, password):
    """Used to parse the data from the inet-provider site, especially users current balances.

    :param login: user's Ellco contract login.
    :param password: user's Ellco contract password.
    :return: Function returns str that contains user's current balance.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    driver.get(ellco_url)
    driver.set_page_load_timeout(45)
    driver.implicitly_wait(2)

    s_username = driver.find_element_by_name("loginForm:username:input")
    s_password = driver.find_element_by_name('loginForm:password:input')
    s_continue = driver.find_element_by_name('loginForm:j_idt77')

    s_username.send_keys(login)
    s_password.send_keys(password)
    s_continue.click()

    return (str(driver.find_element_by_xpath('//*[@id="navbar-top-links-form:balance-dropdown"]/a'
                                             ).text).replace(',00', '')).replace(' ', '')

# ellco_parser('101098193', 'eL0b1R')
