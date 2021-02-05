from analyzer import AnalyzeTone

if __name__ == "__main__":
    rt = AnalyzeTone("This is a test sentence. Why isn't this working.")
    rt.analyze()
    print(rt.result())