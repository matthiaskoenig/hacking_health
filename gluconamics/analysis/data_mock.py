"""
Module for generating mock data.
"""
import numpy as np

from collections import namedtuple

SampleData = namedtuple("SampleData", ["ins", "glc"])

M_NORMAL = 60
M_IGT = 25
M_T2DM = 10


def __factory_random(status, N):
    """ Creates random insulin and glucose data. """


    glc_normal = [4.2, 9.0]
    glc_igt = [3.8, 14.0]
    glc_t2dm = [3.3, 19.0]

    f_std = 0.3

    samples = []
    glc_rand = np.random.rand(N)

    for k in range(N):
        if status == "normal":
            glc_min, glc_max = glc_normal
            m = M_NORMAL
        elif status == "igt":
            glc_min, glc_max = glc_igt
            m = M_IGT
        elif status == "t2dm":
            glc_min, glc_max = glc_t2dm
            m = M_T2DM
        else:
            raise ValueError


        glc = glc_min + glc_rand[k] * (glc_max - glc_min)
        ins = m*glc + np.random.normal(loc=0, scale=f_std * m * glc)

        samples.append(
            SampleData(ins=ins, glc=glc)
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









