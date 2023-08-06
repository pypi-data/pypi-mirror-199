from typing import List, Tuple
from Image_reader import Image, Image_reading_class
from JFIF_Decoder_Algorithms import do_InverseDCT

ITERATION_LIMIT = 100

JFIF_HUFFMAN_CODE_MAX_LENGTH = 16
JFIF_MCU_DEFAULT_SIZE = 1
JFIF_MATRIX_ROW_SIZE = 8
JFIF_IMAGE_COMPONENTS_AMOUNT = 3
JFIF_FILLING_ORDER = [[0,0],[0,1],[1,0],[2,0],[1,1],[0,2],[0,3],[1,2],[2,1],[3,0],[4,0],[3,1],[2,2],[1,3],[0,4],[0,5],
                      [1,4],[2,3],[3,2],[4,1],[5,0],[6,0],[5,1],[4,2],[3,3],[2,4],[1,5],[0,6],[0,7],[1,6],[2,5],[3,4],
                      [4,3],[5,2],[6,1],[7,0],[7,1],[6,2],[5,3],[4,4],[3,5],[2,6],[1,7],[2,7],[3,6],[4,5],[5,4],[6,3],
                      [7,2],[7,3],[6,4],[5,5],[4,6],[3,7],[4,7],[5,6],[6,5],[7,4],[7,5],[6,6],[5,7],[6,7],[7,6],[7,7]]

IDCT_matrix = [[0.0 for i in range(JFIF_MATRIX_ROW_SIZE)] for j in range(JFIF_MATRIX_ROW_SIZE)]
MCU_width_mult, MCU_height_mult = 0, 0

