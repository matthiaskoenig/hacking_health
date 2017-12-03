"""
Module for generating mock data.
"""
import numpy as np

from collections import namedtuple

SampleData = namedtuple("SampleData", ["ins", "glc"])


def __factory_random(status, N):
    """ Creates random insulin and glucose data. """

    m_normal = 1200.0/20.0
    m_igt = 500/20
    m_t2dm = 200.0/20.0

    glc_normal = [4.2, 9.0]
    glc_igt = [3.8, 14.0]
    glc_t2dm = [3.3, 19.0]


    f_std = 0.1

    samples = []
    glc_rand = np.random.rand(N)

    for k in range(N):
        if status == "normal":
            glc_min, glc_max = glc_normal
            m = m_normal
        elif status == "igt":
            glc_min, glc_max = glc_igt
            m = m_igt
        elif status == "t2dm":
            glc_min, glc_max = glc_t2dm
            m = m_t2dm
        else:
            raise ValueError


        glc = glc_min + glc_rand[k] * (glc_max - glc_min)
        ins = m_normal * glc + np.random.normal(loc=0, scale=f_std * m * glc)

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









