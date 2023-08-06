from .load_setting import load_setting


def get_code_import(id):
    SETTING = load_setting()
    base_path = SETTING['base_path'].strip(".").strip("/")
    sec_path = f'repo_{id}'
    return f"from {base_path}.{sec_path}.mycode import MyCode"


