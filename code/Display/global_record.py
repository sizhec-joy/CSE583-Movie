# global_record.py
initial_movie_id_list = [11860,31357,862,9091,63,139405,35196,78406,47939,174271,5,6,11,12,13,14,15,16,18,19,20,21,22]
_curr_movie_id_list = []
_total_list_shown = 0


def set_curr_movie_id_list(list_next_movie_id):
    global _curr_movie_id_list
    _curr_movie_id_list = list_next_movie_id


def get_curr_movie_id_list():
    return _curr_movie_id_list


def add_total_list_shown():
    global _total_list_shown
    _total_list_shown = _total_list_shown + 1


def set_total_list_shown(num):
    global _total_list_shown
    _total_list_shown = num


def get_total_list_shown():
    return _total_list_shown
