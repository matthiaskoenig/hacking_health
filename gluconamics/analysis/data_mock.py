"""
Module for generating mock data.
"""
import numpy as np

from collections import namedtuple

SampleData = namedtuple("SampleData", ["ins", "glc"])


def __factory_random(status, N):
    """ Creates random insulin and glucose data. """
    samples = []
    glc = np.random.rand(N)
    ins = np.random.rand(N)
    for k in range(N):
        samples.append(
            SampleData(ins=ins[k], glc=glc[k])
        )
    return samples


def create_samples(status, N, factory=__factory_random):
    """

    :param username:
    :param status: glucose status
    :param N: number of samples
    :param factory: factory to create random data
    :return:
    """

    if status not in  ["normal", "igt", "t2dm"]:
        raise ValueError("value not supported")

    samples = factory(status=status, N=N)
    return samples









