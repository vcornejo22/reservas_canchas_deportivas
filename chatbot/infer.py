from transformers import AutoModelForCausalLM, AutoTokenizer, AdamW
from datasets import load_dataset
import torch

# Cargar modelo y tokenizador
model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Cargar dataset
dataset = load_dataset("nombre_del_dataset")  # Reemplaza con tu dataset

# Preparar el dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# Configurar el optimizador
optimizer = AdamW(model.parameters(), lr=5e-5)

# Bucle de entrenamiento
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

for epoch in range(3):  # Número de épocas
    model.train()
    for batch in tokenized_dataset["train"]:
        inputs = tokenizer(batch["text"], return_tensors="pt", padding=True, truncation=True).to(device)
        labels = inputs["input_ids"].to(device)

        # Forward pass
        outputs = model(**inputs, labels=labels)
        loss = outputs.loss

        # Backward pass
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        print(f"Epoch {epoch}, Loss: {loss.item()}")