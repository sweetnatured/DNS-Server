import argparse
import socket
from copy import deepcopy

from .answer import Answer
from .header import RCode
from .message import DNSMessage


def main(resolver: str| None):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            data, source = udp_socket.recvfrom(512)
            request = DNSMessage.decode(data)
            print("request decoded")

            records = []
            if resolver:
                ip, port = resolver.split(":")
                port = int(port)
                rheader = deepcopy(request.header)
                rheader.qdcount = 1
                records = []
                for question in request.questions:
                    message = rheader.encode() + question.encode()
                    resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    resolver_socket.sendto(message, (ip, port))
                    data, _ = resolver_socket.recvfrom(512)
                    resolver_response = DNSMessage.decode(data)
                    records.extend(resolver_response.answers)
            request.header.qr = 1
            request.header.qdcount = request.header.ancount = 0
            request.header.rcode = RCode(4) if request.header.opcode else RCode(0)
            response = DNSMessage(header=request.header)

            for question in request.questions:
                response.add_question(question)
            for record in records:
                response.add_answer(record)

            udp_socket.sendto(response.encode(), source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolver", type=str, help="specify the DNS resolver address")
    args = parser.parse_args()
    main(args.resolver)
