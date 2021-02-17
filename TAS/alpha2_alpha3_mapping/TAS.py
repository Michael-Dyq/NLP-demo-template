from typing import Text

class CogCompTAS():
    alpha2ToAlpha3 = {"aa": "aar", "ab": "abk", "af": "afr", "ak": "aka", "am": "amh", "ar": "ara", "an": "arg", "as": "asm", "av": "ava", "ae": "ave", "ay": "aym", "az": "aze", "ba": "bak", "bm": "bam", "be": "bel", "bn": "ben", "bi": "bis", "bo": "bod", "bs": "bos", "br": "bre", "bg": "bul", "ca": "cat", "cs": "ces", "ch": "cha", "ce": "che", "cu": "chu", "cv": "chv", "kw": "cor", "co": "cos", "cr": "cre", "cy": "cym", "da": "dan", "de": "deu", "dv": "div", "dz": "dzo", "el": "ell", "en": "eng", "eo": "epo", "et": "est", "eu": "eus", "ee": "ewe", "fo": "fao", "fa": "fas", "fj": "fij", "fi": "fin", "fr": "fra", "fy": "fry", "ff": "ful", "gd": "gla", "ga": "gle", "gl": "glg", "gv": "glv", "gn": "grn", "gu": "guj", "ht": "hat", "ha": "hau", "sh": "hbs", "he": "heb", "hz": "her", "hi": "hin", "ho": "hmo", "hr": "hrv", "hu": "hun", "hy": "hye", "ig": "ibo", "io": "ido", "ii": "iii", "iu": "iku", "ie": "ile", "ia": "ina", "id": "ind", "ik": "ipk", "is": "isl", "it": "ita", "jv": "jav", "ja": "jpn", "kl": "kal", "kn": "kan", "ks": "kas", "ka": "kat", "kr": "kau", "kk": "kaz", "km": "khm", "ki": "kik", "rw": "kin", "ky": "kir", "kv": "kom", "kg": "kon", "ko": "kor", "kj": "kua", "ku": "kur", "lo": "lao", "la": "lat", "lv": "lav", "li": "lim", "ln": "lin", "lt": "lit", "lb": "ltz", "lu": "lub", "lg": "lug", "mh": "mah", "ml": "mal", "mr": "mar", "mk": "mkd", "mg": "mlg", "mt": "mlt", "mn": "mon", "mi": "mri", "ms": "msa", "my": "mya", "na": "nau", "nv": "nav", "nr": "nbl", "nd": "nde", "ng": "ndo", "ne": "nep", "nl": "nld", "nn": "nno", "nb": "nob", "no": "nor", "ny": "nya", "oc": "oci", "oj": "oji", "or": "ori", "om": "orm", "os": "oss", "pa": "pan", "pi": "pli", "pl": "pol", "pt": "por", "ps": "pus", "qu": "que", "rm": "roh", "ro": "ron", "rn": "run", "ru": "rus", "sg": "sag", "sa": "san", "si": "sin", "sk": "slk", "sl": "slv", "se": "sme", "sm": "smo", "sn": "sna", "sd": "snd", "so": "som", "st": "sot", "es": "spa", "sq": "sqi", "sc": "srd", "sr": "srp", "ss": "ssw", "su": "sun", "sw": "swa", "sv": "swe", "ty": "tah", "ta": "tam", "tt": "tat", "te": "tel", "tg": "tgk", "tl": "tgl", "th": "tha", "ti": "tir", "to": "ton", "tn": "tsn", "ts": "tso", "tk": "tuk", "tr": "tur", "tw": "twi", "ug": "uig", "uk": "ukr", "ur": "urd", "uz": "uzb", "ve": "ven", "vi": "vie", "vo": "vol", "wa": "wln", "wo": "wol", "xh": "xho", "yi": "yid", "yo": "yor", "za": "zha", "zh": "zho", "zu": "zul"}
    alpha3ToAlpha2 = {"aar": "aa", "abk": "ab", "afr": "af", "aka": "ak", "amh": "am", "ara": "ar", "arg": "an", "asm": "as", "ava": "av", "ave": "ae", "aym": "ay", "aze": "az", "bak": "ba", "bam": "bm", "bel": "be", "ben": "bn", "bis": "bi", "bod": "bo", "bos": "bs", "bre": "br", "bul": "bg", "cat": "ca", "ces": "cs", "cha": "ch", "che": "ce", "chu": "cu", "chv": "cv", "cor": "kw", "cos": "co", "cre": "cr", "cym": "cy", "dan": "da", "deu": "de", "div": "dv", "dzo": "dz", "ell": "el", "eng": "en", "epo": "eo", "est": "et", "eus": "eu", "ewe": "ee", "fao": "fo", "fas": "fa", "fij": "fj", "fin": "fi", "fra": "fr", "fry": "fy", "ful": "ff", "gla": "gd", "gle": "ga", "glg": "gl", "glv": "gv", "grn": "gn", "guj": "gu", "hat": "ht", "hau": "ha", "hbs": "sh", "heb": "he", "her": "hz", "hin": "hi", "hmo": "ho", "hrv": "hr", "hun": "hu", "hye": "hy", "ibo": "ig", "ido": "io", "iii": "ii", "iku": "iu", "ile": "ie", "ina": "ia", "ind": "id", "ipk": "ik", "isl": "is", "ita": "it", "jav": "jv", "jpn": "ja", "kal": "kl", "kan": "kn", "kas": "ks", "kat": "ka", "kau": "kr", "kaz": "kk", "khm": "km", "kik": "ki", "kin": "rw", "kir": "ky", "kom": "kv", "kon": "kg", "kor": "ko", "kua": "kj", "kur": "ku", "lao": "lo", "lat": "la", "lav": "lv", "lim": "li", "lin": "ln", "lit": "lt", "ltz": "lb", "lub": "lu", "lug": "lg", "mah": "mh", "mal": "ml", "mar": "mr", "mkd": "mk", "mlg": "mg", "mlt": "mt", "mon": "mn", "mri": "mi", "msa": "ms", "mya": "my", "nau": "na", "nav": "nv", "nbl": "nr", "nde": "nd", "ndo": "ng", "nep": "ne", "nld": "nl", "nno": "nn", "nob": "nb", "nor": "no", "nya": "ny", "oci": "oc", "oji": "oj", "ori": "or", "orm": "om", "oss": "os", "pan": "pa", "pli": "pi", "pol": "pl", "por": "pt", "pus": "ps", "que": "qu", "roh": "rm", "ron": "ro", "run": "rn", "rus": "ru", "sag": "sg", "san": "sa", "sin": "si", "slk": "sk", "slv": "sl", "sme": "se", "smo": "sm", "sna": "sn", "snd": "sd", "som": "so", "sot": "st", "spa": "es", "sqi": "sq", "srd": "sc", "srp": "sr", "ssw": "ss", "sun": "su", "swa": "sw", "swe": "sv", "tah": "ty", "tam": "ta", "tat": "tt", "tel": "te", "tgk": "tg", "tgl": "tl", "tha": "th", "tir": "ti", "ton": "to", "tsn": "tn", "tso": "ts", "tuk": "tk", "tur": "tr", "twi": "tw", "uig": "ug", "ukr": "uk", "urd": "ur", "uzb": "uz", "ven": "ve", "vie": "vi", "vol": "vo", "wln": "wa", "wol": "wo", "xho": "xh", "yid": "yi", "yor": "yo", "zha": "za", "zho": "zh", "zul": "zu"}
    
    # Initialization
    def __init__(self, text="", lang="eng"):
        '''
        Create a TA schema for a document for a given language and with a textual content
        Language must be validated against a list of Alpha-2 / Alpha-3 codes
        Only Alpha-3 code will be stored
        Text cannot be None, but it can eventually be empty ("")
        '''
        self.text = text
        self.lang = self.langReader(lang)

    def getText(self):
        '''
        Return the text of the TAS Object
        '''
        return self.text

    
    def langReader(self, lang):
        '''
        Check if the languge is valid
        '''
        if lang.lower() in self.alpha2ToAlpha3:
            return self.alpha2ToAlpha3[lang]
        
        elif lang.lower() in self.alpha3ToAlpha2:
            return lang

        else:
             return "eng"

    # Language
    def getLang(self):
        return self.lang

    def getLangAlpha3(self):
        return self.lang

    def getLangAlpha2(self):
        return self.alpha3ToAlpha2[self.lang]

    def getDCTS(self):
        pass

    def setDCTS(self):
        pass

if __name__ == "__main__":
    TAS1 = CogCompTAS('I like sushi', 'asdfas')
    print(TAS1.getLang)

    TAS2 = CogCompTAS('I like sushi', 'en')
    print(TAS2.getLang)

