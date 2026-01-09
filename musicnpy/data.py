class PMod:
    """
    A list of possibile pitch models available.

    :Example:
    >>> s = Scale.new(PMode.maj, 60)
    >>> Scale = [60, 62, 64, 65, 67, 69, 71]
    """

    maj = {
        "intervals": [0, 2, 4, 5, 7, 9, 11],
        "scale_harmo": ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim'],
        "chord": [0, 4, 7]
    }

    minNat = {
        "intervals": [0, 2, 4, 5, 7, 9, 11],
        "scale_harmo": ['maj', 'min', 'min', 'maj', 'maj', 'min', 'dim'],
        "chord": [0, 3, 7]
    }