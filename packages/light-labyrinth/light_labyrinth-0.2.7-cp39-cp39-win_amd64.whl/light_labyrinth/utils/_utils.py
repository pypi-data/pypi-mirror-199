from .._light_labyrinth_c._light_labyrinth_c import _libwrapper

class LightLabyrinthLearningHistory:
    def __init__(self, accs_train, errs_train, accs_val=None, errs_val=None, calculated=None):
        self.accs_train = accs_train
        self.accs_val = accs_val
        self.errs_train = errs_train
        self.errs_val = errs_val
        if calculated is not None:
            self.calculated = calculated

def set_random_state(state):
    _libwrapper._set_random_state(state)