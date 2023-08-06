"""
MMCQ - Modified Median Cut Quantization
A well known algorithm for quantizing a given image into a set of colors by median of it`s broadest channels
"""
from numpy import ndarray
from typing import List, Tuple, Union, Dict

class VBox(object):

    def __init__(self, r_min: int, r_max: int, g_min: int, g_max: int, b_min: int, b_max: int, histo: Dict[int, int]):
        self.r1 = r_min
        self.r2 = r_max
        self.g1 = g_min
        self.g2 = g_max
        self.b1 = b_min
        self.b2 = b_max
        self.histo = histo

    def average(self) -> List[int]:
        am = 0
        r_sum = 0
        g_sum = 0
        b_sum = 0
        for i in range(self.r1, self.r2):
            for j in range(self.g1, self.g2):
                for k in range(self.b1, self.b2):
                    ijk_key = MAIN.get_color_index(i, j, k)
                    hist_mult = self.histo.get(ijk_key, 0)
                    am += hist_mult
                    r_sum += i * hist_mult * MAIN.MULT
                    g_sum += j * hist_mult * MAIN.MULT
                    b_sum += k * hist_mult * MAIN.MULT
        if am == 0:
            r_avg = int((self.r1 + self.r2) / 2) * MAIN.MULT
            g_avg = int((self.g1 + self.g2) / 2) * MAIN.MULT
            b_avg = int((self.b1 + self.b2) / 2) * MAIN.MULT
        else:
            r_avg = int(r_sum / am)
            g_avg = int(g_sum / am)
            b_avg = int(b_sum / am)
        return [r_avg, g_avg, b_avg]

    def count(self) -> int:
        _sum = 0
        for i in range(self.r1, self.r2):
            for j in range(self.g1, self.g2):
                for k in range(self.b1, self.b2):
                    ijk_key = MAIN.get_color_index(i, j, k)
                    _sum += self.histo.get(ijk_key, 0)
        return _sum

    @property
    def copy(self):
        return VBox(self.r1, self.r2, self.g1, self.g2, self.b1, self.b2, self.histo)

def palette(input_image: ndarray, colors: int=8, SORT_BY_LIGHTNESS: bool=False) -> List[List[int]]:
    """
    Generates palette out of a image (numpy array) (differs from 'output_palette' by not reformating nor decoding the image)
    Input:
    :param input_image: input image(numpy array) to get palette out of
    :param colors: the amount of colors user wants on his palette
    Output:
    Will output a standard python list of lists of RGB colors in uint8 format ([[5,5,5],[6,6,6],...] for example)
    """
    img = []
    for row in input_image.tolist():
        for pix in row:
            if not pix == [0, 0, 0] or pix[0] + pix[1] + pix[2] >= 750:
                img.append(pix)

    histo = MAIN.get_histo(img)

    if len(histo) <= colors:
        print('IMAGE DOES NOT CONTAIN ENOUGH INFO FOR PROPER PALETTE')
        vbox_mass = []
        for i in range(colors):
            vbox_mass.append(input_image.tolist()[MAIN.get_random_indx(len(input_image), i+1)]
                             [MAIN.get_random_indx(len(input_image), int(i+1)*2)])
        return vbox_mass


    vbox = MAIN.get_vbox(img, histo)

    def iter_(VirtualBox: VBox, colors: int) -> Tuple[List[VBox], int]:
        vbox_list = [VirtualBox]
        n = 1
        i = 0
        input_highres = True
        while n < colors:
            undefined_colors = 0
            vbox1, vbox2, indx, out_highres = MAIN.get_median_cut(vbox_list, i, input_highres)
            if vbox2 == 0:
                del vbox_list[indx]
                vbox_list.append(vbox1)
                i += 1
            elif vbox1 == 1 and vbox2 == 1 and indx == 1:
                if out_highres:
                    input_highres = False
                    continue
                else:
                    undefined_colors = colors-n
                    break
            else:
                del vbox_list[indx]
                vbox_list.append(vbox1)
                vbox_list.append(vbox2)
                n += 1
                i = 0
        return vbox_list, undefined_colors

    vbox_mass, undefined_colors = iter_(vbox, colors)
    vbox_mass.sort(key=lambda x: x.count(), reverse=True)
    vbox_mass = list(map(lambda x: x.average(), vbox_mass))
    for i in range(undefined_colors):
        vbox_mass.append(img[MAIN.get_random_indx(len(img), i+1, random_number)])
    if SORT_BY_LIGHTNESS:
        vbox_mass.sort(key=lambda x: x[0] + x[1] + x[2], reverse=True)
    return vbox_mass


