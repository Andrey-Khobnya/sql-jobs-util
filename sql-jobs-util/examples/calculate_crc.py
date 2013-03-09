""" Transformer for calculating CRC of second column """
import zlib

def transform(row):
    return (row[0], '%X' % zlib.crc32(row[1]))