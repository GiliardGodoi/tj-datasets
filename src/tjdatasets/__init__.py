import nltk
import spacy

nltk.download('punkt')
nltk.download('rslp')
nltk.download('stopwords')

if not any(model.startswith('pt') for model in spacy.util.get_installed_models()):
        spacy.cli.download('pt_core_news_lg')