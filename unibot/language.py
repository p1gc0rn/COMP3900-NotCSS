from langdetect import detect
from langdetect import DetectorFactory 
import sys

def getLang(text, set_lang):
    
    try: 
        DetectorFactory.seed = 0
        lang = detect(text)
        
        if lang in ["hi"]:
            return lang
        
        elif lang in ["ko", "zh-tw", "zh-cn"]:
            return "zh-tw" # default locale - traditional chinese
        
        return "en" # default language - english
    except:
        print("Exception:", sys.exc_info()[0])
        if set_lang == "":
            return "en" # revert to default language - en
        else:
            return set_lang # revert to previous language

if __name__ == "__main__":

    inp = input("Enter text:")
    l = getLang(inp, "")
    print("Detected language:", l)