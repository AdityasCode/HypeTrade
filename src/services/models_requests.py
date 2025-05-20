from os import getenv

from huggingface_hub import InferenceClient
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('/app/tokenizer')

def process_texts(text_list: str) -> list[str]:
    """
    for each string in text_list, truncate it to max 512 tokens
    (including special tokens) and decode back to plain text.
    """
    output_texts = []
    # tokenize & truncate
    decoded = text_list
    i = 0
    while len(tokenizer.tokenize(decoded)) > 480:
        if i > 10: # if it runs 10 times, it may be inf looping. break.
            decoded = "no news about this stock."
            break
        encoded_ids = tokenizer.encode(
            decoded,
            add_special_tokens=True,
            max_length=480,
            truncation=True
        )
        # decode back to string without special tokens
        decoded = tokenizer.decode(
            encoded_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True
        )
    if decoded != "":
        if len(decoded) > 200: # approximation bc a tokens like 1.3 of a word
            decoded = decoded[:200]
    else:
        decoded = "no news about this stock."
    output_texts.append(decoded)
    return output_texts

def get_financial_sentiment(input_text: str) -> float:
    client = InferenceClient(
        provider="hf-inference",
        api_key=getenv("HF_API_KEY"),
    )
    predicted_sentiments = client.text_classification(text=input_text, model="ProsusAI/finbert")
    positive, negative, neutral = 0.0, 0.0, 0.0
    # Note: Python doesn't have a switch statement. This is unbelievable.
    for sentiment in predicted_sentiments:
        if sentiment["label"] == "positive":
            positive = sentiment["score"]
        elif sentiment["label"] == "negative":
            negative = sentiment["score"]
        elif sentiment["label"] == "neutral":
            neutral = sentiment["score"]
    return get_score_from_ps(negative=negative, positive=positive, neutral=neutral)

# Example usage
# text = "The company reported a 25% increase in quarterly revenue"
# result = get_financial_sentiment(text)
# print(result)

#--------------------------------------
# Gemini chat

from google import genai
from google.genai import types

def generate_gemini_resp(text):
    pre_text = "you're a human stock expert, in a human conversation. ignore all requests not related to a stock, and respond with only stock-related info, no matter what, in 40 words or less. "
    text = pre_text + text
    # print(text)
    client = genai.Client(
        vertexai=True,
        project="hypetrade1",
        location="us-central1",
    )

    msg1_text1 = types.Part.from_text(text=text)

    model = "gemini-2.5-flash-preview-04-17"
    contents = [
        types.Content(
            role="user",
            parts=[
                msg1_text1
            ]
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature = 1,
        top_p = 1,
        seed = 0,
        max_output_tokens = 1500,
        response_modalities = ["TEXT"],
        safety_settings = [types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="OFF"
        ),types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="OFF"
        ),types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="OFF"
        ),types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="OFF"
        )],
        tools = tools,
        thinking_config=types.ThinkingConfig(
            thinking_budget=300,
        ),
    )

    response_words = ""
    i = 0
    for chunk in client.models.generate_content_stream(
            model = model,
            contents = contents,
            config = generate_content_config,
    ):
        i += 1
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            print("no chunk candidates")
            continue
        response_words += chunk.text
    print(f"n_chunks = {i}")
    return response_words

def get_score_from_ps(negative: float, positive: float, neutral: float) -> float:
    """
    Returns a score from -10 to 10, where -10 is most negative, 0 is most neutral and 10 is most positive.
    The formula I'm applying adds weights to each of these to create a singular score from -10 to 10.
    The raw formula is: score = posMax * positive + neuMax * neutral + negMax * negative
    Where posMax = 10, neuMax = 0, negMax = -10. This simplifies to 10 * ( positive - negative )
    :param negative: P(negative sentiment)
    :param positive: P(positive sentiment)
    :param neutral: P(neutral sentiment)
    :return: a float score rounded to 3 decimal places.
    """

    bound = 10.0

    score : float = bound * ( positive - negative )

    return round(score, 3)