import streamlit as st  # to develop and friendly interfaces for web applications
from scraper import scrape_website, split_dom_content, clean_body, extract_body  # util functions to scrape web_site
# from scraper module
from parser import parse_with_AI  # to integrate AI in the project from parser module

st.title("AI Web Scraper")  # set title of application

url = st.text_input("Enter a Website URL: ")  # ask for a URL input to scrape

if st.button("Scrape site"):  # button to scrape the URL
    st.write("Scraping website...")  # if you press the button then this message appears
    result = scrape_website(url)  # we scrape de URL website
    body_content = extract_body(result)  # extract body from website
    cleaned_content = clean_body(body_content)  # clean content
    st.session_state.dom_content = cleaned_content  # this store cleaned data in dom_content

    with st.expander("View DOM Content"):  # creates expandable section in the app
        st.text_area("DOM Content", cleaned_content, height=300)  # this creates space where users can view or edit text

if "dom_content" in st.session_state:  # if we have content in the session
    parse_description = st.text_area("Describe what you want to parse")  # then we ask for a prompt

    if st.button("Parse Content"):  # we create a button to activate the parse
        if parse_description:  # if we have a parse description then
            st.write("Parsing the content")  # we write a message

            dom_chunks = split_dom_content(st.session_state.dom_content)  # we split content into chunks (this is needed
            # to prompt the data into our LLM because often they support a certain amount of tokens
            # therefore, if we have a big prompt then we need to chunk the prompt to not exceed that tokes capacity
            result = parse_with_AI(dom_chunks, parse_description)  # parse the data with LLM model
            st.write(result)  # write the result in app
