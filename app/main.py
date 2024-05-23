import socket
from .header import Header, RCode
from .message import DNSMessage
from .question import DNSQuestion, QClass, QType

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

            response_question = DNSQuestion(
                qname="codecrafters.io", qtype=QType.A, qclass=QClass.IN
            )
            response = DNSMessage(header=response_header)
            response.add_question(response_question)
            print(response_header)

            udp_socket.sendto(response.encode(), source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
