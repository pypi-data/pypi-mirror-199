
import matplotlib.pyplot as plt
import numpy as np


def variance(data: np.ndarray, is_sample=True):
    var = np.mean(data ** 2) / (len(data) - is_sample)
    return var


def sd(data, is_sample=True):
    return np.sqrt(variance(data, is_sample=is_sample))


def pdf(x, sd, mu):
    """Probability Density Function. Can be used to create a normal distribution"""
    out = 1 / (sd * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((x - mu) / sd) ** 2)
    return out


def mean_squared_error_3d(y_obs: np.ndarray, y_pred: np.ndarray, axis=0) -> np.ndarray:
    """
    Takes the MSE from a two 3D-arrays along an axis (defaul axis=0)
    From: https://stackoverflow.com/a/66236930 """
    assert np.all(np.array([y_obs.ndim, y_pred.ndim]) == 3)  # Make sure both a 3D arrays
    mse = ((y_obs - y_pred) ** 2).mean(axis=axis)
    return mse


if __name__ == "__main__":
    d = np.array([1, 2, 4, 4, 5, 7])
    print(f"{sd(d, is_sample=False)=}")
    print(f"{sd(d, is_sample=True)=}")
    x_hr = np.linspace(start=0, stop=20, num=201)
    pdf_pred = pdf(x_hr, 2, 5)

    plt.plot(x_hr, pdf_pred)
    plt.show()
