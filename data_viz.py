
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from plotnine import *
import numpy as np
import plotly.express as px

def main():
    st.header('Data')
    st.write('This is an interface for exploring how people discuss Covid-19 vaccine on Twitter from Aug. 1, 2020 to Feb. 28, 2021. All tweets in the dataset, collected from Brandwatch, are about covid-19 vaccine.')
    st.header('Keyword Trends')
    st.write('The following figure shows the temporal trend of the number of tweets that contain a specific keyword. You can search any keyword you are interested in. If you do not type any keyword in the box, the figure simply shows the temporal trends of all tweets.')
    st.write('Since this dataset is a sample (10%) from the whole dataset, the actual number of tweets and retweets should be 9 times more.')
    oretweet = st.selectbox('Do you want to include retweet?',
                            ('Excluding retweet', 'Including retweet'))
    yourtext = st.text_input("Please input a keyword (case insensitive). If you do not type any keyword in the box, the figure simply shows the temporal trends of all tweets." )
    data = pd.read_csv('https://raw.githubusercontent.com/khan1792/data_viz_final/main/lemm_data1.csv.gz')
    data['Date'] = pd.to_datetime(data['Date'])
    if oretweet == 'Excluding retweet':
        bbb = data[data['Full Text'].str.contains(yourtext.lower())].groupby('Date', as_index=False).count()
        bbb['Date'] = pd.to_datetime(bbb['Date'])
        fig1 = px.line(bbb, x="Date", y="Twitter Retweets", title='Excluding retweets',
                       labels={
                           "Twitter Retweets": "Number of Tweets"}
                       )
    else:
        bbb = data[data['Full Text'].str.contains(yourtext.lower())].groupby('Date', as_index=False).sum('Twitter Retweets')
        bbb['Date'] = pd.to_datetime(bbb['Date'])
        fig1 = px.line(bbb, x="Date", y="Twitter Retweets", title='Including retweets',
                       labels={
                           "Twitter Retweets": "Number of Tweets"}
                       )

    st.plotly_chart(fig1)


    st.header('Tweets Sentiment')
    st.write('You can investigate tweet sentiment in this section.')
    Variable = st.selectbox('Which variable do you want to explore?',
                            ('Gender', 'Date', 'Account Type', 'Region'))
    if Variable == 'Gender':
        st.write('In this figure, male and female refer to individual account, while organization refers to organization account. Unknow means we do not know the gender of the account users.')
    iid = data[data['Gender'] == 'male'].index
    data['Gender'][iid] = 'male (individual)'
    iid = data[data['Gender'] == 'female'].index
    data['Gender'][iid] = 'female (individual)'
    p = ggplot(data[['Sentiment', Variable]].dropna(), aes(Variable, fill='Sentiment')) + \
    geom_bar(position='fill') + \
    theme(axis_text_x=element_text(rotation=90)) + \
    labs(title='Sentiment', y = 'Proportion')
    st.pyplot(ggplot.draw(p))


    st.header('Word Relations')
    st.write('You can investigate word relations here. Word relations are computed based on a word2vec model. After L2 normalization and dimension reduction, the distance in the vector space can, at least partially, represent word relations and word similarities. Closer distance implies two words have a stronger relation. Direction also matters in the vector space.')
    yourtext1 = st.text_input("Please input the keywords you are interested and use coma to separate words (case and space insensitive)", 'trump, biden, democrat, republican')
    embedding = pd.read_csv('https://raw.githubusercontent.com/khan1792/data_viz_final/main/lowdimensionresult.csv')
    a = yourtext1.lower().replace(' ','').split(',')
    fig5 = px.scatter_3d(embedding[embedding['words'].isin(a)], x="PC1", y="PC2", z="PC3", text = 'words' )
    fig5.update_traces(textposition='top center')
    fig5.update_layout(
        scene=dict(
            xaxis=dict(nticks=4, range=[-1, 1], ),
            yaxis=dict(nticks=4, range=[-1, 1], ),
            zaxis=dict(nticks=4, range=[-1,  1], ), ),
        margin=dict(r=10, l=10, b=10, t=10))
    st.plotly_chart(fig5)

    st.header('Influence of Tweets')
    st.write('In this section you can investigate the temporal trends of the influence of tweets based on a target variable you are interested in, such as gender difference. The temporal trends are fit through regression models. There are two types of regression models you can choose. The default model is generalized linear model. You can also choose locally weighted regression model by checking the box of "Non-linear fit" if you want to fit a nonlinear trends line. But it would be a little bit time-comsuming. Please uncheck this box, if you only want to explore other sections, to speed up the website lodading process.')
    data['Impact'] = data['Impact'].apply(lambda x: x + 1)
    data['Number of retweets'] = data['Twitter Retweets'].apply(lambda x: x + 1)
    Variable1 = st.selectbox('Which influence metrics do you want to explore?',
                            ('Impact', 'Number of retweets'))
    Variable2 = st.selectbox('Which variable do you want to explore?',
                             ('Gender', 'Account Type', 'Region'))
    facet = st.checkbox('Free scales')
    nonlinear = st.checkbox('Non-linear fit (time-consuming)')


    if facet:
        if nonlinear:
            p1 = ggplot(data) + \
                 geom_smooth(aes('Date', Variable1, color=Variable2), method='lowess') + \
                 theme_bw() + \
                 theme(axis_text_x=element_text(rotation=90)) + \
                 labs(title='Date', y=Variable1) + \
                 facet_wrap(Variable2, scales='free_y')
        else:
            p1 = ggplot(data) + \
                 geom_smooth(aes('Date', Variable1, color=Variable2), method='glm') + \
                 theme_bw() + \
                 theme(axis_text_x=element_text(rotation=90)) + \
                 labs(title='Date', y=Variable1) + \
                 facet_wrap(Variable2, scales='free_y')



    else:
        if nonlinear:
            p1 = ggplot(data) + \
                 geom_smooth(aes('Date', Variable1, color=Variable2), method='lowess') + \
                 theme_bw() + \
                 theme(axis_text_x=element_text(rotation=90)) + \
                 labs(title='Date', y=Variable1)
        else:
            p1 = ggplot(data) + \
                 geom_smooth(aes('Date', Variable1, color=Variable2), method='glm') + \
                 theme_bw() + \
                 theme(axis_text_x=element_text(rotation=90)) + \
                 labs(title='Date', y=Variable1)

    st.pyplot(ggplot.draw(p1))

if __name__ == "__main__":
    main()
