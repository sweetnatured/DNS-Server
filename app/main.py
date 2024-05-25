import socket
from .header import Header, RCode
from .message import DNSMessage
from .question import DNSQuestion, QClass, QType
from .answer import Answer


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            request_header = Header.decode(buf)
            response_header = Header(
                id=request_header.id,
                qr=1,
                opcode=request_header.opcode,
                aa=0,
                tc=0,
                rd=request_header.rd,
                ra=0,
                z=0,
                rcode=RCode(4) if request_header.opcode else RCode(0),
                qdcount=0,
                ancount=0,
                nscount=0,
                arcount=0,
            )

            question = DNSQuestion(
                qname="codecrafters.io".encode(),
                qtype=QType.A,
                qclass=QClass.IN
            )

            answer = Answer(
                qname=question.qname,
                qtype=question.qtype,
                qclass= question.qclass,
                ttl=60,
                rdlength=4,
                rdata="8.8.8.8"
            )

            response = DNSMessage(header=response_header)
            response.add_question(question)
            response.add_answer(answer)

            udp_socket.sendto(response.encode(), source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
