# modules/citation.py
# Campus Buddy - Citation Manager

def apa_book(author, year, title, publisher):
    return (
        f"{author}. ({year}). *{title}*. {publisher}."
    )


def apa_website(author, year, title, website, url):
    return (
        f"{author}. ({year}). *{title}*. "
        f"{website}. {url}"
    )


def apa_article(author, year, title, journal, volume, issue, pages):
    return (
        f"{author}. ({year}). {title}. "
        f"*{journal}*, *{volume}*({issue}), {pages}."
    )


def mla_book(author, title, publisher, year):
    return (
        f"{author}. *{title}*. "
        f"{publisher}, {year}."
    )


def mla_website(author, title, website, year, url):
    return (
        f"{author}. \"{title}.\" "
        f"*{website}*, {year}, {url}."
    )


def ieee_book(author, title, publisher, year):
    return (
        f"[1] {author}, *{title}*. "
        f"{publisher}, {year}."
    )


def ieee_website(author, title, website, year, url):
    return (
        f"[1] {author}, \"{title},\" "
        f"{website}, {year}. {url}"
    )


def citation_help():
    return (
        "📚 CITATION MANAGER\n\n"
        "Supported styles:\n"
        "• APA\n"
        "• MLA\n"
        "• IEEE\n\n"
        "You can generate citations for:\n"
        "📖 Books\n"
        "🌐 Websites\n"
        "📰 Journal Articles"
    )


def format_citation(style, source_type, **kwargs):
    style = style.upper().strip()
    source_type = source_type.lower().strip()

    if style == "APA":

        if source_type == "book":
            return apa_book(
                kwargs["author"],
                kwargs["year"],
                kwargs["title"],
                kwargs["publisher"]
            )

        if source_type == "website":
            return apa_website(
                kwargs["author"],
                kwargs["year"],
                kwargs["title"],
                kwargs["website"],
                kwargs["url"]
            )

        if source_type == "article":
            return apa_article(
                kwargs["author"],
                kwargs["year"],
                kwargs["title"],
                kwargs["journal"],
                kwargs["volume"],
                kwargs["issue"],
                kwargs["pages"]
            )

    elif style == "MLA":

        if source_type == "book":
            return mla_book(
                kwargs["author"],
                kwargs["title"],
                kwargs["publisher"],
                kwargs["year"]
            )

        if source_type == "website":
            return mla_website(
                kwargs["author"],
                kwargs["title"],
                kwargs["website"],
                kwargs["year"],
                kwargs["url"]
            )

    elif style == "IEEE":

        if source_type == "book":
            return ieee_book(
                kwargs["author"],
                kwargs["title"],
                kwargs["publisher"],
                kwargs["year"]
            )

        if source_type == "website":
            return ieee_website(
                kwargs["author"],
                kwargs["title"],
                kwargs["website"],
                kwargs["year"],
                kwargs["url"]
            )

    return "❌ Unsupported citation type or style."


def citation_example():
    return (
        "📚 CITATION EXAMPLE\n\n"
        "APA Book:\n"
        "Author, A. (2024). *Book Title*. Publisher.\n\n"
        "MLA Book:\n"
        "Author. *Book Title*. Publisher, 2024.\n\n"
        "IEEE Book:\n"
        "[1] Author, *Book Title*. Publisher, 2024."
    )
