#!/usr/bin/env python3

import sys, re
import argparse
import shutil
from PIL import Image
from PIL import ImageEnhance
import numpy as np

# Developped by Cedric Bouysset
# Based on python codes by Micah Elliott and Christian Diener

#-----------------------------------------------------------------------
# Map RGB color code to xterm 256 color code
# By MicahElliott
""" Convert values between RGB hex codes and xterm-256 color codes.
Nice long listing of all 256 colors and their codes. Useful for
developing console color themes, or even script output schemes.
Resources:
* http://en.wikipedia.org/wiki/8-bit_color
* http://en.wikipedia.org/wiki/ANSI_escape_code
* /usr/share/X11/rgb.txt
I'm not sure where this script was inspired from. I think I must have
written it from scratch, though it's been several years now.
"""

#__author__    = 'Micah Elliott http://MicahElliott.com'
#__version__   = '0.1'
#__copyright__ = 'Copyright (C) 2011 Micah Elliott.  All rights reserved.'
#__license__   = 'WTFPL http://sam.zoy.org/wtfpl/'


CLUT = [  # color look-up table
#    8-bit, RGB hex

    # Primary 3-bit (8 colors). Unique representation!
    ('00',  '000000'),
    ('01',  '800000'),
    ('02',  '008000'),
    ('03',  '808000'),
    ('04',  '000080'),
    ('05',  '800080'),
    ('06',  '008080'),
    ('07',  'c0c0c0'),

    # Equivalent "bright" versions of original 8 colors.
    ('08',  '808080'),
    ('09',  'ff0000'),
    ('10',  '00ff00'),
    ('11',  'ffff00'),
    ('12',  '0000ff'),
    ('13',  'ff00ff'),
    ('14',  '00ffff'),
    ('15',  'ffffff'),

    # Strictly ascending.
    ('16',  '000000'),
    ('17',  '00005f'),
    ('18',  '000087'),
    ('19',  '0000af'),
    ('20',  '0000d7'),
    ('21',  '0000ff'),
    ('22',  '005f00'),
    ('23',  '005f5f'),
    ('24',  '005f87'),
    ('25',  '005faf'),
    ('26',  '005fd7'),
    ('27',  '005fff'),
    ('28',  '008700'),
    ('29',  '00875f'),
    ('30',  '008787'),
    ('31',  '0087af'),
    ('32',  '0087d7'),
    ('33',  '0087ff'),
    ('34',  '00af00'),
    ('35',  '00af5f'),
    ('36',  '00af87'),
    ('37',  '00afaf'),
    ('38',  '00afd7'),
    ('39',  '00afff'),
    ('40',  '00d700'),
    ('41',  '00d75f'),
    ('42',  '00d787'),
    ('43',  '00d7af'),
    ('44',  '00d7d7'),
    ('45',  '00d7ff'),
    ('46',  '00ff00'),
    ('47',  '00ff5f'),
    ('48',  '00ff87'),
    ('49',  '00ffaf'),
    ('50',  '00ffd7'),
    ('51',  '00ffff'),
    ('52',  '5f0000'),
    ('53',  '5f005f'),
    ('54',  '5f0087'),
    ('55',  '5f00af'),
    ('56',  '5f00d7'),
    ('57',  '5f00ff'),
    ('58',  '5f5f00'),
    ('59',  '5f5f5f'),
    ('60',  '5f5f87'),
    ('61',  '5f5faf'),
    ('62',  '5f5fd7'),
    ('63',  '5f5fff'),
    ('64',  '5f8700'),
    ('65',  '5f875f'),
    ('66',  '5f8787'),
    ('67',  '5f87af'),
    ('68',  '5f87d7'),
    ('69',  '5f87ff'),
    ('70',  '5faf00'),
    ('71',  '5faf5f'),
    ('72',  '5faf87'),
    ('73',  '5fafaf'),
    ('74',  '5fafd7'),
    ('75',  '5fafff'),
    ('76',  '5fd700'),
    ('77',  '5fd75f'),
    ('78',  '5fd787'),
    ('79',  '5fd7af'),
    ('80',  '5fd7d7'),
    ('81',  '5fd7ff'),
    ('82',  '5fff00'),
    ('83',  '5fff5f'),
    ('84',  '5fff87'),
    ('85',  '5fffaf'),
    ('86',  '5fffd7'),
    ('87',  '5fffff'),
    ('88',  '870000'),
    ('89',  '87005f'),
    ('90',  '870087'),
    ('91',  '8700af'),
    ('92',  '8700d7'),
    ('93',  '8700ff'),
    ('94',  '875f00'),
    ('95',  '875f5f'),
    ('96',  '875f87'),
    ('97',  '875faf'),
    ('98',  '875fd7'),
    ('99',  '875fff'),
    ('100', '878700'),
    ('101', '87875f'),
    ('102', '878787'),
    ('103', '8787af'),
    ('104', '8787d7'),
    ('105', '8787ff'),
    ('106', '87af00'),
    ('107', '87af5f'),
    ('108', '87af87'),
    ('109', '87afaf'),
    ('110', '87afd7'),
    ('111', '87afff'),
    ('112', '87d700'),
    ('113', '87d75f'),
    ('114', '87d787'),
    ('115', '87d7af'),
    ('116', '87d7d7'),
    ('117', '87d7ff'),
    ('118', '87ff00'),
    ('119', '87ff5f'),
    ('120', '87ff87'),
    ('121', '87ffaf'),
    ('122', '87ffd7'),
    ('123', '87ffff'),
    ('124', 'af0000'),
    ('125', 'af005f'),
    ('126', 'af0087'),
    ('127', 'af00af'),
    ('128', 'af00d7'),
    ('129', 'af00ff'),
    ('130', 'af5f00'),
    ('131', 'af5f5f'),
    ('132', 'af5f87'),
    ('133', 'af5faf'),
    ('134', 'af5fd7'),
    ('135', 'af5fff'),
    ('136', 'af8700'),
    ('137', 'af875f'),
    ('138', 'af8787'),
    ('139', 'af87af'),
    ('140', 'af87d7'),
    ('141', 'af87ff'),
    ('142', 'afaf00'),
    ('143', 'afaf5f'),
    ('144', 'afaf87'),
    ('145', 'afafaf'),
    ('146', 'afafd7'),
    ('147', 'afafff'),
    ('148', 'afd700'),
    ('149', 'afd75f'),
    ('150', 'afd787'),
    ('151', 'afd7af'),
    ('152', 'afd7d7'),
    ('153', 'afd7ff'),
    ('154', 'afff00'),
    ('155', 'afff5f'),
    ('156', 'afff87'),
    ('157', 'afffaf'),
    ('158', 'afffd7'),
    ('159', 'afffff'),
    ('160', 'd70000'),
    ('161', 'd7005f'),
    ('162', 'd70087'),
    ('163', 'd700af'),
    ('164', 'd700d7'),
    ('165', 'd700ff'),
    ('166', 'd75f00'),
    ('167', 'd75f5f'),
    ('168', 'd75f87'),
    ('169', 'd75faf'),
    ('170', 'd75fd7'),
    ('171', 'd75fff'),
    ('172', 'd78700'),
    ('173', 'd7875f'),
    ('174', 'd78787'),
    ('175', 'd787af'),
    ('176', 'd787d7'),
    ('177', 'd787ff'),
    ('178', 'd7af00'),
    ('179', 'd7af5f'),
    ('180', 'd7af87'),
    ('181', 'd7afaf'),
    ('182', 'd7afd7'),
    ('183', 'd7afff'),
    ('184', 'd7d700'),
    ('185', 'd7d75f'),
    ('186', 'd7d787'),
    ('187', 'd7d7af'),
    ('188', 'd7d7d7'),
    ('189', 'd7d7ff'),
    ('190', 'd7ff00'),
    ('191', 'd7ff5f'),
    ('192', 'd7ff87'),
    ('193', 'd7ffaf'),
    ('194', 'd7ffd7'),
    ('195', 'd7ffff'),
    ('196', 'ff0000'),
    ('197', 'ff005f'),
    ('198', 'ff0087'),
    ('199', 'ff00af'),
    ('200', 'ff00d7'),
    ('201', 'ff00ff'),
    ('202', 'ff5f00'),
    ('203', 'ff5f5f'),
    ('204', 'ff5f87'),
    ('205', 'ff5faf'),
    ('206', 'ff5fd7'),
    ('207', 'ff5fff'),
    ('208', 'ff8700'),
    ('209', 'ff875f'),
    ('210', 'ff8787'),
    ('211', 'ff87af'),
    ('212', 'ff87d7'),
    ('213', 'ff87ff'),
    ('214', 'ffaf00'),
    ('215', 'ffaf5f'),
    ('216', 'ffaf87'),
    ('217', 'ffafaf'),
    ('218', 'ffafd7'),
    ('219', 'ffafff'),
    ('220', 'ffd700'),
    ('221', 'ffd75f'),
    ('222', 'ffd787'),
    ('223', 'ffd7af'),
    ('224', 'ffd7d7'),
    ('225', 'ffd7ff'),
    ('226', 'ffff00'),
    ('227', 'ffff5f'),
    ('228', 'ffff87'),
    ('229', 'ffffaf'),
    ('230', 'ffffd7'),
    ('231', 'ffffff'),

    # Gray-scale range.
    ('232', '080808'),
    ('233', '121212'),
    ('234', '1c1c1c'),
    ('235', '262626'),
    ('236', '303030'),
    ('237', '3a3a3a'),
    ('238', '444444'),
    ('239', '4e4e4e'),
    ('240', '585858'),
    ('241', '626262'),
    ('242', '6c6c6c'),
    ('243', '767676'),
    ('244', '808080'),
    ('245', '8a8a8a'),
    ('246', '949494'),
    ('247', '9e9e9e'),
    ('248', 'a8a8a8'),
    ('249', 'b2b2b2'),
    ('250', 'bcbcbc'),
    ('251', 'c6c6c6'),
    ('252', 'd0d0d0'),
    ('253', 'dadada'),
    ('254', 'e4e4e4'),
    ('255', 'eeeeee'),
]

