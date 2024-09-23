import time

import pyperclip
import streamlit as st

from password_generator import (
    MemorablePasswordGenerator,
    PinCodeGenerator,
    RandomPasswordGenerator,
)

st.image("./images/password-generator-dashboard.jpg")
st.title(":zap: Password Generator")

option = st.radio(
    "**Select a password generator:**",
    ("Memorable password", "Random password", "Pin code password"),
    index=None,
)

st.divider()

if option == "Memorable password":
    st.write("##### All of the below inputs are optional")
    length = st.slider("Select the length of the Memorable password: ", 2, 10)
    capitalized_all_words = st.checkbox("Capitalize all words?")
    capitalized_randomly = st.checkbox("Capitalize random words?")
    separator = st.text_input(
        "Enter a separator (e.g., - / . \\ *):",
        placeholder="e.g. - / . \\ *",
        value="-",
    )
    vocabulary = st.text_input(
        "Enter your vocabulary (space-separated)",
        placeholder=r"e.g name name name",
    )
    if vocabulary:
        vocabulary = vocabulary.strip().split(" ")

        capitalized_randomly = None
    generator = MemorablePasswordGenerator(
        num_of_words=length,
        capitalized_all_words=False if capitalized_randomly else capitalized_all_words,
        capitalized_randomly=False if capitalized_all_words else capitalized_randomly,
        separator=separator,
        vocabulary=vocabulary if vocabulary else None,
    )
elif option == "Random password":
    st.write("##### All of the below inputs are optional")
    length = st.slider("Select the length of the Random password: ", 8, 100)
    include_number = st.checkbox("Include numbers?")
    include_symbols = st.checkbox("Include symbols")
    generator = RandomPasswordGenerator(
        length=length, include_number=include_number, include_symbol=include_symbols
    )
elif option == "Pin code password":
    st.write("##### All of the below inputs are optional")
    length = st.slider("Select the length of the pin code: ", 4, 32)
    generator = PinCodeGenerator(length=length)
else:
    st.write("### `Please select a password generator` ")


if option:
    password = generator.generate()
    st.write(rf"Your password ``` {password} ``` ")

    if st.button("Copy"):
        pyperclip.copy(password)
        alert = st.success("Text copied successfully!", icon="✅")
        time.sleep(3)
        alert.empty()
