import streamlit as st
from feedback_diff_app import main as feedback_diff_main
from lighting_app import parse_args

def main(args):
    # Call the main function from feedback_diff_app.py with our args
    feedback_diff_main(args)

if __name__ == "__main__":
    args = parse_args()
    main(args) 