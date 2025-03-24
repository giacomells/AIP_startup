import struct

def float_to_binary32(value):
    """Converts a float to a binary string representation."""
    [d] = struct.unpack('!I', struct.pack('!f', value))
    return f"{d:032b}"

def extract_parts(binary_str):
    """Extracts the sign, exponent, and mantissa from a binary string representation of a float."""
    sign = binary_str[0]
    exponent = binary_str[1:9]
    mantissa = binary_str[9:32]
    return sign, exponent, mantissa

def binary_addition(bin1, bin2):
    """Adds two binary strings and returns the result."""
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = ''
    carry = 0
    for i in range(max_len - 1, -1, -1):
        total = carry
        total += 1 if bin1[i] == '1' else 0
        total += 1 if bin2[i] == '1' else 0
        result = ('1' if total % 2 == 1 else '0') + result
        carry = 0 if total < 2 else 1

    if carry != 0:
        result = f'1{result}'

    return result.zfill(max_len)

def binary_subtraction(bin1, bin2):
    """Subtracts two binary strings and returns the result."""
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)

    result = ''
    borrow = 0
    for i in range(max_len - 1, -1, -1):
        sub = (1 if bin1[i] == '1' else 0) - (1 if bin2[i] == '1' else 0) - borrow
        if sub == -1:
            sub = 1
            borrow = 1
        elif sub == -2:
            sub = 0
            borrow = 1
        else:
            borrow = 0
        result = ('1' if sub == 1 else '0') + result

    return result.lstrip('0').zfill(max_len)

def normalize_mantissa(mantissa):
    """Normalizes the mantissa and adjusts the exponent accordingly."""
    shift = 0
    while mantissa[0] != '1' and len(mantissa) > 23:
        mantissa = f'{mantissa[1:]}0'
        shift -= 1
    return mantissa[:23], shift



def ieee754_addition(bin1, bin2):
    """Adds two IEEE 754 binary string numbers and returns the result as an IEEE 754 binary string."""
    # Extract components
    sign1, exp1, mant1 = extract_parts(bin1)
    sign2, exp2, mant2 = extract_parts(bin2)

    # Convert exponents to integers
    exp1 = int(exp1, 2) - 127
    exp2 = int(exp2, 2) - 127

    # Align exponents
    if exp1 > exp2:
        shift = exp1 - exp2
        mant2 = '0' * shift + mant2
        exp = exp1
    else:
        shift = exp2 - exp1
        mant1 = '0' * shift + mant1
        exp = exp2

    # Add or subtract mantissas
    if sign1 == sign2:
        result_mantissa = binary_addition(mant1, mant2)
        result_sign = sign1
    else:
        if int(mant1, 2) >= int(mant2, 2):
            result_mantissa = binary_subtraction(mant1, mant2)
            result_sign = sign1
        else:
            result_mantissa = binary_subtraction(mant2, mant1)
            result_sign = sign2

    # Normalize the result
    result_mantissa, shift = normalize_mantissa(result_mantissa)
    exp += shift

    # Convert the exponent back to binary and adjust for bias
    result_exponent = f"{exp + 127:08b}"

    return result_sign + result_exponent + result_mantissa







# Main function to demonstrate the conversion and addition
def main():
    # Take two decimal numbers as input
    num1 = float(input("Enter the first decimal number: "))
    num2 = float(input("Enter the second decimal number: "))

    # Convert the decimal numbers to IEEE 754 binary strings and extract their components
    bin1 = float_to_binary32(num1)
    sign1, exp1, mant1 = extract_parts(bin1)    
    
    bin2 = float_to_binary32(num2)
    sign2, exp2, mant2 = extract_parts(bin2)    
    
    

    print(f"Binary representation of {num1}: {bin1}")
    print(f"Sign: {sign1}, Exponent: {exp1}, Mantissa: {mant1}")
    print(f"Binary representation of {num2}: {bin2}")
    print(f"Sign: {sign2}, Exponent: {exp2}, Mantissa: {mant2}")
 
    #USING THE ALGORITHM FOR IEE754 ADDITION
    binarySum = ieee754_addition(bin1, bin2)
    signSum, expSum, mantSum = extract_parts(binarySum)    
    print(f"Binary representation of the sum: {binarySum}")
    print(f"Sign: {signSum}, Exponent: {expSum}, Mantissa: {mantSum}")
    
    #USING THE CONVERSION FLOAT-BINARY-FLOAT
    floatSum = num1 + num2
    binarySumConverted = float_to_binary32(floatSum)
    signSumConverted, expSumConverted, mantSumConverted = extract_parts(binarySumConverted)    
    print(f"Integer representation of the sum {floatSum}: {binarySumConverted} ")
    print(f"Sign: {signSumConverted}, Exponent: {expSumConverted}, Mantissa: {mantSumConverted}")
    
    
    

if __name__ == "__main__":
    main()
