from dash import dcc, html
from dash_holoniq_wordcloud import DashWordcloud
import plotly.graph_objects as go
from wordcloud import WordCloud
import pandas as pd
import re
from nltk.corpus import stopwords
import nltk
import jbi100_app.views.colors as clrs

class WordsCloud(html.Div):
    def __init__(self, name, title, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        # for now, I put this into it, it can also be installed with
        # python -m nltk.downloader stopwords
        nltk.download("stopwords")

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                html.H6(title),
                html.Img(id=self.html_id)
            ],
        )
        
        

    def update(self, neighbourhood=None):

        # get the relevant data
        if neighbourhood is not None:
            filter = self.df[
                    (self.df.neighbourhood_group == neighbourhood)
                    | (self.df.neighbourhood == neighbourhood)
                    ]
        else:
            filter = self.df

        # count the frequency of the words and choose the 30 most common
        t = self.get_text(filter).split()
        freqs = nltk.FreqDist(t)
        x = freqs.most_common(30)
        boo = {k: v for k,v in x}

        # create a wordcloud
        wc = WordCloud(background_color=clrs.card_colour, width=300, height=360)
        wc.fit_words(boo)

        return wc.to_image()

    def get_text(self, df):

        # join all names in the data together
        text = ' '.join(df["name"].astype(str))

        # remove stop words, special symbols, punctuation, and extra spaces
        pattern = re.compile(r'\b(' + r'|'.join(stopwords.words('english')) + r')\b\s*')
        new_text = pattern.sub('', text)
        x = re.sub("w[^A-Za-z0-9 \n\.]", "", new_text)
        final_text = re.sub("[^A-Za-z0-9 \n\.]", "", x)
        really_final_text = re.sub(" +", " ", final_text)

        # finally, set everything to lowercase
        really_final_text.lower()

        return really_final_text
        

