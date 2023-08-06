import numpy as np

def spectral_skewness(x: np.ndarray):
    """
    Calculate the spectral skewness of a audio signal.
    """
    # Calculate the power spectrum
    x = x.astype(float)
    spectrum = np.abs(np.fft.fft(x))**2
    # Sum across all frequency bins
    mean = np.mean(spectrum)
    std = np.std(spectrum)
    skew = np.mean(np.power(spectrum - mean, 3)) / (std ** 3)
    return skew

def spectral_kurtosis(x: np.ndarray):
    """
    Calculate the spectral skewness of a audio signal.
    """
    x = x.astype(float)
    # Calculate the power spectrum
    spectrum = np.abs(np.fft.fft(x))**2
    # Sum across all frequency bins
    mean = np.mean(spectrum)
    std = np.std(spectrum)
    kurtosis = np.mean(np.power(spectrum - mean, 4)) / (std ** 4)
    return kurtosis

def loudness(x: np.ndarray) -> float:
    """Caclulate the loudness of a audio signal.

    Args:
        x (np.ndarray): Input signal.

    Returns:
        float: Loudness
    """
    rms = np.sqrt(np.mean(x**2))
    loudness = 20 * np.log10(rms) # to db
    return  loudness

def vtlp(x: np.ndarray, sr: int):
    """Calculate the VTLP transform of an audio signal.

    Args:
        x (np.ndarray): Input signal.

    Returns:
        float: vtlp(np.ndarray): VTLP transform of the input signal.
    """
    
    aug = naa.VtlpAug(sampling_rate=sr)
    augmented_data = np.asarray(aug.augment(x))
    
    augmented_data = augmented_data.flatten()
    
    return augmented_data


def pitch(x: np.ndarray, sr: int,factor: tuple):
    """Calculate the pitch transform of an audio signal.

    Args:
        x (np.ndarray): Input signal.
        sr (int): Sampling rate.
        factor (tuple): Factor range.

    Returns:
        float: pitch(np.ndarray): pitch transform of the input signal.
    """
    
    factor = tuple(factor)
    aug = naa.PitchAug(sampling_rate=sr, factor=factor)
    augmented_data = np.asarray(aug.augment(x))
    
     
    return augmented_data

def rollAudio(x: np.ndarray):
    """
    Roll audio by a random amount.
    
    Args:
        x(np.ndarray): Input signal.
        
    Returns:
        np.ndarray: rolled_audio: rolled audio signal.
    """
    # expect audio to be 1 dimensional
    pivot = np.random.randint(x.shape[0])
    rolled_audio = np.roll(x, pivot, axis=0)
    assert x.shape[0] == rolled_audio.shape[0], "Roll audio shape mismatch"
    
    return rolled_audio