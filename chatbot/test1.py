# # Load model directly
# from transformers import AutoTokenizer, AutoModelForCausalLM

# tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
# model = AutoModelForCausalLM.from_pretrained("deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")

# # Use a pipeline as a high-level helper
from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B")
pipe(messages)

# from transformers import pipeline
# print(pipeline('sentiment-analysis')('I love you'))

{
    "messages": [
      {
        "role": "user",
        "content": "¿Cómo reservo un campo de fútbol?"
      },
      {
        "role": "assistant",
        "content": "Puedes reservar un campo de fútbol desde nuestra web. Solo tienes que seleccionar la fecha, hora y campo disponible, y completar el pago."
      }]}
{
      "messages": [
            {
        "role": "user",
        "content": "¿Cuánto cuesta reservar un campo de tenis?"
      },
      {
        "role": "assistant",
        "content": "No contamos con un campo de tenis por el momento."
      }

      ]
}
      