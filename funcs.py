from selenium.webdriver.common.by import By
from googletrans import Translator
import numpy as np
import time


def get_data(lst, key, element):
    """
    :param element: each webdriver block by selenium
    :param lst:   output empty list
    :param key:   css selector for locating data
    :return:      populated list
    """
    _type = element.find_elements(By.CSS_SELECTOR, key)
    if not _type:
        return lst.append(np.NaN)
    else:
        return lst.append(_type[0].text)


def translate_food_names(df):
    """
    # todo: documentation for translate_food_names func
    :param df:
    :return:
    """
    translated_names_lst = []
    count = 0
    success_count = 0

    translator = Translator()
    for item in df.Name:
        while True:
            try:
                time.sleep(0.1)
                translated = translator.translate(text=item, src='sv', dest='en')
                translated_names_lst.append(translated.text)
                success_count += 1
                print(
                    f'                                                         {success_count} TRANSLATED - {translated.text}')
            except (TypeError, AttributeError):
                count += 1
                print(f'ERROR{count}:retrying... {item}')
                continue
            break

    return translated_names_lst


def parse_ingredients(ingredient_df, accepted_ingredients_df):
    """
    :param ingredient_df: a dataframe with column: 'Ingredient'
    :param accepted_ingredients_df: a dataframe with column: 'Ingredient'
    :return: a list of viable ingredients
    """
    parsed_ingredients = []

    for item in accepted_ingredients_df.Ingredient:
        if not ingredient_df[ingredient_df.Ingredient.str.contains(item)].empty:
            parsed_ingredients.append(item)

    return parsed_ingredients
