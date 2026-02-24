class ChordModel:
    """
    Database of chords intervals (semitones from root)

    :Example:

    >>> print(ChordModel.maj)
    >>> [0, 4, 7]
    """

    maj = [0, 4, 7]           
    min = [0, 3, 7]           
    dim = [0, 3, 6]           
    aug = [0, 4, 8]           
    sus2 = [0, 2, 7]          
    sus4 = [0, 5, 7]          

    maj7 = [0, 4, 7, 11]     
    min7 = [0, 3, 7, 10]     
    dom7 = [0, 4, 7, 10]     
    dim7 = [0, 3, 6, 9]      
    half_dim7 = [0, 3, 6, 10]
    aug_maj7 = [0, 4, 8, 11] 
    aug7 = [0, 4, 8, 10]     
    min_maj7 = [0, 3, 7, 11] 

    maj9 = [0, 4, 7, 11, 14]  
    min9 = [0, 3, 7, 10, 14]  
    dom9 = [0, 4, 7, 10, 14]  
    dom_b9 = [0, 4, 7, 10, 13] 

    maj6 = [0, 4, 7, 9]
    min6 = [0, 3, 7, 9]

    neapolitan = [0, 4, 8]

    italian_aug6 = [0, 4, 10]
    french_aug6 = [0, 4, 6, 10]
    german_aug6 = [0, 4, 7, 10]

    tristan = [0, 3, 6, 10] 
    prometheus = [0, 6, 10, 16, 21]

    quartal = [0, 5, 10, 15]
    quintal = [0, 7, 14, 21]

