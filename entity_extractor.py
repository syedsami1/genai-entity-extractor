import re
import dateparser
from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")



# Load NER pipeline with updated aggregation strategy
ner_pipeline = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple",
    token=HF_TOKEN
)

# Regex pattern for common date formats
DATE_REGEX = r"\b(?:\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|" \
             r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|" \
             r"Dec(?:ember)?)(?:\s+\d{4})?|\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|" \
             r"May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|" \
             r"Dec(?:ember)?)\s+\d{1,2})\b"

def normalize_dates(date_strings):
    parsed = [dateparser.parse(d) for d in date_strings]
    return [d.strftime("%Y-%m-%d") for d in parsed if d]

def extract_entities(text):
    result = {"dates": [], "persons": []}

    # Extract entities using Hugging Face model
    entities = ner_pipeline(text)
    for ent in entities:
        label = ent["entity_group"]
        word = ent["word"].strip()

        if label == "PER":
            # Merge subword tokens
            if word.startswith("##"):
                if result["persons"]:
                    result["persons"][-1] += word[2:]
                else:
                    result["persons"].append(word[2:])
            else:
                result["persons"].append(word)

        elif label == "DATE":
            result["dates"].append(word)

    # Extract additional dates using regex
    regex_dates = re.findall(DATE_REGEX, text)
    result["dates"].extend(regex_dates)

    # Normalize all dates
    result["dates"] = normalize_dates(result["dates"])

    # Remove duplicates and clean whitespace
    result["persons"] = list(set([p.strip() for p in result["persons"]]))
    result["dates"] = list(set(result["dates"]))

    # Remove fragments already contained in longer names
    cleaned_persons = []
    for name in result["persons"]:
        if not any(name != other and name in other for other in result["persons"]):
            cleaned_persons.append(name)
    result["persons"] = cleaned_persons

    return result
