from dataclasses import dataclass, field

from .header import Header
from .question import DNSQuestion


@dataclass
class DNSMessage:
    """
    +---------------------+
    |        Header       |
    +---------------------+
    |       Question      | the question for the name server
    +---------------------+
    |        Answer       | RRs answering the question
    +---------------------+
    |      Authority      | RRs pointing toward an authority
    +---------------------+
    |      Additional     | RRs holding additional information
    +---------------------+
    """
    header: Header
    questions: list[DNSQuestion] = field(default_factory=list)
    def add_question(self, question: DNSQuestion):
        self.questions.append(question)
        print(self.header)
        self.header.qdcount += 1

    def encode(self) -> bytes:
        header = self.header.encode()
        questions = b"".join([question.encode() for question in self.questions])
        return header + questions