def decode(image: Image_reading_class, xff: bool = False, marker_name: str = ''):
    img_cc, img_height, img_width, img_bd, marker_name, marker_length, MCU_am, MCU_width, MCU_height = (int,) * 9
    DQT_0 = [[0 for i in range(JFIF_MATRIX_ROW_SIZE)] for j in range(JFIF_MATRIX_ROW_SIZE)]
    DQT_1 = [[0 for i in range(JFIF_MATRIX_ROW_SIZE)] for j in range(JFIF_MATRIX_ROW_SIZE)]
    DC_DHT_0, DC_DHT_1, AC_DHT_0, AC_DHT_1, MCU, components_info, MCU_data, img_data = (list,) * 8
    MCU_width_mult, MCU_height_mult, x, y = 0, 0, 0, 0
    reading_finished = False
    n = 0
    while not reading_finished and not n >= ITERATION_LIMIT:
        if xff or image.read_str(1) == b'\xff':

            if xff:
                xff = False
            else:
                marker_name = image.read_1_dec()


            if marker_name == 219:  # DQT (Define Quantization Table)
                marker_length = image.read(2, 'long')
                val = image.read_str(1)
                if val == b'\x00':
                    for i in range(marker_length - 3):
                        DQT_0[JFIF_FILLING_ORDER[i][1]][JFIF_FILLING_ORDER[i][0]] = image.read_1_dec()
                elif val == b'\x01':
                    for i in range(marker_length - 3):
                        DQT_1[JFIF_FILLING_ORDER[i][0]][JFIF_FILLING_ORDER[i][1]] = image.read_1_dec()
                else:
                    raise IOError("ERROR WHEN ASSIGNING DQT")
                continue



            elif marker_name in (192, 193, 194, 195, 197, 198, 199, 201, 202, 203, 205, 206, 207):  # SOF (Start Of Frame)
                if not marker_name == 192:
                    raise IOError("Only 'Baseline' encoding mode is supported.")

                image.read(2)
                img_bd = image.read_1_dec()
                img_height = round_up_to_bigger_side(image.read(2, 'long')/ JFIF_MATRIX_ROW_SIZE) * JFIF_MATRIX_ROW_SIZE
                img_width = round_up_to_bigger_side(image.read(2, 'long') / JFIF_MATRIX_ROW_SIZE) * JFIF_MATRIX_ROW_SIZE
                img_compcount = image.read_1_dec()
                components_info = [0 for i in range(img_compcount)]
                for i in range(img_compcount):
                    comp_index = image.read_1_dec() - 1
                    subsample_w, subsample_h = image.read(1, 'subdiv')
                    comp_QT = image.read_1_dec()
                    components_info[comp_index] = [subsample_w, subsample_h, comp_QT]

                MCU = generate_MCU(components_info, img_compcount)
                MCU_width, MCU_height = MCU[-3], MCU[-2]
                MCU_width_am = round_up_to_bigger_side(img_width / MCU_width)
                MCU_height_am = round_up_to_bigger_side(img_height / MCU_height)
                MCU_am = MCU_width_am * MCU_height_am

                img_data = [[[] for i in range(max(img_width, MCU_width))] for i in range(max(img_height, MCU_height))]
                if not img_scanmode_baseline:
                    matrices_am = 0
                    width_max, height_max = 0, 0
                    for i in range(img_compcount):
                        matrices_am += MCU[i][0]
                        width_max = components_info[i][0] if components_info[i][0] > width_max else width_max
                        height_max = components_info[i][1] if components_info[i][1] > height_max else height_max
                    raw_matrices_full = [[[[0 for i in range(JFIF_MATRIX_ROW_SIZE)]for j in range(JFIF_MATRIX_ROW_SIZE)]
                                        for k in range(matrices_am)] for l in range(MCU_am * height_max * width_max)]

                continue



            elif marker_name == 196:  # DHT (Define Huffman Table)
                marker_length = image.read(2, 'long')
                table_param, table_count = image.read(1, 'subdiv')
                length_counts = [0 for i in range(16)]
                codes_list = [0 for i in range(marker_length - 2 - 1 - 16)]

                for i in range(16):
                    length_counts[i] = image.read_1_dec()
                for i in range(marker_length - 2 - 1 - 16):
                    codes_list[i] = image.read_1_dec()

                if table_param == 0 and table_count == 0:
                    DC_DHT_0 = HuffmanTable(codes_list, length_counts)
                elif table_param == 0 and table_count == 1:
                    DC_DHT_1 = HuffmanTable(codes_list, length_counts)
                elif table_param == 1 and table_count == 0:
                    AC_DHT_0 = HuffmanTable(codes_list, length_counts)
                else:
                    AC_DHT_1 = HuffmanTable(codes_list, length_counts)
                continue



            elif marker_name == 218:  # SOS (Start Of Scan)
                marker_length = image.read(2, 'long')
                components_count = image.read_1_dec()
                comp_order = []
                DHT_tables_list = [[[] for i in range(2)] for j in range(img_compcount)]
                comp_index = int

                for i in range(components_count):
                    comp_index = image.read_1_dec() - 1
                    indx1, indx2 = image.read(1, 'subdiv')
                    DHT_tables_list[comp_index] = [locals()[f'DC_DHT_{indx1}'],
                                                   locals()[f'AC_DHT_{indx2}']]
                    comp_order.append(comp_index)

                xff = True
                marker_name = 300
                continue



            elif marker_name == 300: # BASELINE ENCODING MODE

                image.read(3)  # skip spectral because algorithm made for baseline mode

                SOS_data = ''
                finished = False
                while not finished:
                    byte = image.read_1_dec()
                    if byte == 255:
                        sec_byte = image.read_1_dec()
                        if not sec_byte == 0:
                            xff = True
                            marker_name = sec_byte
                            break  # FINISHED = TRUE
                    SOS_data += format(byte, '08b')

                MCU_data = [[[[0 for i in range(JFIF_MATRIX_ROW_SIZE)] for l in range(JFIF_MATRIX_ROW_SIZE)]
                             for j in range(MCU[k][0])] for k in comp_order]
                data_indx, prev_data_indx, MCU_width_mult, MCU_height_mult = 0, 0, 0, 0
                DCT_coeff = int
                DC_val = [0 for i in range(len(comp_order))]
                for it in range(MCU_am):
                    for comp in comp_order:
                        DC_table, AC_table = DHT_tables_list[comp]
                        QT_table = locals()[f'DQT_{MCU[comp][-1]}']
                        DCT_coeff, zeros_am = (int,) * 2
                        comp_matrices = []
                        for matrix in range(MCU[comp][0]):
                            raw_matrix = [[0 for i in range(JFIF_MATRIX_ROW_SIZE)] for j in range(JFIF_MATRIX_ROW_SIZE)]
                            finished = False
                            assignment_indx, key = 0, ''
                            while not finished:  # GETTING DC VAL
                                try:
                                    key = SOS_data[prev_data_indx:data_indx]
                                except:
                                    break

                                if DC_table.iselemof(key):
                                    val = DC_table.decode_huffman(key)

                                    if val:
                                        code = SOS_data[data_indx:data_indx + val]
                                        data_indx += val
                                        DCT_coeff = convert_code_to_coeff(code)

                                    else:
                                        DCT_coeff = 0

                                    DC_val[comp] += DCT_coeff
                                    DCT_coeff = DC_val[comp]
                                    raw_matrix[0][0] = DCT_coeff

                                    prev_data_indx = data_indx
                                    assignment_indx += 1

                                    finished = True
                                data_indx += 1

                            finished = False
                            while not finished:  # GETTING AC VALS

                                try:
                                    key = SOS_data[prev_data_indx:data_indx]
                                except:
                                    break

                                if AC_table.iselemof(key):
                                    val = AC_table.decode_huffman(key)

                                    if val:

                                        zeros_am, code_length = int(format(val, '08b')[:4], base=2), \
                                                                int(format(val, '08b')[4:], base=2)

                                        code = SOS_data[data_indx:data_indx + code_length]
                                        data_indx += code_length
                                        prev_data_indx = data_indx

                                        DCT_coeff = convert_code_to_coeff(code)

                                        assignment_indx += zeros_am
                                        if assignment_indx >= 63:
                                            finished = True
                                        else:
                                            raw_matrix[JFIF_FILLING_ORDER[assignment_indx][1]][
                                                JFIF_FILLING_ORDER[assignment_indx][0]] = DCT_coeff
                                            assignment_indx += 1

                                    else:
                                        prev_data_indx = data_indx
                                        finished = True

                                data_indx += 1


                            for i in range(JFIF_MATRIX_ROW_SIZE):  # QUANTIZATION ALGORITHM
                                for j in range(JFIF_MATRIX_ROW_SIZE):
                                    raw_matrix[i][j] = raw_matrix[i][j] * QT_table[i][j]

                            comp_matrices.append(do_InverseDCT(raw_matrix))  # method also sums 128


                        if MCU_width == JFIF_MATRIX_ROW_SIZE and MCU_height == JFIF_MATRIX_ROW_SIZE:
                            MCU_data[comp] = comp_matrices[0]
                        else:
                            MCU_data[comp] = convert_MCU_to_pix_grid(comp_matrices, MCU_width, MCU_height)


                    if (MCU_width_mult * MCU_width) >= MCU_width_am * MCU_width:
                        MCU_width_mult = 0
                        MCU_height_mult += 1
                    x = MCU_width * MCU_width_mult
                    y = MCU_height * MCU_height_mult

                    if components_count == 3:  # means pixels in YCbCr format
                        for k in range(MCU_height):
                            for j in range(MCU_width):
                                img_data[y + j][x + k] = YCbCr_to_RGB(MCU_data[0][k][j], MCU_data[1][k][j],
                                                                      MCU_data[2][k][j])
                    elif components_count == 4:  # means pixels in CMYK format
                        for k in range(img_height):
                            for j in range(img_width):
                                img_data[y + j][x + k] = CMYK_to_RGB(MCU_data[0][k][j], MCU_data[1][k][j],
                                                                     MCU_data[2][k][j], MCU_data[3][k][j])
                    else:
                        raise IOError(f'Format not supported yet, components_count = {components_count}')
                    MCU_width_mult += 1
                continue



            elif marker_name == 217:  # EOI (End Of Image)
                image.close()
                img = Image(img_width, img_height, img_bd, img_cc, img_data)
                return img


            elif marker_name == 254: #COMMENTARY MARKER
                marker_length = image.read(2, 'long')
                print("Some commentary:")
                print(image.read(marker_length - 2, 'str'))


            else: #SKIP MARKER IF NOT IN DATABASE
                marker_length = image.read(2, 'long')
                image.read(marker_length - 2)








    raise IOError("SOMETHING WENT WRONG WHEN DECODING JPEG")
    return 0




