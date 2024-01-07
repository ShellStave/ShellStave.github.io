from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def select_option_and_save_content(url, dropdown_class, option_text1):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--incognito")  # For incognito mode in Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl08_Piskotki_Obvestilo1_LinkPotrdi"))).click()  
    time.sleep(5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, dropdown_class))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//div[span[text()='{option_text1}']]"))).click()  
    time.sleep(2)
    # Add 'active' class to the second span
    driver.execute_script("document.getElementsByClassName('sorti')[0].getElementsByTagName('span')[1].click();")


    start_time = time.time()  # remember when we started
    scroll_element = driver.find_element(By.CLASS_NAME, 'more')
    time.sleep(2)
    while time.time() - start_time < 15:  # should run for approximately 10 seconds
        time.sleep(2)
        driver.execute_script("arguments[0].scrollIntoView(true);", scroll_element)
    # Get the text of the element
    text = driver.execute_script("return document.getElementsByClassName('stavna-lista-scrollabe')[0].innerText;")
    # # Split the text into lines
    lines = text.split('\n')
    
    # Write only lines that contain " - " or "NOGOMET" to the output file
    lines_to_write = []
    for line in lines:
        if " - " in line or "NOGOMET" in line or ".," in line:
            line = line.replace("NOGOMET · ", "")
            lines_to_write.append(line)
    output_file_name = f'estave_output.txt'
    with open(output_file_name, 'w', encoding='utf-8') as f:
        for line in lines_to_write:
            f.write(line + '\n')
    driver.quit()

select_option_and_save_content('https://www.e-stave.com/stave', 'stavne-moznosti-text', 'Vsota 3,5 gola')