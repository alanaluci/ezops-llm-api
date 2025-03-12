import wikipedia

def search_wikipedia(query: str, lang="pt"):
    """Busca um termo na Wikipedia e retorna um resumo."""
    try:
        wikipedia.set_lang(lang)
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Vários resultados encontrados: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        return "Nenhuma informação encontrada na Wikipedia."
    except Exception as e:
        return f"Erro ao buscar na Wikipedia: {str(e)}"
