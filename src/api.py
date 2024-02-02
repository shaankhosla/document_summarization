import os
from pathlib import Path
from typing import Annotated, Any

import numpy as np
import openai  # type: ignore
from dotenv import load_dotenv  # type: ignore
from litestar import Litestar, post  # type: ignore  # type: ignore
from litestar.config.cors import CORSConfig  # type: ignore
from litestar.enums import RequestEncodingType  # type: ignore
from litestar.params import Body  # type: ignore
from retry import retry  # type: ignore
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances_argmin_min

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

cors_config = CORSConfig(
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@retry(tries=3, delay=2, backoff=2)
def _get_text_generation(prompt: str) -> str:
    """Call OpenAI API to generate text

    :param prompt: Any prompt
    :type prompt: str
    :return: GPT-4 Output
    :rtype: str
    """

    messages = [
        {
            "role": "system",
            "content": "You are an expert document summarizer.",
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    input_dict = {
        "model": "gpt-4",
        "messages": messages,
    }
    response = openai.ChatCompletion.create(
        **input_dict,
    )
    return response["choices"][0]["message"]["content"]


def get_summary(text: str) -> str:
    if (
        len(text.split()) < 1000
    ):  # This is arbitrary. This could be better done by using tiktoken to estimate token lengths
        print("Summarizing small document", flush=True)
        prompt = f"Please summarize this text:\n\n{text}"
        return _get_text_generation(prompt)

    print("Summarizing large documents", flush=True)
    chunks = text.split("\n")
    key_chunks, labels = cluster_text_chunks(chunks)
    key_chunks = [x.strip() for x in key_chunks if x.strip != ""]

    return _get_text_generation("\n".join(key_chunks))


def cluster_text_chunks(text_chunks: list[str], n_clusters=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(text_chunks)

    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(X)

    closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X)
    key_chunks = np.array(text_chunks)[closest]

    return key_chunks, kmeans.labels_


@post(path="/summarize")
async def summarize(
    data: Annotated[dict[str, Any], Body(media_type=RequestEncodingType.MULTI_PART)],
) -> str:
    upload_directory = "/data/"
    Path(upload_directory).mkdir(parents=True, exist_ok=True)

    file = data["file"]
    contents = await file.read()
    contents = contents.decode()

    summary = get_summary(contents)
    return summary


app = Litestar(
    route_handlers=[
        summarize,
    ],
    cors_config=cors_config,
)
