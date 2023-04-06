import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import base64


# Load the data
url = 'v5.csv'
df = pd.read_csv(url)  # Replace "your_data.csv" with the name of your data file

# # set the page configuration
# st.set_page_config(page_title="My Streamlit App", page_icon="🚀", layout="centered")

# # add a background color
# st.markdown(
#     """
#     <style>
#     body {
#         background-image: url("C:/Users/avaidya1/Pictures/ABC.png");
#         background-repeat: no-repeat;
#         background-size: cover;
#         background-position: center;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# Load background image
background_image = Image.open("C:/Users/avaidya1/Pictures/ABC.png")
# Set app background image
page_bg_img = '''
<style>
body {
background-image: url("data:image/png;base64,%s");
background-size: cover;
}
</style>
''' % base64.b64encode(open("C:/Users/avaidya1/Pictures/ABC.png", 'rb').read()).decode()

st.markdown(page_bg_img, unsafe_allow_html=True)


# Create a sidebar with a dropdown for selecting the condition
condition_list = df["condition"].unique().tolist()
# selected_condition = st.sidebar.selectbox("Select Condition", condition_list)
st.sidebar.markdown("<b><i>Select Medical Condition</i></b>", unsafe_allow_html=True)
selected_condition = st.sidebar.selectbox("", condition_list)



# Set the background color of the sidebar to blue
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        background-color: #D4D4D4;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Create tabs
tabs = st.tabs(["📈 basis: Most No. of Reviews", "🗃 basis: Highest Useful Count"])

# Display the results in the "Data" tab
with tabs[0]:
    st.subheader("Drug Suggestions :)")

    # Split the tab into two columns
    col1, col2 = st.columns(2)

    # Filter the data based on the selected condition
    filtered_df = df[df["condition"] == selected_condition]

    # Check if the filtered dataframe only has "neu" values
    if filtered_df["NRCsent"].nunique() == 1 and filtered_df["NRCsent"].unique()[0] == "neu":
        only_available_drug = filtered_df["drugName"].iloc[0]
        st.write("Only Available Drug:")
        st.write("- " + only_available_drug)
    else:
        # Filter the data for positive and negative sentiments
        positive_df = filtered_df[filtered_df["NRCsent"] == "positive"]
        negative_df = filtered_df[filtered_df["NRCsent"] == "negative"]

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

        # Display the results
        with col1:
            st.write("<b><span style='font-size: 16pt;'>Most Loved Drug(s):</span></b>", unsafe_allow_html=True)
            if len(most_recommended_drugs_pos) > 1:
                st.write("There are multiple drugs:")
                for drug in most_recommended_drugs_pos:
                    st.success(drug)
            else:
                st.success(most_recommended_drug_pos)
        
        with col2:
            st.write("<b><span style='font-size: 16pt;'>Least Loved Drug(s):</span></b>", unsafe_allow_html=True)
            if len(least_recommended_drugs_neg) > 1:
                st.write("There are multiple drugs:")
                for drug in least_recommended_drugs_neg:
                    st.info(drug)
            else:
                st.info(least_recommended_drug_neg)
        
        
        
        

# Display the chart in the "Chart" tab
with tabs[1]:
    st.subheader("Drug Reviews")
    # Filter the data based on the selected condition
    filtered_df = df[df["condition"] == selected_condition]

