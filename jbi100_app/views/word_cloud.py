from dash import html
from wordcloud import WordCloud
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
            children=[html.H6(title), html.Img(id=self.html_id)],
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
        ## Applying Steven's power law
        boo = {k: v ** (1 / 0.7) for k, v in x}

        # Scale brightness from 20-100% for readability
        min_value = min(x,key=lambda item:item[1])[1]
        max_value = max(x,key=lambda item:item[1])[1]
        color = {k: int(round((v - min_value) * (100-20)/(max_value-min_value) + 20, 0)) for k, v in x}

        # create a wordcloud
        wc = WordCloud(
            background_color=clrs.card_colour,
            width=300,
            height=360,
            color_func=self.my_tf_color_func(color),
        )
        wc.fit_words(boo)

        return wc.to_image()

    def get_text(self, df):

        # join all names in the data together
        text = " ".join(df["name"].astype(str))

        # remove stop words, special symbols, punctuation, and extra spaces
        pattern = re.compile(r"\b(" + r"|".join(stopwords.words("english")) + r")\b\s*")
        new_text = pattern.sub("", text)
        x = re.sub("w[^A-Za-z0-9 \n\.]", "", new_text)
        final_text = re.sub("[^A-Za-z0-9 \n\.]", "", x)
        really_final_text = re.sub(" +", " ", final_text)

        # finally, set everything to lowercase
        really_final_text = really_final_text.lower()

        return really_final_text

    def my_tf_color_func(self, dictionary):
        def my_tf_color_func_inner(
            word, random_state=None, **kwargs
        ):
            return "hsl(0, 70%%, %d%%)" % (dictionary[word])

        return my_tf_color_func_inner
