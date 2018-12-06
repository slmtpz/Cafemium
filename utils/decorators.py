from functools import wraps
from flask import redirect, flash
from flask_login import current_user
from constants import roles


def limit_to_role(role):
    def decorator(fnc):
        @wraps(fnc)
        def role_check_fnc(*args, **kwargs):
            current_role_power = current_user.type
            required_role_power = roles[role]
            if current_role_power >= required_role_power:
                return fnc(*args, **kwargs)
            else:
                flash('Sayfaya erişim yetkiniz yok.')
                return redirect('user')
        return role_check_fnc
    return decorator