# Check if the filtered dataframe only has "neu" values
    if filtered_df["NRCsent"].nunique() == 1 and filtered_df["NRCsent"].unique()[0] == "neu":
        only_available_drug = filtered_df["drugName"].iloc[0]
        st.write("Only Available Drug:")
        st.write("- " + only_available_drug)
    else:
    # Filter the data for positive and negative sentiments
        positive_df = filtered_df[filtered_df["NRCsent"] == "positive"]
        negative_df = filtered_df[filtered_df["NRCsent"] == "negative"]

        # Get the drugName(s) with the most number of observations for positive and negative sentiments
        most_useful_drug_pos = positive_df.loc[positive_df["Useful"].idxmax(), "drugName"]
        most_useful_drug_neg = negative_df.loc[negative_df["Useful"].idxmax(), "drugName"]

        # Get the patient review and review date for the most useful drugs
        pos_review = positive_df.loc[positive_df["Useful"].idxmax(), "patientreview"]
        pos_review_date = positive_df.loc[positive_df["Useful"].idxmax(), "reviewdate"]
        neg_review = negative_df.loc[negative_df["Useful"].idxmax(), "patientreview"]
        neg_review_date = negative_df.loc[negative_df["Useful"].idxmax(), "reviewdate"]
        
        
        def generate_wordcloud(text):
            # Set the maximum font size to 50
            wordcloud = WordCloud(max_font_size=50, width=800, height=400).generate(text)
            plt.figure(figsize=(16,8))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot()

        # # Display the results
        # st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Most Useful Drug Review:</h5>", unsafe_allow_html=True)
        # st.success("- Drug Name: " + most_useful_drug_pos)
        # st.success("- Review Date: "+ pos_review_date)
        # st.success("Patient Review:" + pos_review)
        # # Display the word cloud for positive and negative reviews
        # with st.container():
        #     st.subheader("Word Cloud for Positive Reviews")
        #     positive_text = " ".join(positive_df["patientreview"].tolist())
        #     generate_wordcloud(positive_text)


        # st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Least Useful Drug Review</h5>", unsafe_allow_html=True)
        # st.info("- Drug Name: "+ most_useful_drug_neg)
        # st.info("- Review Date: "+ neg_review_date)
        # st.info("- Patient Review: "+ neg_review)
        # with st.container():
        #     st.subheader("Word Cloud for Negative Reviews")
        #     negative_text = " ".join(negative_df["patientreview"].tolist())
        #     generate_wordcloud(negative_text)
        
        # #for positive reviews
        # st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Most Useful Drug Review:</h5>", unsafe_allow_html=True)
        # most_useful_drug_pos_display = "- Drug Name: " + most_useful_drug_pos + "\n" + \
        #                               "- Review Date: "+ pos_review_date + "\n" + \
        #                               "Patient Review:" + pos_review
        # positive_text = " ".join(positive_df["patientreview"].tolist())
        # with st.container():
        #     st.success(most_useful_drug_pos_display)
        #     st.markdown("<hr>", unsafe_allow_html=True)
        #     st.subheader("Word Cloud for Positive Reviews")
        #     generate_wordcloud(positive_text)
        #     st.markdown("<hr>", unsafe_allow_html=True)
        
        # #for negative reviews
        # st.write("<h5 style='color: #3D59AB; font-family: Arial;'>Least Useful Drug Review</h5>", unsafe_allow_html=True)
        # most_useful_drug_neg_display = "- Drug Name: "+ most_useful_drug_neg + "\n" + \
        #                                "- Review Date: "+ neg_review_date + "\n" + \
        #                                "- Patient Review: "+ neg_review
        # negative_text = " ".join(negative_df["patientreview"].tolist())
        # with st.container():
        #     st.info(most_useful_drug_neg_display)
        #     st.markdown("<hr>", unsafe_allow_html=True)
        #     st.subheader("Word Cloud for Negative Reviews")
        #     generate_wordcloud(negative_text)
        #     st.markdown("<hr>", unsafe_allow_html=True)
        
        # Display the results
        #for positve reviews
        st.markdown("<h3 style='color: #DC143C; font-family: Arial;'>Most Useful Drug Review:</h3>", unsafe_allow_html=True)
        st.success("- **Drug Name:** " + most_useful_drug_pos)
        st.success("- **Review Date:** "+ pos_review_date)
        st.success("- **Patient Review:** " + pos_review)
        
        # Display the word cloud for positive and negative reviews
        with st.container():
            st.markdown("<h5 style='color: #8A360F; font-family: Arial;'>Word Cloud(Positive Reviews)</h5>", unsafe_allow_html=True)
            # st.subheader("Word Cloud (Positive Reviews)")
            positive_text = " ".join(positive_df["patientreview"].tolist())
            generate_wordcloud(positive_text)
        
        # Add a horizontal line to separate positive and negative reviews
        st.markdown("<hr>", unsafe_allow_html=True)
        
        #for negative reviews
        st.markdown("<h3 style='color: #DC143C; font-family: Arial;'>Least Useful Drug Review</h3>", unsafe_allow_html=True)
        st.info("- **Drug Name:** "+ most_useful_drug_neg)
        st.info("- **Review Date:** "+ neg_review_date)
        st.info("- **Patient Review:** "+ neg_review)
        
        with st.container():
            st.markdown("<h5 style='color: #8A360F; font-family: Arial;'>Word Cloud(Negative Reviews)</h5>", unsafe_allow_html=True)
            # st.subheader("Word Cloud(Negative Reviews)")
            negative_text = " ".join(negative_df["patientreview"].tolist())
            generate_wordcloud(negative_text)


  



