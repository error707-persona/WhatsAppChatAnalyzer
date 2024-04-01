from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = 0

    for message in df['message']:
        words += len(message.split())

    extractor = URLExtract()
    urls = []
    for message in df['message']:
        urls.extend(extractor.find_urls(message))

    num_media = df[df['message']=='<Media omitted>\n'].shape[0]

    return num_messages, words, num_media, len(urls)

def fetch_most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'count': 'percent', 'user': 'name'})
    return x, df

def remove_stop_words(df):
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'group_notification']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words and word.isalpha():
                words.append(word)

    return words


def create_word_cloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    newdf = pd.DataFrame(remove_stop_words(df))
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(newdf[0].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    words = remove_stop_words(df)
    word_count = pd.DataFrame(Counter(words).most_common(20))
    word_count.rename(columns={0: 'words', 1: 'count'})
    return word_count

def emoji_analyser(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    