class MAIN(object):
    MULT = 8
    COL_ACCURACY = 2
    MAX_ITERATION = 100

    @staticmethod
    def get_median_cut(vbox_list: List[VBox], i:int, highres:bool) -> Tuple[Union[VBox, int], Union[VBox, int], int, bool]:
        vbox_indx = 0
        MRO = [0, 0, 0]
        for vbox in vbox_list:
            rRange = vbox.r2 - vbox.r1
            gRange = vbox.g2 - vbox.g1
            bRange = vbox.b2 - vbox.b1
            if rRange >= gRange and rRange >= bRange:
                cut_chan = 'r'
                mRange = rRange
            elif gRange >= rRange and gRange >= bRange:
                cut_chan = 'g'
                mRange = gRange
            else:
                cut_chan = 'b'
                mRange = bRange
            if highres:
                if MRO[0] < mRange:
                    MRO = [mRange, cut_chan, vbox_indx]
            else:
                if MRO[0] < vbox.count():
                    MRO = [vbox.count(), cut_chan, vbox_indx]
            vbox_indx += 1
        cut_chan = MRO[1]
        vbox_indx = MRO[2]
        mass = range(getattr(vbox_list[vbox_indx], cut_chan + '1'),
                     getattr(vbox_list[vbox_indx], cut_chan + '2'))
        l = len(mass)
        if l % 2:
            c_cut = mass[int(l / 2)]
        else:
            c_cut = round((mass[int(l / 2) - 1] + mass[int(l / 2)]) / 2)
        vbox1 = vbox_list[vbox_indx].copy
        vbox2 = vbox_list[vbox_indx].copy
        setattr(vbox1, cut_chan + '2', c_cut)
        setattr(vbox2, cut_chan + '1', c_cut + 1)

        if i <= MAIN.MAX_ITERATION:
            if vbox2.count() <= MAIN.COL_ACCURACY:
                if vbox1.count() <= MAIN.COL_ACCURACY:
                    print("IMAGE TOO SMALL/TOO MONOTONIC/TOO RANDOM TO PROPERLY EXPORT THE DESIRED AMOUNT OF COLORS")
                    if vbox1.count() == 1 and vbox2.count() == 1:
                        return vbox1, vbox2, vbox_indx, True
                    else:
                        if highres:
                            return 1,1,1,True
                        else:
                            return 1,1,1,False
                else:
                    return vbox1, 0, vbox_indx, True
            else:
                if vbox1.count() <= MAIN.COL_ACCURACY:
                    return vbox2, 0, vbox_indx, True
                else:
                    return vbox1, vbox2, vbox_indx, True
        else:
            return vbox1, vbox2, vbox_indx, True

    @staticmethod
    def get_color_index(r: int, g: int, b: int) -> int: #basically convert 3 8-bit values into 1 24-bit one
        return (r << MAIN.MULT) + (g << (MAIN.MULT * 2)) + b

    @staticmethod
    def get_histo(img: List[List[int]]) -> Dict[int, int]:
        histo = dict()
        for pix in img:
            r = int(pix[0] / MAIN.MULT)
            g = int(pix[1] / MAIN.MULT)
            b = int(pix[2] / MAIN.MULT)
            histo_key = MAIN.get_color_index(r, g, b)
            histo[histo_key] = histo.setdefault(histo_key, 0) + 1
        return histo

    @staticmethod
    def get_vbox(img: List[List[int]], histo: Dict[int, int]) -> VBox:
        r_min = 255
        r_max = 0
        g_min = 255
        g_max = 0
        b_min = 255
        b_max = 0
        for pix in img:
            r = int(pix[0] / MAIN.MULT)
            g = int(pix[1] / MAIN.MULT)
            b = int(pix[2] / MAIN.MULT)
            r_min = min(r_min, r)
            r_max = max(r_max, r)
            g_min = min(g_min, g)
            g_max = max(g_max, g)
            b_min = min(b_min, b)
            b_max = max(b_max, b)
        return VBox(r_min, r_max, g_min, g_max, b_min, b_max, histo)

    @staticmethod
    def get_random_indx(img_size: int, i: int) -> int: #not really working algorithm, for the proper use
        pi = '31459265358979323846'
        seed = pi[i] * str(str(img_size)[0]*i)[0] // 81
        return int(img_size * seed) - 1
