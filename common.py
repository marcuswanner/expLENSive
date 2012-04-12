def _reverse(instr):
    outstr = ''
    for i in range(len(instr)):
        outstr += instr[(len(instr)-1)-i]
    return outstr

def hexbyte2hex(instr):
    outstr = ''
    for byte in instr:
        outstr += textpart.get(byte)
    return outstr

def hex2hexbyte(instr):
    return reversetextpart.get(instr)

def hex2binary(instr):
    return bin(int(instr, 16))[2:]

def binary2hex(instr):
    return hex(int(instr, 2))[2:]

def hex2decimal(instr):
    return int(instr, 16)

def decimal2hex(instr):
    return hex(instr)[2:]

def hexbyte2binary(byte):
    outstr = hex2binary(hexbyte2hex(byte))
    while len(outstr) < 8:
        outstr = '0' + outstr
    return outstr

def hexbyte2decimal(byte):
    return hex2decimal(hexbyte2hex(byte))
    
def hexdword2decimal(instr):
    outstr = _reverse(instr) #dwords are little-endian in bmp files
    hexpartonly = ''
    for byte in outstr:
        hexpartonly += hexbyte2hex(byte)
    outstr = hex2decimal(hexpartonly)
    return outstr

def decimal2hexbyte(instr):
    if int(instr) > 255:
        raise ValueError("Numbers larger than 255 can't be stored in 1 byte.")
    hexversion = decimal2hex(instr)
    if len(hexversion) == 1:
        finalhexversion = '0' + hexversion
    else:
        finalhexversion = hexversion
    return hex2hexbyte(finalhexversion)

def decimal2hexdword(number):
    if number > 4294967295:
        raise  ValueError("Numbers larger than 4,294,967,295 can't be stored in 4 bytes.")
    hexnumber = decimal2hex(number)
    #pad the number with 0s at the beginning
    hexnumber = '0'*(8-len(hexnumber)) + hexnumber
    splitparts = []
    for i in range(len(hexnumber)/2):
        splitparts.append(hexnumber[i*2:i*2+2])
    splitparts.reverse()
    outstr = ''
    for i in splitparts:
        outstr += hex2hexbyte(i)
    return outstr

def binary2hexbyte(instr):
    if int(instr, 2) > 255:
        raise ValueError("Numbers larger than 11111111 can't be stored in 1 byte.")
    hexversion = binary2hex(instr)
    if len(hexversion) == 1:
        finalhexversion = '0' + hexversion
    else:
        finalhexversion = hexversion
    return hex2hexbyte(finalhexversion)

def invertbinary(instr):
    outstr = ''
    for i in instr:
        if i == '0':
            outstr += '1'
        elif i == '1':
            outstr += '0'
    return outstr

def getbyteindex(byte):
    return hex2decimal(gettextpart(byte))

def readbmpfile(filename):
    infile = open(filename, 'rU') #universal newline mode
    #the header data (width, height, etc.)
    indentifier = infile.read(2)
    if indentifier != 'BM':
        raise TypeError, 'Error!!! Not a valid bitmap file.'
    infile.read(16) #junk data
    ImgWidth = hexdword2decimal(infile.read(4))
    ImgHeight = hexdword2decimal(infile.read(4))
    infile.read(2) #more junk data
    bitsperpixel = hexbyte2hex(infile.read(1))
    if bitsperpixel != '01':
        raise TypeError, 'Error!!! Not a monochrome bitmap.'
    compression = hexbyte2hex(infile.read(1))
    if compression != '00':
        raise TypeError, 'Error!!! Compression not supported.'
    infile.read(32) #more junk data (pallet, etc)
    #now we read the pixel data. Horizontal lines are padded to have a 32-bit
    #multiple length. 0s are black, 1s are white, so we have to invert the data.
    #lines are listed from bottom to top.
    rowarray = []
    bitsperline = ImgWidth + (32-(ImgWidth%32))
    bytesperline = bitsperline/8
    usedbitsperline = ImgWidth
    for row in range(ImgHeight):
        currentlinedata = infile.read(bytesperline)
        currentlineoutput = ''
        for currentpixeldata in currentlinedata:
            currentlineoutput += hexbyte2binary(currentpixeldata)
        currentlineoutput = currentlineoutput[0:usedbitsperline]
        currentlineoutput = invertbinary(currentlineoutput)
        rowarray.append(currentlineoutput)
    rowarray.reverse()
    PixelArray = ''
    for row in rowarray:
        PixelArray += row
    rowarray = None
    infile.close()
    return ImgWidth, ImgHeight, PixelArray

