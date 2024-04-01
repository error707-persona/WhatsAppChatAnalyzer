import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')
plt.rcParams['font.family'] = prop.get_family()

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)


#     fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    st.title('Top Statistics')
    col1,col2,col3,col4 = st.columns(4, gap="large")
    # st.sidebar.button("Show Analysis")
    num_messages, words, num_media, num_links = helper.fetch_stats(selected_user, df)
    with col1:

        st.subheader("Total Messages")
        st.title(num_messages)

    with col2:
        st.header('Total Words')
        st.title(words)

    with col3:
        st.header('Total Media')
        st.title(num_media)

    with col4:
        st.header('Links Shared')
        st.title(num_links)

    # timeline


    if selected_user == 'Overall':

        x, new_df = helper.fetch_most_active_users(df)
        fig, ax = plt.subplots()
        st.header('Most Active Users')
        col1, col2 = st.columns(2)


        with col1:

            ax.bar(x.index, x.values, color='green')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:

            st.dataframe(new_df)
            # ax.bar(new_df['name'], new_df['percent'], color='blue')
            # plt.xticks(rotation='vertical')
            # st.pyplot(fig)

#         worlcloud
    st.title('Word Cloud')



    df_wc = helper.create_word_cloud(selected_user, df)
    fig, ax = plt.subplots()
    plt.imshow(df_wc)
    st.pyplot(fig)

#     Most Common Words
    st.title('Most Common Words Count')
    most_common_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    # horizontal bar chart
    ax.barh(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

#     emoji analysis
    emoji_df = helper.emoji_analyser(selected_user, df)
    st.title('Emoji Usage')
    col1,col2 = st.columns(2)
    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
        st.pyplot(fig)




