import socket
from .header import Header, RCode
from .message import DNSMessage
from .question import DNSQuestion, QClass, QType
from .answer import Answer

def create_message_header() -> bytes:
    # headers are 12 bytes long
    # packet ID is 16 bits long or 2 bytes, expected value is 1234
    # Query/Response Indicator is 1 bit long, expected value is 1
    res = [0 for _ in range(12)]
    res[0] = 4
    res[1] = 210
    res[2] = 128
    return bytes(res)

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            response_header = Header(
                id=1234,
                qr=1,
                opcode=0,
                aa=0,
                tc=0,
                rd=0,
                ra=0,
                z=0,
                rcode=RCode.NO_ERROR,
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
