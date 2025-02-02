from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

import pandas as pd


def _extract_base_table(table: WebElement) -> list[dict[str, str]]:
    title = table.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr')
    title = [h.text.strip(' *_\n') for h in title.find_elements(By.TAG_NAME, 'th')]
    rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')
    data = []
    for row in rows:
        raw_line = row.find_elements(By.TAG_NAME, 'td')
        line_data = [i.text.strip(' *_\n') for i in raw_line]
        data.append(dict(zip(title, line_data)))
    return data


def _parse_internet(table: WebElement) -> pd.DataFrame:
    raw_data = _extract_base_table(table)
    df = pd.DataFrame(raw_data)
    df.drop(columns=['Расчетный период'], inplace=True)
    df['Абонентская плата в расчетный период'] = df['Абонентская плата в расчетный период'].str.extract('(\d+)')
    df['Абонентская плата в расчетный период'] = pd.to_numeric(df['Абонентская плата в расчетный период'])
    df['Скорость доступа'] = df['Скорость доступа'].str.extract('(\d+)')
    df['Скорость доступа'] = pd.to_numeric(df['Скорость доступа']) / 1000
    df.rename(columns={'Абонентская плата в расчетный период': 'Абонентская плата'}, inplace=True)
    return df


def _parse_internet_plus_tv(table: WebElement) -> pd.DataFrame:
    raw_data = _extract_base_table(table)
    raw_df = pd.DataFrame(raw_data)

    base_tarif = pd.DataFrame()
    base_tarif[["Название тарифа", "Количество каналов"]] = raw_df.iloc[:, 0].str.extract(r"(.+)\s\((\d+)\sканал")
    base_tarif["Количество каналов"] = base_tarif["Количество каналов"].astype(int)

    all_combinations = []
    for mode in raw_df.columns[1:]:
        comb = base_tarif.copy()
        prepared_mode = mode
        # prepared_mode = mode.replace('*', '') # если раскомментить, то в названии не будет *, по моему так делать правильно, но в тз не просится
        comb['Base'] = comb['Название тарифа']
        comb['Название тарифа'] += ' + ' + prepared_mode
        comb['Абонентская плата'] = pd.to_numeric(raw_df[mode])
        all_combinations.append(comb)

    res = pd.concat(all_combinations, ignore_index=True)
    res['Скорость доступа'] = res['Название тарифа'].str.extract('.+Интернет (\d+)\*? \+ ТВ')
    res['Скорость доступа'] = pd.to_numeric(res['Скорость доступа'])
    return res


def _parse_internet_plus_tv_private(table: WebElement) -> pd.DataFrame:
    raw_data = _extract_base_table(table)
    raw_df = pd.DataFrame(raw_data)

    base_tarif = pd.DataFrame()
    base_tarif["Название тарифа"] = raw_df.iloc[:, 0]

    all_combinations = []
    for mode in raw_df.columns[1:]:
        comb = base_tarif.copy()
        prepared_mode = mode
        # prepared_mode = mode.replace('*', '')

        # тут кажется противеречия в тз: "Название тарифа (формируется из “строка + столбец _ч”)"
        # далее следует пример, что для первой ячейки должно получиться название "Комбо Лайт + РиалКом Интернет 50 + ТВ_ч"
        # однако так быть не может, потому что в конце названий столбцов есть приписка "Дом". можно конечно обрезать "Дом", но
        # в тз об этом не просится. возможно на момент составления тз таблица имела другой вид
        # я решил руководствоваться прямой инструкцией, а не примерами, то есть "Дом" обрезать не буду,
        # хотя теперь приставка "_ч" теряет смысл (так как уникальность названия теперь достигается с помощью "Дом"), но оставлю это на совести составителя тз 
        # (хотя по хорошему надо уточнить этот момент, но так как это тестовое задание, уточнения наверное неуместны)
        
        # UPD да, определенно сайт поменялся, потому что теперь вместо 48 строк (как в тз) получается 36,
        # потому что в таблице нет тарифа для 200 мб / сек

        comb['Base'] = comb['Название тарифа']
        comb['Название тарифа'] = comb['Название тарифа'] + ' + ' + prepared_mode + '_ч'
        comb['Абонентская плата'] = pd.to_numeric(raw_df[mode])
        
        all_combinations.append(comb)

    res = pd.concat(all_combinations, ignore_index=True)
    res['Скорость доступа'] = res['Название тарифа'].str.extract('.+Интернет \+ ТВ Дом (\d+)\*?')
    res['Скорость доступа'] = pd.to_numeric(res['Скорость доступа'])
    return res


parser_router = {
    'Многоквартирные дома Интернет': _parse_internet,
    'Многоквартирные дома Интернет + Интерактивное ТВ': _parse_internet_plus_tv,
    'Частные дома и коттеджи Интернет': _parse_internet,
    'Частные дома и коттеджи Интернет + Интерактивное ТВ': _parse_internet_plus_tv_private,
}
