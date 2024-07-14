from typing import Optional
from transformers import AutoTokenizer, pipeline
from textSummarizer.config.configuration import ConfigurationManager
from pydantic import BaseModel

class SummaryRequest(BaseModel):
    text: str
    maxSummaryLength: int


class PredictionPipeline:
    """
    A class for performing text summarization using pretrained models.
    """

    def __init__(self):
        """
        Initializes the PredictionPipeline by loading model evaluation configuration.
        """
        self.config = ConfigurationManager().get_model_evaluation_config()

    def predict(
        self,
        request: SummaryRequest,
    ) -> Optional[str]:
        """
        Generates a summary for the given input text.

        Args:
            request (str): The input request string containing 'text=' and ' summary_length='.
            length_penalty (float, optional): The length penalty for beam search. Defaults to 0.8.
            num_beams (int, optional): The number of beams for beam search. Defaults to 8.
            max_length (int, optional): The maximum length of the output summary. Defaults to 128.

        Returns:
            str: The generated summary text.
        """

        try:
            text = request.text
            max_length = request.maxSummaryLength
            print(f"Summary Length: {max_length}, Text: {text}")

            tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
            print(
                f"Tokenizer max length: {tokenizer.model_max_length}"
            )
            gen_kwargs = {"length_penalty": 0.8, "num_beams":8, "max_length": max_length}
            pipe = pipeline("summarization", model=self.config.model_path,tokenizer=tokenizer)

            output = pipe(text, **gen_kwargs)[0]["summary_text"]
            print("\nModel Summary:")
            print(output)

            return output
        except Exception as e:
            # Handle exceptions gracefully
            print(f"An error occurred: {e}")
            return None
