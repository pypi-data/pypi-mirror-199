from numpy import ndarray, asarray
from typing import Tuple, List, Dict


class image(object):
    """
    A unoptimized class used to create images.
    Basically you first provide the information for the image in numpy array form, then it is converted into
    Dict[Tuple[int, int], List[int]] form, where Tuple defines the x, y coordinates of a pixel, and List is the
    pixel in RGB uint8 form ({(0,0):[255,255,255],...} for example)
    """

    def __init__(self, image: ndarray):
        self.img = dict()
        x = -1
        y = -1
        for row in image.tolist():
            y += 1
            for pix in row:
                x += 1
                if x >= image.shape[1]:
                    x = 0
                self.img[x,y] = pix


    def translate(self, coord: Tuple[int, int]=(0,0)):
        new_img = dict()
        for k,v in self.img.items():
            x,y = k
            new_x = x
            new_y = y
            new_x += int(coord[0])
            new_y += int(coord[1])
            new_img[new_x,new_y] = v
        self.img = new_img


    def items(self):
        return self.img.items()

    def pop(self, index: int, out: int=0) -> int:
        return self.img.pop(index, out)

    def change_color(self, color: List[int]=[0,0,0]) -> Dict[Tuple[int, int], List[int]]:
        for k,v in self.img.items():
            self.img[k] = color
        return self.img

    def get_alpha(self) -> Dict[Tuple[int, int], List[int]]:
        alpha = dict()
        for k,v in self.img:
            if v == 0 or v == [0,0,0]:
                alpha[k] = 0
            else:
                alpha[k] = 1
        return alpha


    @staticmethod
    def merge(img_B: Dict[Tuple[int, int], List[int]], img_A: Dict[Tuple[int, int], List[int]], alpha: Dict[Tuple[int, int], List[int]] = dict()) -> Dict[Tuple[int, int], List[int]]:
        comp = dict()
        for k_B,v_B in img_B.items():
            a = alpha.pop((k_B), 0)
            if type(a) == list:
                for x in a:
                    a = x
            r_B, g_B, b_B = v_B
            r_A, g_A, b_A = img_A.pop(k_B, [0,0,0])
            comp[k_B] = [r_A + r_B * (1 - a), g_A + g_B * (1 - a), b_A + b_B * (1 - a)]
        return comp


    @staticmethod
    def convert_to_numpy(img: Dict[Tuple[int, int], List[int]], width: int) -> ndarray:
        l = list()
        l2 = list()
        n_cycleAm = 0
        for k,v in img.items():
            l2.append(v)
            n_cycleAm += 1
            if n_cycleAm >= width:
                l.append(l2[:])
                n_cycleAm = 0
                l2.clear()
        out_img = asarray(l, dtype='uint8')
        return out_img