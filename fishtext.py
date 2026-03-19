from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import io

# Устанавливаем кодировку для вывода
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    link = "https://fishtext.ru/index.php"
    browser = webdriver.Chrome()
    browser.get(link)

    input1 = browser.find_element(By.XPATH, "//input[@name='zas']")
    input1.clear()
    input1.send_keys("99")
    browser.find_element(By.CLASS_NAME, "input-group-btn").click()

    time.sleep(2)
    
    elements = browser.find_elements(By.CLASS_NAME, "text-justify")
    full_text = " ".join([el.text.lower() for el in elements])
    word_count = full_text.count("структура")
    print(f"Слово 'структура' встречается {word_count} раз(а)")

finally:
    # Ждем для визуального контроля и закрываем браузер
    time.sleep(10)
    browser.quit()