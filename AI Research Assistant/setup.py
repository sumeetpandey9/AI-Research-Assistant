import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def download_nltk_data():
    nltk.download('punkt')
    nltk.download('stopwords')

if __name__ == "__main__":
    download_nltk_data()
    print("NLTK data downloaded successfully.")