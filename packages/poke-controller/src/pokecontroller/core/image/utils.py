def parse_crop(fmt: int, crop: list[int]) -> tuple[int, int, int, int]:
    """
    fmt形式のcropを (x-start, y-start, width, height) に変換するユーティリティ関数.
    サポートされていないfmtの場合はcropをそのまま返す.

    - Pillow形式(x,yの順序)
    fmt=1: [x-start, y-start, x-end, y-end]
    fmt=2: [x-start, y-start, width, height]
    fmt=3: [x-start, x-end, y-start, y-end]
    fmt=4: [x-start, width, y-start, height]
    - opencv形式(y, xの順序)
    fmt=11: [y-start, x-start, y-end, x-end]
    fmt=12: [y-start, x-start, height, width]
    fmt=13: [y-start, y-end, x-start, x-end]
    fmt=14: [y-start, height, x-start, width]
    """
    if fmt < 10:  # pillow format
        if fmt == 1:  # [x-start, y-start, x-end, y-end]
            return (crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1])
        elif fmt == 2:  # [x-start, y-start, width, height]
            return (crop[0], crop[1], crop[2], crop[3])
        elif fmt == 3:  # [x-start, x-end, y-start, y-end]
            return (crop[0], crop[2], crop[1] - crop[0], crop[3] - crop[2])
        elif fmt == 4:  # fmt == 4 [x-start, width, y-start, height]
            return (crop[0], crop[2], crop[1], crop[3])
        else:
            return crop

    else:  # opencv format
        if fmt == 11:  # [y-start, x-start, y-end, x-end]
            return (crop[1], crop[0], crop[3] - crop[1], crop[2] - crop[0])
        elif fmt == 12:  # [y-start, x-start, height, width]
            return (crop[1], crop[0], crop[3], crop[2])
        elif fmt == 13:  # [y-start, y-end, x-start, x-end]
            return (crop[2], crop[0], crop[3] - crop[2], crop[1] - crop[0])
        elif fmt == 14:  # fmt == 14 [y-start, height, x-start, width]
            return (crop[2], crop[0], crop[3], crop[1])
        else:
            return crop