class ScaleModel:
    """
    Database of scales with intervals and diatonic harmonization.

    :Example:

    >>> print(ScaleModel.maj["intervals"])
    >>> [0, 2, 4, 5, 7, 9, 11]
    >>> print(ScaleModel.maj["harmo"])
    >>> [ChordModel.maj, ChordModel.min, ...]
    """

    # --- Scale diatoniche ---

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

    minHarm = {
        "intervals": [0, 2, 3, 5, 7, 8, 11],  
        "harmo": [
            ChordModel.min,
            ChordModel.dim,
            ChordModel.aug,
            ChordModel.min,
            ChordModel.maj,   
            ChordModel.maj,
            ChordModel.dim7
        ]
    }

    minMel = {
        "intervals": [0, 2, 3, 5, 7, 9, 11], 
        "harmo": [
            ChordModel.min_maj7,
            ChordModel.min7,
            ChordModel.aug_maj7,
            ChordModel.dom7,
            ChordModel.dom7,
            ChordModel.half_dim7,
            ChordModel.half_dim7
        ]
    }

    # --- Scale pentatoniche ---

    pentaMaj = {
        "intervals": [0, 2, 4, 7, 9],        
        "harmo": [
            ChordModel.maj,
            ChordModel.min,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.min
        ]
    }

    pentaMin = {
        "intervals": [0, 3, 5, 7, 10],       
        "harmo": [
            ChordModel.min,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.min,
            ChordModel.maj
        ]
    }

    # --- Scale simmetriche ---

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

    dimHalfWhole = {
        "intervals": [0, 1, 3, 4, 6, 7, 9, 10], 
        "harmo": [
            ChordModel.dim7,
            ChordModel.dom7,
            ChordModel.dim7,
            ChordModel.dom7,
            ChordModel.dim7,
            ChordModel.dom7,
            ChordModel.dim7,
            ChordModel.dom7
        ]
    }

    dimWholeHalf = {
        "intervals": [0, 2, 3, 5, 6, 8, 9, 11], 
        "harmo": [
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7,
            ChordModel.dim7
        ]
    }

    # --- Scale jazz ---

    blues = {
        "intervals": [0, 3, 5, 6, 7, 10],      
        "harmo": [
            ChordModel.dom7,
            ChordModel.min7,
            ChordModel.half_dim7,
            ChordModel.aug,
            ChordModel.dom7,
            ChordModel.dom7
        ]
    }

    bebop = {
        "intervals": [0, 2, 4, 5, 7, 9, 10, 11], 
        "harmo": [
            ChordModel.maj7,
            ChordModel.min7,
            ChordModel.min7,
            ChordModel.maj7,
            ChordModel.dom7,
            ChordModel.min7,
            ChordModel.half_dim7,
            ChordModel.dom7
        ]
    }

    # --- Scale esotiche / cromatiche ---

    chromatic = {
        "intervals": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        "harmo": [
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.maj
        ]
    }

    prometheus = {
        "intervals": [0, 2, 4, 6, 9, 10],     
        "harmo": [
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.dom7
        ]
    }

    altered = {
        "intervals": [0, 1, 3, 4, 6, 8, 10],   
        "harmo": [
            ChordModel.dom7,
            ChordModel.aug,
            ChordModel.aug,
            ChordModel.aug_maj7,
            ChordModel.half_dim7,
            ChordModel.min7,
            ChordModel.dom7
        ]
    }

    lydianDom = {
        "intervals": [0, 2, 4, 6, 7, 9, 10],   
        "harmo": [
            ChordModel.dom7,
            ChordModel.dom7,
            ChordModel.half_dim7,
            ChordModel.aug,
            ChordModel.min7,
            ChordModel.min7,
            ChordModel.maj
        ]
    }

    harmonicMaj = {
        "intervals": [0, 2, 4, 5, 7, 8, 11],   
        "harmo": [
            ChordModel.maj7,
            ChordModel.min7,
            ChordModel.min7,
            ChordModel.maj7,
            ChordModel.dom7,
            ChordModel.aug_maj7,
            ChordModel.dim7
        ]
    }

    # --- Scale etniche ---

    hijaz = {
        "intervals": [0, 1, 4, 5, 7, 8, 10],   
        "harmo": [
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.min
        ]
    }

    hijazKar = {
        "intervals": [0, 1, 4, 5, 7, 8, 11],   
        "harmo": [
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.maj
        ]
    }

    nahawand = {
        "intervals": [0, 2, 3, 5, 7, 8, 11],   
        "harmo": [
            ChordModel.min,
            ChordModel.dim,
            ChordModel.aug,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.dim7
        ]
    }

    rast = {
        "intervals": [0, 2, 3, 5, 7, 9, 10],   
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

    bayati = {
        "intervals": [0, 1, 3, 5, 7, 8, 10],   
        "harmo": [
            ChordModel.min,
            ChordModel.aug,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.dim
        ]
    }

    # --- Scala ungherese ---

    hungarianMin = {
        "intervals": [0, 2, 3, 6, 7, 8, 11],   
        "harmo": [
            ChordModel.min,
            ChordModel.aug,
            ChordModel.maj,
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.maj,
            ChordModel.dim
        ]
    }

    hungarianMaj = {
        "intervals": [0, 3, 4, 6, 7, 9, 10],   
        "harmo": [
            ChordModel.aug,
            ChordModel.dom7,
            ChordModel.min,
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.aug
        ]
    }

    # --- Scale spagnole ---

    phrygianDom = {
        "intervals": [0, 1, 4, 5, 7, 8, 10],   
        "harmo": [
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.min,
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.min
        ]
    }

    spanishOctatonic = {
        "intervals": [0, 1, 3, 4, 5, 7, 8, 10],
        "harmo": [
            ChordModel.min,
            ChordModel.aug,
            ChordModel.dom7,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.dim
        ]
    }

    # --- Scale giapponesi ---

    hirajoshi = {
        "intervals": [0, 2, 3, 7, 8],          
        "harmo": [
            ChordModel.min,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.min,
            ChordModel.maj
        ]
    }

    insen = {
        "intervals": [0, 1, 5, 7, 10],         
        "harmo": [
            ChordModel.min,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.dom7,
            ChordModel.maj
        ]
    }

    iwato = {
        "intervals": [0, 1, 5, 6, 10],         
        "harmo": [
            ChordModel.dim,
            ChordModel.maj,
            ChordModel.dim,
            ChordModel.aug,
            ChordModel.half_dim7
        ]
    }

    yo = {
        "intervals": [0, 2, 5, 7, 9],          
        "harmo": [
            ChordModel.sus2,
            ChordModel.maj,
            ChordModel.sus4,
            ChordModel.maj,
            ChordModel.min
        ]
    }

    # --- Scale indiane (thaat) ---

    bhairav = {
        "intervals": [0, 1, 4, 5, 7, 8, 11],   
        "harmo": [
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.min,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.maj
        ]
    }

    kafi = {
        "intervals": [0, 2, 3, 5, 7, 9, 10],   
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

    kalyan = {
        "intervals": [0, 2, 4, 6, 7, 9, 11],  
        "harmo": [
            ChordModel.maj,
            ChordModel.min,
            ChordModel.min,
            ChordModel.aug,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.dim
        ]
    }

    todi = {
        "intervals": [0, 1, 3, 6, 7, 8, 11],  
        "harmo": [
            ChordModel.dim,
            ChordModel.aug,
            ChordModel.dim,
            ChordModel.aug,
            ChordModel.maj,
            ChordModel.aug,
            ChordModel.maj
        ]
    }

    # --- Scale africane / pentatoniche regionali ---

    slendro = {
        "intervals": [0, 2, 5, 7, 10],          
        "harmo": [
            ChordModel.sus2,
            ChordModel.sus4,
            ChordModel.min,
            ChordModel.sus4,
            ChordModel.sus2
        ]
    }

    pelog = {
        "intervals": [0, 1, 3, 7, 8],           
        "harmo": [
            ChordModel.min,
            ChordModel.aug,
            ChordModel.maj,
            ChordModel.min,
            ChordModel.dim
        ]
    }