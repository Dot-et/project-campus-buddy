"""
citation.py
Campus Buddy Bot – Citation Module
OOP-based academic citation & references manager
"""

# =========================
# BASE CLASS (ENCAPSULATION)
# =========================

class Citation:
    def __init__(self, title, author, year, source_type="Book"):
        self._title = title
        self._author = author
        self._year = year
        self._source_type = source_type

    def format(self):
        """Polymorphic method"""
        raise NotImplementedError

    def telegram_view(self):
        
        return (
            f"📚 *{self._title}*\n"
            f"✍️ {self._author}\n"
            f"📅 {self._year}\n"
            f"📖 {self._source_type}"
        )


# =========================
# INHERITANCE + POLYMORPHISM
# =========================

class APACitation(Citation):
    def format(self):
        return f"{self._author} ({self._year}). {self._title}."


class MLACitation(Citation):
    def format(self):
        return f'{self._author}. "{self._title}." {self._year}.'


# =========================
# MANAGER CLASS (AGGREGATION)
# =========================

class CitationManager:
    """
    Central citation manager for the whole bot
    """

    def __init__(self):
        self.__citations = []

    # -------- Core Features --------

    def add_citation(self, citation: Citation):
        self.__citations.append(citation)

    def list_citations(self):
        if not self.__citations:
            return "❌ No references available."

        msg = "📌 *Academic References*\n\n"
        for i, c in enumerate(self.__citations, start=1):
            msg += f"{i}. {c.format()}\n"
        return msg

    def telegram_list(self):
        if not self.__citations:
            return "❌ No citations saved yet."

        msg = "📚 *Sources Used*\n\n"
        for c in self.__citations:
            msg += c.telegram_view() + "\n\n"
        return msg

    # -------- Integration Helpers --------

    def auto_add_dictionary_source(self):
        self.add_citation(
            APACitation(
                title="Oxford Learner’s Dictionary",
                author="Oxford University Press",
                year=2023,
                source_type="Dictionary"
            )
        )

    def auto_add_quotes_source(self):
        self.add_citation(
            MLACitation(
                title="Famous Quotations",
                author="BrainyQuote",
                year=2024,
                source_type="Website"
            )
        )

    def auto_add_gpa_source(self):
        self.add_citation(
            APACitation(
                title="Ethiopian Higher Education Grading System",
                author="Ministry of Education (MoE)",
                year=2022,
                source_type="Policy Document"
            )
        )
