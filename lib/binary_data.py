import base64


class BinaryData():
    @classmethod
    def decode_from_str(cls, img_str: str) -> bytes:
        decoded_data = base64.b64decode(img_str)
        return decoded_data

    @classmethod
    def encode_to_str(cls, img_binary: bytes) -> str:
        base64_data = base64.encodebytes(img_binary).decode("ascii")
        return base64_data