class HuffmanTable(object):


    def __init__(self, codes_list:List[int], length_counts:List[int]):
        self.huffman_codes = {}
        codes_length_list = HuffmanTable.convert_LC2CL(length_counts)
        huffman_code_counter = 0
        code_length_counter = 1
        for i in range(len(codes_length_list)):
            finished = False
            while not finished:
                if codes_length_list[i] == code_length_counter:
                    self.huffman_codes[format(huffman_code_counter, f'0{code_length_counter}b')] = codes_list[i]
                    huffman_code_counter += 1
                    finished = True
                else:
                    huffman_code_counter <<= 1
                    code_length_counter += 1


    def iselemof(self, huffman_code: str) -> bool:
        if huffman_code in self.huffman_codes:
            return True
        else:
            return False


    def decode_huffman(self, huffman_code: str) -> int:
        return self.huffman_codes[huffman_code]


    @staticmethod
    def convert_LC2CL(length_counts: List[int]) -> List[int]:
        codes_length_list = []
        for i in range(JFIF_HUFFMAN_CODE_MAX_LENGTH):
            for j in range(length_counts[i]):
                codes_length_list.append(i + 1)

        return codes_length_list



def generate_MCU(components_info: List[List[int]], img_compcount: int) -> Tuple:
    MCU_width = JFIF_MCU_DEFAULT_SIZE
    MCU_height = JFIF_MCU_DEFAULT_SIZE
    MCU_compcount = 0
    MCU = components_info.copy()
    for i in range(img_compcount):
        width_s, height_s, qt = components_info[i]
        compcount = width_s * height_s
        MCU_width = max(MCU_width, width_s)
        MCU_height = max(MCU_height, height_s)
        MCU[i] = [compcount, qt]
        MCU_compcount += compcount
    MCU.append(MCU_width * 8)
    MCU.append(MCU_height * 8)
    MCU.append(MCU_compcount)
    return MCU


