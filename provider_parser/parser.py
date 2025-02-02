from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd

import table_parsers


class Parser:
    def __init__(self, driver: webdriver.Chrome):
        self._driver = driver
        self.collected_data: dict[str, pd.DataFrame] = dict()
    
    def _find_tables_under_id(self, id: str) -> dict[str, WebElement]:
        d = self._driver.find_elements(By.XPATH, f"//div[@id='{id}']/div/*")
        tables = {}
        for idx, elem in enumerate(d):
            if elem.tag_name == 'table':
                tables[d[idx-1].text] = elem
        return tables

    def _extract_data_from_table(self, table: WebElement, table_name: str, btn_name: str):
        parsed_table = table_parsers.parser_router[f'{btn_name} {table_name}'](table)
        self.collected_data[f'{btn_name} {table_name}'] = parsed_table
    
    def get_data_from_collapse(self, collapse_id: int, btn_name: str, verbose: bool = False):
        tables = self._find_tables_under_id(f'collapse{collapse_id}')
        result = []
        if verbose:
            print('-'*10)
            print(f'found {len(tables)} tables, starting parse them...')
        for table_name, table in tables.items():
            r = self._extract_data_from_table(
                table=table,
                table_name=table_name,
                btn_name=btn_name
            )
            result.append(r)
        if verbose:
            print(f'tables parsed successfully!')
            print('-'*10)
        return result
    
    def _prepare_data_to_save(self):
        base = self.collected_data['Многоквартирные дома Интернет + Интерактивное ТВ'][['Количество каналов', 'Base']].copy()
        base.drop_duplicates(inplace=True)
        self.collected_data['Частные дома и коттеджи Интернет + Интерактивное ТВ'] = self.collected_data['Частные дома и коттеджи Интернет + Интерактивное ТВ'].merge(
            base,
            on='Base'
        )
        all_data = pd.concat(self.collected_data.values())
        res = all_data[[
            'Название тарифа', 
            'Количество каналов', 
            'Скорость доступа', 
            'Абонентская плата',
        ]]
        return res

    def save_xlsx(self, fname: str):
        save_data = self._prepare_data_to_save()
        save_data.to_excel(f'{fname}.xlsx', index=False)

    def save_csv(self, fname: str):
        save_data = self._prepare_data_to_save()
        save_data.to_csv(f'{fname}.csv', index=False)
