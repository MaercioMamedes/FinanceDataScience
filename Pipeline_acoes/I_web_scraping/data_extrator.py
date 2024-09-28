from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime


# abrir página
driver = WebDriver()
url = "https://www.fundamentus.com.br/resultado.php"
driver.get(url)
driver.minimize_window()

# carregar dados
"""Coluna"""

table = driver.find_element(By.TAG_NAME, "table")
thead = table.find_element(By.TAG_NAME, "thead")
header = thead.find_element(By.TAG_NAME, "tr")
th = header.find_elements(By.TAG_NAME, "th")

"""linha"""

tbody = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/table/tbody")


# extrair dados
columns = []
rows = []

for i in th:
    if i.text.strip():
        columns.append(i.text)


for tr in tbody.find_elements(By.TAG_NAME, "tr"):
    data = []
    for i in tr.find_elements(By.TAG_NAME, "td"):
        if i.text.strip():
            data.append(i.text)

        elif not i.text.strip() and len(data)<13:
            data.append(None)

    rows.append(data)

# limpar dados


# salvar num arquivo csv
data_atual = datetime.now().strftime('%Y_%m_%d')

df = pd.DataFrame(data=rows, columns=columns)
df.to_csv(f"../data/{data_atual}_data.csv", index=False, sep=";")