def convert_MCU_to_pix_grid(comp_matrices: List[List[List[List[int]]]], MCU_width: int, MCU_height: int) ->\
                                                                                List[List[List[int]]]:
    pix_grid = list
    if not len(comp_matrices) == 1:
        pix_grid = [[] for j in range(MCU_height)]
        cm_indx, cm_indx_2, pix_row_indx, cm_row_indx = 0, 0, 0, 0
        for i in range(MCU_height // JFIF_MATRIX_ROW_SIZE):
            for j in range(JFIF_MATRIX_ROW_SIZE):
                cm_indx = cm_indx_2
                for k in range(MCU_width // JFIF_MATRIX_ROW_SIZE):
                    pix_grid[pix_row_indx] += comp_matrices[cm_indx][cm_row_indx]
                    cm_indx += MCU_width // JFIF_MATRIX_ROW_SIZE
                pix_row_indx += 1
                cm_row_indx += 1
            cm_indx_2 += 1
            cm_row_indx = 0

    else:
        pix_grid = [[0 for i in range(MCU_width)] for j in range(MCU_height)]
        for i in range(MCU_height):
            for j in range(MCU_width):
                pix_grid[i][j] = comp_matrices[0][i // (MCU_height // 8)][j // (MCU_width // 8)]

    return pix_grid


def YCbCr_to_RGB(Y: int,Cb: int,Cr: int) -> List[int]:
    Cb = Cb - 128
    Cr = Cr - 128
    R = round(Y + 1.402*Cr)
    G = round(Y - 0.34414*Cb - 0.71414*Cr)
    B = round(Y + 1.772*Cb)

    R = min(max(0,R),255)
    G = min(max(0,G),255)
    B = min(max(0,B),255)

    return [R,G,B]

def CMYK_to_RGB(C: int,M: int,Y: int,K: int) -> List[int]:
    K = 1-K
    R = 255 * (1-C) * K
    G = 255 * (1-M) * K
    B = 255 * (1-Y) * K

    R = min(max(0, R), 255)
    G = min(max(0, G), 255)
    B = min(max(0, B), 255)

    return [R,G,B]


def convert_code_to_coeff(code: str) -> int:
    if code == '':
        return 0
    elif code[0] == '1':
        return int(code, base=2)
    elif code[0] == '0':
        return int(code, base=2) - (2 ** len(code) - 1)
    else:
        raise IOError(code + " is not binary!")

def round_up_to_bigger_side(dec: int) -> int:
    if dec > int(dec):
        dec = int(dec) + 1
    return int(dec)

