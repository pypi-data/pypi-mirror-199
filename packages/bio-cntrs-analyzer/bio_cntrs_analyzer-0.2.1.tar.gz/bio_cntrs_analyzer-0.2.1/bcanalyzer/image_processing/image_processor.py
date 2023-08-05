import cv2
import numpy as np
from scipy import stats

from sdd_segmentation.sdd import sdd_threshold_selection
from bcanalyzer.image_processing.utils import invertByMask, getLargestContourThresh
from bcanalyzer.common.io import im_load


_img_cache = {
    'im_name': None,
    'raw_image_np': None
}


def mean_window(data, axis):
    res = np.sum(data, axis=axis)
    return res


def std_window(data, axis):
    res = np.std(data, axis=axis)
    return res

# Rolling 2D window for ND array


def roll(a,      # ND array
         b_shape,      # rolling 2D window array size
         dx=1,   # horizontal step, abscissa, number of columns
         dy=1):  # vertical step, ordinate, number of rows
    shape = a.shape[:-2] + \
        ((a.shape[-2] - b_shape[-2]) // dy + 1,) + \
        ((a.shape[-1] - b_shape[-1]) // dx + 1,) + \
        b_shape  # sausage-like shape with 2D cross-section
    strides = a.strides[:-2] + \
        (a.strides[-2] * dy,) + \
        (a.strides[-1] * dx,) + \
        a.strides[-2:]
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def sliding_window(data, win_shape, fcn, dx=1, dy=1):
    n = data.ndim  # number of dimensions
    # np.all over 2 dimensions of the rolling 2D window for 4D array
    result = fcn(roll(data, win_shape, dx, dy), axis=(n, n+1))
    return result


def tile_array(a, b0, b1):
    r, c = a.shape                                    # number of rows/columns
    rs, cs = a.strides                                # row/column strides
    # view a as larger 4D array
    x = np.lib.stride_tricks.as_strided(a, (r, b0, c, b1), (rs, 0, cs, 0))
    return x.reshape(r*b0, c*b1)                      # create new 2D array


def edge_density(img_np: np.array,
                 win_size: int,
                 win_step: int = 10,
                 canny_1: float = 41,
                 canny_2: float = 207) -> np.array:
    """Method is implemented algorithm for local edge density estimation, 
    proposed in "Sinitca, A. M., Kayumov, A. R., Zelenikhin, P. V., 
    Porfiriev, A. G., Kaplun, D. I., & Bogachev, M. I. (2023). 
    Segmentation of patchy areas in biomedical images based on local edge
    density estimation. Biomedical Signal Processing and Control, 79, 104189."

    https://www.sciencedirect.com/science/article/abs/pii/S1746809422006437

    Args:
        img_np (np.array): Gray scale image
        win_size (int): Size of averaging windows
        win_step (int, optional): Step for windows sliding. Defaults to 10.
        canny_1 (float, optional): 1st threshold for canny. Defaults to 41.
        canny_2 (float, optional): 2nd threshold for canny. Defaults to 207.

    Returns:
        np.array: Edge dencity map
    """
    dxy = win_step
    mid = cv2.Canny(img_np, canny_1, canny_2)

    result = sliding_window(mid, (win_size, win_size),
                            mean_window, dx=dxy, dy=dxy) // ((win_size*win_size))
    result = tile_array(result, dxy, dxy)
    h_pad = img_np.shape[0] - result.shape[0]
    w_pad = img_np.shape[1] - result.shape[1]
    result = np.pad(result, ((
        h_pad//2, h_pad//2+img_np.shape[0] % 2), (w_pad//2, w_pad//2+img_np.shape[1] % 2)), 'edge')
    return result


def process_image(img_path, params, largest_cnt_only=False, force_q_th=False):
    print(params)
    threshhold = params['thre']
    threshhold_abs = params['thre_abs']
    use_abs_threshhold = params['use_abs_threshhold']
    largest_cnt_only = params['is_single_object']
    do_bg_removing = params['do_bg_removing']
    do_otsu_thresholding = params['do_otsu_thresholding']
    canny_1 = params['canny_1']
    canny_2 = params['canny_2']

    win_size_perc = int(params['win_size'])
    dxy = 10

    channel_r = params['channel_r']
    channel_g = params['channel_g']
    channel_b = params['channel_b']

    if _img_cache['im_name'] == img_path:
        img_np = _img_cache['raw_image_np'].copy()
    else:
        img_np = im_load(img_path)
        _img_cache['im_name'] = img_path
        _img_cache['raw_image_np'] = img_np.copy()

    win_size = int(img_np.shape[0] * win_size_perc / 100)

    if len(img_np.shape) == 3:
        img_np[:, :, 0] *= channel_b
        img_np[:, :, 1] *= channel_g
        img_np[:, :, 2] *= channel_r
        gray = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    elif len(img_np.shape) == 2:
        gray = img_np.copy()
        img_np = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)
    else:
        raise ValueError(
            f"Unsupported count of channels ({len(img_np.shape)})")

    if do_bg_removing:
        gray = gray.astype(float) / 255.0
        k_size = win_size*3
        bg = cv2.blur(gray, (k_size, k_size))
        gray = gray - bg

        gray -= gray.min()
        gray = (gray * 255).astype(np.uint8)

    mid = cv2.Canny(gray, canny_1, canny_2)

    result = sliding_window(mid, (win_size, win_size),
                            mean_window, dx=dxy, dy=dxy) // ((win_size*win_size))
    result = tile_array(result, dxy, dxy)
    h_pad = img_np.shape[0] - result.shape[0]
    w_pad = img_np.shape[1] - result.shape[1]
    result = np.pad(result, ((
        h_pad//2, h_pad//2+img_np.shape[0] % 2), (w_pad//2, w_pad//2+img_np.shape[1] % 2)), 'edge')

    th_perc = None
    if do_otsu_thresholding == "Otsu":
        th, img_thresh = cv2.threshold(
            np.uint8(result), 0, 255, cv2.THRESH_OTSU+cv2.THRESH_BINARY_INV)
        img_thresh = np.uint8(img_thresh)
    elif do_otsu_thresholding.startswith("SDD"):
        T = sdd_threshold_selection(result.astype(float), 15)
        if len(T) < 1:
            th = 0
        elif do_otsu_thresholding == "SDD lower":
            th = T[0]
        elif do_otsu_thresholding == "SDD median":
            th = T[round(len(T)/2)]
        elif do_otsu_thresholding == "SDD upper":
            th = T[-1]

        img_thresh = np.where(result > th, 0, 1).astype(np.uint8)
    else:
        th = None
        if use_abs_threshhold and threshhold_abs is not None and not force_q_th:
            th = threshhold_abs
        else:
            th = np.percentile(result, threshhold)
            th_perc = threshhold
        img_thresh = np.where(result > th, 0, 1).astype(np.uint8)

    if th_perc is None:
        th_perc = stats.percentileofscore(result.flatten(), th, kind="weak")

    img_thresh = img_thresh[..., np.newaxis]
    #canny_thresh = cv2.bitwise_not(canny_thresh)
    if largest_cnt_only:
        img_thresh = getLargestContourThresh(img_thresh)

    preview = invertByMask(img_np, img_thresh)

    res_meta = {}
    res_meta["thre_abs"] = th
    res_meta["thre"] = th_perc
    res_meta["canny_1"] = canny_1
    res_meta["canny_2"] = canny_2
    print("res_meta", res_meta)
    return preview, img_thresh, res_meta
