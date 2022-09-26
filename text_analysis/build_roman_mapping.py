import argparse


ROMAN = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]


def int_to_roman(number: int) -> str:
    """
    Converts integer to roman numeral.

    Args:
        number: integer to be converted.

    Returns:
        roman numeral.
    """

    result = []
    for arabic, roman in ROMAN:
        factor, number = divmod(number, arabic)
        result.append(roman * factor)
        if number == 0:
            break
    return "".join(result)


def main():
    parser = argparse.ArgumentParser(description='Generate roman => int mappings file.')
    parser.add_argument('--max-number', type=int, default=3999,
                        help='Max number to generate roman equivalent.')
    parser.add_argument('--output-path', type=str, required=True,
                        help='Filename to write results.')
    cmd_args = parser.parse_args()
    
    with open(cmd_args.output_path, 'w') as f:
        for n in range(1, cmd_args.max_number + 1):
            f.write(f'{int_to_roman(n)} => {n}\n')


if __name__ == '__main__':
    main()
