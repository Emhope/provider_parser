from selenium import webdriver
from selenium.webdriver.common.by import By

import time


class ButtonClicker:
    '''
    Clicker can find and click on buttons
    It needs url for init and then you can ask him to click
    '''
    def __init__(self, url: str):
        self._browser = webdriver.Chrome()
        self._browser.get(url)
        self.refresh()
    
    def _get_button_by_text(self, text: str, refreshed: bool = False):
        for button in self._buttons:
            if button.text == text:
                return button
        if not refreshed:
            print(f'Didnt find button with such text. Trying to refresh...')
            self.refresh()
            self._get_button_by_text(text, refreshed=True)
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

    def refresh(self):
        self._buttons = self._browser.find_elements(By.TAG_NAME, 'button')

    def quit(self):
        self._browser.quit()


if __name__ == '__main__':
    needed_buttons = ['Многоквартирные дома', 'Частные дома и коттеджи']
    URL = 'https://www.rialcom.ru/internet_tariffs/'
    clicker = ButtonClicker(url=URL)
    clicker.click_button_by_text(needed_buttons[0], verbose=True)
    time.sleep(5)
    clicker.click_button_by_text(needed_buttons[0], verbose=True)
    time.sleep(5)
    clicker.click_button_by_text('dsfs', verbose=True)
    time.sleep(5)
    clicker.quit()
