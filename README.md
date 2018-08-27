# stm32_crc_tool
Calculate a CRC checksum as implemented in the STM32F2 and STM32F4 hardware (On these controllers the CRC-Module cannot be configured). Pass the data as command line argument to this program to calculate the CRC checksum with 32 bits with the same algorithm as on the STM32Fx modules.
 
 ## usage
    usage: stm32 crc tool [-h] [-d] [-b BITS] [-p POLY] [-i VALUE] [data [data ...]]
 ### positional arguments:
    data                  list of characters that will be treated as numbers

### optional arguments:
    -h, --help            show this help message and exit
    -d, --demo            display a demonstration of the stm32f4 crc algorithm
    -b BITS, --bits BITS  specify the bit length of the checksum (default is 32
                          bits)
    -p POLY, --poly POLY  specify the crc polynome (default is 0x04C11DB7)
    -i VALUE, --init VALUE
                          specify the initial crc value (default is 0xFFFFFFFF)

The default values equal the ones embedded in the STM hardware modules.
