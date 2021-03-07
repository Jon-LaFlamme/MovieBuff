

def new_title_validation(form: object) -> bool:
    id_ok = valid_id(form.get['id'])
    title_ok = valid_title(form.get['title'])
    return id_ok and title_ok


def valid_id(id: str) -> bool:
    return id[:2] == 'tt'


def valid_title(title: str) -> bool:
    if title[0] == '\'' or title[-1] == '\'':
        return False
    elif '\\' in title:
        return False
    else: return True


