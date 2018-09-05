# stm32_crc_tool
Calculate a CRC checksum as implemented in the STM32Fx Controllers without Crypto-Hash module (e.g.: F405, F407, F427, F469, etc.). On these controllers the CRC-Module cannot be configured.

Pass the data as command line argument to this program to calculate the CRC checksum with 32 bits with the same algorithm as on the STM32Fx modules.
 
## usage
    usage: stm32_crc_tool [-h] [-v] [-d] [-b BITS] [-p POLY] [-i VAL]
                          [data [data ...]]
### positional arguments:
    data                  list of characters that will be treated as numbers

### optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    -d, --demo            display a demonstration of the stm32f4 crc algorithm
    -b BITS, --bits BITS  bit length of the checksum (default is 32 bits)
    -p POLY, --poly POLY  crc polynome (default is 0x04C11DB7)
    -i VAL, --init VAL    initial crc value (default is 0xFFFFFFFF)

The default values equal the ones embedded in the STM hardware modules.
