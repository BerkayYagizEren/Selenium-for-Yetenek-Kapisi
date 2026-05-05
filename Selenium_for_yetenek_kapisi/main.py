from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def focus_degistir_ve_don(driver):

    try:
        ana_sayfa_window = driver.current_window_handle

        # 1. Yeni boş sekme aç
        driver.execute_script("window.open('about:blank', '_blank');")
        time.sleep(1)

        # 2. Yeni sekmeye geç
        yeni_sekme = [window for window in driver.window_handles if window != ana_sayfa_window][0]
        driver.switch_to.window(yeni_sekme)
        print("Focus yeni sekmeye kaydırıldı, 3 sn bekleniyor...")

        time.sleep(3)  # İstediğin 3 saniyelik bekleme

        # 3. Sekmeyi kapat ve ana sayfaya dön
        driver.close()
        driver.switch_to.window(ana_sayfa_window)
        print("Ana sekmeye geri dönüldü.")
    except Exception as e:
        print(f"Sekme operasyonu hatası: {e}")


def video_tikla_ve_oynat(driver):
   
    try:
        wait = WebDriverWait(driver, 15)
        video_element = wait.until(EC.presence_of_element_located((By.ID, "YtnkPlayer_html5_api")))

        # Ortalama
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", video_element)
        time.sleep(1)

        # Videoya Tıkla
        driver.execute_script("arguments[0].click();", video_element)
        print(f"[{time.strftime('%H:%M:%S')}] Videoya tıklandı.")

        # --- SENİN İSTEDİĞİN SEKME DEĞİŞTİRME MANTIĞI ---
        focus_degistir_ve_don(driver)

    except Exception as e:
        print(f"Video tetiklenemedi: {e}")


def egitim_botunu_baslat():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 25)

    try:
        # LOGIN VE NAVIGASYON (Buraları hızlı geçiyorum)
        driver.get("https://ytnk.tv/")
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btnGiris"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "TxtEposta"))).send_keys("berkayeren@ogr365.iyte.edu.tr")
        driver.find_element(By.ID, "TxtSifre").send_keys("123")
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[@id='ytnktv']//button[contains(@onclick, 'Giris()')]"))).click()

        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Career Planning Course"))).click()
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Continue"))).click()

        # İLK BAŞLATMA
        time.sleep(5)
        video_tikla_ve_oynat(driver)

        # ANA DÖNGÜ
        while True:
            try:
                # Next Topic butonunu bekle
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "swal-button--nextone"))
                )

                next_button.click()
                print(f"\n[{time.strftime('%H:%M:%S')}] Next Topic tıklandı!")

                time.sleep(10)  # Sayfanın yenilenmesi için

                # Her Next'ten sonra videoya tıkla ve sekme değiştir-kapat yap
                video_tikla_ve_oynat(driver)

            except:
                time.sleep(5)
                continue

    except Exception as e:
        print(f"\nSistem durdu: {e}")


if __name__ == "__main__":
    egitim_botunu_baslat()