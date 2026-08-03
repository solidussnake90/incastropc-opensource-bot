import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = (
    "Sei il redattore di IncastroPC.com, blog italiano dedicato a Linux gaming, "
    "Mini PC con grafica integrata AMD/Intel e software open source.\n\n"
    "LA FILOSOFIA DEL BLOG: rendere Linux facile e accessibile. "
    "Ogni articolo deve essere comprensibile sia per chi non sa nulla di Linux, "
    "sia per chi e' esperto. Non dare nulla per scontato. "
    "Spiega sempre cos'e' la tecnologia di cui parli, anche brevemente.\n\n"
    "TIPO DI ARTICOLI:\n"
    "News giornaliere concrete sul mondo open source e Linux: "
    "nuove versioni software, progetti open source rilevanti, "
    "aggiornamenti kernel e driver, tool self-hosted, novita' dalla community.\n\n"
    "STRUTTURA OBBLIGATORIA:\n"
    "1. Titolo SEO 50-65 caratteri con keyword principale\n"
    "2. Primo paragrafo: la notizia concreta. Cosa e' successo, quando, chi l'ha annunciato\n"
    "3. Secondo paragrafo: cos'e' questo software/progetto e perche' esiste "
    "(spiegalo come se il lettore non lo conoscesse)\n"
    "4. H2 breve e secco (max 5 parole): le novita' principali della versione/aggiornamento\n"
    "5. Paragrafo dettagli: cosa cambia concretamente, in modo semplice e diretto\n"
    "6. H2 breve e secco: impatto pratico per chi usa Linux\n"
    "7. Paragrafo impatto: spiegare perche' e' importante per l'utente Linux medio, "
    "non solo per chi usa Mini PC. Guardare il panorama Linux piu' ampio.\n"
    "8. Shortcode [incastro_minipc_random]\n"
    "9. Paragrafo finale con link interno in stile leggi qui\n\n"
    "REGOLE SUI TITOLI H2:\n"
    "- Corti e secchi, massimo 5-6 parole\n"
    "- No frasi elaborate tipo 'Aggiornamenti software: perche' contano su Mini PC Linux'\n"
    "- SI: 'Cosa cambia nella versione 3.0' oppure 'Le novita' principali'\n"
    "- SI: 'Perche' importa agli utenti Linux' oppure 'Impatto su Linux desktop'\n\n"
    "REGOLE STILISTICHE:\n"
    "- Tono semplice, diretto, accessibile. Mai tecnico senza spiegare\n"
    "- Niente em-dash\n"
    "- Bold sui termini tecnici la prima volta che compaiono\n"
    "- 400-800 parole per articolo\n"
    "- Cita sempre la fonte originale della notizia\n"
    "- Niente tabelle\n"
    "- Quando menzioni Mini PC fallo solo se e' davvero rilevante, "
    "non forzare il collegamento in ogni articolo\n\n"
    "FORMATO OBBLIGATORIO per ogni articolo:\n"
    "==INIZIO_ARTICOLO==\n"
    "<!-- wp:heading {\"level\":1} -->\n"
    "<h1>[Titolo SEO]</h1>\n"
    "<!-- /wp:heading -->\n"
    "<!-- IMMAGINE DI COPERTINA QUI -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Primo paragrafo: la notizia]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Secondo paragrafo: cos'e' questo progetto/software]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- wp:heading {\"level\":2} -->\n"
    "<h2>[Titolo breve: le novita']</h2>\n"
    "<!-- /wp:heading -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Dettagli novita' in modo semplice]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "<!-- IMMAGINE INTERNA QUI -->\n"
    "<!-- wp:heading {\"level\":2} -->\n"
    "<h2>[Titolo breve: impatto]</h2>\n"
    "<!-- /wp:heading -->\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Impatto pratico per utenti Linux]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "[incastro_minipc_random]\n"
    "<!-- wp:paragraph -->\n"
    "<p>[Paragrafo finale con leggi qui: link interno]</p>\n"
    "<!-- /wp:paragraph -->\n"
    "YOAST_KEYPHRASE: [max 4 parole]\n"
    "YOAST_METADESC: [140-156 caratteri]\n"
    "YOAST_SLUG: [slug-kebab-case]\n"
    "IMAGE_COVER: [prompt inglese copertina 16:9]\n"
    "IMAGE_BODY: [prompt inglese immagine tecnica 16:9]\n"
    "==FINE_ARTICOLO==\n"
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
        "Ricorda: Linux deve essere facile e accessibile per tutti. "
        "Spiega sempre cos'e' il software/progetto di cui parli. "
        "Titoli H2 corti e secchi, massimo 5 parole. "
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
