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
        """
        Updates the word cloud based on the current settings,
        taking into account Steven's power law

        :param neighbourhood: the neighbourhood we are looking at
        """

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

        # Applying Steven's power law
        spl_frequencies = {k: v ** (1 / 0.7) for k, v in x}

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
        wc.fit_words(spl_frequencies)

        return wc.to_image()

    def get_text(self, df):
        """
        Takes all the text in the current data from the "name" attribute
        and removes all irrelevant words and symbols

        :param df: the current data
        """

        # join all names in the data together
        text = " ".join(df["name"].astype(str))

        # remove stop words, special symbols, punctuation, and extra spaces
        stpwds = re.compile(r"\b(" + r"|".join(stopwords.words("english")) + r")\b\s*")
        new_text = stpwds.sub("", text)
        without_symbols = re.sub("w[^A-Za-z0-9 \n\.]", "", new_text)
        x = re.sub("[^A-Za-z0-9 \n\.]", "", without_symbols)
        without_extra_spaces = re.sub(" +", " ", x)

        # finally, set everything to lowercase
        without_extra_spaces = without_extra_spaces.lower()

        return without_extra_spaces

    def my_tf_color_func(self, dictionary):
        def my_tf_color_func_inner(
            word, random_state=None, **kwargs
        ):
            return "hsl(202, 100%%, %d%%)" % (dictionary[word])

        return my_tf_color_func_inner
