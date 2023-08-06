# 7-segment display numbers 
zero = "\n\t||||||\n\t||  ||\n\n\t||  ||\n\t||||||\n"
one = "\n\t    ||\n\t    ||\n\t    ||\n\t    ||\n\t    ||\n"
two = "\n\t||||||\n\t    ||\n\t||||||\n\t||\n\t||||||\n"
three = "\n\t||||||\n\t    ||\n\t||||||\n\t    ||\n\t||||||\n"
four = "\n\t||  ||\n\t||  ||\n\t||||||\n\t    ||\n\t    ||\n"
five = "\n\t||||||\n\t||\n\t||||||\n\t    ||\n\t||||||\n"
six = "\n\t||||||\n\t||\n\t||||||\n\t||  ||\n\t||||||\n"
seven = "\n\t||||||\n\t    ||\n\t    ||\n\t    ||\n\t    ||\n"
eight = "\n\t||||||\n\t||  ||\n\t||||||\n\t||  ||\n\t||||||\n"
nine = "\n\t||||||\n\t||  ||\n\t||||||\n\t    ||\n\t    ||"


# Ascii class 
class Ascii:

    def encode(value: int) -> str:
        print(chr(value))


    def decode(value: str) -> int:
        print(ord(value))

    
    def ConvertToBinary(value: str) -> str:
        print(str(bin(ord(value))))

    
    def ConvertToHex(value: str) -> str:
        print(str(hex(ord(value))))
    
    
    def ConvertToOctal(value: str) -> str:
        print(str(oct(ord(value))))
    
# Logic gates class
class LogicGates:

    def AND(a: int,b: int) -> bool:
        if a == 1 and b == 1:
            print(True)
            return 1
        
        elif a == 0 or b == 0:
            print(False)
            return 1
        
        else:
            raise Exception('Input can be just 1 or 0')


    def OR(a: int, b: int) -> bool:
        if a == 1 or b == 1:
            print(True)
            return 1
        
        elif a == 0 and b == 0:
            print(False)
            return 0
        
        else:
            raise Exception('Input can be just 1 or 0')
    

    def NOT(a: int) -> bool:
        if a == 1:
            print(False)
            return 0
        
        elif a == 0:
            print(True)
            return 1
        
        else:
            raise Exception('Input can be just 1 or 0')


    def NOR(a: int, b: int) -> bool:
        if a == 1 or b == 1:
            print(False)
            return 0
        
        elif a == 0 and b == 0:
            print(True)
            return 1
        
        else:
            raise Exception('Input can be just 1 or 0')
    

    def NAND(a: int, b: int) -> bool:
        if a == 1 and b == 1:
            print(False)
            return 0
        
        elif a == 0 and b == 0 or a == 1 and b == 0 or a == 0 and b == 1:
            print(True)
            return 1
    

    def XOR(a: int, b: int) -> bool:
        if a == 0 and b == 0:
            print(False)
            return 0
        
        elif a == 0 and b == 1 or a == 1 and b == 0:
            print(True)
            return 1
        
        elif a == 1 and b == 1:
            print(False)
            return 0
        
        else:
            raise Exception('Input can be just 1 or 0')
    

    def XNOR(a: int, b: int) -> bool:
        if a == 0 and b == 0:
            print(True)
            return 1
        
        elif a == 0 and b == 1 or a == 1 and b == 0:
            print(False)
            return 0
        
        elif a == 1 and b == 1:
            print(True)
            return 1
        
        else:
            raise Exception('Input can be just 1 or 0')
    

    def Buffer(a: int) -> bool:
        if a == 1:
            print(True)
            return 1
        
        elif a == 0:
            print(False)
            return 0
    
# Binary class
class Binary:

    def encode(value: int) -> bin:
        print(str(bin(value)))
    

    def decode(value: str) -> int:
        print(str(int(value, 2)))


    def ConvertToAscii(value: str) -> str:
        print(str(chr(int(value, 2))))

    
    def ConvertToHex(value: str) -> str:
        print(str(hex(int(value, 2))))


    def ConvertToOctal(value: str) -> str:
        print(str(oct(int(value, 2))))

    def ConvertToDecimal(value: str) -> int:
        print(str(int(value, 2)))

