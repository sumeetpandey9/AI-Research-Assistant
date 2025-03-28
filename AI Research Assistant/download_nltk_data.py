import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        print("NLTK data downloaded successfully.")
    except Exception as e:
        print(f"An error occurred while downloading NLTK data: {e}")

if __name__ == "__main__":
    download_nltk_data()