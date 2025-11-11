CURRENT_CASE_ID = None

def set_current_case(case_id):
    global CURRENT_CASE_ID
    CURRENT_CASE_ID = case_id

def get_current_case():
    return CURRENT_CASE_ID