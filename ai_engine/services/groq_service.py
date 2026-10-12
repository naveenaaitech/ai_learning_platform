import os
import json

from groq import Groq
from dotenv import load_dotenv

from ..schemas import InterviewResponse


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(prompt):

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_interview_questions(technology, difficulty, count):

    prompt = f"""
    Generate {count} interview questions about {technology}.

    Difficulty level: {difficulty}

    Return ONLY valid JSON.

    The JSON must follow this structure:

    {{
        "technology": "{technology}",
        "difficulty": "{difficulty}",
        "questions": [
            {{
                "question": "Question text",
                "topic": "Topic name",
                "difficulty": "{difficulty}"
            }}
        ]
    }}

    Rules:
    - Generate exactly {count} questions.
    - Questions must be suitable for the requested difficulty.
    - Questions must be technically relevant to {technology}.
    - Do not include answers.
    - Avoid duplicate questions.
    - Return only JSON.
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        response_format={
            "type": "json_object"
        },
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content

    data = json.loads(content)

    validated_data = InterviewResponse.model_validate(data)

    return validated_data.model_dump()