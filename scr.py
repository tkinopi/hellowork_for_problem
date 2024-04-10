from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
import csv
import itertools
from time import sleep
import bs4
import requests
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
def get_urls():
    driver = webdriver.Chrome(service=Service())
    driver.get("https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?action=initDisp&screenId=GECA110010")
    driver.maximize_window()
    sleep(3)
    driver.find_element(By.ID,"ID_ippanCKBox1").click()
    select = Select(driver.find_element(By.ID,"ID_tDFK1CmbBox"))
    select.select_by_value("27")
    driver.find_elements(By.CSS_SELECTOR,"div.flex.align_center.mt05 button")[0].click()
    sleep(3)
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID,"ID_LskCheck0711"))
    sleep(3)
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID,"ID_ok3"))
    sleep(3)
    driver.execute_script("arguments[0].click();", driver.find_element(By.ID,"ID_searchBtn"))
    sleep(3)

    urls = [url.get_attribute("href") for url in driver.find_elements(By.ID,"ID_dispDetailBtn")]
    driver.execute_script("arguments[0].click();", driver.find_element(By.NAME,"fwListNaviBtnNext"))
    num = int(driver.find_elements(By.CSS_SELECTOR,"div.m05 span.fb")[0].text.replace("件",""))
    last_num = num / 30
    count = 0
    urls = []
    while True:
        count += 1
        result = [urls.append([url.get_attribute("href")]) for url in driver.find_elements(By.ID,"ID_dispDetailBtn")]
        try:
            driver.find_elements(By.NAME,"fwListNaviBtnNext")[0].click()
        except:
            break
        if count > last_num:
            break
    return urls

# urlの内容を取得
# url = 'https://www.hellowork.mhlw.go.jp/kensaku/GECA110010.do?screenId=GECA110010&action=dispDetailBtn&kJNo=2707007864841&kJKbn=1&jGSHNo=V4MTZKzXtQ%2F3PbI5Eoas8Q%3D%3D&fullPart=1&iNFTeikyoRiyoDtiID=&kSNo=&newArrived=&tatZngy=1&shogaiKbn=0'

def get_job_info(url):
    html = requests.get(url).text

    # Beautifulsoup4で解析
    soup = bs4.BeautifulSoup(html, "html.parser")

    # 'table'タグ、class='normal mb1'のすべてを探します
    tables = soup.find_all('table', {'class': 'normal mb1'})

    # URLを含む辞書を初期化します
    result_dict = {'url': url}

    for table in tables:
        # その中のすべての 'tr' タグを探します。
        for tr in table.find_all('tr'):
            # 'th' タグで key を取得します。
            th = tr.find('th')
            if th:
                key = th.get_text().strip()

                # 'td' タグで value を取得します。
                td = tr.find('td')
                if td:
                    value = td.get_text().strip()

                    # 辞書に key-value ペアを追加します。
                    result_dict[key] = value

    return result_dict


# # あなたのリスト型の求人情報データ
# jobs = [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value3', 'key2': 'value4'}]

def write_to_spreadsheet(jobs):
    # 全角のキーを半角に変換し、特殊な文字を削除または置換します
    for job in jobs:
        for key in list(job.keys()):
            new_key = key.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
            job[new_key] = job.pop(key).replace('\n', ' ').replace('\r', ' ')
    # pandas DataFrameに変換
    df = pd.DataFrame(jobs)

    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './credentials.json',
        ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
                )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1nSpTz2KpxIj11nxK4BOj6507HzcWJemXHQeclHTObCQ')

    # ワークシートを選択（例では最初のワークシートを選択）
    worksheet = sh.worksheet("シート1")

    df = df.fillna("")  # NaN値を空文字（""）に置き換え

    # DataFrameをGoogle Spreadsheetに書き込む
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

def get_sheet_a_data():
    # Google APIを使用するための認証情報（jsonファイル）
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        './credentials.json',
        ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    )

    # gspread clientの生成
    gc = gspread.authorize(credentials)

    # Google Spreadsheetを開く
    sh = gc.open_by_key('1nSpTz2KpxIj11nxK4BOj6507HzcWJemXHQeclHTObCQ')

    # ワークシートを選択（例ではシート名が "Sheet1" のワークシートを選択）
    worksheet = sh.worksheet("hellowork")

    # A列のデータを全て取得
    col_values = worksheet.col_values(1)  # 1 corresponds to 'A' column

    # url格納用のlist
    urls = []

    # 確認のために取得したURLを表示
    for url in col_values:
        print(url)
        urls.append(url)

    return urls





# with open("hellowork.csv", mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     # リストのデータを行ごとにCSVに書き込む
#     for row in itertools.chain.from_iterable(urls):
#         writer.writerow([row])