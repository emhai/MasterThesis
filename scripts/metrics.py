import argparse
import os
import warnings

from skimage.metrics import structural_similarity
from math import log10, sqrt
import cv2
import numpy as np

import lpips


# https://www.geeksforgeeks.org/python-peak-signal-to-noise-ratio-psnr/
def PSNR(original_path, synthesized_path):

    original = cv2.imread(original_path)
    synthesized = cv2.imread(synthesized_path)

    mse = np.mean((original - synthesized) ** 2)
    if mse == 0:  # MSE is zero means no noise is present in the signal .
        # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def additional_SSIM(diff, original, synthesized):
    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(original.shape, dtype='uint8')
    filled_after = synthesized.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(synthesized, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    cv2.imshow('original', original)
    cv2.imshow('sythesized', synthesized)
    # cv2.imshow('diff', diff)
    # cv2.imshow('mask', mask)
    # cv2.imshow('filled after', filled_after)
    # cv2.waitKey(0)

# https://stackoverflow.com/questions/71567315/how-to-get-the-ssim-comparison-score-between-two-images
def SSIM(original_path, synthesized_path):

    original = cv2.imread(original_path)
    synthesized = cv2.imread(synthesized_path)

    before_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    after_gray = cv2.cvtColor(synthesized, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(before_gray, after_gray, full=True)

    # additional_SSIM(diff, original, synthesized)
    return score


# https://github.com/richzhang/PerceptualSimilarity/blob/master/test_network.py
def LPIPS(original_path, synthesized_path):

    spatial = True
    loss_fn = lpips.LPIPS(net='alex', spatial=spatial, verbose=False)  # Can also set net = 'squeeze' or 'vgg'

    original = lpips.im2tensor(lpips.load_image(original_path))
    synthesized = lpips.im2tensor(lpips.load_image(synthesized_path))

     # use gpu
    # original = original.cuda()
    # synthesized = synthesized.cuda()

    d = loss_fn.forward(original, synthesized)

    if not spatial:
        return d
    else:
        return d.mean()
        # The mean distance is approximately the same as the non-spatial distance

        # Visualize a spatially-varying distance map between ex_p0 and ex_ref
        # pylab.imshow(d[0, 0, ...].data.cpu().numpy())
        # pylab.show()

def run(original_path, synthesized_path):
    warnings.filterwarnings("ignore", category=UserWarning) # in torchvision "Arguments other than a weight enum ... deprecated"
    warnings.filterwarnings("ignore", category=FutureWarning) # in lpips "You are using torch.load with weights_onl=False ... deprecated"

    lpips = LPIPS(original_path, synthesized_path)
    lpips = lpips.item()
    psnr= PSNR(original_path, synthesized_path)
    ssim = SSIM(original_path, synthesized_path)
    # print(f"For files {original_name}, {synthesized_name}: PSNR: {psnr:.3f}, SSIM: {ssim:.3f}, LPIPS: {lpips:.3f}")
    return lpips, psnr, ssim

def main():
    """
    Takes path to two pictures and returns SSIM, LPIPS, PSNR. Called by wrappers viewcrafter_metrics and mvsplat_metrics
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('original_path', type=str, help='Path to the ground truth image')
    parser.add_argument('synthesized_path', type=str, help='Path to the synthesized image')

    args = parser.parse_args()
    original_path = args.original_path.rstrip("/")
    synthesized_path = args.synthesized_path.rstrip("/")

    run(original_path, synthesized_path)


if __name__ == "__main__":
    main()