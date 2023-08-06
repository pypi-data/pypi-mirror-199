from typing import Tuple, Union, List
class Image_reading_class(object):

    def __init__(self, path, input_mode="rb"):
        self.image = open(path, mode=input_mode)

    def read(self, len: int = 1, mode: str = 'str') -> Union[int, str, Tuple[int, int]]:
        if mode == 'str':
            return self.read_str(len)
        elif mode == 'long':
            return self.read_two_bytes_as_long_dec()
        elif mode == 'dec':
            return self.read_1_dec()
        else:
            return self.read_byte_as_2_dec()

    def read_str(self, len: int) -> str:
        return self.image.read(len)

    def read_byte_as_2_dec(self) -> Tuple[int, int]:
        byte = format(self.read_1_dec(), '08b')
        return int(byte[:4], base=2), int(byte[4:], base=2)

    def read_two_bytes_as_long_dec(self) -> int:
        dec = 0
        mult = 8 #right formula would be (len-1)*8 but since len always = 2, it is a constant
        for i in range(2):
            dec += self.read_1_dec() << mult
            mult -= 8
        return dec

    def read_1_dec(self) -> int:
        return ord(self.image.read(1))

    def read_all(self) -> Tuple[str, ...]:
        return self.image.read()

    def close(self):
        self.image.close()

