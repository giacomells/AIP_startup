import struct

def float_to_binary32(value):
    """Converts a float to a binary string representation."""
    [d] = struct.unpack('!I', struct.pack('!f', value))
    return f"{d:032b}"

def binary32_to_float(binary_str):
    """Converts a binary string representation to a float."""
    int_repr = int(binary_str, 2)
    return struct.unpack('!f', struct.pack('!I', int_repr))[0]

def extract_parts(binary_str):
    """Extracts the sign, exponent, and mantissa from a binary string representation of a float."""
    sign = int(binary_str[0], 2)
    exponent = int(binary_str[1:9], 2)
    mantissa = binary_str[9:]
    return sign, exponent, mantissa

def normalize_mantissa_and_exponent(mantissa, exponent):
    """Normalizes the mantissa and adjusts the exponent accordingly."""
    while mantissa[0] != '1' and exponent > 0:
        mantissa = f'{mantissa[1:]}0'
        exponent -= 1
    return mantissa, exponent

def ieee754_addition(bin1, bin2):
    """Adds two binary IEEE 754 numbers."""
    sign1, exp1, mant1 = extract_parts(bin1)
    sign2, exp2, mant2 = extract_parts(bin2)

    # Align exponents
    if exp1 > exp2:
        mant2 = '0' * (exp1 - exp2) + mant2
        exp2 = exp1
    elif exp2 > exp1:
        mant1 = '0' * (exp2 - exp1) + mant1
        exp1 = exp2

    # Add mantissas
    if sign1 == sign2:
        mantissa_sum = binary_addition(f'1{mant1}', f'1{mant2}')
        sign_sum = sign1
    elif mant1 >= mant2:
        mantissa_sum = binary_subtraction(f'1{mant1}', f'1{mant2}')
        sign_sum = sign1
    else:
        mantissa_sum = binary_subtraction(f'1{mant2}', f'1{mant1}')
        sign_sum = sign2

    # Normalize result
    mantissa_sum, exp_sum = normalize_mantissa_and_exponent(mantissa_sum[1:], exp1)

    # Construct final binary representation
    exp_sum_bin = f"{exp_sum:08b}"
    mantissa_sum_bin = mantissa_sum[:23].ljust(23, '0')
    return f"{sign_sum}{exp_sum_bin}{mantissa_sum_bin}"

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

def main():
    test_cases = [
        (1.5, 2.5),
        (-3.0, 2.0),
        (-1.5, -2.5),
        (1.234, 5.678),
        (0.1, 0.2),
        (2.75, -1.25),
        (-0.125, -0.375),
        (7.5, 1.75),
        (-7.5, -1.75),
        (3.14, -2.71)
    ]

    PositiveTest = 0

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
        normalized_mant_sum, exp_sum = normalize_mantissa_and_exponent(mant_sum, exp_sum)
        normalized_mant_sum_converted, exp_sum_converted = normalize_mantissa_and_exponent(mant_sum_converted, exp_sum_converted)

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
