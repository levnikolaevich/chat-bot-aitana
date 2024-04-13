from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import os

class Chat:
    """
    A chat class for interacting with a conversational language model.

    Attributes:
        __tokenizer (AutoTokenizer): The tokenizer for the specified model.
        __model (AutoModelForCausalLM): The causal language model for generating responses.
    """

    def __init__(self, model_id="google/gemma-1.1-2b-it"):
        """
        Initializes the Chat class with a specified conversational model.

        Args:
            model_id (str): Identifier for the model to load (default is "google/gemma-1.1-2b-it").
        """
        allowed_model_ids = ["google/gemma-1.1-2b-it", "google/gemma-1.1-7b-it"]

        if model_id not in allowed_model_ids:
            raise ValueError(
                f"model_id '{model_id}' is not supported. Please use one of the following: {', '.join(allowed_model_ids)}")

        self.__device = "cpu"
        torch_dtype = torch.float32

        if torch.cuda.is_available():
            os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
            self.__device = "cuda"
            torch_dtype = torch.bfloat16

        print("Device detected: ", self.__device)

        self.__tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.__model = AutoModelForCausalLM.from_pretrained(
                        model_id,
                        torch_dtype=torch_dtype).to(self.__device)
        self.__model_id = model_id
        self.__chat_history = []

    # ====================
    # = Get Answer Region
    # ====================
    def get_answer(self, content, max_new_tokens=150):
        response = None

        if self.__model_id in ["google/gemma-1.1-2b-it", "google/gemma-1.1-7b-it"]:
            response = self.get_answer_gemma(content, max_new_tokens)
        elif self.__model_id in ["openai/chat-gpt"]:
            response = self.get_answer_open_chat(content, max_new_tokens)

        return response

    def get_answer_gemma(self, content, max_new_tokens=150):
        """
        Generates a response to the input content using the loaded model.

               Args:
                   content (str): The input text content to generate a response to.
                   max_new_tokens (int): The maximum number of new tokens to generate (default is 150).

               Returns:
                   str: The generated response text.
        """
        print(f"get_answer from LLM started max_new_tokens={max_new_tokens}")
        start_time = time.time()

        chat = [{"role": "user", "content": content}]
        prompt = self.__tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

        input_ids = self.__tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(self.__device)

        outputs = self.__model.generate(input_ids=input_ids, max_new_tokens=max_new_tokens)

        response_text = self.__tokenizer.decode(outputs[0])
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"get_answer from LLM finished. Time taken to get answer from LLM: {elapsed_time} seconds")
        return self.__clean_model_response(response_text)

    def get_answer_open_chat(self, content, max_new_tokens=150):
        """
        Generates a response to the input content using the loaded model.

               Args:
                   content (str): The input text content to generate a response to.
                   max_new_tokens (int): The maximum number of new tokens to generate (default is 150).

               Returns:
                   str: The generated response text.
        """
        print(f"get_answer from LLM started max_new_tokens={max_new_tokens}")
        start_time = time.time()

        chat = [{"role": "user", "content": content}]
        prompt = self.__tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)

        input_ids = self.__tokenizer.encode(prompt, add_special_tokens=False, return_tensors="pt").to(self.__device)

        outputs = self.__model.generate(input_ids=input_ids, max_new_tokens=max_new_tokens)

        response_text = self.__tokenizer.decode(outputs[0])
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"get_answer from LLM finished. Time taken to get answer from LLM: {elapsed_time} seconds")
        return self.__clean_model_response(response_text)

    def __clean_model_response(self, response_text):
        """
        Cleans the model's response by removing predefined tokens that indicate the start of the model's turn and
        any service tokens indicating the end of a turn or end of sequence. This makes the response more human-readable.

        Args:
            response_text (str): The raw response text from the model.

        Returns:
            str: The cleaned response text, ready for presentation to the user.
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

    # ====================
    # = Chat History Region
    # ====================
    def update_chat_history(self, histories):
        self.__chat_history.extend(histories)

    def get_chat_history(self):
        return self.__chat_history

    def clean_chat_history(self):
        self.__chat_history = []
