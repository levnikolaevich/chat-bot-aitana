from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Chat:
    """
    A chat class for interacting with a conversational language model.

    Attributes:
        tokenizer (AutoTokenizer): The tokenizer for the specified model.
        model (AutoModelForCausalLM): The causal language model for generating responses.
    """

    def __init__(self, model_id="google/gemma-2b-it"):
        """
        Initializes the Chat class with a specified conversational model.

        Args:
            model_id (str): Identifier for the model to load (default is "google/gemma-2b-it").
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id).to(self.device)

    def _clean_model_response(self, response_text):
        """
        Cleans the model's response by removing the prompt and service tokens.

        Args:
            response_text (str): The raw response text from the model.

        Returns:
            str: The cleaned response text from the model.
        """
        start_token = "<start_of_turn>model"
        end_tokens = ["<end_of_turn>", "<eos>"]

        start_index = response_text.find(start_token)
        if start_index != -1:
            response_text = response_text[start_index + len(start_token):]

        for token in end_tokens:
            end_index = response_text.find(token)
            if end_index != -1:
                response_text = response_text[:end_index].strip()

        return response_text

    def get_answer(self, content, max_new_tokens=250):
        """
        Generates a response to the input content using the loaded model.

        Args:
            content (str): The input text content to generate a response to.
            max_new_tokens (int): The maximum number of new tokens to generate (default is 150).

        Returns:
            str: The generated response text.
        """
        chat = [{"role": "user", "content": content}]
        prompt = self.tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

        input_ids = self.tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(self.device)

        outputs = self.model.generate(input_ids=input_ids, max_new_tokens=max_new_tokens)

        response_text = self.tokenizer.decode(outputs[0])
        return self._clean_model_response(response_text)