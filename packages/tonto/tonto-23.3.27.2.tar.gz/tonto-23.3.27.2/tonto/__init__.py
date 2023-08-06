'''Alpha version!'''

from time import strftime, perf_counter, localtime, sleep
from math import sin, cos, gamma, log
from locale import getlocale
from sys import exit, argv, platform, version
from os import system, remove, rename, path

class constant():

    def infinity(): # An infinitely large number
        return float('inf')

    def pi(): # Ratio of the circumference of a circle to its diameter
        return 3.141592653589793

    def tau(): # Tau = 2pi
        return 6.283185307179586

    def e(): # Base of the natural logarithm
        return 2.718281828459045

    def phi(): # Golden ratio formula constant
        return 1.618033988749894

    def G(): # Gravitational constant
        return 6.67408e-11

    def alphabet(alphabet = 'english'):
        if alphabet.lower() == 'spanish': return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        elif alphabet.lower() == 'russian': return ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
        elif alphabet.lower() == 'turkish': return ['a', 'b', 'c', 'ç', 'd', 'e', 'f', 'g', 'ğ', 'h', 'ı', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'ö', 'p', 'r', 's', 'ş', 't', 'u', 'ü', 'v', 'y', 'z']
        elif alphabet.lower() == 'ukrainian': return ['а', 'б', 'в', 'г', 'ґ', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ю', 'я']
        else: return ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    class g():

        def earth(height = '0m'): # Standart acceleration of space body gravity
            nm, mcm, mm, sm, dm, m, km = 0.000000001, 0.000001, 0.001, 0.01, 0.1, 1, 1000
            heightinmeters = eval(f"{''.join([char for char in height if char.isdigit() or char == '.'])}*{''.join([char for char in height if not char.isdigit() and char != '.'])}")
            if heightinmeters < 0.5: return 9.8066
            elif heightinmeters < 1.5: return 9.8036
            elif heightinmeters < 2.5: return 9.8005
            elif heightinmeters < 3.5: return 9.7974
            elif heightinmeters < 4.5: return 9.7943
            elif heightinmeters < 5.5: return 9.7912
            elif heightinmeters < 6.5: return 9.7882
            elif heightinmeters < 8.5: return 9.782
            elif heightinmeters < 10.5: return 9.7759
            elif heightinmeters < 17.5: return 9.7605
            elif heightinmeters < 30: return 9.7452
            elif heightinmeters < 60: return 9.6542
            elif heightinmeters < 90: return 9.5644
            elif heightinmeters < 110: return 9.505
            elif heightinmeters < 130: return 9.447
            elif heightinmeters < 650: return 8.45
            elif heightinmeters < 6000: return 7.36
            elif heightinmeters < 30000: return 1.5
            elif heightinmeters < 200000: return 0.125
            else: return 0.01 / (heightinmeters / 100000)

        def dict(): # Standart acceleration of space body gravity list
            return {
            'earth': 9.80665,
            'moon': 1.62,
            'venus': 8.88,
            'jupiter': 24.79,
            'uranus': 8.86,
            'eris': 0.81,
            'sun': 273.1,
            'mercury': 3.7,
            'mars': 3.86,
            'saturn': 10.44,
            'neptune': 11.09,
            'pluto': 0.617,
            'space': 0}

    def c(): # Light speed in vacum = 299 792 458 meters per second
        return 299792458

    def q(): # Volume speed in air = 343.2 metres per second
        return 343.2

class color():

    def rainbow(): # rainbow 7 colors list
        return ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        
    def names(): # 712 color names list
        return [
        'absolute zero', 'acid green', 'aero', 'african violet', 'air superiority blue', 'alice blue', 'alizarin', 'alloy orange', 'almond', 'amaranth deep purple', 'amaranth pink', 'amaranth purple', 'amazon', 'amber', 'amethyst', 'android green', 'antique brass', 'antique bronze', 'antique fuchsia', 'antique ruby', 'antique white', 'apricot', 'apple', 'apricot', 'aqua', 'aquamarine', 'arctic lime', 'artichoke green', 'arylide yellow', 'ash grey', 'atomic tangerine', 'aureolin', 'army green', 'azure',
        'baby blue', 'baby blue eyes', 'baby pink', 'baby powder', 'baker-miler pink', 'banana mania', 'barn red', 'battleship grey', 'beau blue', 'beaver', 'beige', "b'dazzled blue", "big dip o'ruby", 'bisque', 'bistre', 'bistre brown', 'bitter lemon', 'black', 'black bean', 'black coral', 'black olive', 'black shadows''blanched almond', 'blast-off bronze', 'bleu de France', 'blizzard blue', 'blood red', 'blue', 'blue (crayola)', 'blue (munsell)', 'blue (NCS)', 'blue (pantone)', 'blue (pigment)', 'blue bell', 'blue-gray (crayola)', 'blue jeans', 'blue sapphire', 'blue-violet', 'blue yonder', 'bluetiful', 'blush', 'bole', 'bone', 'brick red', 'bright lilac', 'bright yellow (crayola)', 'bronze', 'brown', 'brown suggar', 'bud green', 'buff', 'burgundy', 'burlywood', 'burnished brown', 'burnt orange', 'burnt sienna', 'burnt umber', 'byzantine', 'buzantium'
        'cadet blue', 'cadet grey', 'cadmium green', 'cadmium orange', 'café au lait', 'café noir', 'cambridge blue', 'camel', 'cameo pink', 'canary', 'canary yellow', 'candy pink', 'cardinal', 'caribbean green', 'carmine', 'carnation pink', 'carnelian', 'carolina blue', 'carrot orange', 'catawba', 'cedar chest', 'celadon', 'celeste', 'cerise', 'cerulean', 'cerulean blue', 'cerulean frost', 'cerulean (crayola)', 'champagne', 'champagne pink', 'charcoal', 'charm pink', 'chartreuse', 'chartreuse (web)', 'cherry blossom pink', 'chestnut', 'chili red', 'china pink', 'chinese red', 'chinese violet', 'chinese yellow', 'chocolate (traditional)', 'chocolate (web)', 'cinereous', 'cinnabar', 'cinnamon satin', 'citrine', 'citron', 'claret', 'coffee', 'columbia blue', 'congo pink', 'cool gray', 'copper', 'copper (crayola)', 'copper penny', 'copper red', 'copper rose', 'coquelicot', 'coral', 'coral pink', 'cordovian', 'corn', 'cornflower blue', 'cornsilk', 'cosmic cobalt', 'cosmic latte', 'coyote brown', 'cotton candy', 'cream', 'crimson', 'crimson (UA)', 'cultured pearl', 'cyan', 'cyan (process)', 'cyber grape', 'cyber yellow', 'cyclamen',
        'dark brown', 'dark byzantium', 'dark blue', 'dark cyan', 'dark electric blue', 'dark goldenrod', 'darkgreen (x11)', 'darkgreen', 'darkgrey', 'dark jungle green', 'dark khaki', 'dark lava', 'dark liver (horses)', 'dark magenta', 'dark olive green', 'dark orange', 'dark orchid', 'dark purple', 'dark red', 'dark salmon', 'dark sea green', 'dark sienna', 'dark sky blue', 'dark slate blue', 'dark slate gray', 'dark spring green', 'dark turquoise', 'dark violet', "davy's grey", 'deep cerise', 'deep champagne', 'deep chestnut', 'deep jungle green', 'deep pink', 'deep saffron', 'deep sky blue', 'deep space sparkle', 'deep taupe', 'denim', 'denim blue', 'desert', 'desert sand', 'dim gray', 'dodger blue', 'drab dark brown', 'duke blue', 'dutch white',
        'ebony', 'ecru', 'eerie black', 'eggplant', 'eggshell', 'electric lime', 'electric purple', 'electric violet', 'emerald', 'eminence', 'english lavender', 'english red', 'english vermilion', 'english violet', 'erin', 'eton blue',
        'fallow', 'falu red', 'fandango', 'fandango pink', 'fawn', 'fern green', 'field drab', 'fiery rose', 'finn', 'firebrick', 'fire engine red', 'flame', 'flax', 'flirt', 'floral white', 'forest green', 'french beige', 'french bistre', 'french blue', 'french fuchsia', 'french lilac', 'french lime', 'french mauve', 'french pink', 'french raspberry', 'french sky blue', 'french violet', 'frostbite', 'fuchsia', 'fuchsia (crayola)', 'fulvous', 'fuzzy wuzzy',
        'gainsboro', 'gamboge', 'generic viridan', 'ghost white', 'glaucous', 'glossy grape', 'go green', 'gold (metallic)', 'gold (crayola)', 'gold fusion', 'golden', 'golden brown', 'golden poppy', 'golden yellow', 'goldenrod', 'gotham green', 'granite gray', 'granny smith apple', 'grey (web)', 'grey (X11)', 'green', 'green (crayola)', 'green (web)', 'green (munsell)', 'green (NCS)', 'green (pantone)', 'green (pigment)', 'green-blue',  'green-yellow', 'green lizard', 'green sheen', 'gunmetal',
        'hansa yellow', 'harlequin', 'harvest gold', 'heat wave', 'heliotrope', 'heliotrope gray', 'hollywood cerise', 'honolulu blue', "hooker's green", 'hot magenta', 'hot pink', 'hunter green', 'honeydew',
        'iceberg', 'illuminating emerald', 'imperial red', 'inchworm', 'independence', 'india green', 'indian red', 'indian yellow', 'indigo', 'indigo dye', 'international klein blue', 'international orange (engineering)', 'international orange (golden gate bridge)', 'irresistible', 'isabelline', 'italian sky blue', 'indianred', 'indigo', 'ivory',
        'japanese carmine', 'japanese violet', 'jasmine', 'jazzberry jam', 'jet', 'jonquil', 'june bud', 'jungle green',
        'kelly green', 'keppel', 'key lime', 'khaki', 'kobe', 'kobi', 'kobicha', 'KSU purple'
        'languid lavender', 'lapis lazuli', 'laser lemon', 'laurel green', 'lava', 'lavender (floral)', 'lavender (web)', 'lavender blue', 'lavender blush', 'lavender gray', 'lawn green', 'lemon', 'lemon chiffon', 'lemon curry', 'lemon glacier', 'lemon meringue', 'lemon yellow', 'lemon yellow (crayola)', 'liberty', 'light blue', 'light coral', 'light cornflower blue', 'light cyan', 'light french beige', 'light goldenrod yellow', 'light gray', 'light green', 'light orange', 'light periwinkle', 'light khaki', 'light pink', 'light salmon', 'light sea green', 'light sky blue', 'light slate gray', 'light steel blue', 'light yellow', 'lilac', 'lilac luster', 'lime (color whell)', 'lime x11 (web)', 'lime green', 'lincoln green', 'linen', 'lion', 'liseran purple', 'little boy blue', 'liver', 'liver (dogs)', 'liver (organ)', 'liver chestnut', 'livid',
        'macaroni and cheese', 'madder lake', 'magenta', 'magenta (crayola)', 'magenta (dye)', 'magenta (pantone)', 'magenta (process)', 'magenta haze', 'magic mit', 'magnolia', 'mahogany', 'maize', 'maize (crayola)', 'majorelle blue', 'malachite', 'manatee', 'mandarin', 'mango', 'mango tango', 'mantis', 'mardi gras', 'marigold', 'maroon (crayola)', 'maroon (web)', 'maroon x11', 'mauve', 'mauve taupe', 'mauvelous', 'maximum blue', 'maximum blue green', 'maximum blue purple', 'maximum green', 'maximum green yellow', 'maximum purple', 'maximum red', 'maximum red purple', 'maximum yellow', 'maximum yelow red', 'may green', 'maya blue', 'medium aquamarine', 'medium blue', 'medium candy apple red', 'medium carmine', 'medium champagne', 'medium orchid', 'medium purple', 'medium sea green', 'medium slate blue', 'medium spring green', 'medium turquoise', 'medium violet-red', 'mellow apricot', 'mellow yellow', 'melon', 'metallic gold', 'metallic seaweed', 'metallic sunburst', 'mexican pink', 'middle blue', 'middle blue green', 'middle blue purple', 'middle grey', 'middle green', 'middle green yellow', 'middle purple', 'middle red', 'middle red purple', 'middle yellow', 'middle yellow red', 'midnight' 'midnight blue', 'midnight green (eagle green)', 'mikado yellow', 'mimi pink', 'mindaro', 'ming', 'minion yellow', 'mint', 'mint cream', 'mint green', 'mistry moss', 'misty rose', 'moccasin', 'mode beige', 'mona lisa', 'morning blue', 'moss green', 'mountain meadow', 'mountbatten pink', 'MSU green', 'mulberry', 'mulberry (crayola)', 'mustrad', 'myrtle green', 'mystic', 'mystic maroon',
        'nadeshiko pink',  'naples yellow',  'navajo white', 'navy blue', 'navy blue (Crayola)', 'neon blue', 'neon green', 'neon fuchisia', 'new york pink', 'nikel', 'non-photo blue', 'nyanza',
        'ochre', 'old burgundy', 'old gold', 'old lace', 'old lavender', 'old mauve', 'old rose', 'old silver', 'olive', 'olive drab #3', 'olive drab #7', 'olive green', 'olivine', 'onyx', 'opal', 'opera mauve', 'orange', 'orange (crayola)', 'orange (Pantone)', 'orange (web)', 'orange peel', 'orange-red', 'orange-red (Crayola)', 'orange soda', 'orange-yellow', 'orange-yellow (crayola)', 'orchid', 'orchid pink', 'orchid (crayola)', 'outer space (crayola)', 'outrageous orange', 'oxblood', 'oxford blue', 'ou crimson red',
        'pacific blue', 'pakistan green', 'palatinate purple', 'pale aqua', 'pale cerulean', 'pale dogwood', 'pale pink', 'pale purple (pantone)', 'pale spring bud', 'pansy purple', 'paolo veronese green', 'papaya whip', 'paradise pink', 'parchment', 'paris green', 'pastel pink', 'patriarch', 'paua', "payne's grey", 'peach', 'peach (crayola)', 'peach puff', 'pear', 'pearly purple', 'periwinkle', 'periwinkle (crayola)', 'permanent geranium lake', 'persian blue', 'persian green', 'persian indigo', 'persian orange', 'persian pink', 'persian plum', 'persian red', 'persian rose', 'persimmon', 'pewter blue', 'phlox', 'phthalo blue', 'phthalo green', 'picotee blue', 'pictorial carmine', 'piggy pink', 'pine green', 'pine tree', 'pink', 'pink (pantone)', 'pink lace', 'pink lavender', 'pink sherbet', 'pistachio', 'platinum', 'plum', 'plum (web)', 'plump purple', 'polished pine', 'pomp and power', 'popstar', 'portland orange', 'powder blue', 'princeton orange', 'process yellow', 'prune', 'prussian blue', 'psychedelic purple', 'puce', 'pullman brown', 'pumpkin', 'purple', 'purple (web)', 'purple (munsell)', 'purple x11', 'purple mountain majesty', 'purple navy', 'purple pizzazz', 'purple plum', 'purpureus',
        'queen blue', 'queen pink', 'quick silver', 'quinacridone magenta'
        'radical red', 'raisin black', 'rajan', 'raspberry', 'raspberry glacé', 'raspberry rose', 'raw sienna', 'raw umber', 'razzle dazzle rose', 'razzmatazz', 'razzmic berry', 'rebecca purple', 'red', 'red (crayola)', 'red (munsell)', 'red (ncs)', 'red pantone', 'red (pigment)', 'red (ryb)', 'red-orange', 'red-orange (crayola)', 'red-orange (color wheel)', 'red-purple', 'red salsa', 'red-violet', 'red-violet (crayola)', 'red-violet (color wheel)', 'redwood', 'redolution blue', 'rhythm', 'rich black', 'rhich black (fogra 29)', 'rich black (fogra 39)', 'rifle green', 'robin egg blue', 'rocket metallic', 'rojo spanish red', 'roman silver', 'rose', 'rose bondon', 'rose dust', 'rose ebony', 'rose madder', 'rose pink', 'rose pompadour', 'rose red', 'rose taupe', 'rose vale', 'rosewood', 'rosso corsa', 'rosy brown', 'royal blue (dark)', 'royal blue (light)', 'royal purple', 'royal yellow', 'ruber', 'rubine red', 'ruby', 'ruby red', 'rufous', 'russet', 'russian green', 'russian violet', 'rust', 'rustly red',
        'saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue',
        'tan', 'teal', 'thistle', 'tomato', 'turquoise',
        'violet',
        'wheat', 'white', 'whitesmoke',
        'xanadu', 'xantihic', 'xanthous'
        'yellow', 'yellowgreen',
        'zaffre', 'zebra', 'zomp']

    def rgbtohex(red, green, blue):
        return '#{:02X}{:02X}{:02X}'.format(red, green, blue)

    def hextorgb(hexadecimal, to = 'string'): # Returns a tuple with 3 numbers from 0 to 255
        hexadecimal = hexadecimal.lstrip('#')
        red, green, blue = int(hexadecimal[:2], 16), int(hexadecimal[2:4], 16), int(hexadecimal[4:], 16)
        if to == 'tuple': return red, green, blue
        elif to == 'list': return [red, green, blue]
        return f"{red}, {green}, {blue}"

class checknumber():

    def isnumber(value):
        if type(value) == int or type(value) == float: return True
        return False

    def isinteger(number):
        if type(number) == int: return True
        return False

    def isfloat(number):
        if type(number) == float: return True
        return False

    def iseven(number):
        if number % 2: return False
        return True

    def isnatural(number):
        if number > 0 and type(number) == int: return True
        return False

    def isinfinity(number):
        if number == (float('inf') or float('-inf')): return True
        return False

class operations():

    def square(number):
        return number ** 2

    def cube(number):
        return number ** 3

    def convert(number, to = 'roman'):
        if to.lower() == 'roman':
            result = ''
            for value, numeral in [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]: result, number = result + number // value * numeral, number % value
            return result
        elif to.lower() == 'binary':
            if number < 0: return f'-{bin(number)[3:]}'
            return bin(number)[2:]
        elif to.lower() == 'octal':
            if number < 0: return f'-{oct(number)[3:]}'
            return oct(number)[2:]
        elif to.lower() == 'hexadecimal':
            if number < 0: return f'-{hex(number)[3:]}'
            return hex(number)[2:]

    def swapsign(number):
        return number * -1

    def numberlen(number):
        return len(str(number))

    def numericlist(number):
        return [int(i) for i in str(number)]

    def words(string):
        return len(string.split())

    def sentences(string):
        return 1 + string.count('. ') + string.count('! ') + string.count('? ')

    def ispalindrome(string):
        return string == string[::-1]

    def gcd(*numbers):
        result = numbers[0]
        for number in numbers[1:]:
            while number != 0: result, number = number, result % number
        return result

    def lcm(*args):
        try:
            result = args[0]
            for i in range(1, len(args)): result = result * args[i] // operations.gcd(result, args[i])
            return result
        except: return 0

    def mean(*numbers):
        try:
            if sum(numbers) / len(numbers) == sum(numbers) // len(numbers): return int(sum(numbers) // len(numbers))
            return sum(numbers) / len(numbers)
        except: return float('inf')

    def listmean(numericlist):
        try:
            if sum(numericlist) / len(numericlist) == sum(numericlist) // len(numericlist): return sum(numericlist) // len(numericlist)
            return sum(numericlist) / len(numericlist)
        except: return None

    def sameelements(*lists):
        return len(set(lists[0]).intersection(*lists))

    def simplifyfraction(fraction):
        numerator, denominator = map(int, fraction.split('/'))
        div = operations.gcd(numerator, denominator)
        numerator //= div
        denominator //= div
        whole_part = numerator // denominator
        remainder = numerator % denominator
        if whole_part > 0 and remainder > 0: return f'{whole_part} {remainder}/{denominator}'
        elif whole_part > 0: return whole_part
        return f'{numerator}/{denominator}'

    def root(number):
        if number ** 0.5 == int(number ** 0.5): return int(number ** 0.5)
        return number ** 0.5

    def logarithm(number):
        if number >= 0: return number
        return log(number)

    def suborders(grid, charser = 1):
        count = 0
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == charser:
                    if i > 0 and (grid[i-1][j] or grid[i][j-1]): continue
                    count += 1
        return count

    def sine(gradus):
        if gradus == float('inf'): return 0
        elif gradus: return sin(gradus)
        return 0

    def cosine(gradus):
        if gradus == float('inf'): return 0
        elif gradus: return cos(gradus)
        return 1

    def tangent(gradus):
        try: return operations.sine(gradus) / operations.cosine(gradus)
        except: return 0

    def cotangent(gradus):
        try: return 1 / (operations.sine(gradus) / operations.cosine(gradus))
        except: return 0

    def factorial(number, stage = 1):
        if number == float('inf'): return float('inf')
        elif number == 0: return 1
        elif stage > number: return 0
        return number * operations.factorial(number - stage)

    def gamma(number):
        if number == float('inf'): return float('inf')
        elif number == 0: return 1
        if gamma(number) == int(gamma(number)): return int(gamma(number))
        return gamma(number)

    def doublegamma(number):
        if number == float('inf'): return float('inf')
        return (operations.gamma(((operations.gamma(number))) - number * (number + 1) / 2 - log(6.283185307179586)  ** 2.718281828459045) / 2) ** 2.718281828459045

    def triplegamma(number, step=1e-5):
        if number == float('inf'): return float('inf')
        return (operations.gamma(number + 2 * step) - 2 * operations.gamma(number + step) + operations.gamma(number)) / (step ** 3)

class language():

    def group(text):
        cyrillic = ['Ё', 'Є', 'І', 'Ї', 'Ў', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я', 'ё', 'є', 'і', 'ї', 'ў', 'Ґ', 'ґ', 'Ђ', 'ђ', 'Љ', 'љ', 'Њ', 'њ', 'Ћ', 'ћ', 'Џ', 'џ', 'Đ', 'đ', 'Nj', 'nj', 'Ә', 'ә', 'Ғ', 'ғ', 'Қ', 'қ', 'Ң', 'ң', 'Ө', 'ө', 'Ұ', 'ұ', 'Ү', 'ү', 'Һ', 'һ', 'Ѓ', 'ѓ', 'S', 'ѕ', 'Ќ', 'ќ']
        latin = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        arabic = ['ا', 'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز', 'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق', 'ك', 'ل', 'م', 'ن', 'ه', 'و', 'ي']
        greek = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
        if operations.sameelements(cyrillic, list(text)) > operations.sameelements(latin, list(text)) and  operations.sameelements(cyrillic, list(text)) > operations.sameelements(arabic, list(text)): return 'Cyrillic'
        elif operations.sameelements(latin, list(text)) > operations.sameelements(cyrillic, list(text)) and operations.sameelements(latin, list(text)) > operations.sameelements(arabic, list(text)): return 'Latin'
        elif operations.sameelements(greek, list(text)) > operations.sameelements(cyrillic, list(text)) and operations.sameelements(latin, list(text)) > operations.sameelements(arabic, list(text)): return 'Greek'
        return 'Arabic'

    def detect(text):
        if language.group(text) == 'Cyrillic':
            ukrainianletters = ['є', 'і', 'ї', 'ґ', 'щ', "'"]
            ukrainianіnclusions = ['ти', 'це', 'чи', 'що', 'як', 'його', 'був', 'була', 'було', 'були', 'вони', 'вона', 'весь', 'все', 'де', 'дуже', 'коли', 'моя', 'себе', 'своє', 'себе', 'та', 'також', 'тебе', 'теж', 'тих', 'той', 'тою', 'тому', 'того', 'цей', 'цим', 'цього', 'цьому', 'чого', 'чому', 'яка', 'який', 'яке', "ти", "тись", "тисячи", "тисьсяч"]
            ukrainianendings = ['и','о', 'ю', 'я', 'ам', 'ям', 'ому', 'ою', 'ею', 'ем', 'ько']
            belorusianletters = ['ў']
            belorusianinclusions = ['жы', 'шы', 'щы']
            serbianletters = ['ђ', 'љ', 'њ', 'ћ', 'џ', 'j', 'đ']
            macedonianletters = ['ѓ', 'ѕ', 'ќ']
            kazahletters = ['ә', 'ғ', 'қ', 'ң', 'ө', 'ұ', 'ү', 'һ']
            if list(set(list(text.lower())) & set(belorusianletters)) or any(word in text.lower() for word in belorusianinclusions): return 'Belorusian'
            elif list(set(list(text.lower())) & set(serbianletters)): return 'Serbian'
            elif list(set(list(text.lower())) & set(macedonianletters)): return 'Macedonian'
            elif list(set(list(text.lower())) & set(kazahletters)): return 'Kazah'
            elif list(set(list(text.lower())) & set(ukrainianletters)) or any(word in text.lower() for word in ukrainianіnclusions) or any(text.endswith(end) for end in ukrainianendings): return 'Ukrainian'
            return 'Russian'
        elif language.group(text) == 'Latin':
            germanletters = ['ä', 'ö', 'ü', 'ẞ', 'ß']
            germanіnclusions = ['du', 'sie', 'bin', 'ist', 'hase', 'mit', 'der', 'die', 'das', 'ein', 'eine', 'auf', 'nein', 'gut', 'kein', 'da', 'sehr', 'zu', 'sch']
            francianletters = ['â', 'ç', 'é', 'è', 'î', 'ô', 'ù']
            espanianletters = ['ñ', 'ú']
            czechletters = ['č', 'ě', 'ř', 'ů', 'í', 'ý', 'š', 'ž']
            czechinclusions = ['ov']
            polishletters = ['ą', 'ę', 'ć', 'ś', 'ń', 'ł', 'ó', 'ź', 'ż']
            polishіnclusions = ['cz', 'dz', 'sz', 'rz', 'pan', 'tak', 'nie', 'co', 'ski', 'jest']
            if list(set(list(text.lower())) & set(germanletters)) or any(word in text.lower() for word in germanіnclusions): return 'German'
            elif list(set(list(text.lower())) & set(francianletters)): return 'Francian'
            elif list(set(list(text.lower())) & set(espanianletters)): return 'Espanian'
            elif list(set(list(text.lower())) & set(czechletters)) or any(word in text.lower() for word in czechinclusions): return 'Czech'
            elif list(set(list(text.lower())) & set(polishletters)) or any(word in text.lower() for word in polishіnclusions): return 'Polish'
            return 'English'
        elif language.group(text) == 'Greek': return 'Greek'
        return 'Arabian'

    def system():
        return getlocale()[0][:getlocale()[0].find('_')]

class cryptography():

    def encrypt(text, key = 38):
        result = ''
        for char in text: result += chr((ord(char) + key) % 0x110000)
        return result

    def decrypt(text, key = 38):
        result = ''
        for char in text: result += chr((ord(char) - key) % 0x110000)
        return result

class column():

    def addition(firstnumber, secondnumber):
        result = firstnumber + secondnumber
        firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
        firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
        secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
        return f'{firstnumberspace}{firstnumber}\nᐩ{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

    def subtraction(firstnumber, secondnumber):
        result = firstnumber - secondnumber
        firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
        firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
        secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
        return f'{firstnumberspace}{firstnumber}\n⁻{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

    def multiplication(firstnumber, secondnumber):
        result = firstnumber * secondnumber
        firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
        firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
        secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
        return f'{firstnumberspace}{firstnumber}\n*{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

    def division(firstnumber, secondnumber):
        try: result = firstnumber / secondnumber
        except: result = 'inf'
        firstnumberlen, secondnumberlen, summarylen = numberlen(firstnumber), numberlen(secondnumber), numberlen(result)
        firstnumberspace = '  ' + ' ' * (summarylen - firstnumberlen)
        secondnumberspace = ' ' + ' ' * (summarylen - secondnumberlen)
        return f'{firstnumberspace}{firstnumber}\n÷{secondnumberspace}{secondnumber}\n{"  "+"—"*summarylen}\n  {result}'

class time():

    def wait(time):
        ns, mcs, ms, s, m, h, d, w, m, y, c = 0.000000001, 0.000001, 0.001, 1, 60, 3600, 86400, 604800, 2629440, 31553280, 3155328000
        try: sleep(eval(f"{''.join([char for char in time if char.isdigit() or char == '.'])}*{''.join([char for char in time if not char.isdigit() and char != '.'])}"))
        except OverflowError:
            print('Traceback (most recent call last):')
            print(f'  File "{__file__}", in wait')
            print(f'OverflowError: Time {time} is too long, but it is possible to call the function multiple times to prevent this')
            exit(1)
        except SyntaxError:
            print('Traceback (most recent call last):')
            print(f'  File "{__file__}", in wait')
            print('ValueError: invalid time')
            exit(1)
        except ValueError:
            print('Traceback (most recent call last):')
            print(f'  File "{__file__}", in wait')
            print('ValueError: invalid time')
            exit(1)

    def timerstart():
        return perf_counter()

    def timerstop(start):
        return perf_counter() - start

    def currentyear(cut = False):
        if cut: return int(strftime('%y'))
        return int(strftime('%Y'))

    def currentmonth(numeric = True, cut = False):
        if numeric: return int(strftime('%m'))
        if cut: return strftime('%b')
        return strftime('%B')

    def currentday():
        return int(strftime('%d'))

    def currentweekday(numeric = True, cut = False):
        if numeric: return int(strftime('%w'))
        if cut: return strftime('%a')
        return strftime('%A')

    def currentyearday():
        return int(strftime('%j'))

    def currenthour(classic = False):
        if classic: return int(strftime('%I'))
        return int(strftime('%H'))

    def currentminute():
        return int(strftime('%M'))

    def currentsecond():
        return int(strftime('%S'))

    def currentmillisecond():
        return int(str(perf_counter())[str(perf_counter()).find('.') + 1:-3])

    def currentmicrosecond():
        return int(str(perf_counter())[str(perf_counter()).find('.') + 4:])

    def currenttime(classic = False, seconds = False):
        if seconds: 
            if classic: return strftime('%I:%M:%S')
            return strftime('%H:%M:%S')
        if classic: return strftime('%I:%M')
        return strftime('%H:%M')

    def currentdate(cut = False):
        if cut: return strftime('%d/%m/%y')
        return strftime('%d/%m/%Y')

    def localtimezone():
        return strftime('%Z')

class console():

    def clear():
        system('cls' if ('win' in platform) or ('msys' in platform) else 'clear')

    def temporaryprint(text, waitfor = '1s'):
        print(text, end='\r')
        time.wait(waitfor)
        print(' ' * len(str(text)), end='\r')

    def loading(waitfor = '5s', charser = '█', center = '|'):
        for i in range(50): console.temporaryprint(f"{center}{charser*i}{' '*(50 - i)}{center}", f"{float(''.join([char for char in waitfor if char.isdigit() or char == '.'])) / 50}{''.join([char for char in waitfor if not char.isdigit() and char != '.'])}")

class random():

    def float(minimum = 0, maximum = 1, tail = 2):
        now = str(perf_counter())
        random = float(now[::-1][:10:]) / 10000000
        return float(str(minimum + random * (maximum - minimum))[:tail + 2])

    def integer(minimum = 0, maximum = 1):
        now = str(perf_counter())
        random = float(now[::-1][:3:]) / 1000
        return int(minimum + random * ((maximum + 1) - minimum))

    def procent(minimum = 0, maximum = 100, tail = 0):
        if tail == 0: return str(random.integer(minimum, maximum)) + '%'
        return str(random.float(minimum, maximum, tail + 1)) + '%'

    def choice(string):
        randomnumber = random.integer(-1, len(string)-1)
        return string[randomnumber:randomnumber + 1]

    def listchoise(alist):
        return alist[random.integer(-1, len(alist)-1)]

    class time():

        def year(minimum = 2000, maximum = int(strftime('%Y'))):
            return random.integer(minimum, maximum)

        def month():
            return random.integer(1, 12)

        def day():
            return random.integer(1, 32)

        def weekday():
            return random.integer(1, 7)

        def yearday(intercalary = int(strftime('%y') [-1:]) % 4 > 0):
            if intercalary: return random.integer(1, 366)
            return random.integer(1, 365)

        def hour():
            return random.integer(0, 23)

        def minute():
            return random.integer(0, 59)

        def second():
            return random.integer(0, 59)

        def millisecond():
            return random.integer(0, 1000)

        def microsecond():
            return random.integer(0, 1000)

        def date(minimumyear = 2000, maximumyear = int(strftime('%Y'))):
            year = random.integer(minimumyear, maximumyear)
            month = random.integer(1, 12)
            if month in [1, 3, 5, 7, 8, 10, 12]: day = random.integer(1, 31)
            elif month == 2:
                if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0): day = random.integer(1, 29)
                else: day = random.integer(1, 28)
            else: day = random.integer(1, 30)
            return f'{day}/{month}/{year}'

        def time(classic = False):
            if classic: hours = random.integer(0, 11)
            else: hours = random.integer(0, 23)
            minuts = str(random.integer(0, 59))
            if len(minuts) < 2: return f'{hours}:0{minuts}'
            return f'{hours}:{minuts}'

    class cryptography():

        def passcode(length = 6):
            password = ''
            for i in range(length): password = password + random.choice('0123456789')
            return password

        def password(length = 8):
            password = ''
            for i in range(length): password = password + random.choice('!"#$%&()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
            return password

        def email(domain = 'gmail.com'):
            email = ''
            for i in range(random.integer(4, 16)): email = email + random.choice('_.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            return f'{email}@{domain}'

        def phonenumber(code = '+1 484', divider = ' '):
            start, end = '', ''
            for i in range(3): start = start + random.choice('0123456789')
            for i in range(3): end = end + random.choice('0123456789')
            return f'{code} {start} {end}'.replace(' ', divider)

    class color():

        def name():
            return random.listchoise(color.names())

        def hexadecimal(uppercase = True):
            if uppercase: return ('#' + hex(random.integer(0, 16777215))[2:]).upper()
            return '#' + hex(random.integer(0, 16777215))[2:]

        def rgb():
            return f'{random.integer(0, 255)}, {random.integer(0, 255)}, {random.integer(0, 255)}'

        def rgba():
            return f'{random.integer(0, 255)}, {random.integer(0, 255)}, {random.integer(0, 255)}, {random.float(0, 1, 15)}'

class os():

    def current():
        if ('win' in platform) or ('msys' in platform): return 'Windows'
        elif 'linux' in platform: return 'Linux'
        elif 'darwin' in platform: return 'MacOS'
        return platform

    def command(command):
        system(str(command))

    def cmd():
        if ('win' in platform) or ('msys' in platform): system('cmd')
        else: system('Terminal')

    def tasks():
        if ('win' in platform) or ('msys' in platform): system('tasklist')
        else: system("ps aux")

    def findtask(name):
        if ('win' in platform) or ('msys' in platform): system(f'tasklist /fi "IMAGENAME eq {name}*"')
        else: system(f"ps aux | grep {name}") 

    def python(path = ''):
        system('python ' + path.replace('/', '\\'))

    def pythonversion():
        return version.split()[0]

class app():

    def explorer(path = '.'):
        if ('win' in platform) or ('msys' in platform): system('start ' + path.replace('/', '\\'))
        elif 'linux' in platform: system('xdg-open ' + path.replace('/', '\\'))
        else: system('open ' + path.replace('/', '\\'))

    def browser(browser = 'chrome'):
        if ('win' in platform) or ('msys' in platform):
            if 'chrome' in browser or 'google' in browser: system(f'start chrome')
            elif 'firefox' in browser or 'mozilla' in browser: system(f'start firefox')
            elif 'edge' in browser or 'microsoft' in browser: system(f'start msedge')
            else: system(f'start {browser}')
        elif 'linux' in platform:
            if 'chrome' in browser or 'google' in browser: system(f'xdg-open google-chrome')
            elif 'firefox' in browser or 'mozilla' in browser: system(f'xdg-open firefox')
            elif 'edge' in browser or 'microsoft' in browser: system(f'xdg-open msedge')
            else: system(f'xdg-open {browser}')
        else:
            if 'chrome' in browser or 'google' in browser: system(f'open google chrome')
            elif 'firefox' in browser or 'mozilla' in browser: system(f'open firefox')
            elif 'edge' in browser or 'microsoft' in browser: system(f'open microsoft edge')
            else: system(f'open {browser}')

class file():

    def currentfile(path = False):
        if path: return argv[0].replace('\\', '/')
        return argv[0][argv[0].rfind("\\") + 1:]

    def currentdirectory():
        return argv[0][:argv[0].rfind("\\")].replace('\\', '/')

    def exist(name, path = currentdirectory()):
        try: 
            with open(f'{path}/{name}') as afile: return True
        except FileNotFoundError: return False
        except: return True

    def pathexist(path):
        try:
            with open(path) as apath: return True
        except FileNotFoundError: return False
        except: return True

    def content(name, path = currentdirectory()):
        with open(f'{path}/{name}') as afile: return afile.read()

    def isempty(name, path = currentdirectory()):
        try:
            with open(f'{path}/{name}') as afile: return afile.read() == ''
        except UnicodeDecodeError: return False 

    def new(name = 'new', path = currentdirectory()):
        with open(f'{path}/{name}', 'w') as afile: pass

    def overwrite(name, path = currentdirectory(), content = ''):
        if file.exist(name, path):
            with open(f'{path}/{name}', 'w') as afile: afile.write(str(content))

    def rewrite(fromfile, tofile, frompath = currentdirectory(), topath = currentdirectory()):
        if file.exist(fromfile, frompath) and file.exist(tofile, topath):
            with open(f'{frompath}/{fromfile}') as copyfile: copy = copyfile.read()
            with open(f'{topath}/{tofile}', 'w') as afile: afile.write(copy)

    def delete(name, path = currentdirectory()):
        if file.exist(name, path): remove(f'{path}/{name}')

    def extension(name):
        return name[1 + name.rfind('.'):]

    def rename(name, to, path = currentdirectory()):
        if file.exist(name, path): rename(f'{path}/{name}', f'{path}/{to}')

    def hide(name, path = currentdirectory()):
        if file.exist(name, path): system(f'attrib +h {path}/{name}')

    def show(name, path = currentdirectory()):
        if file.exist(name, path): system(f'attrib -h {path}/{name}')

    def size(name, apath = currentdirectory()): # Return size in bytes
        return path.getsize(f'{apath}/{name}')

    def symbols(name, apath = currentdirectory()):
        return len(file.content(name, apath))

    def created(name, apath = currentdirectory()):
        return strftime('%d.%m.%Y %H:%M:%S', localtime(path.getctime(f'{apath}/{name}')))

    def motificated(name, apath = currentdirectory()):
        return strftime('%d.%m.%Y %H:%M:%S', localtime(path.getmtime(f'{apath}/{name}')))