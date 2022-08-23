import requests


def sendTGReport(message):
    message = message.replace(" ", "+")
    request = requests.get("https://api.telegram.org/bot5325298001:AAHYe0JX3nhT0UQXi8Lzr1tDDH1Cvv5oIM8/sendMessage?chat_id=1894287130&parse_mode=markdown&text=" + message)