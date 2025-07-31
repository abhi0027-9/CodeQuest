
import sys
from io import StringIO
from groq import Groq

GROQ_API_KEY = "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"

def check_output_with_groq(user_output, expected_output):
    """Uses GROQ to compare user output with expected output."""
    prompt = f"""
        Evaluate the user's code against the given question.

        ### Question:
        {expected_output}

        ### User's Code:
        {user_output}

        ### Instructions:
        1. Analyze whether the user's code correctly solves the problem.
        2. If the code is correct, return: **"Correct"**.
        3. If the code is incorrect, return: **"Incorrect"**, followed by:
        - The specific mistake or issue in the code.
       
        """



    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def check_output_with_groqphp(user_output, expected_output):
    """Uses GROQ to compare user output with expected output."""
    prompt = f"""
        Evaluate the user's php code against the given question.

        ### Question:
        {expected_output}

        ### User's Code:
        {user_output}

        ### Instructions:
        1. Analyze whether the user's code correctly solves the problem.
        2. If the code is correct, return: **"Correct"**.
        3. If the code is incorrect, return: **"Incorrect"**, followed by:
        - The specific mistake or issue in the code.
       
        """



    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def check_error_with_groq(user_output, expected_output, user_code):
    """Uses GROQ to compare user output with expected output and suggest fixes."""
    prompt = f"""
     A user has written a Python program for a coding challenge. 

    **User's Code:**
    ```python
    {user_code}
    ```

    **Program's Output:**
    ```
    {user_output}
    ```

    **Expected Output:**
    ```
    {expected_output}
    ```

    Task:  
    - If the output is correct, return: "Correct! Your solution works as expected."
    - If incorrect, identify errors, explain them clearly, and suggest improvements.
    - If there is a syntax or runtime error, provide a corrected version of the code.
    - Keep the response clear and beginner-friendly."""

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def check_error_with_groq_php(user_output, expected_output, user_code):
    """Uses GROQ to compare user output with expected output and suggest fixes."""
    prompt = f"""
     A user has written a php program for a coding challenge. 

    **User's Code:**
    ```python
    {user_code}
    ```

    **Program's Output:**
    ```
    {user_output}
    ```

    **Expected Output:**
    ```
    {expected_output}
    ```

    Task:  
    - If the output is correct, return: "Correct! Your solution works as expected."
    - If incorrect, identify errors, explain them clearly, and suggest improvements.
    - If there is a syntax or runtime error, provide a corrected version of the code.
    - Keep the response clear and beginner-friendly."""

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

import os
import sys
from io import StringIO
from groq import Groq
from django.shortcuts import render

from django.contrib.auth.decorators import login_required


def analyze_code_with_groq(user_code, user_output, expected_output):
    """Uses GROQ to analyze code, detect mistakes, and assign scores."""
    prompt = f"""
    A student has attempted a coding challenge.

    **Student's Code:**
    ```python
    {user_code}
    ```

    **Student's Output:**
    ```
    {user_output}
    ```

    **question**
    ```
    {expected_output}
    ```

    Task:
    - If  correct, return: "Correct, Score: 5".
    - If there is a small mistake, explain it and return: "Partially correct, Score: X" (where X is between 1-4).
    - If there are major issues, explain them and return: "Incorrect, Score: 0".
    - If there is a syntax or runtime error, explain it and suggest corrections.

    Keep the response structured and concise.
    """

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()



def analyze_code_with_groqphp(user_code, user_output, expected_output):
    """Uses GROQ to analyze code, detect mistakes, and assign scores."""
    prompt = f"""
    A student has attempted a coding challenge.

    **Student's Code:**
    ```php
    {user_code}
    ```

    **Student's Output:**
    ```
    {user_output}
    ```

    **question**
    ```
    {expected_output}
    ```

    Task:
    - If  correct, return: "Correct, Score: 5".
    - If there is a small mistake, explain it and return: "Partially correct, Score: X" (where X is between 1-4).
    - If there are major issues, explain them and return: "Incorrect, Score: 0".
    - If there is a syntax or runtime error, explain it and suggest corrections.

    Keep the response structured and concise.
    """

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()



def check_outputcode_with_groq(user_output, expected_output):
    """Uses GROQ to compare user output with expected output."""
    prompt = f"""
        Evaluate the user's code against the output of the code.

        ### Question:
        {expected_output}

        ### User's Code:
        {user_output}

        1. Analyze whether the user's code correctly solves the problem.
        2. If the code is correct, return: **"Correct"**.
        3. If the code is incorrect, return: **"Incorrect"**, followed by:
        - The specific mistake or issue in the code.
       
        """



    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()



def check_error(user_output, user_code):
    """Uses GROQ to compare user output with expected output and suggest fixes."""
    prompt = f"""
     A user has written a Python program for a coding challenge. 

    **User's Code:**
    ```python
    {user_code}
    ```

    **Program's Output:**
    ```
    {user_output}
    ```

    **Expected Output:**
    ```

    ```

    Task:  
    - If the output is correct, return: "Correct! Your solution works as expected."
    - If incorrect, identify errors, explain them clearly, and suggest improvements.
    - If there is a syntax or runtime error, provide a corrected version of the code.
    - Keep the response clear and beginner-friendly."""

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
