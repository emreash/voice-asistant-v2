from playsound import playsound
from gtts import gTTS
import speech_recognition as sr
import os
import time
from datetime import datetime
import random
import webbrowser
import re
import wikipedia

# Ses tanıyıcı nesnesi
r = sr.Recognizer()

# Ses kaydetme fonksiyonu
def record(ask=False):
    with sr.Microphone() as source:
        if ask:
            speak(ask)
        try:
            print("Dinliyorum...")
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            voice = r.recognize_google(audio, language="tr-TR")
            return voice
        except sr.UnknownValueError:
            speak("Üzgünüm, seni anlayamadım. Lütfen tekrar et.")
            return ""
        except sr.RequestError as e:
            speak(f"Bir hata oluştu: {e}. Lütfen internet bağlantını kontrol et.")
            return ""
        except Exception as e:
            speak(f"Beklenmeyen bir hata oluştu: {e}")
            return ""

# Yanıt verme fonksiyonu
def response(voice):
    if re.search(r"\bmerhaba\b", voice):
        speak("Merhaba! Nasılsın?")
    elif re.search(r"\bselam\b", voice):
        speak("Selamlar!")
    elif re.search(r"\bteşekkür\b", voice):
        speak("Rica ederim.")
    elif re.search(r"\b(görüşürüz|güle güle|kapat)\b", voice):
        speak("Görüşürüz! Kendine iyi bak.")
        exit()
    elif re.search(r"\bbugün günlerden ne\b", voice):
        today = check_day()
        speak(f"Bugün günlerden {today}.")
    elif re.search(r"\bsaat kaç\b", voice):
        clock = datetime.now().strftime("%H:%M")
        speak(f"Saat şu an {clock}.")
    elif re.search(r"\bgoogle'da ara\b", voice):
        speak("Ne aramamı istersin?")
        search = record()
        if search:
            url = f"https://www.google.com/search?q={search}"
            webbrowser.open(url)
            speak(f"{search} için bulduklarımı listeliyorum.")
    elif re.search(r"\bnot et\b", voice):
        take_note()
    elif re.search(r"\bşaka yap\b", voice):
        tell_joke()
    elif re.search(r"\barat\b", voice) or re.search(r"\bwikipedia\b", voice):
        speak("Hangi konu hakkında bilgi almak istersin?")
        topic = record()
        if topic:
            search_wikipedia(topic)
        else:
            speak("Herhangi bir konu söylemedin.")
    else:
        speak("Bu komutu anlamadım. Lütfen tekrar eder misin?")

# Gün bilgisi
def check_day():
    days = {
        "Monday": "Pazartesi",
        "Tuesday": "Salı",
        "Wednesday": "Çarşamba",
        "Thursday": "Perşembe",
        "Friday": "Cuma",
        "Saturday": "Cumartesi",
        "Sunday": "Pazar"
    }
    today = datetime.now().strftime("%A")
    return days.get(today, "Bilinmeyen bir gün")

# Konuşma fonksiyonu
def speak(string):
    tts = gTTS(text=string, lang="tr")
    file = "answer.mp3"
    tts.save(file)
    playsound(file)
    os.remove(file)

# Not alma fonksiyonu
def take_note():
    speak("Dosya ismi ne olsun?")
    filename = record()
    if filename:
        filename += ".txt"
        speak("Lütfen kaydetmek istediğin şeyleri söyle.")
        content = record()
        if content:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            speak(f"Notun {filename} ismiyle kaydedildi.")
        else:
            speak("Kaydedilecek bir şey söylemedin.")
    else:
        speak("Dosya ismi belirtmedin.")

# Şaka yapma fonksiyonu
def tell_joke():
    jokes = [
        "Adamın biri doktora gitmiş, doktor yok demiş.",
        "Dün gece bir şaka düşündüm ama sabah kalkınca unutmuşum. Ama hala komikti.",
        "İki balık karşılaşmış, biri diğerine selam demiş, diğeri şaşırmış: Balıklar konuşamaz ki!"
    ]
    joke = random.choice(jokes)
    speak(joke)

# Wikipedia'da arama fonksiyonu
def search_wikipedia(topic):
    wikipedia.set_lang("tr")  # Türkçe dil desteği
    try:
        result = wikipedia.summary(topic, sentences=2)  # İlk 2 cümlelik özet
        speak(f"{topic} hakkında şunları buldum: {result}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("Bu konuda birden fazla sonuç var. Daha spesifik olabilir misin?")
    except wikipedia.exceptions.PageError:
        speak("Maalesef bu konu hakkında bir şey bulamadım.")
    except Exception as e:
        speak(f"Bir hata oluştu: {e}")

# Ana döngü
if __name__ == "__main__":
    playsound("HOME.mp3")  # Açılış sesi
    while True:
        voice = record()
        if voice:
            voice = voice.lower()
            print(f"Komut: {voice}")
            response(voice)