# Hex class
class Hex:

    def encode(value: int) -> str:
        print(str(hex(value)))

    
    def decode(value: str) -> int:
        print(str(int(value, 16)))

    
    def ConvertToBinary(value: str) -> str:
        print(str(bin(int(value, 16))))


    def ConvertToAscii(value: str) -> str:
        print(str(chr(int(value, 16))))

    
    def ConvertToOctal(value: str) -> str:
        print(str(oct(int(value, 16))))

# Octal class
class Octal:

    def encode(value: int) -> str:
        print(str(oct(value)))
    

    def decode(value: str) -> str:
        print(str(int(value, 8)))

    
    def ConvertToBinary(value: str) -> str:
        print(str(bin(int(value, 8))))

    
    def ConvertToHex(value: str) -> str:
        print(str(hex(int(value, 8))))

    
    def ConvertToAscii(value: str) -> str:
        print(str(chr(int(value, 8))))

# 7-segment display class   
class SevenSegmentDisplay:
    
    def FromBinaryToDecimal(value: str) -> str:
        if (str(int(value, 2)) == '0'):
            print(zero)

        elif (str(int(value, 2)) == '1'):
            print(one)
        
        elif (str(int(value, 2)) == '2'):
            print(two)

        elif (str(int(value, 2)) == '3'):
            print(three)
        
        elif (str(int(value, 2)) == '4'):
            print(four)
        
        elif (str(int(value, 2)) == '5'):
            print(five)
        
        elif (str(int(value, 2)) == '6'):
            print(six)
        
        elif (str(int(value, 2)) == '7'):
            print(seven)

        elif (str(int(value, 2)) == '8'):
            print(eight)
        
        elif (str(int(value, 2)) == '9'):
            print(nine)
        
        elif (int(str(int(value, 2))) > 9):
            raise Exception('Value is too large')
        
    
    def FromHexToDecimal(value: str) -> str:
        if (str(int(value, 16)) == '0'):
            print(zero)

        elif (str(int(value, 16)) == '1'):
            print(one)
        
        elif (str(int(value, 16)) == '2'):
            print(two)

        elif (str(int(value, 16)) == '3'):
            print(three)
        
        elif (str(int(value, 16)) == '4'):
            print(four)
        
        elif (str(int(value, 16)) == '5'):
            print(five)
        
        elif (str(int(value, 16)) == '6'):
            print(six)
        
        elif (str(int(value, 16)) == '7'):
            print(seven)

        elif (str(int(value, 16)) == '8'):
            print(eight)
        
        elif (str(int(value, 16)) == '9'):
            print(nine)
        
        elif (int(str(int(value, 16))) > 9):
            raise Exception('Value is too large')
    

    def FromOctalToDecimal(value: str) -> str:
        if (str(int(value, 8)) == '0'):
            print(zero)

        elif (str(int(value, 8)) == '1'):
            print(one)
        
        elif (str(int(value, 8)) == '2'):
            print(two)

        elif (str(int(value, 8)) == '3'):
            print(three)
        
        elif (str(int(value, 8)) == '4'):
            print(four)
        
        elif (str(int(value, 8)) == '5'):
            print(five)
        
        elif (str(int(value, 8)) == '6'):
            print(six)
        
        elif (str(int(value, 8)) == '7'):
            print(seven)

        elif (str(int(value, 8)) == '8'):
            print(eight)
        
        elif (str(int(value, 8)) == '9'):
            print(nine)
        
        elif (int(str(int(value, 8))) > 9):
            raise Exception('Value is too large')
    

    def FromDecimalToDecimal(value: int) -> str:
        if (value == 0):
            print(zero)
        
        elif (value == 1):
            print(one)

        elif (value == 2):
            print(two)

        elif (value == 3):
            print(three)
        
        elif (value == 4):
            print(four)
        
        elif (value == 5):
            print(five)
        
        elif (value == 6):
            print(six)

        elif (value == 7):
            print(seven)
        
        elif (value == 8):
            print(eight)
        
        elif (value == 9):
            print(nine)
        
        elif (value > 9):
            raise Exception('Value is too large')
