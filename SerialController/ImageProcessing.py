#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import cv2
from numpy import ndarray, array, argmax
import os
from typing import List, Tuple, Optional
from logging import getLogger, DEBUG, NullHandler

from pokecontroller.core.image import (
    Image,
    ImageReadMode,
    ImageBinarizeHsvArgs,
    TemplateMatcherMode,
    TemplateMatcherGenerator,
    parse_crop,
)


def crop_image(image: ndarray, crop: List[int] = None) -> ndarray:
    """
    画像をトリミングする
    [y軸始点, y軸終点, x軸始点, x軸終点]
    """
    return crop_image_extend(image, crop_fmt=13, crop=crop)


def crop_image_extend(image: ndarray, crop_fmt: int | str = None, crop: List[int] = None) -> ndarray:
    """
    画像をトリミングする
    ・Pillow形式
    x軸(横軸),y軸(縦軸),画像の左上が原点
    crop_fmt=1: [x軸始点, y軸始点, x軸終点, y軸終点]
    crop_fmt=2: [x軸始点, y軸始点, トリミング後の画像のサイズ(横), トリミング後の画像のサイズ(縦)]
    crop_fmt=3: [x軸始点, x軸終点, y軸始点, y軸終点]
    crop_fmt=4: [x軸始点, トリミング後の画像のサイズ(横), y軸始点, トリミング後の画像のサイズ(縦)]
    ・opencv形式(y, xの順番)
    crop_fmt=11: [y軸始点, x軸始点, y軸終点, x軸終点]
    crop_fmt=12: [y軸始点, x軸始点, トリミング後の画像のサイズ(縦), トリミング後の画像のサイズ(横)]
    crop_fmt=13: [y軸始点, y軸終点, x軸始点, x軸終点]
    crop_fmt=14: [y軸始点, トリミング後の画像のサイズ(縦), x軸始点, トリミング後の画像のサイズ(横)]
    """

    fmt = int(crop_fmt) if crop_fmt is not None else None

    if fmt is None or crop is None:
        return image

    args = parse_crop(fmt, crop)
    try:
        return Image(image).crop(args).raw_value
    except:
        return image


def getInterframeDiff(frame1: ndarray, frame2: ndarray, frame3: ndarray, threshold: float) -> ndarray:
    """
    Get interframe difference binarized image
    フレーム間差分により2値化された画像を取得する
    """
    image1, image2, image3 = Image(frame1), Image(frame2), Image(frame3)
    return image1.binarize_by_interframe_diff(image2, image3, threshold).raw_value


def getImage(path: str, mode: str = "color"):
    """
    画像の読み込みを行う。
    """
    if not path:
        return None

    if mode == "binary":
        m = ImageReadMode.BINARY
    elif mode == "gray":
        m = ImageReadMode.GRAY
    else:  # mode == "color"
        m = ImageReadMode.COLOR

    try:
        return Image.read_from(path, m).raw_value
    except:
        print(f"{path}が開けませんでした。ファイル名およびファイルの格納場所を確認してください。")
        return None


def doPreprocessImage(
        image: ndarray,
        use_gray: bool = True,
        crop: List[int] = None,
        BGR_range: Optional[dict] = None,
        threshold_binary: Optional[int] = None,
) -> Tuple[ndarray, int, int]:
    """
    画像をトリミングしてグレースケール化/2値化する
    2値化関連のContributor: mikan kochan 空太 (敬称略)
    """
    src = crop_image(image, crop=crop)  # トリミング

    img = Image(src)
    if use_gray:
        img = img.to_grayscale()
    elif BGR_range is not None:  # 2値化
        args = ImageBinarizeHsvArgs(
            lower=array(BGR_range["lower"]),
            upper=array(BGR_range["upper"]),
        )
        img = img.binarize_by_hsv(args)
    if threshold_binary is not None:
        img = img.binarize_by_threshold(threshold_binary)

    return img.raw_value, img.width, img.height


