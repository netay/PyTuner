# coding=utf8
import math

# Ля первой октавы
# Если требуется не 440, а 442, достаточно поменять это значение
basic_A0_frequency = 440.0

flat_symbol = '♭'
sharp_symbol = '♯'


class Tone:
    def __init__(self, freq: float):
        self.freq = freq

    @staticmethod
    def lowest():
        return Tone(20)

    @staticmethod
    def highest():
        return Tone(22050)


class Note(Tone):

    def __init__(self, n: int):
        self.n = n
        super().__init__(freq=basic_A0_frequency * math.pow(2, (self.n - 9)/12.0))

    def name_sharp(self) -> str:
        octave = self.n // 12 + 4
        sign = ''
        letter = ''
        if self.n % 12 == 0:
            letter = 'C'
        elif self.n % 12 == 1:
            letter = 'C'
            sign = sharp_symbol
        elif self.n % 12 == 2:
            letter = 'D'
        elif self.n % 12 == 3:
            letter = 'D'
            sign = sharp_symbol
        elif self.n % 12 == 4:
            letter = 'E'
        elif self.n % 12 == 5:
            letter = 'F'
        elif self.n % 12 == 6:
            letter = 'F'
            sign = sharp_symbol
        elif self.n % 12 == 7:
            letter = 'G'
        elif self.n % 12 == 8:
            letter = 'G'
            sign = sharp_symbol
        elif self.n % 12 == 9:
            letter = 'A'
        elif self.n % 12 == 10:
            letter = 'A'
            sign = sharp_symbol
        elif self.n % 12 == 11:
            letter = 'H'
        return f"{letter}{sign}{octave}"

    def name_flat(self) -> str:
        octave = self.n // 12 + 4
        sign = ''
        letter = ''
        if self.n % 12 == 0:
            letter = 'C'
        elif self.n % 12 == 1:
            letter = 'D'
            sign = flat_symbol
        elif self.n % 12 == 2:
            letter = 'D'
        elif self.n % 12 == 3:
            letter = 'E'
            sign = flat_symbol
        elif self.n % 12 == 4:
            letter = 'E'
        elif self.n % 12 == 5:
            letter = 'F'
        elif self.n % 12 == 6:
            letter = 'G'
            sign = flat_symbol
        elif self.n % 12 == 7:
            letter = 'G'
        elif self.n % 12 == 8:
            letter = 'A'
            sign = flat_symbol
        elif self.n % 12 == 9:
            letter = 'A'
        elif self.n % 12 == 10:
            letter = 'H'
            sign = flat_symbol
        elif self.n % 12 == 11:
            letter = 'H'
        return f"{letter}{sign}{octave}"

    def name(self, format_: str = 'sharp') -> str:
        if format_ == 'sharp':
            return self.name_sharp()
        elif format_ == 'flat':
            return self.name_flat()
        else:
            raise ValueError("Format should be flat or sharp!")

    @staticmethod
    def C(i: int):
        return Note(12*(i - 4))

    @staticmethod
    def C_sharp(i: int):
        return Note(1 + 12*(i - 4))

    @staticmethod
    def D_flat(i: int):
        return Note(1 + 12*(i - 4))

    @staticmethod
    def D(i: int):
        return Note(2 + 12*(i - 4))

    @staticmethod
    def D_sharp(i: int):
        return Note(3 + 12*(i - 4))

    @staticmethod
    def E_flat(i: int):
        return Note(3 + 12*(i - 4))

    @staticmethod
    def E(i: int):
        return Note(4 + 12*(i - 4))

    @staticmethod
    def F(i: int):
        return Note(5 + 12*(i - 4))

    @staticmethod
    def F_sharp(i: int):
        return Note(6 + 12*(i - 4))

    @staticmethod
    def G_flat(i: int):
        return Note(6 + 12*(i - 4))

    @staticmethod
    def G(i: int):
        return Note(7 + 12*(i - 4))

    @staticmethod
    def G_sharp(i: int):
        return Note(8 + 12*(i - 4))

    @staticmethod
    def A_flat(i: int):
        return Note(8 + 12*(i - 4))

    @staticmethod
    def A(i: int):
        return Note(9 + 12*(i - 4))

    @staticmethod
    def A_sharp(i: int):
        return Note(10 + 12*(i - 4))

    @staticmethod
    def H_flat(i: int):
        return Note(10 + 12*(i - 4))

    @staticmethod
    def H(i: int):
        return Note(11 + 12*(i - 4))

    def sharp(self):
        return Note(self.n + 1)

    def flat(self):
        return Note(self.n - 1)
