from transformers import AutoModelForCausalLM, AutoTokenizer
from neon_solvers import AbstractSolver


class DialoGPTSolver(AbstractSolver):
    # https://huggingface.co/models?pipeline_tag=conversational&search=dialogpt
    personas = {
        "small": "microsoft/DialoGPT-small",
        "medium": "microsoft/DialoGPT-medium",
        "large": "microsoft/DialoGPT-large",

        # TODO - validate quality of models below, no quality control yet!
        "chat-small-en": "liam168/chat-DialoGPT-small-en",
        "marx": "CoderEFE/DialoGPT-marxbot",
        "palpatine": "Filosofas/DialoGPT-medium-PALPATINE2",
        "cleverbot": "KOSTAS/DialoGPT-small-Cleverbot"
    }

    def __init__(self, config=None):
        super().__init__(name="DialoGPT", priority=95, config=config,
                         enable_cache=False, enable_tx=True)
        checkpoint = self.config.get("model") or "microsoft/DialoGPT-medium"
        if checkpoint in self.personas:
            checkpoint = self.personas[checkpoint]
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)
        self.model = AutoModelForCausalLM.from_pretrained(checkpoint)

    # officially exported Solver methods
    def get_spoken_answer(self, query, context=None):
        input_ids = self.tokenizer.encode(query + self.tokenizer.eos_token,
                                          return_tensors='pt')

        # TODO - from config
        ans = self.model.generate(input_ids,
                                  max_length=2046,
                                  pad_token_id=self.tokenizer.eos_token_id,
                                  no_repeat_ngram_size=3,
                                  do_sample=True,
                                  top_k=45,
                                  top_p=0.7,
                                  temperature=0.85)
        return self.tokenizer.decode(ans[:, input_ids.shape[-1]:][0],
                                     skip_special_tokens=True)


if __name__ == "__main__":
    bot = DialoGPTSolver({"model": "ingen51/DialoGPT-medium-GPT4"})

    sentence = bot.spoken_answer("Qual é o teu animal favorito?", {"lang": "pt-pt"})
    print(sentence)

    for q in ["hello!",
              "who are you?",
              "what is the speed of light?",
              "what is the meaning of life?",
              "Does god exist?",
              "What is your favorite color?",
              "What is your favorite animal?",
              "What is best in life?"]:
        a = bot.get_spoken_answer(q)
        print(q, a)
