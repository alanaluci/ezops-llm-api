EzOps LLM API
API baseada em FastAPI e spaCy para Processamento de Linguagem Natural (NLP).


📌 Sobre o Projeto
A EzOps LLM API é uma API de Processamento de Linguagem Natural que utiliza FastAPI e spaCy para responder perguntas e processar textos. Além disso, ela possui integração com ferramentas adicionais, como:

📊 Calculadora → Resolve expressões matemáticas.
📚 Pesquisa na Wikipedia → Busca definições e conceitos diretamente da Wikipedia.
O projeto foi desenvolvido para suportar inferência otimizada com PyTorch e Transformers da Hugging Face.

🚀 Tecnologias Utilizadas
Python 3.12
FastAPI
Uvicorn
spaCy
Docker
Transformers (Hugging Face)
PyTorch

📦 Como Rodar o Projeto
1️⃣ Clonar o Repositório
git clone https://github.com/alanaluciaso/ezops-llm-api.git
cd ezops-llm-api
2️⃣ Criar o Ambiente Virtual e Instalar Dependências
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
3️⃣ Baixar Modelo NLP (spaCy)
python -m spacy download pt_core_news_sm
4️⃣ Rodar a API
uvicorn main:app --reload
A API estará disponível em: http://127.0.0.1:8000

🛠 Testando a API
🔍 Exemplo de Requisição
Envie um JSON com um campo text:

json
{
  "text": "2 + 2"
}
📌 Resposta esperada
json
{
  "input": "2 + 2",
  "response": "Resultado da expressão matemática: 4",
  "tools_used": ["Calculator"]
}
✅ Rodando os Testes
Usamos pytest para validar o funcionamento da API.

1️⃣ Instalar pytest e httpx:
pip install pytest httpx
2️⃣ Executar os testes:
pytest tests/
Se todos os testes passarem, significa que a API está funcionando corretamente! ✅

📦 Rodando com Docker
Caso queira rodar a API dentro de um container Docker, siga os passos abaixo:

1️⃣ Criar a imagem
docker build --no-cache --platform linux/aarch64 -t ezops-llm-api .
2️⃣ Rodar o container
docker run -p 8000:8000 ezops-llm-api
A API estará disponível em: http://127.0.0.1:8000

3️⃣ Acessar a Documentação
Swagger UI: http://localhost:8000/docs
Redoc: http://localhost:8000/redoc

🔄 Endpoints Disponíveis
📌 Health Check
http
GET /health
Resposta:
json
{ "status": "OK" }
📌 Processamento de Texto

POST /process
Body:
json
{ "text": "O spaCy é uma biblioteca incrível!" }
Resposta:
json
{
  "tokens": ["O", "spaCy", "é", "uma", "biblioteca", "incrível", "!"],
  "entities": []
}
🔧 Solução de Problemas
❌ Erro: "Bind for 0.0.0.0:8000 failed: port is already allocated"
✅ Solução: A porta 8000 já está em uso. Pare o processo que a está ocupando:


lsof -i :8000
kill -9 <PID>
Ou rode em outra porta:


docker run -p 8080:8000 ezops-llm-api
❌ Erro: "No module named uvicorn"
✅ Solução: O uvicorn pode não estar instalado corretamente dentro do container. Certifique-se de que está listado no requirements.txt.

❌ Erro: "tarfile.ReadError: not a gzip file"
✅ Solução: O download do modelo do spaCy pode ter falhado. Tente remover e baixar novamente:
rm -rf /app/pt_core_news_sm.tar.gz
docker build --no-cache --platform linux/aarch64 -t ezops-llm-api .

📜 Licença
Este projeto é open-source.

👩‍💻 Contribuindo
Sinta-se à vontade para abrir Issues e Pull Requests para melhorias no projeto!

📬 Contato
📌 Desenvolvido por Alana Lucia Souza Oliveira.