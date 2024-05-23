def encode_name(qname: str) -> bytes:
    encoded = bytes()
    for label in qname.encode("ascii").split(b"."):
        encoded += bytes([len(label)]) + label
    return encoded + b"\x00"