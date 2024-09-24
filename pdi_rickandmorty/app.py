import streamlit as st

def hello(name):
    return f"Hello {name}!"

def main():
    st.write(hello("World"))

if __name__ == "__main__":
    main()