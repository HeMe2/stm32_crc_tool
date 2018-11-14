#!/usr/bin/python3

from struct import unpack

_debug_mode = False


def _debug_msg(a, b) -> None:
    if _debug_mode:
        print(a, b)


def msb(val: int, bits: int = 8) -> bool:
    """returns whether the Most Significant Bit (msb) of the provided value is 1
    :rtype: bool
    :param val: numeric value to check the most msb
    :param bits: bit length of the value
    :return: true if the msb is a 1, false otherwise
    """
    return bool(val & (1 << (bits - 1)))


def embedded_crc(input_data: int, poly: int = 0x04C11DB7, initial_crc: int = 0xFFFFFFFF, sizeof_input: int = 32) -> int:
    """Calculates the crc for one given integer. This function represents one iteration on the embedded crc peripheral
    in the STM controller family. (The parameter default values equal the ones embedded in the STM hardware modules.)
    :rtype: int
    :param input_data: one integer value with the specified bit length
    :param poly: crc polynomial to use in the algorithm
    :param initial_crc: crc value to start with (e.g. value from the previous iteration)
    :param sizeof_input: bit length of the desired crc value
    :return: crc value of the given integer
    """
    # create the proper mask
    msk = 0
    for i in range(sizeof_input):
        msk = (msk << 1) | 1

    # start of the algorithm described in the stm32 crc application manual
    _debug_msg("initial_crc", bin(initial_crc))
    _debug_msg("input_data", bin(input_data))

    crc = initial_crc ^ input_data
    _debug_msg("crc = initial ^ input", bin(crc))

    b_index = 0
    while b_index < sizeof_input:

        _debug_msg("crc", bin(crc))

        if msb(crc, sizeof_input):
            crc = ((crc << 1) ^ poly) & msk
            _debug_msg("crc ^ poly", bin(crc))
        else:
            crc = (crc << 1) & msk

        b_index += 1

    return crc


def prepare_data(data: str) -> [int]:
    """Convert a string into a list of integers. (Uses utf-8 encoding on most machines.)
    :rtype: [int]
    :param data: string to convert
    :return: list of the int representations of the  chars from the string
    """
    reduced_data = []
    for word in data:
        for char in word:
            reduced_data.append(ord(char))
    return reduced_data


def process_queue(data: str, poly: int = 0x04C11DB7, initial_crc: int = 0xFFFFFFFF, sizeof_input: int = 32) -> int:
    """Calculates the crc for a string. (The parameter default values equal the ones embedded in the STM hardware
    modules.)
    :rtype: int
    :param data: the crc value is calculated for this string
    :param poly: crc polynomial to use in the algorithm
    :param initial_crc: crc value to start with
    :param sizeof_input: bit length of the desired crc value
    :return: crc value of the provided string
    """
    data = prepare_data(data)
    crc = initial_crc
    for val in data:
        crc = embedded_crc(val, poly, crc, sizeof_input)
    return crc


def process_file(filename: str, poly: int = 0x04C11DB7, initial_crc: int = 0xFFFFFFFF, sizeof_input: int = 32) -> int:
    """Calculates the crc for a file, interpreted as binary data. (The parameter default values equal the ones embedded
    in the STM hardware modules.)
    :rtype: int
    :param filename: path to the file
    :param poly: crc polynomial to use in the algorithm
    :param initial_crc: crc value to start with
    :param sizeof_input: bit length of the desired crc value
    :return: crc value of the provided file
    """
    crc = initial_crc
    with open(filename, "rb") as input_file:
        binary = input_file.read()

        for i in range(len(binary) // 4):
            chunk = binary[i * 4: i * 4 + 4]
            _debug_msg("chunk", chunk)
            val = unpack('i', chunk)[0]
            _debug_msg("unpacked value", val)
            crc = embedded_crc(val, poly, crc, sizeof_input)

        remaining_bytes = len(binary) % 4
        if remaining_bytes > 0:
            chunk = binary[-remaining_bytes:] + bytes(4 - remaining_bytes)
            _debug_msg("chunk", chunk)
            val = unpack('i', chunk)[0]
            _debug_msg("unpacked value", val)
            crc = embedded_crc(val, poly, crc, sizeof_input)

    return crc


def _demonstration() -> None:
    """Prints a demonstration of the stm32 crc algorithm. The first example matches the example from the stm32f4
    app note: AN4187. The second shows uses 32 bits as implemented in the stm32f4 hardware"""
    global _debug_mode
    print("stm - crc tool demonstration\n")

    print("start first test with:\n")

    print("input_data = 0xC1")
    print("poly = 0xCB")
    print("initial_crc = 0xFF")

    print("(configuration as in the stm crc application note, algorithm set to 8 bit mode)")

    input_data = 0xC1
    poly = 0xCB
    initial_crc = 0xFF

    _debug_mode = True
    crc = embedded_crc(input_data, poly, initial_crc, 8)
    _debug_mode = False
    print("computed crc =", hex(crc))

    print("\n\nstart another test with:\n")

    print("input_data = 0x00000041")
    print("poly = 0x04D11CDB7 (in stm32f4 hardware embedded)")
    print("initial_crc = 0xFFFFFFFF (in stm32f4 hardware embedded)")

    input_data = 0x00000041
    poly = 0x04C11DB7
    initial_crc = 0xFFFFFFFF

    crc = embedded_crc(input_data)
    print("computed crc =", hex(crc))


def _handle_arguments() -> (object, object):
    import argparse
    parser = argparse.ArgumentParser(description="Calculate a CRC checksum as implemented in the STM32Fx "
                                                 "Controllers without Crypto-Hash module (e.g.: F405, F407, "
                                                 "F427, F469, etc.). On these controllers the CRC-Module cannot "
                                                 "be configured. "
                                                 "Pass the data as command line argument to this program to "
                                                 "calculate the CRC checksum with 32 bits with the same "
                                                 "algorithm as on the STM32Fx modules.",
                                     prog="stm32_crc_tool",
                                     epilog="The default values equal the ones embedded in the STM hardware "
                                            "modules.")

    parser.add_argument("data", nargs='*',
                        help="list of characters that will be treated as numbers")
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.1")
    parser.add_argument("--verbose", action="store_true",
                        help="enables additional debug output")
    parser.add_argument("-d", "--demo", action="store_true",
                        help="display a demonstration of the stm32f4 crc algorithm")
    parser.add_argument("-b", "--bits", type=int, metavar="BITS", default=32,
                        help="bit length of the checksum (default is 32 bits)")
    parser.add_argument("-p", "--poly", type=int, default=0x04C11DB7,
                        help="crc polynomial (default is 0x04C11DB7)")
    parser.add_argument("-i", "--init", type=int, metavar="VAL", default=0xFFFFFFFF,
                        help="initial crc value (default is 0xFFFFFFFF)")
    parser.add_argument("-f", "--file", type=str, metavar="PATH",
                        help="use a file as input. The file will be parsed in 4 byte chunks.")

    return parser.parse_args(), parser


if __name__ == "__main__":
    # read command line arguments
    args, argument_parser = _handle_arguments()

    if args.demo:
        _demonstration()
    else:
        if args.verbose:
            _debug_mode = True

        if args.file is not None:
            CRC = process_file(args.file, args.poly, args.init, args.bits)
            print(hex(CRC))
        elif len(args.data) == 0:
            argument_parser.print_help()
        else:
            CRC = process_queue(args.data, args.poly, args.init, args.bits)
            print(hex(CRC))
