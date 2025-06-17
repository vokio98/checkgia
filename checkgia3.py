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
        name = driver.find_element(By.CLASS_NAME, "name_pro_detail").text.strip()
        price_sale = driver.find_element(By.CLASS_NAME, "price_sale").text.strip()
        price_market = driver.find_element(By.CLASS_NAME, "price_giaban").text.strip()
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
        driver.get(f"https://www.dienmayxanh.com/search?key={product_code}")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "main-contain")))
        item = driver.find_element(By.CLASS_NAME, "main-contain")
        detail_link = item.get_attribute("href")
        driver.get(detail_link)
        name = driver.find_element(By.CLASS_NAME, "product-name").text.strip()
        price_sale = driver.find_element(By.CLASS_NAME, "box-price-present").text.strip()
        price_market = driver.find_element(By.CLASS_NAME, "box-price-old").text.strip()
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
        driver.get(f"https://www.nguyenkim.com/tim-kiem.html?tu-khoa={product_code}&search=")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-header")))
        detail_link = driver.find_element(By.CLASS_NAME, "product-header").get_attribute("href")
        driver.get(detail_link)
        name = driver.find_element(By.CLASS_NAME, "product_info_name").text.strip()
        price_sale = driver.find_element(By.CLASS_NAME, "nk-price-final").text.strip()
        price_market = driver.find_element(By.CLASS_NAME, "product_info_price_value-real").text.strip()
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
    input_file = "ma_san_pham.xlsx"
    try:
        df_input = pd.read_excel(input_file)
        ma_sps = df_input["Mã SP"].dropna().astype(str).tolist()
    except Exception as e:
        print(f"❌ Không thể đọc file '{input_file}':", e)
        exit()

    all_rows = []

    for ma_sp in ma_sps:
        print(f"🔍 Đang xử lý mã: {ma_sp}")
        all_rows.append({
            "Mã SP": ma_sp,
            "Website": "",
            "Tên sản phẩm": "",
            "Giá sale": "",
            "Giá gốc": "",
            "Link sản phẩm": ""
        })

        for func in [get_dienmaycholon, get_dienmayxanh, get_nguyenkim]:
            result = func(ma_sp)
            result["Mã SP"] = ""  # không trùng dòng mẹ
            all_rows.append(result)
        time.sleep(1)

    df = pd.DataFrame(all_rows)
    df.to_excel("ket_qua_gia.xlsx", index=False)
    print("✅ Đã xuất kết quả ra file: ket_qua_gia.xlsx")
