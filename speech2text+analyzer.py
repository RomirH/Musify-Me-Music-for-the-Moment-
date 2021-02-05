from analyzer import AnalyzeTone
# from rt_speech2text import MyRecognizeCallback

if __name__ == "__main__":
    rt = AnalyzeTone("This is a test sentence. This works!")
    rt.analyze()
    print(rt.result())