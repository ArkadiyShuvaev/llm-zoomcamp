import os
import uuid
import json
import boto3

session = boto3.Session(profile_name="private")
bedrock_runtime = session.client("bedrock-runtime", region_name="us-east-1")

# def ask_llm(
#     openai_model_name: str, messages: list[dict], mock_answer: bool = False
# ) -> str:
#     if not mock_answer:
#         response = (
#             client.chat.completions.create(
#                 model=openai_model_name, messages=messages, max_tokens=150
#             )
#             .choices[0]
#             .message.content.strip()
#         )
#     else:
#         response = "hello" + str(uuid.uuid4())
#     return response


def ask_llm(model_name: str = "amazon.titan-text-lite-v1", messages: list[dict] = [], mock_answer: bool = False) -> str:

    if mock_answer is True:
        return f"Hello {str(uuid.uuid4())}"

    prompt = messages[0]["content"]

    # # model = "amazon.titan-text-express-v1"
    # model = "amazon.titan-text-premier-v1:0"
    # model_name = "amazon.titan-text-lite-v1"

    kwargs = {
        "modelId": model_name,
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 500,
                    "stopSequences": [],
                    "temperature": 0.9,
                    "topP": 0.9,
                },
            }
        ),
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    body_as_plain_text = response.get("body").read()
    response_body = json.loads(body_as_plain_text)

    result = response_body["results"][0]["outputText"]

    return result.strip()


def build_prompt(query: str, search_results: list[str]) -> str:
    prompt_template = """
        You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
        Use only the facts from the CONTEXT when answering the QUESTION.

        QUESTION: {question}

        CONTEXT: 
        {context}
        """.strip()

    context = ""

    for search_result in search_results:
        context = context + f"{search_result}\n\n"

    prompt = prompt_template.format(question=query, context=context).strip()
    return prompt