def opneImage(image: ndarray, crop: List[int] = None, title="image"):
    """
    キー入力があるまで画像を表示する
    Contributor: kochan (敬称略)
    """
    src = crop_image(image, crop=crop)  # トリミング
    cv2.imshow(f"{title}", src)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class ImageProcessing:
    """
    画像に関する処理を行う。
    """

    __logger = None
    __activate_logger = False
    __gsrc = None
    __gtmpl = None
    __gresult = None
    __use_gpu = False
    image_type = ndarray

    def __init__(self, use_gpu: bool = False):
        # ロガーを起動する(1回だけ)
        if not self.__activate_logger:
            self.__logger = getLogger(__name__)
            self.__logger.addHandler(NullHandler())
            self.__logger.setLevel(DEBUG)
            self.__logger.propagate = True

        matcher_mode = TemplateMatcherMode.GPU if use_gpu else TemplateMatcherMode.CPU
        self.__matcher = TemplateMatcherGenerator.generate(preferred_mode=matcher_mode)
        if self.__matcher.mode == TemplateMatcherMode.GPU:
            print("template matching:mask is ignored.")
            self.__use_gpu = True
        else:
            self.__use_gpu = False

    def imwrite(self, filename: str, image: ndarray, params: int = None) -> bool:
        """
        画像を書き込む
        """
        try:
            return Image(raw_value=image).write_to(filename)
        except Exception as e:
            print(e)
            self.__logger.error(f"Image Write Error: {e}")
            return False

    def doTemplateMatch(
            self, image: ndarray, template_image: ndarray, mask_image: ndarray = None
    ) -> Tuple[float, tuple]:
        """
        テンプレートマッチングをする
        画像は必要に応じて事前にグレースケール化やトリミングをしておく必要がある
        """
        result = self.__matcher \
            .set_image(Image(image)) \
            .set_template(Image(template_image)) \
            .set_mask(Image(mask_image) if mask_image is not None else None) \
            .match()
        if result is None:
            return 0.0, (0.0, 0.0)
        else:
            return result.value, result.location

    def isContainTemplate(
            self,
            image: ndarray,
            template_image: ndarray,
            mask_image: ndarray = None,
            threshold: float = 0.7,
            use_gray: bool = True,
            crop: List[int] = None,
            BGR_range: Optional[dict] = None,
            threshold_binary: Optional[int] = None,
            crop_template: list[int] = None,
            show_image: bool = False,
    ) -> Tuple[bool, tuple, int, int, float]:
        """
        テンプレートマッチングを行い類似度が閾値を超えているかを確認する
        """
        # テンプレートマッチング対象画像を加工する
        src, _, _ = doPreprocessImage(
            image, use_gray=use_gray, crop=crop, BGR_range=BGR_range, threshold_binary=threshold_binary
        )

        # [DEBUG] テンプレートマッチング対象画像を表示する
        if show_image:
            cv2.imshow("image", src)
            cv2.waitKey()

        # テンプレート画像を加工する
        template, width, height = doPreprocessImage(
            template_image,
            use_gray=use_gray,
            crop=crop_template,
            BGR_range=BGR_range,
            threshold_binary=threshold_binary,
        )

        # テンプレートマッチングを行う
        max_val, max_loc = self.doTemplateMatch(src, template, mask_image=mask_image)

        # 類似度が閾値を超えたかを戻り値として返す(合わせて位置とテンプレート画像のサイズも返す)
        return max_val > threshold, max_loc, width, height, max_val

    def isContainTemplate_max(
            self,
            image: ndarray,
            template_image_list: List[ndarray],
            mask_image_list: List[ndarray] = [],
            threshold: float = 0.7,
            use_gray: bool = True,
            crop: List[int] = None,
            BGR_range: Optional[dict] = None,
            threshold_binary: Optional[int] = None,
            crop_template: list[int] = None,
            show_image: bool = False,
    ) -> Tuple[int, List[float], List[tuple], List[int], List[int], List[bool]]:
        """
        複数のテンプレート画像を用いてそれぞれテンプレートマッチングを行い類似度が最も大きい画像のindexを返す
        """
        # パラメータチェックを行う
        if len(template_image_list) == len(mask_image_list):
            mask_image_list_temp = mask_image_list
        if len(mask_image_list) == 0:
            mask_image_list_temp = [None for i in range(len(template_image_list))]
        else:
            print("The number of template images and mask images don't match. ")
            return -1, [], [], [], [], []

        # ループをまわしてテンプレート画像数分テンプレートマッチングを行う
        max_val_list = []
        max_loc_list = []
        width_list = []
        height_list = []
        judge_threshold_list = []

        # テンプレートマッチング対象画像を加工する
        src, _, _ = doPreprocessImage(
            image, use_gray=use_gray, crop=crop, BGR_range=BGR_range, threshold_binary=threshold_binary
        )

        # [DEBUG] テンプレートマッチング対象画像を表示する
        if show_image:
            cv2.imshow("image", src)
            cv2.waitKey()

        for template_image, mask_image in zip(template_image_list, mask_image_list_temp):
            # テンプレート画像を加工する
            template, width, height = doPreprocessImage(
                template_image,
                use_gray=use_gray,
                crop=crop_template,
                BGR_range=BGR_range,
                threshold_binary=threshold_binary,
            )
            max_val, max_loc = self.doTemplateMatch(src, template, mask_image=mask_image)
            max_val_list.append(max_val)
            max_loc_list.append(max_loc)
            width_list.append(width)
            height_list.append(height)
            judge_threshold_list.append(max_val > threshold)

        return argmax(max_val_list), max_val_list, max_loc_list, width_list, height_list, judge_threshold_list

    def saveImage(self, image: ndarray, filename: str = None, crop: List[int] = None):
        """
        画像を保存する。
        """
        cropped_image = crop_image(image, crop=crop)

        # ファイル名からパスを抽出する
        capture_dir = os.path.dirname(filename)

        # 画像保存用ディレクトリの存在を確認し、なかったら作成する。
        if not os.path.exists(capture_dir):
            os.makedirs(capture_dir)
            self.__logger.debug("Created Capture folder")

        # 画像を保存する
        try:
            Image(cropped_image).write_to(filename)
            self.__logger.debug(f"Capture succeeded: {filename}")
            print("capture succeeded: " + filename)
        except cv2.error as e:
            print("Capture Failed")
            self.__logger.error(f"Capture Failed :{e}")


# FIXME: delete or migrate to tests
if __name__ == "__main__":
    ImgProc = ImageProcessing()
    ImgProc.set_template_path("./")
    camera = cv2.VideoCapture(0)
    if camera.isOpened():
        _, image = camera.read()
        ret, _, _, _, _ = ImgProc.isContainTemplate(image, "test.png")
        print(ret)
        camera.release()
    else:
        pass
