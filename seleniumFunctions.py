from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def wait(by,search_value):
    global driver
    if by=='class':
        if ' ' in search_value:
            search_value = search_value.replace(' ', '.')
        element = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.CLASS_NAME, search_value)))
        elements=driver.find_elements(by=By.CLASS_NAME,value=search_value)
    elif by=='tag':
        element = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.TAG_NAME, search_value)))
        elements = driver.find_elements(by=By.TAG_NAME, value=search_value)
    elif by=='css':
        element = WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, search_value)))
        elements = driver.find_elements(by=By.CSS_SELECTOR, value=search_value)
    if len(elements)==1:
        return element
    else:
        print(f"The element {search_value} is not unique")
def screenshot_page():
    global driver
    driver.save_screenshot('webPage.png')
def open_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Users\usher\Desktop\Apps\FriendsFinal\userData")
    #options.binary_location = r"C:\Users\usher\Desktop\Apps\FriendsFinal\chromedriver.exe"
    global driver
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    if find_qr():
        sleep(20)
        screenshot_page()
        main()
        sleep(60)
    return driver

def send_message(name,message):
    #driver.minimize_window()
    text_box=wait('class',"_2vDPL")
    elements=text_box.find_elements(by=By.TAG_NAME, value='div')
    goal=elements[1]
    goal.send_keys(name)
    sleep(3)
    element = wait('css', 'div[style*="transform: translateY(72px);"]')
    element.click()
    element=wait('css','div[title="Scrivi un messaggio"]')
    element.send_keys(message)
    element.send_keys(Keys.RETURN)
    sleep(10)
def find_qr():
    try:
        qr=wait('class','_19vUU')
        return True
    except:
        return False
def close_driver():
    global driver
    driver.quit()
def send_email_with_attachment(sender_email, sender_password, receiver_email, subject, message_body, attachment_file,smtp_server,smtp_port):
    # Set up email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach message body
    msg.attach(MIMEText(message_body, 'plain'))

    # Attach screenshot image
    with open(attachment_file, 'rb') as f:
        img = MIMEImage(f.read())
        img.add_header('Content-Disposition', 'attachment', filename=attachment_file)
        msg.attach(img)
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(sender_email, sender_password)
    # Connect to SMTP server and send email
    server.sendmail(sender_email, receiver_email, msg.as_string())

def main():
    smtp_server = "it38.siteground.eu"
    smtp_port=587
    output_file = 'webPage.png'
    sender_email = 'michele.usher@krilldesign.net'
    sender_password = 'Krill2018!'
    receiver_email = 'ushermichele2002@gmail.com'
    subject = 'Webpage Screenshot'
    message_body = 'Please find the screenshot attached.'
    send_email_with_attachment(sender_email, sender_password, receiver_email, subject, message_body, output_file,smtp_server,smtp_port)

#open_whatsapp()

