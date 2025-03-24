import struct

def float_to_binary32(value):
    """Converts a float to a binary string representation."""
    [d] = struct.unpack('!I', struct.pack('!f', value))
    return f"{d:032b}"

def extract_parts(binary_str):
    """Extracts the sign, exponent, and mantissa from a binary string representation of a float."""
    sign = binary_str[0]
    exponent = binary_str[1:9]
    mantissa = '1' + binary_str[9:]  # Add implicit leading 1
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
        result = '1' + result

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
    while mantissa[0] != '1' and len(mantissa) > 1:
        mantissa = mantissa[1:] + '0'
        shift -= 1
    if len(mantissa) == 0:
        mantissa = '0'
        shift = 0
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
        #GESTIONE DELLA SOTTRAZIONE IN MANIERA PIÙ ACCURATA
        if exp1 > exp2:
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




def main():
    test_cases = [
        (1, 2),
        (0, 1),
        (-1, 2),
        (-2, 1),
        (2.5, 1.3),
        (1.5, 0.5),
        (3.0, 4.0),
        (1.234, 5.678),
        (0.1, 0.2),
    ]
    
    PositiveTest = 0
    
    # DOBBIAMO PROVARE CON NUMERI NEGATIVI, ENTRA IN LOOP E NON NE ESCE PIÙ!!!

    for num1, num2 in test_cases:
        bin1 = float_to_binary32(num1)
        bin2 = float_to_binary32(num2)

        print(f"Decimal numbers: {num1}, {num2}")
        print(f"Binary representation of {num1}: {bin1}")
        print(f"Binary representation of {num2}: {bin2}")

        # Using the algorithm for IEEE 754 addition
        binary_sum = ieee754_addition(bin1, bin2)
        sign_sum, exp_sum, mant_sum = extract_parts(binary_sum)
        print("IEEE 754 Addition Result:")
        print(f"Binary representation of the sum: {binary_sum}")
        print(f"Sign: {sign_sum}, Exponent: {exp_sum}, Mantissa: {mant_sum}")

        # Using the conversion float-binary-float
        float_sum = num1 + num2
        binary_sum_converted = float_to_binary32(float_sum)
        sign_sum_converted, exp_sum_converted, mant_sum_converted = extract_parts(binary_sum_converted)
        print("Float-Binary-Float Conversion Result:")
        print(f"Binary representation of the sum {float_sum}: {binary_sum_converted}")
        print(f"Sign: {sign_sum_converted}, Exponent: {exp_sum_converted}, Mantissa: {mant_sum_converted}")

        # Normalize mantissas for comparison
        normalized_mant_sum = normalize_mantissa(mant_sum)[0]
        normalized_mant_sum_converted = normalize_mantissa(mant_sum_converted)[0]

        # Compare normalized mantissas
        if normalized_mant_sum == normalized_mant_sum_converted:
            print("Verification: Results match! ✔️")
            PositiveTest += 1
        else:
            print("Verification: Results do not match! ❌")

        print("-" * 40)
        
    # Print summary
    print(f"Total tests: {len(test_cases)}")
    print(f"Tests passed: {PositiveTest}")
    print(f"Tests failed: {len(test_cases) - PositiveTest}")

if __name__ == "__main__":
    main()