def _str2hex(hexstr):
    return int(hexstr, 16)

def _strip_hash(rgb):
    # Strip leading `#` if exists.
    if rgb.startswith('#'):
        rgb = rgb.lstrip('#')
    return rgb

def _create_dicts():
    short2rgb_dict = dict(CLUT)
    rgb2short_dict = {}
    for k, v in short2rgb_dict.items():
        rgb2short_dict[v] = k
    return rgb2short_dict, short2rgb_dict

def short2rgb(short):
    return SHORT2RGB_DICT[short]

def rgb2short(rgb):
    """ Find the closest xterm-256 approximation to the given RGB value.
    @param rgb: Hex code representing an RGB value, eg, 'abcdef'
    @returns: String between 0 and 255, compatible with xterm.
    >>> rgb2short('123456')
    ('23', '005f5f')
    >>> rgb2short('ffffff')
    ('231', 'ffffff')
    >>> rgb2short('0DADD6') # vimeo logo
    ('38', '00afd7')
    """
    rgb = _strip_hash(rgb)
    incs = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
    # Break 6-char RGB code into 3 integer vals.
    parts = [ int(h, 16) for h in re.split(r'(..)(..)(..)', rgb)[1:4] ]
    res = []
    for part in parts:
        i = 0
        while i < len(incs)-1:
            s, b = incs[i], incs[i+1]  # smaller, bigger
            if s <= part <= b:
                s1 = abs(s - part)
                b1 = abs(b - part)
                if s1 < b1: closest = s
                else: closest = b
                res.append(closest)
                break
            i += 1
    #print '***', res
    res = ''.join([ ('%02.x' % i) for i in res ])
    equiv = RGB2SHORT_DICT[ res ]
    #print '***', res, equiv
    return equiv, res

