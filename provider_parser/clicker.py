from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time


class ButtonClicker:
    '''
    Clicker can find and click on buttons
    It needs url for init and then you can ask him to click
    '''
    def __init__(self, url: str):
        self._browser = webdriver.Chrome()
        self._browser.get(url)
    
    def _get_button_by_text(self, text: str, refreshed: bool = False):
        try:
            btn = self._browser.find_element(By.XPATH, f"//button[contains(text(),'{text}')]")
            return btn
        except NoSuchElementException:
            raise KeyError(f"Cant find button with text '{text}'")

    def click_button_by_text(self, text: str, delay: float = 0.1, verbose: bool = False):
        if verbose:
            print('-'*10)
            print(f"finding button by text '{text}'...")
        try:
            btn = self._get_button_by_text(text)
            if verbose:
                print('button found!')
                print('click')
                print('-'*10)
            btn.click()
            time.sleep(delay)
        except KeyError as e:
            raise e

    def quit(self):
        self._browser.quit()


if __name__ == '__main__':
    needed_buttons = ['Многоквартирные дома', 'Частные дома и коттеджи']
    URL = 'https://www.rialcom.ru/internet_tariffs/'
    clicker = ButtonClicker(url=URL)
    clicker.click_button_by_text(needed_buttons[0], verbose=True, delay=1)
    clicker.click_button_by_text(needed_buttons[1], verbose=True, delay=1)
    clicker.click_button_by_text('dsfs', verbose=True, delay=1)
    clicker.quit()
