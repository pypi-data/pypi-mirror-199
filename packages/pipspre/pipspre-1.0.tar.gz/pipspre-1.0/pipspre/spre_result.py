# -*- coding:utf-8 -*-

from aip import AipSpeech
import speech_recognition as sr

APP_ID = '30187775'
API_KEY = '24wDR31XDqOB5T0VLr3NBoH2'
SECRET_KEY = 'hvAhPj0MavYaKP9KYwjFUn8BNcpHAL9m'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def spre_result():
    r = sr.Recognizer()
    mic = sr.Microphone()
    print("请说话...")

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    print("\n正在分析...")

    result = client.asr(audio.get_wav_data(convert_rate=16000), 'wav', 16000, {'dev_pid': 1537, })
    try:
        text = result['result'][0]
    except Exception as e:
        print(e)
        text = ""
    return text



