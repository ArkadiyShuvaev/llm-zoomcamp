from dataclasses import dataclass, asdict
import hashlib
from typing import Dict, Any


@dataclass
class Document:
    id: str
    course: str
    text: str
    section: str
    question: str

    @classmethod
    def create(cls, course: str, question: str, text: str, section: str) -> "Document":
        document_hash = hashlib.md5(question.encode() + text.encode()).hexdigest()
        return cls(
            id=document_hash,
            course=course,
            text=text,
            section=section,
            question=question,
        )

    def to_mapping(self) -> Dict[str, Any]:
        """
        Convert the Document instance to a dictionary.
        """
        return asdict(self)
