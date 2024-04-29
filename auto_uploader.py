from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
import json
import getpass
import config
import random


def login_facebook(driver, email, password):
    driver.get("https://www.facebook.com/")
    try:
        wait_by(driver, By.XPATH, "//a[@aria-label='Marketplace']")
        return True
    except:
        pass
    try:
        input_email = wait_by(driver, By.ID, "email")
        input_email.clear()
        input_email.send_keys(email)

        input_password = wait_by(driver, By.ID, "pass")
        input_password.clear()
        input_password.send_keys(password)

        driver.find_element(By.NAME, "login").click()

        wait_by(driver, By.XPATH, "//a[@aria-label='Marketplace']")
        return True
    except Exception as e:
        print(f"Login failed: {str(e)}")
        return False


def set_element_text_by_xpath(driver, xpath, text):
    title_element = driver.find_element(By.XPATH, xpath)
    title_element.send_keys(text)


def set_category(driver):
    category_xpath = "//span[contains(text(), 'Kategori')]//following-sibling::div"
    try:
        category_element = wait_by(driver, By.XPATH, category_xpath)
        category_element.click()
        time.sleep(2)
    except:
        pass
    try:
        driver.find_elements(
            By.XPATH, "//span[contains(text(), 'Mebel')]")[1].click()
    except:
        pass
    try:
        driver.find_element(
            By.XPATH, "(//span[contains(text(), 'Mebel')])[3]").click()
    except:
        pass
    try:
        driver.find_element(
            By.XPATH, "//span[contains(text(), 'Mebel')]").click()
    except:
        pass


def set_description(driver, description):
    description_xpath = "//span[contains(text(),'Keterangan')][1]/following-sibling::textarea"
    description_element = driver.find_element(
        By.XPATH, description_xpath)
    description_element.click()
    description_element.send_keys(description)


