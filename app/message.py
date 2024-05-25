from dataclasses import dataclass, field
from io import BytesIO

from .answer import Answer
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
    answers: list[Answer] = field(default_factory=list)

    def add_question(self, question: DNSQuestion):
        self.questions.append(question)
        self.header.qdcount += 1

    def add_answer(self, answer: Answer):
        self.answers.append(answer)
        self.header.ancount += 1

    def encode(self) -> bytes:
        header = self.header.encode()
        questions = b"".join([question.encode() for question in self.questions])
        answers = b"".join([answer.encode() for answer in self.answers])

        return header + questions + answers

    @staticmethod
    def decode(data: bytes) -> "DNSMessage":
        reader = BytesIO(data)
        header = Header.decode(reader)
        questions = [DNSQuestion.decode(reader) for _ in range(header.qdcount)]
        records = [Answer.decode(reader) for _ in range(header.ancount)]
        return DNSMessage(header=header, questions=questions, answers=records)