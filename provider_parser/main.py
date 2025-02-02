from clicker import ButtonClicker
from parser import Parser


if __name__ == '__main__':
    URL = 'https://www.rialcom.ru/internet_tariffs/'
    needed_buttons = ['Многоквартирные дома', 'Частные дома и коттеджи']
    clicker = ButtonClicker(URL)
    parser = Parser(clicker._browser)

    for btn in needed_buttons:
        clicker.click_button_by_text(btn)
        parser.get_data_from_collapse(needed_buttons.index(btn)+1, btn)

    clicker.quit()
    # parser.save_csv('data')
    parser.save_xlsx('data')