def set_condition(driver, action):
    condition_element = wait_by(
        driver, By.XPATH, "//span[contains(text(), 'Kondisi')]")
    action.move_to_element(condition_element).click().send_keys(
        Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
    time.sleep(2)


def set_product_label(driver, label):
    label_xpath = "(//textarea)[2]"
    label_element = wait_by(driver, By.XPATH, label_xpath)
    label_element.click()
    label_element.send_keys(label)
    label_element.send_keys(Keys.ENTER)


def set_how_to_send(driver, action):
    how_to_send_xpath = "(//div[@role='checkbox']/div/div/div/div/i)[6]"
    try:
        how_to_send_element = wait_by(driver, By.XPATH, how_to_send_xpath)
        action.move_to_element(how_to_send_element).click().perform()
    except:
        pass


def publish(driver):
    try:
        wait_by(driver, By.XPATH,
                "//span[contains(text(), 'Berikutnya')]").click()
    except Exception as e:
        pass
    try:
        wait_by(driver, By.XPATH,
                "//span[contains(text(), 'Publikasikan')]").click()
    except Exception as e:
        print(f"Error publishing product: {str(e)}")
        pass


def upload_product(driver, products_informations_json, labels, description, price, color, location_count):
    # Iterate through product folders
    print(f"Mengunggah {len(products_informations_json)} produk...\n")
    real_uploaded = 0
    try:
        for upload_count, product_information in enumerate(products_informations_json):
            uploaded = False
            location_change = False
            # Go to Facebook Marketplace
            driver.get("https://www.facebook.com/marketplace/create/item")

            locations = config.locations
            product_per_locations_count = len(
                products_informations_json)//len(locations)
            if (upload_count+1) % (product_per_locations_count+1) == 0 and (location_count+1) != len(locations):
                location_count += 1
                location_change = True
            print(
                f"Mengunggah produk ke {upload_count+1} dari {len(products_informations_json)} produk di {locations[location_count]}")

            # upload product images
            for image_count, image in enumerate(product_information['image_paths']):
                upload_image_xpath = "//input[contains(@accept,'image')]"
                upload_image_element = wait_by(
                    driver, By.XPATH, upload_image_xpath)
                upload_image_element.send_keys(image)

                if image_count != 0:
                    btns_delete_image = wait_by(
                        driver, By.XPATH, "//div[contains(@aria-label, 'Hapus')]/i")
                    btns_delete_image = driver.find_elements(
                        By.XPATH, "//div[contains(@aria-label, 'Hapus')]/i")
                    # print(f"panjang btn delete {len(btns_delete_image)}")
                    for btn_count, btn_delete_image in enumerate(btns_delete_image):
                        # print(f"iterasi btn delete ke {btn_count}")
                        btn_count += 1
                        if int(len(product_information['image_paths'])) == int(image_count+1):
                            try:
                                btn_delete_image.click()
                                break
                            except:
                                pass
                        if btn_count != image_count+1:
                            try:
                                btn_delete_image.click()
                            except:
                                pass
                        time.sleep(1)

            action = ActionChains(driver)

            # set title
            set_element_text_by_xpath(
                driver, "//span[contains(text(),'Judul')][1]/following-sibling::input", product_information['judul'])
            # set price
            set_element_text_by_xpath(
                driver, "//span[contains(text(), 'Harga')][1]/following-sibling::input", price)
            # click detail selengkapnya
            wait_by(driver, By.XPATH,
                    "//span[contains(text(), 'Detail Selengkapnya')]").click()

            set_category(driver)
            set_description(driver, description)
            set_condition(driver, action)
            for label in labels:
                set_product_label(driver, label)
            # set color
            set_element_text_by_xpath(
                driver, "//span[contains(text(), 'Warna')]/following-sibling::input", color)
            location_xpath = "//span[contains(text(), 'Lokasi')]/following-sibling::input"
            location_element = wait_by(driver, By.XPATH, location_xpath)
            location_element.clear()

            if len(locations) == 1:
                action.move_to_element(location_element).click().send_keys(
                    locations[0]).perform()
            else:
                try:
                    action.move_to_element(location_element).click().send_keys(
                        locations[location_count]).perform()
                except:
                    action.move_to_element(location_element).click().send_keys(
                        locations[location_count]).perform()
            if len(locations) == 1:
                xpath_first_location = f"//span[contains(text(), '{
                    locations[0].title()}')]"
                xpath_first_locations = f"(//span[contains(text(), '{
                    locations[0].title()}')])[0]"
            else:
                xpath_first_location = f"//span[contains(text(), '{
                    locations[location_count].title()}')]"
                xpath_first_locations = f"(//span[contains(text(), '{
                    locations[location_count].title()}')])[0]"
            try:
                wait_by(driver, By.XPATH, xpath_first_location).click()
            except Exception as e:
                pass
            try:
                wait_by(driver, By.XPATH, xpath_first_locations).click()
            except Exception as e:
                pass
            set_how_to_send(driver, action)
            publish(driver)

            time.sleep(5)
            real_uploaded += 1
            uploaded = True
    except:
        global fail
        fail = True
        driver.quit()
        time.sleep(5)
        if location_change and (uploaded == False):
            return location_count-1, real_uploaded
        else:
            return location_count, real_uploaded
    global done
    print(f"{len(products_informations_json)} produk selesai diunggah\n")
    done = True


# Add the following function for better WebDriverWait usage
def wait_by(driver, by, xpath):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, xpath))
    )


