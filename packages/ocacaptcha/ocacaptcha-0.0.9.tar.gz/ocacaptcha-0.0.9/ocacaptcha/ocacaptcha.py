from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
import urllib.request
import requests
import hashlib
import random
import time
def solve_captcha(driver, actions, action_type, user_api_key, amount_captcha_attempts):
    capctha_circle = driver.find_elements("xpath",'//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]') ##check capctha the same shapes
    if len(capctha_circle) > 0:
        for i in range(1, 3):
            capctha_circle = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]') ##check capctha the same shapes
            if len(capctha_circle) > 0:
                print('Solving capctcha circle...')
                slider_captcha_location = driver.find_element(By.XPATH, '//div[contains(@class,"secsdk-captcha-drag-icon")]//*[name()="svg"]') ##get cordinates img x and y 
                coordinate_slider_captcha = slider_captcha_location.location
                coordinate_slider_captcha_x = coordinate_slider_captcha['x']
                coordinate_slider_captcha_y = coordinate_slider_captcha['y']
            
                #start request solving capthca
                full_img_url = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_container")]/div/img[1][contains(@style,"transform: translate(-50%, -50%) rotate")]').get_attribute("src") #get link full img
                open_full_img_url = urllib.request.urlopen(full_img_url) #open link
                full_img_url_html_bytes = open_full_img_url.read() #read link
                full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8') #encode to base64 full img link
                hash_object = hashlib.md5()
                hash_object.update(full_screenshot_img_url_base64.encode())
                full_img_md5 = hash_object.hexdigest()
                small_img_url = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_container")]/div/img[2][contains(@style,"transform: translate(-50%, -50%) rotate")]').get_attribute("src") #get link small img
                open_small_img_url = urllib.request.urlopen(small_img_url) #open link
                small_img_url_html_bytes = open_small_img_url.read() #read link
                small_screenshot_img_url_base64 = base64.b64encode(small_img_url_html_bytes).decode('utf-8') #encode to base64 small img link
                hash_object = hashlib.md5()
                hash_object.update(small_screenshot_img_url_base64.encode())
                small_img_md5 = hash_object.hexdigest()
                action_type = 'tiktokcircle'
                #user_api_key = 'nCN8QJfYcNlqVvq0koOCKLyx7abxaO4U7qf' #paste your api key in the field 

                multipart_form_data = {
                    'FULL_IMG_CAPTCHA': (None, full_img_md5),
                    'SMALL_IMG_CAPTCHA': (None, small_img_md5),
                    'ACTION': (None, action_type),
                    'USER_KEY': (None, user_api_key)
                }
                solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                print(solve_captcha.content)
                #end request solving capthca
            
                response_solve_captcha = str(solve_captcha.content)
                if response_solve_captcha != "b'FAILED_SOLVE_CAPTCHA'":
                    response_solve_captcha = solve_captcha.json()
                    response_cordinate_x = int((response_solve_captcha["cordinate_x"]))
                    response_cordinate_y = int((response_solve_captcha["cordinate_y"]))
                    response_cordinate_x_range_move_number = int(response_cordinate_x) - 5            
                    actions.click_and_hold(slider_captcha_location)
                    for i in range(0, 1):
                        actions.move_by_offset(response_cordinate_x_range_move_number, 0)  
                        time.sleep(0.0001)   
                    for i in range(0, 5):
                        actions.move_by_offset(1, 0)  
                        time.sleep(0.1)   
                    actions.release().perform() 
                    time.sleep(10)    
                else:
                    refresh_captcha_circle = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                    time.sleep(5)  
            else:
                print("Captcha success solved")
                break
    capctha_3D = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_img")]/img') ##check capctha the same shapes
    if len(capctha_3D) > 0:
        for i in range(1, 30):
            capctha_3D = driver.find_elements("xpath", '//div[contains(@class,"captcha_verify_img")]/img') ##check capctha the same shapes
            if len(capctha_3D) > 0:
                print('Solving capctcha the same shapes...')
                full_img_url_location = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img') ##get cordinates img x and y 
                coordinate_full_img_url = full_img_url_location.location
                coordinate_full_img_url_x = coordinate_full_img_url['x']
                coordinate_full_img_url_y = coordinate_full_img_url['y']
            
                #start request solving capthca
                full_img_url = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_img")]/img').get_attribute("src") #get link full img                  
                open_full_img_url = urllib.request.urlopen(full_img_url) #open link
                full_img_url_html_bytes = open_full_img_url.read() #read link
                full_screenshot_img_url_base64 = base64.b64encode(full_img_url_html_bytes).decode('utf-8') #encode to base64 full img link
                hash_object = hashlib.md5()
                hash_object.update(full_screenshot_img_url_base64.encode())
                full_img_md5 = hash_object.hexdigest()
                action_type = 'tiktok3D'
                #user_api_key = 'nCN8QJfYcNlqVvq0koOCKLyx7abxaO4U7qf' #paste your api key in the field 

                multipart_form_data = {
                    'FULL_IMG_CAPTCHA': (None, full_img_md5),
                    'ACTION': (None, action_type),
                    'USER_KEY': (None, user_api_key)
                }   
                solve_captcha = requests.post('https://captcha.ocasoft.com/api/res.php', files=multipart_form_data)
                print(solve_captcha.content)
                #end request solving capthca
            
                response_solve_captcha = str(solve_captcha.content)
                if response_solve_captcha != "b'FAILED_SOLVE_CAPTCHA'":
                    solve_captcha = solve_captcha.json()
                    cordinate_x_1 = (solve_captcha["cordinate_x_1"])
                    cordinate_y_1 = (solve_captcha["cordinate_y_1"])
                    cordinate_x_2 = (solve_captcha["cordinate_x_2"])
                    cordinate_y_2 = (solve_captcha["cordinate_y_2"])
                    target_cordinate_x_1 = int(cordinate_x_1)+int(coordinate_full_img_url_x)
                    target_cordinate_y_1 = int(cordinate_y_1)+int(coordinate_full_img_url_y)
                    target_cordinate_x_2 = int(cordinate_x_2)+int(coordinate_full_img_url_x)
                    target_cordinate_y_2 = int(cordinate_y_2)+int(coordinate_full_img_url_y)
                    actions.move_by_offset(target_cordinate_x_1, target_cordinate_y_1).click().perform()
                    actions.move_by_offset(-target_cordinate_x_1, -target_cordinate_y_1).perform()
                    time.sleep(0.1 or 0.5)
                    actions.move_by_offset(target_cordinate_x_2, target_cordinate_y_2).click().perform()
                    time.sleep(1 or 2)    
                    click_verify_3D_captcha = driver.find_element(By.XPATH, '//div[contains(@class,"verify-captcha-submit-button")]').click()
                    time.sleep(10) 
                else:
                    refresh_captcha_circle = driver.find_element(By.XPATH, '//div[contains(@class,"captcha_verify_action")]//span[contains(@class,"secsdk_captcha_refresh--icon")]').click()
                    time.sleep(5) 
            else:
                print("Captcha success solved")
                break
                