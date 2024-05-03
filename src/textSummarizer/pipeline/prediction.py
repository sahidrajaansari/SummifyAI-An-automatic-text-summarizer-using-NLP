from typing import Optional
from transformers import AutoTokenizer, pipeline
from textSummarizer.config.configuration import ConfigurationManager


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
        request: str,
        max_length: int = 128,
        length_penalty: float = 0.8,
        num_beams: int = 8,
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
            tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
            pipe = pipeline(
                "summarization", model=self.config.model_path, tokenizer=tokenizer
            )
            # Find the index of '=' to split the string
            equal_index = request.find("=")

            # Extract the text part (including the quotes)
            text_part = request[equal_index + 2 :]

            # Find the index of ' summary_length=' to split the string
            summary_length_index = text_part.find(" summary_length=")

            # Extract the text portion without quotes
            text = text_part[: summary_length_index - 1]

            # Extract the summary length
            max_length = int(text_part[summary_length_index + 16 :])
            
            print(f"Summary Length: {max_length}, Text: {text}")

            print("Dialogue:")
            print(text)

            output = pipe(
                text,
                length_penalty,
                num_beams,
                max_length,
            )[0]["summary_text"]
            
            print("\nModel Summary:")
            print(output)
            return output
        except Exception as e:
            # Handle exceptions gracefully
            print(f"An error occurred: {e}")
            return None
