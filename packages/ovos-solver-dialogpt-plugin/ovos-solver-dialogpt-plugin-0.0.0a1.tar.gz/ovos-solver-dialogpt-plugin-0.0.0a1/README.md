# <img src='https://raw.githack.com/FortAwesome/Font-Awesome/master/svgs/solid/robot.svg' card_color='#40DBB0' width='50' height='50' style='vertical-align:bottom'/> DialoGPT Persona
 
Give Mycroft some sass with [DialoGPT](https://github.com/microsoft/DialoGPT)

While this can not compete with [ChatGPT Persona](https://github.com/OpenVoiceOS/ovos-solver-plugin-openai-persona) it is an offline alternative, you can use any model from huggingface to have different personas

Find models [here](https://huggingface.co/models?pipeline_tag=conversational&search=dialogpt)

## Examples 
* "What is best in life?"
* "Do you like dogs"
* "Does God exist?"


## Usage

Spoken answers api

```python
from ovos_solver_dialogpt import DialoGPTSolver

d = DialoGPTSolver({"model": "microsoft/DialoGPT-large"})
sentence = d.spoken_answer("What is best in life?")
print(sentence)
# To be alive.

sentence = d.spoken_answer("Qual é o teu animal favorito?", {"lang": "pt-pt"})
print(sentence)
# Adoro todos os animais

d = DialoGPTSolver({"model": "ingen51/DialoGPT-medium-GPT4"})
for q in ["hello!",
          "who are you?",
          "what is the speed of light?",
          "what is the meaning of life?",
          "Does god exist?",
          "What is your favorite color?",
          "What is your favorite animal?",
          "What is best in life?"]:
    a = d.get_spoken_answer(q)
    print(q, a)
    # hello! Hiya there.
    # who are you? I'm the guy that runs the place. 
    # what is the speed of light? About 186,600 mph
    # what is the meaning of life? The meaning of existence is to suffer alone.
    # Does god exist? Yes. He does.
    # What is your favorite color? I don't have one in particular.
    # What is your favorite animal? Horned lizard.
    # What is best in life? A warm home.
```