RGB2SHORT_DICT, SHORT2RGB_DICT = _create_dicts()




# -------------------------------------------------------------------------------
# Based on Christian Diener (cdiener) asciinator
# https://gist.github.com/cdiener/10567484


# This is a list of characters from low to high "blackness" in order to map the
# intensities of the image to ascii characters 
orig_chars = ' .,:;irsXA253hMHGS#9B&@'
# Reverse the original list to correspond to our needs
chars = np.asarray(list(reversed(orig_chars)))


# Get some important constants like the filename f, the image size scaling SC and a
# intensity correction factor from the command line arguments. The WCF is a width correction
# factor we will use since most font characters are higher than wide.
parser = argparse.ArgumentParser(description='Transforms an image into an ASCII style colored text on your terminal.', epilog='Only the input image is mandatory for the script to work.')

group_input = parser.add_argument_group('Basic arguments')
group_input.add_argument("-i", "--input", nargs='?', required=True, help="Path to the image in jpg/png format.")
group_input.add_argument("-o", "--output", nargs='?', required=False, default=None, help="Path to the output text file.")
group_input.add_argument("-m", "--mode", nargs='?', required=False, default="256", choices=["256","RGB"], help="Color palette used for the output : RGB or 256 colors. If your terminal supports TrueColour, go for RGB.")
group_input.add_argument("-a", "--ascii", nargs='?', required=False, default=1.0, type=float, metavar="FLOAT", help="ASCII level correction factor. Changes the assignment of a pixel to a higher or lower level character.")
group_input.add_argument("-c", "--color", nargs='?', required=False, default=1.0, type=float, metavar="FLOAT", help="Color saturation correction factor. Changes the intensity of colors on the output.")

