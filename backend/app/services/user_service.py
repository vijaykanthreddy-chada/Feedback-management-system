from app.models.user import User


def get_users_by_role(role=None):
    query = User.query

    if role:
        query = query.filter_by(role=role)

    users = query.all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role.value
        })

    return result