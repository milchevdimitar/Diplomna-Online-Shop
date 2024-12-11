from models import db, User
from sqlalchemy.exc import IntegrityError

def validate_user_data(username, email, rank=None):
    """
    Проверява дали въведените данни за потребителя са валидни.
    """
    errors = []

    if not username or len(username) < 3:
        errors.append("Потребителското име трябва да съдържа поне 3 символа.")

    if not email or "@" not in email:
        errors.append("Невалиден имейл адрес.")

    if rank is not None and (not isinstance(rank, int) or rank < 0):
        errors.append("Рангът трябва да бъде цяло число, по-голямо или равно на 0.")

    return errors

def create_user(username, email, rank=0):
    """
    Създава нов потребител в базата данни.
    """
    errors = validate_user_data(username, email, rank)
    if errors:
        return {"success": False, "errors": errors}

    new_user = User(username=username, email=email, rank=rank)
    try:
        db.session.add(new_user)
        db.session.commit()
        return {"success": True, "user": new_user}
    except IntegrityError:
        db.session.rollback()
        return {"success": False, "errors": ["Имейлът вече съществува."]}

def delete_user(user_id):
    """
    Изтрива потребител от базата данни по ID.
    """
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "error": "Потребителят не е намерен."}

    try:
        db.session.delete(user)
        db.session.commit()
        return {"success": True}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}

def update_user(user_id, username=None, email=None, rank=None):
    """
    Актуализира данните на съществуващ потребител.
    """
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "error": "Потребителят не е намерен."}

    if username:
        user.username = username

    if email:
        user.email = email

    if rank is not None:
        user.rank = rank

    errors = validate_user_data(user.username, user.email, user.rank)
    if errors:
        return {"success": False, "errors": errors}

    try:
        db.session.commit()
        return {"success": True, "user": user}
    except IntegrityError:
        db.session.rollback()
        return {"success": False, "errors": ["Имейлът вече съществува."]}
    except Exception as e:
        db.session.rollback()
        return {"success": False, "error": str(e)}

def get_user_by_id(user_id):
    """
    Извлича потребител по ID.
    """
    user = User.query.get(user_id)
    if not user:
        return {"success": False, "error": "Потребителят не е намерен."}

    return {"success": True, "user": user}
