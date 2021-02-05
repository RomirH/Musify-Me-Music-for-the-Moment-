from analyzer import AnalyzeTone
from speech_to_text import SpeechToText

if __name__ == "__main__":
    rt = AnalyzeTone("This is a test sentence. Why isn't this working.")
    rt.analyze()
    print(rt.result())
    SpeechToText()