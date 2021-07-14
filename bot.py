import numpy as np
import pyautogui
import time
from PIL import ImageGrab, Image
import cv2 as cv


debug = True


class Bot:
    # flag
    prepare_flag = cv.imread("prepare.png")
    back_flag = cv.imread("back.png")
    alright_flag = cv.imread("alright.png")
    get_flag = cv.imread("get.png")
    retry_flag = cv.imread("retry.png")
    # screen
    screen = (982, 336, 1894, 829)
    # stage section
    #   before enter fight -> p_enter(25524)
    s_index = (1495, 733, 1639, 764)
    #   back flag -> p_fight(23726)
    s_enter_fight = (1004, 761, 1068, 820)
    #   alright -> pretry_deter_alr(33828)
    #   get -> pretry_deter_alr(33989)
    #   retry -> pretry_deter_alr(33600)
    s_retry_alri = (1374, 728, 1494, 788)
    s_get = (1381, 742, 1500, 800)
    # function point
    p_enter = (1594, 750)
    p_fight = (1427, 549)
    p_retry_alri_get = (1380, 750)

    def __init__(self):
        self.status = 'index'

    @staticmethod
    def get_cords():
        """used to get coordinate of the necessary button
        """
        print(pyautogui.position())

    @staticmethod
    def function_grab(section: tuple):
        """used to grab function button

        Args:
            section(tuple): input the test section
        Returns:
            gray(int): the gray image's sum of color

        """
        # image = ImageGrab.grab(section)
        # image.save("get.png", "PNG")
        image = np.array(ImageGrab.grab(section))
        return image

    @staticmethod
    def compare_img_hist(img1, img2):
        """
        Compare the similarity of two pictures using histogram(直方图)
            Attention: this is a comparision of similarity, using histogram to calculate
    ​
            For example:
             1. img1 and img2 are both 720P .PNG file,
                and if compare with img1, img2 only add a black dot(about 9*9px),
                the result will be 0.999999999953
    ​
        :param img1: img1 in MAT format(img1 = cv2.imread(image1))
        :param img2: img2 in MAT format(img2 = cv2.imread(image2))
        :return: the similarity of two pictures
        """
        # Get the histogram data of image 1, then using normalize the picture for better compare
        img1_hist = cv.calcHist([img1], [1], None, [256], [0, 256])
        img1_hist = cv.normalize(img1_hist, img1_hist, 0, 1, cv.NORM_MINMAX, -1)

        img2_hist = cv.calcHist([img2], [1], None, [256], [0, 256])
        img2_hist = cv.normalize(img2_hist, img2_hist, 0, 1, cv.NORM_MINMAX, -1)

        similarity = cv.compareHist(img1_hist, img2_hist, 0)

        return similarity

    def start(self):
        """start game
        """
        if self.status == 'index':

            # common
            if self.compare_img_hist(self.function_grab(self.s_index), self.prepare_flag) >= 0.9:
                self.status = 'ready'
                time.sleep(0.5)
                pyautogui.click(self.p_enter)

                # break
                while True:
                    if debug:
                        print("index: ", self.compare_img_hist(self.function_grab(self.s_enter_fight), self.back_flag))
                    if self.compare_img_hist(self.function_grab(self.s_enter_fight), self.back_flag) >= 0.9:
                        return
                    if self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) >= 0.9:
                        pyautogui.click(self.p_retry_alri_get)
                        self.status = 'index'
                        return
                    if self.compare_img_hist(self.function_grab(self.s_get), self.get_flag) >= 0.9:
                        pyautogui.click(self.p_retry_alri_get)

            # get money
            elif self.compare_img_hist(self.function_grab(self.s_get), self.get_flag) >= 0.9:
                pyautogui.click(self.p_retry_alri_get)

                # break
                while True:
                    if self.compare_img_hist(self.function_grab(self.s_index), self.prepare_flag) >= 0.9:
                        return

            # network offline
            elif self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) >= 0.9:
                pyautogui.click(self.p_retry_alri_get)
                return

        elif self.status == 'ready':

            # common
            if self.compare_img_hist(self.function_grab(self.s_enter_fight), self.back_flag) >= 0.9:
                self.status = 'fight'
                time.sleep(0.5)
                pyautogui.click(self.p_fight)

                # break
                while True:
                    if debug:
                        print("ready: ",
                              self.compare_img_hist(self.function_grab(self.s_retry_alri), self.alright_flag))
                    if self.compare_img_hist(self.function_grab(self.s_retry_alri), self.alright_flag) >= 0.9:
                        return
                    if self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) == 1:
                        pyautogui.click(self.p_retry_alri_get)

            # network offline
            elif self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) >= 0.9:
                pyautogui.click(self.p_retry_alri_get)
                return

        elif self.status == 'fight':

            # common
            if self.compare_img_hist(self.function_grab(self.s_retry_alri), self.alright_flag) >= 0.9:
                self.status = 'index'
                time.sleep(0.5)
                pyautogui.click(self.p_retry_alri_get)

                # break
                while True:
                    if debug:
                        print("fight", self.compare_img_hist(self.function_grab(self.s_index), self.prepare_flag))
                    if self.compare_img_hist(self.function_grab(self.s_index), self.prepare_flag) >= 0.9:
                        return
                    if self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) >= 0.9:
                        pyautogui.click(self.p_retry_alri_get)

            # network offline
            elif self.compare_img_hist(self.function_grab(self.s_retry_alri), self.retry_flag) == 1:
                pyautogui.click(self.p_retry_alri_get)
                return


if __name__ == "__main__":
    robot = Bot()
    while True:
        robot.start()
