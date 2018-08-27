#!/usr/bin/python3

_debug_mode = False


def debug_msg(a, b):
    if(_debug_mode):
        print(a, b)


def msb(val:int, bits: int=8)-> bool:
    """returns whether the Most Significant Bit (msb) of the provided value is 1
       (only for 32 bit variables)"""
    return bool(val & (1 << (bits-1)))


def embedded_crc(input_data: int, poly: int=0x04C11DB7, initial_crc: int=0xFFFFFFFF, sizeof_input: int=32) -> int:
    # create the proper mask
    msk = 0
    for i in range(sizeof_input):
        msk = (msk << 1) | 1

    # start of the algorithm described in the stm32 crc application manual
    debug_msg("initial_crc", bin(initial_crc))
    debug_msg("input_data", bin(input_data))

    crc = initial_crc ^ input_data
    debug_msg("crc = initial ^ input", bin(crc))
    
    bindex = 0
    while bindex < sizeof_input:

        debug_msg("crc", bin(crc))

        if msb(crc, sizeof_input):
            crc = ((crc << 1) ^ poly) & msk
            debug_msg("crc ^ poly", bin(crc))
        else:
            crc = (crc << 1) & msk

        bindex += 1

    return crc


def prepare_data(data):
    reduced_data = []
    for word in data:
        for char in word:
            reduced_data.append(ord(char))
    return reduced_data

def process_queue(data, poly: int=0x04C11DB7, initial_crc: int=0xFFFFFFFF, sizeof_input: int=32) -> int:
    data = prepare_data(data)
    crc = initial_crc
    for val in data:
        crc = embedded_crc(val, poly, crc, sizeof_input)
    return crc


def demonstration():
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


def handle_arguments():
    parser = argparse.ArgumentParser(description="Calculate a CRC checksum as implemented in the STM32F2 and "
                                                 "STM32F4 hardware (On these controllers the CRC-Module cannot "
                                                 "be configured). Pass the data as command line argument to "
                                                 "this program to calculate the CRC checksum with 32 bits with "
                                                 "the same algorithm as on the STM32Fx modules.", 
                                     prog="stm32 crc tool",
                                     epilog="The default values equal the ones embedded in the STM hardware "
                                            "modules.")

    parser.add_argument("data", nargs='*',
                        help="list of characters that will be treated as numbers")
    parser.add_argument("-d", "--demo", action="store_true", 
                        help="display a demonstration of the stm32f4 crc algorithm")
    parser.add_argument("-b", "--bits", type=int, metavar="BITS", default=32, 
                        help="specify the bit length of the checksum (default is 32 bits)")
    parser.add_argument("-p", "--poly", type=int, default=0x04C11DB7, 
                        help="specify the crc polynome (default is 0x04C11DB7)")
    parser.add_argument("-i", "--init", type=int, metavar="VALUE", default=0xFFFFFFFF, 
                        help="specify the initial crc value (default is 0xFFFFFFFF)")

    return parser.parse_args(), parser


if __name__=="__main__":
    # read command line arguments
    import argparse
    args, parser = handle_arguments()

    if args.demo:
        demonstration()
    else:
        if len(args.data) == 0:
            parser.print_help()
        else:
            crc = process_queue(args.data, args.poly, args.init, args.bits)
            print(hex(crc))
