from deep_translator import GoogleTranslator

class TranslatorClient:
    def __init__(self):
        self.ro_en = GoogleTranslator(source='ro', target='en')