textpart = {
    '\x00': '00',
    '\x01': '01',
    '\x02': '02',
    '\x03': '03',
    '\x04': '04',
    '\x05': '05',
    '\x06': '06',
    '\x07': '07',
    '\x08': '08',
    '\x09': '09',
    '\x0a': '0a',
    '\x0b': '0b',
    '\x0c': '0c',
    '\x0d': '0d',
    '\x0e': '0e',
    '\x0f': '0f',
    '\x10': '10',
    '\x11': '11',
    '\x12': '12',
    '\x13': '13',
    '\x14': '14',
    '\x15': '15',
    '\x16': '16',
    '\x17': '17',
    '\x18': '18',
    '\x19': '19',
    '\x1a': '1a',
    '\x1b': '1b',
    '\x1c': '1c',
    '\x1d': '1d',
    '\x1e': '1e',
    '\x1f': '1f',
    '\x20': '20',
    '\x21': '21',
    '\x22': '22',
    '\x23': '23',
    '\x24': '24',
    '\x25': '25',
    '\x26': '26',
    '\x27': '27',
    '\x28': '28',
    '\x29': '29',
    '\x2a': '2a',
    '\x2b': '2b',
    '\x2c': '2c',
    '\x2d': '2d',
    '\x2e': '2e',
    '\x2f': '2f',
    '\x30': '30',
    '\x31': '31',
    '\x32': '32',
    '\x33': '33',
    '\x34': '34',
    '\x35': '35',
    '\x36': '36',
    '\x37': '37',
    '\x38': '38',
    '\x39': '39',
    '\x3a': '3a',
    '\x3b': '3b',
    '\x3c': '3c',
    '\x3d': '3d',
    '\x3e': '3e',
    '\x3f': '3f',
    '\x40': '40',
    '\x41': '41',
    '\x42': '42',
    '\x43': '43',
    '\x44': '44',
    '\x45': '45',
    '\x46': '46',
    '\x47': '47',
    '\x48': '48',
    '\x49': '49',
    '\x4a': '4a',
    '\x4b': '4b',
    '\x4c': '4c',
    '\x4d': '4d',
    '\x4e': '4e',
    '\x4f': '4f',
    '\x50': '50',
    '\x51': '51',
    '\x52': '52',
    '\x53': '53',
    '\x54': '54',
    '\x55': '55',
    '\x56': '56',
    '\x57': '57',
    '\x58': '58',
    '\x59': '59',
    '\x5a': '5a',
    '\x5b': '5b',
    '\x5c': '5c',
    '\x5d': '5d',
    '\x5e': '5e',
    '\x5f': '5f',
    '\x60': '60',
    '\x61': '61',
    '\x62': '62',
    '\x63': '63',
    '\x64': '64',
    '\x65': '65',
    '\x66': '66',
    '\x67': '67',
    '\x68': '68',
    '\x69': '69',
    '\x6a': '6a',
    '\x6b': '6b',
    '\x6c': '6c',
    '\x6d': '6d',
    '\x6e': '6e',
    '\x6f': '6f',
    '\x70': '70',
    '\x71': '71',
    '\x72': '72',
    '\x73': '73',
    '\x74': '74',
    '\x75': '75',
    '\x76': '76',
    '\x77': '77',
    '\x78': '78',
    '\x79': '79',
    '\x7a': '7a',
    '\x7b': '7b',
    '\x7c': '7c',
    '\x7d': '7d',
    '\x7e': '7e',
    '\x7f': '7f',
    '\x80': '80',
    '\x81': '81',
    '\x82': '82',
    '\x83': '83',
    '\x84': '84',
    '\x85': '85',
    '\x86': '86',
    '\x87': '87',
    '\x88': '88',
    '\x89': '89',
    '\x8a': '8a',
    '\x8b': '8b',
    '\x8c': '8c',
    '\x8d': '8d',
    '\x8e': '8e',
    '\x8f': '8f',
    '\x90': '90',
    '\x91': '91',
    '\x92': '92',
    '\x93': '93',
    '\x94': '94',
    '\x95': '95',
    '\x96': '96',
    '\x97': '97',
    '\x98': '98',
    '\x99': '99',
    '\x9a': '9a',
    '\x9b': '9b',
    '\x9c': '9c',
    '\x9d': '9d',
    '\x9e': '9e',
    '\x9f': '9f',
    '\xa0': 'a0',
    '\xa1': 'a1',
    '\xa2': 'a2',
    '\xa3': 'a3',
    '\xa4': 'a4',
    '\xa5': 'a5',
    '\xa6': 'a6',
    '\xa7': 'a7',
    '\xa8': 'a8',
    '\xa9': 'a9',
    '\xaa': 'aa',
    '\xab': 'ab',
    '\xac': 'ac',
    '\xad': 'ad',
    '\xae': 'ae',
    '\xaf': 'af',
    '\xb0': 'b0',
    '\xb1': 'b1',
    '\xb2': 'b2',
    '\xb3': 'b3',
    '\xb4': 'b4',
    '\xb5': 'b5',
    '\xb6': 'b6',
    '\xb7': 'b7',
    '\xb8': 'b8',
    '\xb9': 'b9',
    '\xba': 'ba',
    '\xbb': 'bb',
    '\xbc': 'bc',
    '\xbd': 'bd',
    '\xbe': 'be',
    '\xbf': 'bf',
    '\xc0': 'c0',
    '\xc1': 'c1',
    '\xc2': 'c2',
    '\xc3': 'c3',
    '\xc4': 'c4',
    '\xc5': 'c5',
    '\xc6': 'c6',
    '\xc7': 'c7',
    '\xc8': 'c8',
    '\xc9': 'c9',
    '\xca': 'ca',
    '\xcb': 'cb',
    '\xcc': 'cc',
    '\xcd': 'cd',
    '\xce': 'ce',
    '\xcf': 'cf',
    '\xd0': 'd0',
    '\xd1': 'd1',
    '\xd2': 'd2',
    '\xd3': 'd3',
    '\xd4': 'd4',
    '\xd5': 'd5',
    '\xd6': 'd6',
    '\xd7': 'd7',
    '\xd8': 'd8',
    '\xd9': 'd9',
    '\xda': 'da',
    '\xdb': 'db',
    '\xdc': 'dc',
    '\xdd': 'dd',
    '\xde': 'de',
    '\xdf': 'df',
    '\xe0': 'e0',
    '\xe1': 'e1',
    '\xe2': 'e2',
    '\xe3': 'e3',
    '\xe4': 'e4',
    '\xe5': 'e5',
    '\xe6': 'e6',
    '\xe7': 'e7',
    '\xe8': 'e8',
    '\xe9': 'e9',
    '\xea': 'ea',
    '\xeb': 'eb',
    '\xec': 'ec',
    '\xed': 'ed',
    '\xee': 'ee',
    '\xef': 'ef',
    '\xf0': 'f0',
    '\xf1': 'f1',
    '\xf2': 'f2',
    '\xf3': 'f3',
    '\xf4': 'f4',
    '\xf5': 'f5',
    '\xf6': 'f6',
    '\xf7': 'f7',
    '\xf8': 'f8',
    '\xf9': 'f9',
    '\xfa': 'fa',
    '\xfb': 'fb',
    '\xfc': 'fc',
    '\xfd': 'fd',
    '\xfe': 'fe',
    '\xff': 'ff',
    }

reversetextpart = dict(zip(textpart.values(), textpart.keys()))
