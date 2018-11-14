# stm32_crc_tool
Calculate a CRC checksum as implemented in the STM32Fx Controllers without Crypto-Hash module (e.g.: F405, F407, F427, 
F469, etc.). On these controllers the CRC-Module cannot be configured.

Pass the data as command line argument to this program to calculate the CRC checksum with 32 bits with the same 
algorithm as on the STM32Fx modules.
 
## Usage
    usage: stm32_crc_tool [-h] [-v] [--verbose] [-d] [-b BITS] [-p POLY] [-i VAL]
                          [-f PATH]
                          [data [data ...]]
### Positional arguments:
    data                  list of characters that will be treated as numbers

### Optional arguments:
    -h, --help            show this help message and exit
    -v, --version         show program's version number and exit
    --verbose             enables additional debug output
    -d, --demo            display a demonstration of the stm32f4 crc algorithm
    -b BITS, --bits BITS  bit length of the checksum (default is 32 bits)
    -p POLY, --poly POLY  crc polynomial (default is 0x04C11DB7)
    -i VAL, --init VAL    initial crc value (default is 0xFFFFFFFF)
    -f PATH, --file PATH  use a file as input. The file will be parsed in 4 byte
                          chunks.

The default values equal the ones embedded in the STM hardware modules.

### Example
Linux:

    user@machine: $ python3 stm32_crc_tool.py -f stm32_crc_tool.py -b 8 -p 171 -i 00
    0xb6

## Library usage
The stm32_crc_tool can also be used as a library for other python programs. Therefore the stm32_crc_tool python file 
needs to be included. Then these functions are available: 

### embedded_crc
```python
embedded_crc(input_data:int, poly:int=79764919, initial_crc:int=4294967295, sizeof_input:int=32) -> int
```
Calculates the crc for one given integer. This function represents one iteration on the embedded crc peripheral
in the STM controller family. (The parameter default values equal the ones embedded in the STM hardware modules.)
    
_rtype_ `int`

_param_ input_data: one integer value with the specified bit length

_param_ poly: crc polynomial to use in the algorithm

_param_ initial_crc: crc value to start with (e.g. value from the previous iteration)

_param_ sizeof_input: bit length of the desired crc value

_return_ crc value of the given integer

### msb
```python
msb(val:int, bits:int=8) -> bool
```
returns whether the Most Significant Bit (msb) of the provided value is 1

_rtype_ bool

_param_ **val**: numeric value to check the most msb

_param_ **bits**: bit length of the value

_return_ true if the msb is a 1, false otherwise

### prepare_data
```python
prepare_data(data:str) -> [<class 'int'>]
```
Convert a string into a list of integers. (Uses utf-8 encoding on most machines.)

_rtype_ [int]

_param_ **data**: string to convert

_return_ list of the int representations of the  chars from the string

### process_file
```python
process_file(filename:str, poly:int=79764919, initial_crc:int=4294967295, sizeof_input:int=32) -> int
```
Calculates the crc for a file, interpreted as binary data. (The parameter default values equal the ones embedded
in the STM hardware modules.)

_rtype_ int

_param_ **filename**: path to the file

_param_ **poly**: crc polynomial to use in the algorithm

_param_ **initial_crc**: crc value to start with

_param_ **sizeof_input**: bit length of the desired crc value

_return_ crc value of the provided file

### process_queue
```python
process_queue(data:str, poly:int=79764919, initial_crc:int=4294967295, sizeof_input:int=32) -> int
```
Calculates the crc for a string. (The parameter default values equal the ones embedded in the STM hardware
modules.)

_rtype_ int

_param_ **data**: the crc value is calculated for this string

_param_ **poly**: crc polynomial to use in the algorithm

_param_ **initial_crc**: crc value to start with

_param_ **sizeof_input**: bit length of the desired crc value

_return_ crc value of the provided string

## Licence
This software is provided under the [MIT licence](LICENCE). 


## Future work
My personal plans for this repository:
- Improve the performance of the file crc calculation
- Add CI
