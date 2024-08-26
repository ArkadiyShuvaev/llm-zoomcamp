from dataclasses import dataclass, asdict
import hashlib
from typing import Dict


@dataclass
class Document:
    id: str
    section: str
    question: str
    text: str
    access_control: str | None

    @classmethod
    def create(cls, section: str, question: str, text: str, id: str | None = None, access_control: str | None = None) -> "Document":
        if id is None:
            id = hashlib.md5(question.encode() + text.encode()).hexdigest()

        return cls(id=id, section=section, question=question, text=text, access_control=access_control)

    def to_mapping(self) -> Dict[str, str | None]:
        """
        Convert the Document instance to a dictionary.
        """
        return asdict(self)
