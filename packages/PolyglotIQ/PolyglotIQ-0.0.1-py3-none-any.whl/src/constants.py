

SUPPORTED_LANGS = ['gu', 'eo', 'sq', 'en', 'vi', 'af', 'gd', 'yi', 'ca', 'bn', 'ne', 'tr', 'is', 'hi', 'lv', 'hu', 'tk', 'ro', 'ru', 'pa', 'it', 'jv', 'pl', 'uk', 'fr', 'ts', 'lg', 'mk', 'ilo', 'tl', 'ug', 'st', 'ay', 'az', 'id', 'be', 'th', 'gn', 'sr', 'ht', 'sw', 'ga', 'cy', 'da', 'mn', 'ml', 'lt', 'zh-CN', 'bg', 'ku', 'kk', 'ka', 'sd', 'mg', 'sk', 'si', 'eu', 'kri', 'my', 'fa', 'lb', 'bs', 'lo', 'ceb', 'ta', 'kn', 'su', 'ar', 'hr', 'he', 'nl', 'ja', 'hy', 'ko', 'el', 'fy', 'ms', 'es', 'ps', 'so', 'no', 'ur', 'la', 'et', 'pt', 'de', 'sv', 'zh-TW', 'km', 'fi', 'mr', 'am', 'uz', 'cs', 'gl', 'te', 'ky', 'sl']


class DetectionResults(object):
    def __init__ (self, text: str, language: str) -> None:
        self.text = text
        self.language_code = language

    @property
    def text(self) -> str:
        return self.text

    @property
    def language(self) -> str:
        return self.language_code
