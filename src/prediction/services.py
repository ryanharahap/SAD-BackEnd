from typing import List
from .schemas import PlaystoreRequest, YoutubeRequest, NewsRequest
import os
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle
import nltk
from nltk.corpus import stopwords
import re
import pandas as pd

current_directory = os.path.dirname(os.path.realpath(__file__))
playstore_model_path = os.path.join(current_directory, 'ml-model', 'model_playstore_v2.h5')
youtube_model_path = os.path.join(current_directory, 'ml-model', 'model_youtube_v1.h5')
news_model_path = os.path.join(current_directory, 'ml-model', 'model_news_v2.h5')

# Load the model from the .pkl file
# with open(news_model_path, 'rb') as file:
#     loaded_model = pickle.load(file)

class PredictionService:
  def __init__(self):
    nltk.download('punkt')
    nltk.download('stopwords')
    self.playstore_model = load_model(playstore_model_path, compile=False)
    self.youtube_model = load_model(youtube_model_path, compile=False)
    self.news_model = load_model(news_model_path, compile=False)
    self.tokenizer = Tokenizer()
  
  def playstore_predict(self, data: List[PlaystoreRequest]):
    result = []

    for datum in data:
      # Convert to a sequence
      sequences = self.tokenizer.texts_to_sequences([datum.review])
      # Pad the sequence
      padded = pad_sequences(sequences, padding='post', maxlen=200)
      prediction = self.playstore_model.predict(padded)
      pred_label = 1 if prediction >= 0.5 else 0
      sentiment = "Positive" if pred_label == 1 else "Negative"
        
      result.append({
        "user": datum.user,
        "review": datum.review,
        "score": datum.score,
        "thumbs_up_count": datum.thumbs_up_count,
        "submitted_at": datum.submitted_at,
        "sentiment": sentiment
      })

    return {
      'status': 'success',
      'predictions': result
    }
  
  def youtube_predict(self, data: List[YoutubeRequest]):
    result = []
    
    for datum in data:
      # Convert to a sequence
      self.tokenizer.fit_on_texts(datum.comment)
      sequences = self.tokenizer.texts_to_sequences(datum.comment)
      # Pad the sequence
      padded = pad_sequences(sequences, padding='post', maxlen=37)
      predictions = self.youtube_model.predict(padded)
      print(predictions)
      sentiment = "Negative" if predictions[0][0] >= 0.5 else "Positive"

      result.append({
        "author": datum.author,
        "published_at": datum.published_at,
        "updated_at": datum.updated_at,
        "like_count": datum.like_count,
        "comment": datum.comment,
        "sentiment": sentiment
      })

    return {
      'status': 'success',
      'predictions': result
    }
  
  def news_predict(self, data: List[NewsRequest]):
    result = []
    
    for datum in data:
      text_to_predict = self.__remove_symbols(datum.title)
      tokenized_text = self.__tokenized(pd.Series([text_to_predict]))
      filtered_text = self.__remove_stopwords(tokenized_text.iloc[0])

      text_seq = self.tokenizer.texts_to_sequences([filtered_text])

      text_pad = pad_sequences(text_seq, maxlen=22, padding='post')

      pred_label = self.news_model.predict(text_pad)

      sentiment = "Positive" if pred_label > 0.5 else "Negative"

      result.append({
        "title": datum.title,
        "source": datum.source,
        "link": datum.link,
        "published_date": datum.published_date,
        "sentiment": sentiment
      })

    return {
      'status': 'success',
      'predictions': result
    }

  def __remove_symbols(self, text):
    text = text.lower()
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

  def __normalize_alay(self, text, alay_dict_map):
      return ' '.join([alay_dict_map[word] if word in alay_dict_map else word for word in text.split(' ')])

  def __tokenized(self, data):
      return data.apply(nltk.word_tokenize)

  def __remove_stopwords(self, tokens):
      stop_words = set(stopwords.words('indonesian'))
      return [word for word in tokens if word not in stop_words]
