from .schemas import InputBase
import os
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pickle

current_directory = os.path.dirname(os.path.realpath(__file__))
playstore_model_path = os.path.join(current_directory, 'ml-model', 'model_playstore_v2.h5')
youtube_model_path = os.path.join(current_directory, 'ml-model', 'model_youtube_v1.h5')
news_model_path = os.path.join(current_directory, 'ml-model', 'model_news_v2.h5')

# Load the model from the .pkl file
# with open(news_model_path, 'rb') as file:
#     loaded_model = pickle.load(file)

MAX_LENGTH = 200

class PredictionService:
  def __init__(self):
    self.playstore_model = load_model(playstore_model_path, compile=False)
    self.youtube_model = load_model(youtube_model_path, compile=False)
    self.news_model = load_model(news_model_path, compile=False)
    self.tokenizer = Tokenizer()
  
  def playstore_predict(self, data: InputBase):
    # Convert to a sequence
    sequences = self.tokenizer.texts_to_sequences(data.sentence)
    # Pad the sequence
    padded = pad_sequences(sequences, padding='post', maxlen=MAX_LENGTH)
    predictions = self.playstore_model.predict(padded)
    if predictions[0] >= 0.5:
      sentiment = "Positive"
    else:
      sentiment = "Negative"
    return {
      'status': 'success',
      'input': data.sentence,
      'sentiment': sentiment
    }
  
  def youtube_predict(self, data: InputBase):
    # Convert to a sequence
    sequences = self.tokenizer.texts_to_sequences(data.sentence)
    # Pad the sequence
    padded = pad_sequences(sequences, padding='post', maxlen=MAX_LENGTH)
    predictions = self.youtube_model.predict(padded)
    if predictions[0] >= 0.5:
      sentiment = "Positive"
    else:
      sentiment = "Negative"
    return {
      'status': 'success',
      'input': data.sentence,
      'prediction': sentiment
    }
  
  def news_predict(self, data: InputBase):
    # Convert to a sequence
    sequences = self.tokenizer.texts_to_sequences(data.sentence)
    # Pad the sequence
    padded = pad_sequences(sequences, padding='post', maxlen=MAX_LENGTH)
    predictions = self.news_model.predict(padded)
    if predictions[0] >= 0.5:
      sentiment = "Positive"
    else:
      sentiment = "Negative"
    return {
      'status': 'success',
      'input': data.sentence,
      'prediction': sentiment
    }
