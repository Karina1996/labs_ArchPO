import smtplib
from email.mime.multipart import MIMEMultipart      # Многокомпонентный объект
from email.mime.text import MIMEText                # Текст/HTML
import email
import rsa
import hashlib
import imaplib
import os
import base64

global letter
global sign
# модуль 1 - отправляет письм по эл. почте с ЭЦП
def send_email_with_encrypted_file(recipient_email, sender_email, sender_email_password, pubkey, privkey):
    data = b'open message'
    # генерация ЭЦП
    signature = rsa.sign(data, privkey, 'SHA-256')
    # Отправляем открытый текст и ЭЦП по email
    # msg = email.message.Message()
    msg = MIMEMultipart()                               # Создаем сообщение
    # msg.set_payload('-----' + str(data) + '-----' + str(signature))
    letter = msg.attach(MIMEText(str(data) + '\n', 'plain'))                 
    sign = msg.attach(MIMEText(str(signature), 'plain'))  
    msg['From'] = sender_email                              # Адресат
    msg['To'] = recipient_email                             # Получатель
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)       # Создаем объект SMTP
    smtp_server.ehlo()
    # smtp_server.set_debuglevel(True)                      # Включаем режим отладки - если отчет нужен
    smtp_server.starttls()                                  # Начинаем шифрованный обмен по TLS
    smtp_server.login(sender_email, sender_email_password)  # Получаем доступ
    smtp_server.sendmail(sender_email, recipient_email, msg.as_bytes()) # Отправляем сообщение
    smtp_server.quit()                                      # Закрывает соединение
  

# модуль 2 - получение и проверка подлинности письма   
def receive_and_decrypt_email(recipient_email, recipient_email_password, pubkey, privkey):
    # Получаем последнее зашифрованное письмо
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
    imap_server.login(recipient_email, recipient_email_password)
    imap_server.select('inbox')
    result, data = imap_server.search(None, 'ALL')
    latest_email_id = data[0].split()[-1]
    result, data = imap_server.fetch(latest_email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    data = email_message.get_payload(0)
    sign = email_message.get_payload(1)
    try:
        rsa.verify(data, sign, pubkey) # передать текст письма и ЭЦП
        print('Письмо имеет действительную подпись!')
    except rsa.pkcs1.VerificationError:
        print('Подпись недействительна!')

if __name__ == "__main__":
    (pubkey, privkey) = rsa.newkeys(512)  # Генерируем ключи RSA
    send_email_with_encrypted_file('lazarevak1996@gmail.com', 'lazarevak1996@gmail.com', '', pubkey, privkey) 
    receive_and_decrypt_email('lazarevak1996@gmail.com', '', pubkey, privkey)