def get_image_and_product_paths(products_folder):
    image_paths = []
    product_paths = []
    for product_folder in os.listdir(products_folder):
        product_path = os.path.join(products_folder, product_folder)
        product_paths.append(product_path)
        if os.path.isdir(product_path):
            images_folder = os.path.join(product_path, "images")

        if os.path.exists(images_folder) and os.path.isdir(images_folder):
            # Get all image files in the 'images' folder
            product_images = [os.path.join(images_folder, img) for img in os.listdir(
                images_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]

            # Add image paths to the list
            image_paths.append(product_images)
    return image_paths, product_paths


def get_product_informations(product_paths, image_paths, json_file_path):
    informations = []
    information_paths = []
    for product_path in product_paths:
        for file_or_folder_name in os.listdir(product_path):
            if file_or_folder_name.lower().endswith(('.txt')):
                information_paths.append(os.path.join(
                    product_path, file_or_folder_name))

    # for information_path in information_paths:
    for index, information_path in enumerate(information_paths):
        info_dict = {}
        with open(information_path, "r") as info_file:
            lines = info_file.readlines()
            for line in lines:
                key, value = map(str.strip, line.split(':', 1))
                info_dict[key.lower()] = value
            informations.append(info_dict)
        info_dict['image_paths'] = image_paths[index]

    # Save informations to a JSON file in the products folder
    if not os.path.isdir(json_file_path):
        os.makedirs(os.path.dirname(json_file_path), exist_ok=True)
    with open(json_file_path, "w") as json_file:
        json.dump(informations, json_file, indent=2)
    return informations


def set_driver(chrome_driver_path):
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")
    # option.add_argument("--headless=new")
    option.add_argument(
        f"--user-data-dir=C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option(
        "prefs", {"profile.default_content_setting_values.notifications": 1}
    )

    # set driver
    return webdriver.Chrome(service=chrome_driver_path, options=option)


def read_json_data(folder_path, file_name):
    file_path = os.path.join(folder_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    else:
        print(f"File not found: {file_path}")
        return None


def run_upload_product(price):
    # Set your Facebook email and password
    fb_email = config.fb_email
    fb_password = config.fb_password

    current_dir = os.path.abspath(os.getcwd())
    chrome_driver_path = config.chrome_driver_path
    products_folder = config.products_folder

    # get image paths, product paths and approduct informations
    image_paths, product_paths = get_image_and_product_paths(
        products_folder)
    json_file_path_and_filename = config.json_file_path_and_filename
    informations = get_product_informations(
        product_paths, image_paths, json_file_path_and_filename)

    products_informations_json_path = config.products_informations_json_path
    products_informations_json_filename = config.json_filename
    products_informations_json = read_json_data(
        products_informations_json_path, products_informations_json_filename)
    service = Service(chrome_driver_path)
    global driver
    driver = set_driver(service)

    # Log in to Facebook
    if login_facebook(driver, fb_email, fb_password):
        print("Login Successful")
    else:
        print("There is something wrong with login")

    # Upload products
    description = config.description

    labels = config.labels

    color = config.color
    try:
        location_count, real_uploaded = upload_product(
            driver, products_informations_json, labels, description, price, color, 0)
        return location_count, real_uploaded
    except:
        pass


def run_reupload_products(location_count, real_uploaded, price):
    global fail
    fail = False
    chrome_driver_path = config.chrome_driver_path

    products_informations_json_path = config.products_informations_json_path
    products_informations_json_filename = config.json_filename
    products_informations_json = read_json_data(
        products_informations_json_path, products_informations_json_filename)

    if real_uploaded != 0:
        products_informations_json = products_informations_json[real_uploaded:]
        # Save informations to a JSON file in the products folder
        if not os.path.isdir(config.json_file_path_and_filename):
            os.makedirs(os.path.dirname(
                config.json_file_path_and_filename), exist_ok=True)
        with open(config.json_file_path_and_filename, "w") as json_file:
            json.dump(products_informations_json, json_file, indent=2)

    service = Service(chrome_driver_path)
    global driver
    driver = set_driver(service)

    # Upload products
    description = config.description
    labels = config.labels
    color = config.color

    try:
        location_count, real_uploaded = upload_product(
            driver, products_informations_json, labels, description, price, color, location_count)
    except:
        pass
    return location_count, real_uploaded


fail = False
done = False


def main():
    location_count_global = 0
    real_uploaded_global = 0
    while True:
        price = random.randrange(
            config.price[0],
            config.price[1],
            config.price[2]
        )
        if done:
            break
        else:
            if not fail:
                location_count, real_uploaded = run_upload_product(price)
                location_count_global = location_count
                real_uploaded_global = real_uploaded
                continue
            else:
                location_count, real_uploaded = run_reupload_products(
                    location_count_global, real_uploaded_global, price)
                location_count_global = location_count
                real_uploaded_global = real_uploaded
                continue


if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
