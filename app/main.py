from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from tools.calculator import parse_math_expression
from tools.wikipedia_search import search_wikipedia
import torch
import spacy
import logging
from config import HUGGINGFACE_MODEL

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criando a instância do FastAPI
app = FastAPI(
    title="EZOps LLM API",
    description="API para interagir com um modelo LLM da Hugging Face",
    version="1.0"
)

# Carregar modelo e tokenizador
try:
    logger.info(f"Carregando modelo Hugging Face: {HUGGINGFACE_MODEL}")
    tokenizer = AutoTokenizer.from_pretrained(HUGGINGFACE_MODEL)
    model = AutoModelForCausalLM.from_pretrained(
        HUGGINGFACE_MODEL, 
        torch_dtype=torch.float16, 
        device_map="auto",
        low_cpu_mem_usage=True
    )
    logger.info("Modelo carregado com sucesso.")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    raise

# Carregar NLP (SpaCy) apenas uma vez
logger.info("Carregando modelo NLP (spaCy)...")
nlp = spacy.load("pt_core_news_sm")
logger.info("Modelo NLP carregado com sucesso.")

# Criando modelos Pydantic para entrada e saída
class UserInput(BaseModel):
    text: str  # O usuário precisa enviar um JSON com um campo "text"

class LLMResponse(BaseModel):
    input: str
    response: str
    tools_used: list = []

# Função para verificar se o input é uma pergunta de definição/conceito
def is_wikipedia_query(text: str) -> bool:
    """Verifica se a pergunta parece uma busca por conceito."""
    text = text.lower().strip()
    
    keywords = ["o que é", "quem foi", "quem é", "defina", "explique", "significa", "como funciona"]
    
    # Retorna True se o texto começar com uma das palavras-chave
    return any(text.startswith(kw) for kw in keywords)

# Criando um endpoint POST chamado "/infer"
@app.post("/infer", response_model=LLMResponse)
def infer(request: UserInput):
    """Recebe um texto do usuário e retorna uma resposta gerada pelo modelo da Hugging Face."""
    input_text = request.text
    tools_used = []

    # Detecta automaticamente onde o modelo está carregado
    model_device = next(model.parameters()).device
    logger.info(f"Modelo rodando no dispositivo: {model_device}")

    # Verifica se o input é uma expressão matemática
    math_result = parse_math_expression(input_text)
    if math_result is not None:
        return LLMResponse(
            input=input_text,
            response=f"Resultado da expressão matemática: {math_result}",
            tools_used=["Calculator"]
        )

    # Verifica se o input pede um conceito da Wikipedia
    if is_wikipedia_query(input_text):
        wiki_result = search_wikipedia(input_text)
        tools_used.append("Wikipedia Search")
        return LLMResponse(
            input=input_text,
            response=wiki_result,
            tools_used=tools_used
        )
    # Configurar tokenizador para evitar aviso de pad_token_id
    tokenizer.pad_token = tokenizer.eos_token

    # Tokeniza o texto e move para o mesmo dispositivo do modelo
    inputs = tokenizer(input_text, return_tensors="pt").to(model_device)

    # O modelo gera uma resposta baseada no input
    outputs = model.generate(
        **inputs,
        max_new_tokens=50,  # Limita a quantidade de tokens gerados
        temperature=0.7,  # Controla a criatividade do modelo
        top_p=0.9,  # Evita que ele gere respostas muito aleatórias
        do_sample=True  # Ativa amostragem para gerar respostas mais rápidas
    )

    # Converte a resposta do modelo de volta para texto legível
    response_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return LLMResponse(
        input=input_text,
        response=response_text
    )
