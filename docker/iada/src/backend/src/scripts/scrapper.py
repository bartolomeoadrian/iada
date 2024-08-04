import requests
from ..utils.gemini import generation_config, genai
from ..utils.chroma import chroma_client
from bs4 import BeautifulSoup
from collections import deque


# Configuración de Gemini
scrapper_model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Dado un documento HTML debes dar una descripción de que se trata la página web y cuales son sus posibilidades",
)

chat = scrapper_model.start_chat()

# Configuración de ChromaDB
webpage_collection = chroma_client.get_or_create_collection("webpage_descriptions")


# Función para obtener la descripción de una página web usando Google Gemini
def get_description(html):
    print(html)
    response = chat.send_message(html)
    print(response.text)
    return response.text


# Función para rastrear el sitio web
def scrape_website(base_url, depth):
    visited = set()
    queue = deque([(base_url, 0)])

    while queue:
        url, current_depth = queue.popleft()
        if current_depth > depth or url in visited:
            continue

        visited.add(url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        description = get_description(response.text)
        webpage_collection.add(documents=[description], ids=[url])

        if current_depth < depth:
            for link in soup.find_all("a", href=True):
                next_url = link["href"]
                if next_url.startswith("/"):
                    next_url = base_url + next_url
                if next_url.startswith(base_url):
                    queue.append((next_url, current_depth + 1))


scrape_website("https://hcdn.gob.ar", 1)
