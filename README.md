# Scientific Article Generator

This Streamlit application uses the Anthropic API to generate comprehensive scientific review articles based on user-provided topics and pre-loaded source articles.

## Features

- Password-protected access
- Topic-based scientific article generation
- Real-time streaming of generated content
- Based on pre-loaded source articles

## Requirements

- Python 3.7+
- Streamlit
- Langchain
- Anthropic API key

## Installation

1. Clone this repository:

```bash
git clone https://github.com/shemtovsamuel/scientific-article-generator-AI.git
cd scientific-article-generator-AI
```

2. Create a virtual environment and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   Create a `.streamlit/secrets.toml` file in the project directory and add your Anthropic API key and password:

```bash
ANTHROPIC_API_KEY = "your_anthropic_api_key_here"
PASSWORD = "your_chosen_password_here"
```

5. Prepare your source articles:
   Place your source articles in the `articles` directory as `article1.txt`, `article2.txt`, and `article3.txt`.

## Usage

1. Run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

2. Open the provided URL in your web browser.

3. Enter the password to access the application.

4. Input your desired topic and click "Generate Article" to create a scientific review article.

## Customization

- Modify the `prompt` template in `app.py` to adjust the article generation instructions.
- Update the source articles in the `articles` directory to change the reference material for generation.

By Samuel Shemtov
