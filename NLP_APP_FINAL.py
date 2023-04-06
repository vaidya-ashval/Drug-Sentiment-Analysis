import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#import dash_core_components as dcc
#import dash_html_components as html
#from PIL import Image
import base64
st.set_option('deprecation.showPyplotGlobalUse', False)

data_file = 'v6.csv'

# Load the data
df = pd.read_csv(data_file)  # Replace "your_data.csv" with the name of your data file

st.set_page_config(layout="wide")

# Create a sidebar with a dropdown for selecting the condition
condition_list = df["condition"].unique().tolist()
condition_list.sort()  # Sort the list in ascending order
# selected_condition = st.sidebar.selectbox("Select Condition", condition_list)
st.sidebar.markdown("<b><i>SELECT A MEDICAL CONDITION</i></b>", unsafe_allow_html=True)
selected_condition = st.sidebar.selectbox("", condition_list)


def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
side_bg = "Picture7.png"
sidebar_bg(side_bg)


# Create tabs
tabs = st.tabs(["📈 General Sentiment Analysis", "🗃 Homburg et al. (2015)"])

def generate_wordcloud(text):
            # Set the maximum font size to 50
            wordcloud = WordCloud(max_font_size=50, width=400, height=200,background_color='white').generate(text)
            plt.figure(figsize=(8, 4))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot()

# Display the results in the "Data" tab
with tabs[0]:
    st.subheader("💊 Drug Suggestions for " + selected_condition)

    # Split the tab into two columns
    col1, col2 = st.columns(2)

    # Filter the data based on the selected condition
    filtered_df = df[df["condition"] == selected_condition]

    # Check if the filtered dataframe only has "neu" values
    if filtered_df["RobertaSentiment"].nunique() == 1 and filtered_df["RobertaSentiment"].unique()[0] == "Neu":
        only_available_drug = filtered_df["drugName"].iloc[0]
        st.write("Only Available Drug:")
        st.write("- " + only_available_drug)
    else:
        # Filter the data for positive and negative sentiments
        positive_df = filtered_df[filtered_df["RobertaSentiment"] == "Pos"]
        negative_df = filtered_df[filtered_df["RobertaSentiment"] == "Neg"]

        # Get the drugName(s) with the most number of observations for positive and negative sentiments
        most_recommended_drug_pos = positive_df["drugName"].value_counts().idxmax()
        least_recommended_drug_neg = negative_df["drugName"].value_counts().idxmax()

        # Check if there are multiple drugNames with the most number of observations for positive sentiment
        most_recommended_drugs_pos = positive_df["drugName"].value_counts()
        most_recommended_drugs_pos = most_recommended_drugs_pos[most_recommended_drugs_pos == most_recommended_drugs_pos.max()]
        most_recommended_drugs_pos = most_recommended_drugs_pos.index.tolist()

        # Check if there are multiple drugNames with the most number of observations for negative sentiment
        least_recommended_drugs_neg = negative_df["drugName"].value_counts()
        least_recommended_drugs_neg = least_recommended_drugs_neg[least_recommended_drugs_neg == least_recommended_drugs_neg.max()]
        least_recommended_drugs_neg = least_recommended_drugs_neg.index.tolist()

        # Display the drug suggestions with the corresponding word clouds
        with col1:
            st.write("<b><span style='font-size: 16pt;'>Most Loved Drug:</span></b>", unsafe_allow_html=True)
            if len(most_recommended_drugs_pos) > 1:
                st.success(most_recommended_drugs_pos[0])
            else:
                st.success(most_recommended_drug_pos)
            st.write("<b><span style='font-size: 16pt;'>Word Cloud for Most Loved Drug</span></b>", unsafe_allow_html=True)
            positive_text = " ".join(positive_df[positive_df["drugName"] == most_recommended_drug_pos]["patientreview"].tolist())
            generate_wordcloud(positive_text)
        
        with col2:
            st.write("<b><span style='font-size: 16pt;'>Least Loved Drug:</span></b>", unsafe_allow_html=True)
            if len(least_recommended_drugs_neg) > 1:
                st.info(least_recommended_drugs_neg[0])
            else:
                st.info(least_recommended_drug_neg)
            st.write("<b><span style='font-size: 16pt;'>Word Cloud for Least Loved Drug</span></b>", unsafe_allow_html=True)
            negative_text = " ".join(negative_df[negative_df["drugName"] == least_recommended_drug_neg]["patientreview"].tolist())
            generate_wordcloud(negative_text)

# Display the chart in the "Chart" tab
with tabs[1]:
    st.subheader("💊 Drug Suggestions for " + selected_condition+ " based on Homburg et al. (2015)")
    # Filter the data based on the selected condition
    filtered_df = df[df["condition"] == selected_condition]

    # Check if the filtered dataframe only has "neu" values
    if filtered_df["RobertaSentiment"].nunique() == 1 and filtered_df["RobertaSentiment"].unique()[0] == "neu":
        only_available_drug = filtered_df["drugName"].iloc[0]
        st.write("Only Available Drug:")
        st.write("- " + only_available_drug)
    else:
        # Filter the data for positive and negative sentiments
        positive_df = filtered_df[filtered_df["RobertaSentiment"] == "Pos"]
        negative_df = filtered_df[filtered_df["RobertaSentiment"] == "Neg"]

        # Get the drugName(s) with the most number of observations for positive and negative sentiments
        most_useful_drug_pos = positive_df.loc[positive_df["Useful"].idxmax(), "drugName"]
        most_useful_drug_neg = negative_df.loc[negative_df["Useful"].idxmax(), "drugName"]

        # Get the patient review and review date for the most useful drugs
        pos_review = positive_df.loc[positive_df["Useful"].idxmax(), "patientreview"]
        pos_review_date = positive_df.loc[positive_df["Useful"].idxmax(), "reviewdate"]
        neg_review = negative_df.loc[negative_df["Useful"].idxmax(), "patientreview"]
        neg_review_date = negative_df.loc[negative_df["Useful"].idxmax(), "reviewdate"]

     

        # Display the results
        columns = st.columns(2)
        with columns[0]:
            st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Most Useful Drug Review:</h5>", unsafe_allow_html=True)
            st.success("- Drug Name: " + most_useful_drug_pos)
            st.success("- Patient Review:\n" + pos_review)
            # Display the word cloud for positive reviews
            with st.container():
                st.subheader("Word Cloud for Positive Reviews")
                positive_text = " ".join(positive_df["patientreview"].tolist())
                generate_wordcloud(positive_text)

        with columns[1]:
            st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Least Useful Drug Review:</h5>", unsafe_allow_html=True)
            st.info("- Drug Name: " + most_useful_drug_neg)
            st.info("- Patient Review:\n" + neg_review)
            # Display the word cloud for negative reviews
            with st.container():
                st.subheader("Word Cloud for Negative Reviews")
                negative_text = " ".join(negative_df["patientreview"].tolist())
                generate_wordcloud(negative_text)
                
        
