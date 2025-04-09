from rolepermissions.roles import AbstractUserRole

class Admin(AbstractUserRole):
    available_permissions = {
        "view_users": True,
        "add_user": True,
        "edit_user": True,
        "delete_user": True,
    }

class Staff(AbstractUserRole):
    available_permissions = {
        "view_users": True,
    }
