import time

import pandas as pd
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

find_request = "microsoft surface планшет"
find_target = "surface"
cycle_ = 0


def excel_input(data):
    data.to_excel('Surfaces.xlsx')


def get_actual_product():
    global cycle_
    cycle_ += 1
    driver = webdriver.Edge()
    try:
        driver.get("https://www.avito.ru/")
        elem = driver.find_element(by=By.ID, value="downshift-input")
        elem.send_keys(find_request, Keys.ENTER)

        nouts = driver.find_elements(by=By.CLASS_NAME, value="iva-item-titleStep-pdebR")
        dt = None
        count = 1
        for nout in nouts:
            if find_target not in nout.text.lower():
                continue
            title = nout.text
            nout.click()
            driver.switch_to.window(driver.window_handles[1])
            address = driver.find_element(by=By.CLASS_NAME, value="style-item-address__string-wt61A")

            if "Перм" in address.text:
                print("\n", title)
                print("Адрес", address.text)
                # print("Продавец", driver.find_element(by=By.XPATH, value="//div[@data-marker='seller-info/name']").text)
                saller = driver.find_element(by=By.XPATH,
                                             value="//span[@class='text-text-LurtD text-size-ms-_Zk4a']").text
                print("Продавец", saller)
                price = driver.find_element(by=By.XPATH,
                                            value="//div[@class='style-price-value-mHi1T style-item-price-main-jpt3x "
                                                  "item-price']").text.replace(
                    "\n", "")
                print("Цена", price)
                print("Ссылка", driver.current_url)
                harki = driver.find_element(by=By.XPATH, value="//ul[@class='params-paramsList-zLpAu']")
                print("Хар-ки", harki.text)
                print("\n" + str(cycle_) + str(count) + "#" * 50)
                count += 1
                dt_new = pd.DataFrame(
                    {"Продукт": [title], 'Последняя цена': [price], "Адрес": [address.text], 'Продавец': [saller],
                     'Cсылка': [driver.current_url], 'Хар-ки': [harki.text]})
                dt = pd.concat([dt, dt_new], ignore_index=True, axis=0)
            else:
                break
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        excel_input(dt)


    except Exception as e:
        print(e)

    finally:
        time.sleep(10)
        driver.close()
        driver.quit()


if __name__ == "__main__":
    schedule.every(1).minutes.do(get_actual_product)

    while True:
        schedule.run_pending()
        time.sleep(30)
