import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_dienmaycholon(product_code):
    driver = init_driver()
    data = {"Website": "dienmaycholon", "Tên sản phẩm": "", "Giá sale": "", "Giá gốc": "", "Link sản phẩm": ""}
    try:
        search_code = product_code.lower().replace("-", "")
        driver.get(f"https://dienmaycholon.com/tu-khoa/{search_code}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product_block_img a")))
        detail_link = driver.find_element(By.CSS_SELECTOR, "div.product_block_img a").get_attribute("href")
        driver.get(detail_link)
        try:
            name = driver.find_element(By.CLASS_NAME, "name_pro_detail").text.strip()
        except:
            name = "Không tìm thấy"
        try:
            price_sale = driver.find_element(By.CLASS_NAME, "price_sale").text.strip()
        except:
            price_sale = "N/A"
        try:
            price_market = driver.find_element(By.CLASS_NAME, "price_giaban").text.strip()
        except:
            price_market = "N/A"
        data.update({
            "Tên sản phẩm": name,
            "Giá sale": price_sale,
            "Giá gốc": price_market,
            "Link sản phẩm": detail_link
        })
    except Exception as e:
        print("⚠️ DMCL:", e)
    finally:
        driver.quit()
    return data

def get_dienmayxanh(product_code):
    driver = init_driver()
    data = {"Website": "dienmayxanh", "Tên sản phẩm": "", "Giá sale": "", "Giá gốc": "", "Link sản phẩm": ""}
    try:
        search_url = f"https://www.dienmayxanh.com/search?key={product_code}"
        driver.get(search_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main-contain")))
        item = driver.find_element(By.CLASS_NAME, "main-contain")
        detail_link = item.get_attribute("href")
        driver.get(detail_link)

        try:
            name = driver.find_element(By.CLASS_NAME, "product-name").text.strip()
        except:
            name = "Không tìm thấy"
        try:
            price_sale = driver.find_element(By.CLASS_NAME, "box-price-present").text.strip()
        except:
            price_sale = "N/A"
        try:
            price_market = driver.find_element(By.CLASS_NAME, "box-price-old").text.strip()
        except:
            price_market = "N/A"

        data.update({
            "Tên sản phẩm": name,
            "Giá sale": price_sale,
            "Giá gốc": price_market,
            "Link sản phẩm": detail_link
        })
    except Exception as e:
        print("⚠️ DMX:", e)
    finally:
        driver.quit()
    return data

def get_nguyenkim(product_code):
    driver = init_driver()
    data = {"Website": "nguyenkim", "Tên sản phẩm": "", "Giá sale": "", "Giá gốc": "", "Link sản phẩm": ""}
    try:
        search_url = f"https://www.nguyenkim.com/tim-kiem.html?tu-khoa={product_code}&search="
        driver.get(search_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-title")))
        detail_link = driver.find_element(By.CLASS_NAME, "product-title").get_attribute("href")
        driver.get(detail_link)

        try:
            name = driver.find_element(By.CLASS_NAME, "product_info_name").text.strip()
        except:
            name = "Không tìm thấy"
        try:
            price_sale = driver.find_element(By.CLASS_NAME, "nk-price-final").text.strip()
        except:
            price_sale = "N/A"
        try:
            price_market = driver.find_element(By.CLASS_NAME, "product_info_price_value-real").text.strip()
        except:
            price_market = "N/A"

        data.update({
            "Tên sản phẩm": name,
            "Giá sale": price_sale,
            "Giá gốc": price_market,
            "Link sản phẩm": detail_link
        })
    except Exception as e:
        print("⚠️ NK:", e)
    finally:
        driver.quit()
    return data

if __name__ == "__main__":
    ma_sp = input("🔍 Nhập mã sản phẩm: ").strip()
    results = [
        get_dienmaycholon(ma_sp),
        get_dienmayxanh(ma_sp),
        get_nguyenkim(ma_sp),
    ]

    df = pd.DataFrame(results)
    df.to_excel("ket_qua_gia.xlsx", index=False)
    print("✅ Đã xuất kết quả ra file: ket_qua_gia.xlsx")
