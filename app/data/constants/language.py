
from enum import IntEnum

class SystemLanguage(IntEnum):
    Afrikaans = 0
    Arabic = 1
    Basque = 2
    Belarusian = 3
    Bulgarian = 4
    Catalan = 5
    Chinese = 6
    Czech = 7
    Danish = 8
    Dutch = 9
    English = 10
    Estonian = 11
    Faroese = 12
    Finnish = 13
    French = 14
    German = 15
    Greek = 16
    Hebrew = 17
    Hugarian = 18
    Icelandic = 19
    Indonesian = 20
    Italian = 21
    Japanese = 22
    Korean = 23
    Latvian = 24
    Lithuanian = 25
    Norwegian = 26
    Polish = 27
    Portuguese = 28
    Romanian = 29
    Russian = 30
    SerboCroatian = 31
    Slovak = 32
    Slovenian = 33
    Spanish = 34
    Swedish = 35
    Thai = 36
    Turkish = 37
    Ukrainian = 38
    Vietnamese = 39
    Unknown = 40

    @property
    def code(self) -> str:
        return SystemLanguageCodes.get(self, 'xx')

SystemLanguageCodes = {
    SystemLanguage.Afrikaans: 'af',
    SystemLanguage.Arabic: 'ar',
    SystemLanguage.Basque: 'eu',
    SystemLanguage.Belarusian: 'be',
    SystemLanguage.Bulgarian: 'bg',
    SystemLanguage.Catalan: 'ca',
    SystemLanguage.Chinese: 'zh',
    SystemLanguage.Czech: 'cs',
    SystemLanguage.Danish: 'da',
    SystemLanguage.Dutch: 'nl',
    SystemLanguage.English: 'en',
    SystemLanguage.Estonian: 'et',
    SystemLanguage.Faroese: 'fo',
    SystemLanguage.Finnish: 'fi',
    SystemLanguage.French: 'fr',
    SystemLanguage.German: 'de',
    SystemLanguage.Greek: 'el',
    SystemLanguage.Hebrew: 'he',
    SystemLanguage.Hugarian: 'hu',
    SystemLanguage.Icelandic: 'is',
    SystemLanguage.Indonesian: 'id',
    SystemLanguage.Italian: 'it',
    SystemLanguage.Japanese: 'ja',
    SystemLanguage.Korean: 'ko',
    SystemLanguage.Latvian: 'lv',
    SystemLanguage.Lithuanian: 'lt',
    SystemLanguage.Norwegian: 'no',
    SystemLanguage.Polish: 'pl',
    SystemLanguage.Portuguese: 'pt',
    SystemLanguage.Romanian: 'ro',
    SystemLanguage.Russian: 'ru',
    SystemLanguage.SerboCroatian: 'sh',
    SystemLanguage.Slovak: 'sk',
    SystemLanguage.Slovenian: 'sl',
    SystemLanguage.Spanish: 'es',
    SystemLanguage.Swedish: 'sv',
    SystemLanguage.Thai: 'th',
    SystemLanguage.Turkish: 'tr',
    SystemLanguage.Ukrainian: 'uk',
    SystemLanguage.Vietnamese: 'vi',
    SystemLanguage.Unknown: 'xx'
}