group_args = parser.add_argument_group('Output scale arguments')
group_args.add_argument("--auto", nargs='?', required=False, default="h", choices=["h","w"], help="Automatically scale the output based on height (h) or width (w) of your terminal. Default : h")
group_args.add_argument("-s","--scale", nargs='?', required=False, default=1.0, type=float, metavar="FLOAT", help="Rescale the output by this correction factor.")
group_args.add_argument("-p", "--pixel", nargs='?', required=False, default=1.9, type=float, metavar="FLOAT", help="Correction factor to account for the difference in height/width of a character compared to a pixel. Default : 1.9")

args = parser.parse_args()

f    = args.input
o    = args.output 
SC   = args.scale
GCF  = args.ascii
WCF  = args.pixel
SF   = args.color
mode = args.mode

# This line opens the image 
img = Image.open(f)

# Get the size of the terminal for autoscaling
termsize = shutil.get_terminal_size()

# here we set the new size of the image. The whole image is scaled by the scale factor given
# in the command line arguments and we also correct the image with the width correction factor
# so that the resulting asciii image has approximately the same aspect ratio as the original
# image.
if args.auto == "h":
    auto_factor = termsize[1] / img.size[1]
else:
    auto_factor = termsize[0] / (img.size[0] * WCF)

S = ( round(img.size[0]*SC*WCF*auto_factor), round(img.size[1]*SC*auto_factor) )

# Here we resize the image and add up the rgb values of the image to get the overall intensity
# values for each pixel.
img = np.sum( np.asarray( img.resize(S) ), axis=2)  

# Here we scale the smallest intensity value to zero
img -= img.min()
# We divide the intensity values by it maximum so all intensities are now between 0 and 1. We invert
# the intensity scale by subtracting it from one, so that the whitest pixels map to the space character
# and the darkest pixels to the @ character. The now scaled intensities are now raised to the power of the
# intensity correction factor GCF which alters the intensity histogram of the image and, thus, gives some
# some freedom to counteract very dark or light images. A CGF of 1 gives the original pixel intensities. 
# Finally the scaled intensities are multiplied with the biggest index of the character array chars (n-1)
# and, later, truncated to int which basically maps every intensity value of the original image to an index 
# of the ascii character array. 
img = (1.0 - img/img.max())**GCF*(chars.size-1)
 
# Here we assemble and print our ascii art. The image is truncated to int and the entire image matrix is passed
# as an index to the character array. This is possible because numpy actually allows indices to be vectors or matrices
# where the output will have the same dimensions of the matrix "filtered" by the indexed vector. For example, if
#
#
#     v = array(['a', 'b', 'c', 'd']) and M = array( [[0, 1],     it follows that v[M] = [['a', 'b'],  
#                                                     [2, 3]] )                           ['c', 'd']]
#
# In the inner generator we combine the characters of each row (r) of the now ascii-mapped image to a single string
# and in the outer join we combine all of the row characters by gluing them with together with newline characters.
# All of that is printed and done :) 

# Convert to RGB and resize
rgb_im = Image.open(f).convert('RGB').resize(S)
# Apply color correction
improved = ImageEnhance.Color(rgb_im).enhance(SF)
# Convert to array
rgb_arr = np.array(improved)
# Print
if o is not None:
    o = open("output.txt", "w")

for line,l in zip(rgb_arr, img.astype(int)):
    if o is not None:
        o.write('$display("')
    s = list(chars[l])
    for pixel,p in zip(line,s):
        r, g, b = pixel
        if mode == "RGB":
            pix = "\x1b[38;2;{};{};{}m{}\x1b[0m".format(r,g,b,p)
        else:
            # convert RGB to Hex code
            colorHEX = "{0:02x}{1:02x}{2:02x}".format(r, g, b)
            # convert Hex code to xterm-256 color code
            c, rgb = rgb2short(colorHEX)
            pix = "\x1b[38;5;{}m{}\x1b[0m".format(c,p)
        print(pix, end="")
        if o is not None:
            o.write(pix)
    print()
    if o is not None:
        o.write('");\n')

if o is not None:
    o.close()
