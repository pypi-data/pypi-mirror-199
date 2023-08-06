import codecs
import csv

import cobolio.config as cfg


display = codecs.getdecoder(cfg.codepage)


def yield_records(file, rec_size):
    rec_bytes = file.read(rec_size)
    while rec_bytes:
        yield rec_bytes
        rec_bytes = file.read(rec_size)


def add_decimal_point(number, scale):
    if scale > 0:
        if isinstance(number, (int, float, complex)):
            result = int(number) / int('1'.ljust(scale + 1, '0'))
        else:
            result = '{}.{}'.format(number[:-scale], number[-scale:])
    else:
        result = number
    return result


def unpack_zd(data, scale):
    if not data:
        return ""
    last_hexbyte = data[-1].encode(cfg.codepage).hex()
    zd_sign = {'f': '+', 'c': '+', 'd': '-'}
    sign = zd_sign.get(last_hexbyte[0].lower(), '+')
    unpacked_val = '{}{}{}'.format(sign, data[:-1], last_hexbyte[1])
    return add_decimal_point(unpacked_val, scale)


def unpack_comp(data, disp_size, scale):
    if data:
        comp_dec = int.from_bytes(data, byteorder='big', signed=True)
    else:
        comp_dec = 0
    comp_dec = f'{comp_dec:+0{disp_size}.0f}'
    return add_decimal_point(comp_dec, scale)


def unpack_comp3(data, scale):
    if not data:
        return ""

    hexbytes = data.hex()
    if hexbytes[-1].lower() in ('b', 'd', 'B', 'D'):
        unpacked = "-{}".format(hexbytes[:-1])
    else:
        unpacked = "+{}".format(hexbytes[:-1])
    return add_decimal_point(unpacked, scale)


def handle_non_printable(data, mask):
    out_data = []
    for char in data:
        if char.isprintable():
            out_data.append(char)
        else:
            out_data.append(mask)
    return ''.join(out_data)


def convert_cobol_data_to_csv(cobol_file, rec_length, layout, output_file):
    # cobolFile = open(input_datafile, 'rb')
    # outputFile = open(output_datafile, 'w', newline='')
    out_file = csv.writer(output_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)

    header_list = []
    for name, start, size, disp_size, usage, sign, scale in layout:
        header_list.append(name)
    out_file.writerow(header_list)

    for rec_data in yield_records(cobol_file, rec_length):
        record_list = []
        for name, start, size, disp_size, usage, sign, scale in layout:
            field = rec_data[start:start + size]
            if usage == 'COMP-3':
                comp3_unpacked = unpack_comp3(field, scale)
                if not comp3_unpacked.replace(
                        '.', '', 1
                ).replace(
                    '-', '', 1
                ).replace(
                    '+', '', 1
                ).replace(',', '').isnumeric() and comp3_unpacked:
                    comp3_unpacked = '0x{}'.format(str(field.hex()).upper())  # Sending the hex value of EBCDIC data
                record_list.append(comp3_unpacked)
            elif usage == 'COMP':
                comp_unpacked = unpack_comp(field, disp_size, scale)
                if not comp_unpacked.replace(
                        '.', '', 1
                ).replace(
                    '-', '', 1
                ).replace(
                    '+', '', 1
                ).replace(
                    ',', ''
                ).isnumeric() and comp_unpacked:
                    comp_unpacked = '0x{}'.format(str(field.hex()).upper())  # Sending the hex value of EBCDIC data
                record_list.append(comp_unpacked)
            else:
                disp = list(display(field))[0]
                if sign == 'SIGNED':
                    disp = unpack_zd(disp, scale)
                if not disp.isprintable():
                    # disp = handle_non_printable(disp, '.') ## Replaces non-printable char with '.'
                    disp = '0x{}'.format(str(field.hex()).upper())  # Sending the hex value of EBCDIC data
                record_list.append(disp)

        out_file.writerow(record_list)


def get_copybook_layout(parse_dict):
    lrecl = 0
    layout = []

    for item_1 in parse_dict:
        if 'lrecl_max' in parse_dict[item_1][0].keys():
            lrecl = parse_dict[item_1][0]['lrecl_max']

        for item_2 in parse_dict[item_1]:

            if 'usage' in parse_dict[item_1][item_2].keys():
                usage = parse_dict[item_1][item_2]['usage']
            else:
                usage = 'DISPLAY'

            data_name = parse_dict[item_1][item_2]['data_name'].replace('-', '_')
            offset = parse_dict[item_1][item_2]['offset']

            if 'storage_length' in parse_dict[item_1][item_2].keys():
                length = parse_dict[item_1][item_2]['storage_length']
            else:
                length = 0

            if 'disp_length' in parse_dict[item_1][item_2].keys():
                disp_length = parse_dict[item_1][item_2]['disp_length']
            else:
                disp_length = 0

            sign = 'UNSIGNED'
            if 'signed' in parse_dict[item_1][item_2].keys():
                if parse_dict[item_1][item_2]['signed']:
                    sign = 'SIGNED'

            if 'scale' in parse_dict[item_1][item_2].keys():
                scale = parse_dict[item_1][item_2]['scale']
            else:
                scale = 0

            if length > 0:
                layout.append((data_name, offset, length, disp_length, usage, sign, scale))

    return lrecl, layout
