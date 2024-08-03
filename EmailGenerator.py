from LinkedIn import scrape_linkedin_profile
import streamlit as st
from openai import OpenAI


client = OpenAI(
    # This is the default and can be omitted
    api_key=st.secrets["api_key"],
)


def list_to_string(my_list, separator=", "):
    return separator.join(map(str, my_list))

def return_goodFormat(text_block):
    # Strip the 'TextBlock(text="' prefix and the trailing part
    text = text_block[len('TextBlock(text="'):-len('",type="text")')]

    # Replace the escaped newline characters with actual newlines
    formatted_text = text.replace('\\n\\n', '\n\n').replace('\\n', '\n')

    return formatted_text


def submit_prompt(prompt, system_prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        stop=None,
        temperature=0,
    )
    return response.choices[0].message.content

def generate_email(profile_data, email_tone, num_words, email_context, feedback=""):
    prompt = "ok"
    system_prompt = f"""
      When the user enter "ok" RUN the following prompt:
        <instruction>
        You are a Email Generator, your only goal is to formulate a clear email with its subject based on the following attributes:
        Candidate Information: provided a scraped linkedin profile as a json format of the candidate : {profile_data}
        The Email Tone : {email_tone}
        Number of words: {num_words}
        The Email Context: {email_context}
        Additional Feedback: {feedback}
        </instruction>
        <rules>
        Rule 1: Your output must be an Email and an Email ONLY!
        Rule 2: Do not engage with the user with any sort of conversation, just output the email.
        Rule 3: If additional feedback is provided, adjust the email accordingly.
        </rules> """
    return submit_prompt(prompt, system_prompt)

if __name__ == "__main__":
    
    # Title of the webpage
    st.title("Email Generator")

    # Text input for LinkedIn URL   
    linkedin_url = st.text_input("Enter LinkedIn URL:")
    email = st.secrets["email"]
    password = st.secrets["password"]
    name = ""
    bio = ""
    about = ""
    
    # Dropdown for email tone
    email_tone = st.selectbox(
        "Select Email Tone:",
        ["Formal", "Friendly", "Neutral"]
    )

    # Text input for number of words
    num_words = st.text_input("Enter Number of Words for Email Length:")

    # Text input for email context
    email_context = st.text_area("Enter Email Context:")

    # Button to generate email
    if st.button("Generate Email"):
        if linkedin_url:
            name, bio, about = scrape_linkedin_profile(linkedin_url, email, password)
        profile_data = {
        "name": name,
        "bio": bio,
        "about": about
        }
        generated_email = generate_email(profile_data, email_tone, num_words, email_context)
        st.session_state.generated_email = generated_email

    # Display generated email
    if 'generated_email' in st.session_state:
        st.subheader("Generated Email:")
        st.write(st.session_state.generated_email)

        # Feedback for email adjustment
        st.subheader("Feedback for Email Adjustment:")
        feedback = st.text_area("Enter your feedback to adjust the email:")

        # Button to regenerate email based on feedback
        if st.button("Regenerate Email"):
            regenerated_email = generate_email(profile_data, email_tone, num_words, email_context, feedback)
            st.session_state.generated_email = return_goodFormat(list_to_string(regenerated_email))
            st.experimental_rerun()
