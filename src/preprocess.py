import re
import string
from typing import Any

import pandas as pd

STOPWORDS = {
    'i','me','my','myself','we','our','ours','ourselves','you','your','yours',
    'yourself','he','him','his','himself','she','her','hers','herself','it',
    'its','itself','they','them','their','theirs','themselves','what','which',
    'who','whom','this','that','these','those','am','is','are','was','were',
    'be','been','being','have','has','had','having','do','does','did','doing',
    'a','an','the','and','but','if','or','because','as','until','while','of',
    'at','by','for','with','about','against','between','into','through',
    'during','before','after','above','below','to','from','up','down','in',
    'out','on','off','over','under','again','further','then','once','here',
    'there','when','where','why','how','all','both','each','few','more',
    'most','other','some','such','no','nor','not','only','own','same','so',
    'than','too','very','s','t','can','will','just','don','should','now',
    'd','ll','m','o','re','ve','y','ain','aren','couldn','didn','doesn',
    'hadn','hasn','haven','isn','ma','mightn','mustn','needn','shan',
    'shouldn','wasn','weren','won','wouldn'
}

def clean_text(text: Any) -> str:
    text = str(text).lower()
    text = re.sub(r'http\S+|www\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = text.split()
    tokens = [token for token in tokens if token not in STOPWORDS and len(token) > 1]
    return ' '.join(tokens)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding='latin-1')
    df = df[['v1', 'v2']].rename(columns={'v1': 'label', 'v2': 'message'})
    df = df.drop_duplicates().reset_index(drop=True)
    df['label_encoded'] = df['label'].map({'ham': 0, 'spam': 1})
    df['cleaned'] = df['message'].apply(clean_text)
    return df


def save_processed_data(df: pd.DataFrame, path: str) -> None:
    df.to_csv(path, index=False, encoding='latin-1')


if __name__ == '__main__':
    processed = load_data('data/spam.csv')
    save_processed_data(processed, 'data/processed_spam.csv')
    print('Processed data saved to data/processed_spam.csv')
