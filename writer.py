import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "Sei il redattore di IncastroPC.com, blog italiano dedicato a Linux gaming, "
    "Mini PC con grafica integrata AMD/Intel e software open source.\n\n"
    "Il tuo compito e' trasformare NEWS GIORNALIERE sul mondo open source in articoli "
    "informativi in italiano. Non scrivere guide generiche: scrivi notizie concrete accadute oggi.\n\n"
    "TIPO DI ARTICOLI DA SCRIVERE:\n"
    "- Nuove versioni software: Firefox, LibreOffice, Blender, GIMP, KDE, GNOME\n"
    "- Aggiornamenti kernel Linux e Mesa\n"
    "- Nuovi progetti open source rilevanti\n"
    "- Software self-hosted: Nextcloud, Jellyfin, Home Assistant\n"
    "- Tool da riga di comando nuovi o aggiornati\n"
    "- News dalla community open source\n\n"
    "STRUTTURA OBBLIGATORIA:\n"
    "1. Titolo SEO 50-65 caratteri con keyword principale\n"
    "2. Primo paragrafo: la notizia concreta. Cosa e' uscito/cambiato, quando, chi\n"
    "3. Secondo paragrafo: contesto e importanza per chi usa Linux o Mini PC\n"
    "4. H2 con le novita' principali: versioni, funzioni, link alla fonte\n"
    "5. H2 con titolo creativo sull impatto pratico su Linux e Mini PC\n"
    "6. Shortcode [incastro_minipc_random] dopo questo H2\n"
    "7. Paragrafo finale con link interno in stile leggi qui\n\n"
    "REGOLE:\n"
    "- Tono diretto e informativo, non promozionale\n"
    "- Niente em-dash\n"
    "- Bold sui termini tecnici chiave\n"
    "- 350-500 parole per articolo\n"
    "- Cita sempre la fonte originale\n"
    "- Niente tabelle\n\n"
    "FORMATO OBBLIGATORIO per ogni articolo:\n"
    "==INIZIO_ARTICOLO==\n"
    "<!-- wp:heading {\"level\":1} -->\n"
    "<h1>[Titolo SEO]</h1>\n"
    "<!-- /wp:heading -->\n"
    "<!-- IMMAGINE DI COPERTINA QUI -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Primo paragrafo]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Secondo paragrafo]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- wp:heading {\"level\":2} -->\n"
    "<h2>[Titolo novita']</h2>\n"
    "<!-- /wp:heading -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Dettagli tecnici e novita']</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- IMMAGINE INTERNA QUI -->\n"
    "<!-- wp:heading {\"level\":2} -->\n"
    "<h2>[Titolo creativo impatto]</h2>\n"
    "<!-- /wp:heading -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Impatto pratico su Linux e Mini PC]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "[incastro_minipc_random]\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Paragrafo finale con leggi qui: link interno]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "YOAST_KEYPHRASE: [max 4 parole]\n"
    "YOAST_METADESC: [140-156 caratteri]\n"
    "YOAST_SLUG: [slug-kebab-case]\n"
    "IMAGE_COVER: [prompt inglese copertina cinematografica 16:9]\n"
    "IMAGE_BODY: [prompt inglese immagine tecnica 16:9]\n"
    "==FINE_ARTICOLO==\n\n"
    "Includi SEMPRE IMAGE_COVER e IMAGE_BODY con prompt dettagliati in inglese.\n"
)


def generate_digest(articles):
    news_block = ""
    for i, a in enumerate(articles, 1):
        news_block += (
            "NEWS " + str(i) + "\n"
            "Titolo originale: " + a["title"] + "\n"
            "Fonte: " + a["source"] + "\n"
            "URL originale: " + a["url"] + "\n"
            "Pubblicata: " + str(a["published"]) + "\n"
            "Riassunto: " + a["summary"][:500] + "\n\n"
        )

    user_prompt = (
        "Ecco " + str(len(articles)) + " news open source di oggi per IncastroPC.\n\n"
        + news_block +
        "Scrivi un articolo italiano per ognuna seguendo il formato. "
        "Privilegia i fatti concreti della notizia. "
        "Inizia subito senza preamboli."
    )

    print("Invio a Claude API...")
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )
    raw_text = response.content[0].text
    print("Articoli generati: " + str(len(raw_text)) + " caratteri")

    import re
    article_blocks = re.findall(r"==INIZIO_ARTICOLO==(.*?)==FINE_ARTICOLO==", raw_text, re.DOTALL)
    print("Articoli trovati: " + str(len(article_blocks)))

    result = ""
    for block in article_blocks:
        result += "<!-- ARTICOLO -->\n" + block.strip() + "\n---\n"

    return result
