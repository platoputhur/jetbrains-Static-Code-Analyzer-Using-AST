import copy


def my_copy(obj, copy_mode):
    return copy.deepcopy(obj) if copy_mode == "deep copy" else obj.copy()
