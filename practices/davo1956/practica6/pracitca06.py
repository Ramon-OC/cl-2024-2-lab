# -*- coding: utf-8 -*-
"""pracitca06.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1E5m2-Q0PWxT_tB2L017v3p1jDZ_a4v56

# Practica 06

Alumno: David Pérez Jacome \\
Número de Cuenta: 316330420

**Actividades**

1. Crear un par de modelos del lenguaje usando un corpus en español
  - Corpus: El Quijote
    - URL: https://www.gutenberg.org/ebooks/2000
    - Modelo de n-gramas con n = [2, 3]
    - Hold out con test = 30% y train = 70%

2. Evaluar los modelos y reportar la perplejidad de cada modelo
  - Comparar los resultados entre los diferentes modelos del lenguaje (bigramas, trigramas)
  - ¿Cual fue el modelo mejor evaluado? ¿Porqué?
"""

# Importar las bibliotecas necesarias
import requests
import re
import nltk
from nltk.util import ngrams
from collections import defaultdict, Counter
import numpy as np

# Descargar recursos necesarios de NLTK
nltk.download('punkt')

# URL del corpus
url = "https://www.gutenberg.org/files/2000/2000-0.txt"

# Descargar el corpus
response = requests.get(url)
corpus = response.text

# Preprocesar el texto
def preprocess_text(text):
    # Eliminar encabezado y pie de página del Proyecto Gutenberg
    start_index = text.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
    end_index = text.find("*** END OF THIS PROJECT GUTENBERG EBOOK")
    text = text[start_index:end_index]

    # Convertir a minúsculas y eliminar caracteres no deseados
    text = text.lower()
    text = re.sub(r'[^a-záéíóúñü\s]', '', text)
    return text

corpus = preprocess_text(corpus)

# Tokenizar el texto
tokens = nltk.word_tokenize(corpus)

# Dividir en entrenamiento (70%) y prueba (30%)
train_size = int(len(tokens) * 0.7)
train_tokens = tokens[:train_size]
test_tokens = tokens[train_size:]

# Función para entrenar modelos de n-gramas
def train_ngram_model(tokens, n):
    model = defaultdict(Counter)
    ngrams_list = list(ngrams(tokens, n, pad_left=True, pad_right=True, left_pad_symbol="<s>", right_pad_symbol="</s>"))
    for ngram in ngrams_list:
        context = ngram[:-1]
        word = ngram[-1]
        model[context][word] += 1
    return model

# Entrenar modelos de bigramas y trigramas
bigram_model = train_ngram_model(train_tokens, 2)
trigram_model = train_ngram_model(train_tokens, 3)

# Función para calcular la probabilidad de una palabra dado el contexto
def get_ngram_prob(model, context, word):
    context_counts = model[context]
    context_total = sum(context_counts.values())
    word_count = context_counts[word]
    return word_count / context_total if context_total > 0 else 0

# Función para calcular la perplejidad
def calculate_perplexity(model, tokens, n):
    ngrams_list = list(ngrams(tokens, n, pad_left=True, pad_right=True, left_pad_symbol="<s>", right_pad_symbol="</s>"))
    N = len(ngrams_list)
    log_prob_sum = 0
    for ngram in ngrams_list:
        context = ngram[:-1]
        word = ngram[-1]
        prob = get_ngram_prob(model, context, word)
        log_prob_sum += np.log(prob if prob > 0 else 1e-10)  # Evitar log(0)
    perplexity = np.exp(-log_prob_sum / N)
    return perplexity

# Calcular la perplejidad de los modelos en el conjunto de prueba
bigram_perplexity = calculate_perplexity(bigram_model, test_tokens, 2)
trigram_perplexity = calculate_perplexity(trigram_model, test_tokens, 3)

# Imprimir los resultados
print(f"Perplejidad del modelo de bigramas: {bigram_perplexity}")
print(f"Perplejidad del modelo de trigramas: {trigram_perplexity}")

# Análisis de los resultados
if bigram_perplexity < trigram_perplexity:
    print("El modelo de bigramas tiene mejor desempeño.")
else:
    print("El modelo de trigramas tiene mejor desempeño.")

print("\nAnálisis:")
print("La perplejidad mide la incertidumbre del modelo al predecir la siguiente palabra.")
print("Un menor valor de perplejidad indica un modelo más seguro y mejor desempeño.")
print("El modelo con la perplejidad más baja será el mejor evaluado.")

"""**Observaciones**

1. Preprocesamiento del Texto: Se eliminan los encabezados y pies de página del Proyecto Gutenberg y se convierte el texto a minúsculas, eliminando caracteres no deseados.

2. ivisión de Datos: El corpus se divide en un conjunto de entrenamiento (70%) y un conjunto de prueba (30%).

3. Cálculo de Perplejidad: Se calcula la perplejidad de los modelos utilizando el conjunto de prueba.
4. Análisis: Se compara la perplejidad de ambos modelos para determinar cuál tiene mejor desempeño.

**Respuestas**

1. Comparación de Resultados: La comparación se basa en la perplejidad calculada para cada modelo.

2. Mejor Modelo: El modelo con la perplejidad más baja es el mejor evaluado. Esto generalmente ocurre porque este modelo es más efectivo para predecir la siguiente palabra en el corpus dado.
"""