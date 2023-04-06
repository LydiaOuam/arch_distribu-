import requests
import streamlit as st
import pandas as pd
import altair as alt


# Set page title and header
st.set_page_config(page_title="Voiture Sentiment Analysis", page_icon=":money_with_wings:")
st.title("Voiture Sentiment Analysis")
st.header("Visualizing Sentiment Analysis for Top News Stories")
# Set the page width to 100% to avoid horizontal scrolling


# Define the API endpoint URL
url='https://api.aylien.com/news/stories'

# Define the initial payload parameters
type_param = st.text_input('Enter type:', 'bmw')
payload = {
    'aql': f'text:({type_param}) AND language:en',
    'published_at.start': 'NOW-7DAYS/DAY',
    'published_at.end': 'NOW',
    'sort_by': 'published_at',
    'sort_direction': 'desc',
    'cursor': '*',
    'per_page': 100
}

headers = {
    'X-Application-ID': 'acec876a',
    'X-Application-Key': '419ececeb9d87be8607f81a9e05bbd9f'
}

# Fetch the data from the API
response = requests.get(url, headers=headers, params=payload)
data = response.json()

# Extract the desired fields from the API response
extracted_data = []
for article in data['stories']:
    extracted_article = {
        'type': type_param,
        'id': article['id'],
        'sentiment_body_p': article['sentiment']['body']['polarity'],
        'sentiment_body_s': article['sentiment']['body']['score'],
        'sentiment_title_p': article['sentiment']['title']['polarity'],
        'sentiment_title_s': article['sentiment']['title']['score'],
        'published': article['published_at']
    }
    extracted_data.append(extracted_article)

# Allow the user to choose the visualization type
visualization_type = st.sidebar.selectbox('Choose visualization type', ('Table', 'Line plot', 'Area plot'))

# Display the extracted data in a Streamlit table
if visualization_type == 'Table':
    table = st.table(pd.DataFrame(extracted_data))
else:
    chart_data = pd.DataFrame(extracted_data)
    chart = alt.Chart(chart_data).mark_line().encode(
        x='published',
        y='sentiment_body_s',
        color='type'
    ).properties(
        width=800,
        height=400
    )

    # Display the data as a line plot if selected
    if visualization_type == 'Line plot':
        st.altair_chart(chart)

    # Display the data as an area plot if selected
    elif visualization_type == 'Area plot':
        st.altair_chart(chart.mark_area(opacity=0.3))
