"""Utility script to calculate distance between two sentences."""

import argparse
import os

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from scipy.spatial.distance import cosine, euclidean


class ResponseValidation:
    """Validate LLM response."""

    def __init__(self, model_path: str):
        """Initialize."""
        self._embedding_model = HuggingFaceEmbedding(model_path)

    def get_similarity_score(self, q1: str, q2: str) -> None:
        """Calculate similarity score between two strings."""
        res_vec = self._embedding_model.get_text_embedding(q1)
        ans_vec = self._embedding_model.get_text_embedding(q2)

        # Distance score
        cos_score = cosine(res_vec, ans_vec)
        euc_score = euclidean(res_vec, ans_vec)

        # Naive length consideration with reduced weightage.
        len_res, len_ans = len(q1), len(q2)
        len_score = (abs(len_res - len_ans) / (len_res + len_ans)) * 0.1

        score = len_score + (cos_score + euc_score) / 2
        # TODO: OLS-409 Use non-contextual score to evaluate response

        print(
            f"cos_score: {cos_score}, "
            f"euc_score: {euc_score}, "
            f"len_score: {len_score}\n"
            f"final_score: {score}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Utility script for calculating distance between two embeddings"
    )
    parser.add_argument(
        "-m", "--model-path", required=True, help="path to the embedding model"
    )
    parser.add_argument("-q1", "--query1", required=True, help="Query 1")
    parser.add_argument("-q2", "--query2", required=True, help="Query 2")
    args = parser.parse_args()

    os.environ["TRANSFORMERS_CACHE"] = args.model_path
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

    ResponseValidation(args.model_path).get_similarity_score(args.query1, args.query2)
