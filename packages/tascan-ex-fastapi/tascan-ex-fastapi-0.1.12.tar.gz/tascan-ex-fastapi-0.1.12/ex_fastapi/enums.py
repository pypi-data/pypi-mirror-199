from enum import Enum


class TempCodeTypes(Enum):
    EmailActivation = 'EA'
    PwdReset = 'PR'
    PwdChange = 'PC'
