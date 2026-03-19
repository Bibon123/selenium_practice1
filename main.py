import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


URL = "https://fishtext.ru"
ABZATS_COUNT = "99"  # Количество абзацев для генерации
WORD_TO_FIND = "структура"  # Искомое слово с учётом регистра


def setup_driver():
    """Настройка драйвера браузера (здесь для Chrome)."""
    options = Options()

    print("setup_driver: Создаём опции для Chrome")
    options.add_argument("--start-maximized")

    try:
        print("setup_driver: Запускаем Chrome WebDriver")
        driver = webdriver.Chrome(options=options)
        print("setup_driver: Драйвер запущен")
        return driver
    except Exception as exc:
        print(f"setup_driver: Ошибка при запуске драйвера: {exc}")
        raise


def generate_text_and_count_word(driver, url, abzats, target_word):
    """Основная функция: открывает сайт, генерирует текст и считает слова."""
    try:
        print(f"1. Открываем сайт: {url}")
        driver.get(url)

        time.sleep(2)

        print(f"2. Вводим количество абзацев: {abzats}")
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or @type='number']"))
        )
        input_field.clear()
        input_field.send_keys(abzats)

        print("3. Нажимаем кнопку генерации...")
        try:
            generate_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Сгенерировать') or contains(text(), 'генерации')]")
        except:
            try:
                generate_button = driver.find_element(By.XPATH, "//input[@type='submit'] | //button[@type='submit']")
            except:
                print("   Отдельная кнопка не найдена. Возможно, генерация происходит автоматически.")
                generate_button = None

        if generate_button:
            print("3.1 Нажимаем кнопку и ждём")
            generate_button.click()
            print("3.2 Кнопка нажата")
            time.sleep(3)
            print("3.3 Подождали 3 секунды после клика")
        else:
            print("3.1 Кнопка генерации не найдена, ждём 3 секунды")
            time.sleep(3)

        #Получаем весь сгенерированный текст
        print("4. Получаем сгенерированный текст...")
        text_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'text') or contains(@class, 'content') or contains(@class, 'result')]"))
        )
        full_text = text_element.text

        if not full_text:
            full_text = driver.find_element(By.TAG_NAME, "body").text
            print("   Текст найден в общем блоке body.")

        print(f"5. Подсчитываем вхождения слова '{target_word}' с учётом регистра...")
        word_count = full_text.count(target_word)

        print(f"\n--- Начало сгенерированного текста (первые 500 символов) ---")
        print(full_text[:500] + "...")
        print(f"--- Конец отрывка ---\n")

        return word_count

    except Exception as e:
        print(f" Произошла ошибка: {e}")
        return None

def main():
    print("main: старт")
    driver = setup_driver()
    print("main: драйвер настроен, начинаем генерацию")
    try:
        count = generate_text_and_count_word(driver, URL, ABZATS_COUNT, WORD_TO_FIND)
        if count is not None:
            print(f"\n🔍 РЕЗУЛЬТАТ: Слово «{WORD_TO_FIND}» встречается в тексте {count} раз(а).")
        else:
            print("Не удалось выполнить подсчёт из-за ошибки.")
    finally:
        print("Закрываем браузер.")
        driver.quit()

if __name__ == "__main__":
    main()