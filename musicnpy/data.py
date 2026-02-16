class ChordModel:
    """
    Database di accordi disponibili
    """
    maj = [0, 4, 7]
    min = [0, 3, 7]
    dim = [0, 3, 6]
    dim7 = [0, 3, 6, 11]
    aug = [0, 4, 8]


class ScaleModel:
    """
    A list of possibile pitch models available.

    :Example:
    >>> s = Scale.new(ScaleModel.maj, 60)
    >>> Scale = [60, 62, 64, 65, 67, 69, 71]
    """

    maj = {
        "intervals": [0, 2, 4, 5, 7, 9, 11],
        "harmo": [
            ChordModel.maj, 
            ChordModel.min, 
            ChordModel.min, 
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.dim
        ]
    }

    minNat = {
        "intervals": [0, 2, 3, 5, 7, 8, 10],
        "harmo": [
            ChordModel.min,
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.maj
        ]
    }

    esaton = {
        "intervals": [0, 2, 4, 6, 8, 10],
        "harmo": [
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.aug
        ]
    }

#TODO pattern ritmici noti