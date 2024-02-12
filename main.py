""" Instamagic Home Page """
import streamlit as st
import unittest
from unittest.mock import patch
import main

def purpose_select(purpose_options: str):
    """ Purpose Selection """
    purpose = st.selectbox("What is the purpose of your post?", purpose_options)
    return purpose

def other_purpose():
    """ Other Purpose option if use selects "Other" """
    other_purpose = st.text_input("Please specify the purpose of your post")
    return other_purpose

class TestMain(unittest.TestCase):

    @patch('main.st.selectbox', return_value='Test Purpose')
    def test_purpose_select(self, mock_selectbox):
        purpose_options = ['Test Purpose', 'Other']
        result = main.purpose_select(purpose_options)
        mock_selectbox.assert_called_once_with("What is the purpose of your post?", purpose_options)
        self.assertEqual(result, 'Test Purpose')

    @patch('main.st.text_input', return_value='Test Other Purpose')
    def test_other_purpose(self, mock_text_input):
        result = main.other_purpose()
        mock_text_input.assert_called_once_with("Please specify the purpose of your post")
        self.assertEqual(result, 'Test Other Purpose')

if __name__ == '__main__':
    unittest.main()
