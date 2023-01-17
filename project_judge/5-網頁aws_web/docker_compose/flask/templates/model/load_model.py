import pickle
from pathlib import Path

import numpy as np

directory = Path(__file__).resolve().parent


def pred_crime(F_01, F_02, F_03, F_04, F_06, F_07, F_08, F_11, F_13, F_14, crimePredCategory):

    input_List = [F_01, F_02, F_03, F_04, F_06, F_07,
                  F_08, F_11, F_13, F_14, crimePredCategory]
    np_List = np.array(input_List)
    data = np_List.reshape((1, -1))
    with open(directory/"crime_name.pickle", 'rb') as n:
        crimeModelName = pickle.load(n)
    crimeName = crimeModelName.predict(data)
    with open(directory/"crime_time.pickle", 'rb') as t:
        crimeModelTime = pickle.load(t)
    crimeTime = crimeModelTime.predict(data)

    return crimeName, crimeTime
