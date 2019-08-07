# from . import db, models
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class SecureAdminView(ModelView):
    """
    This class inherits Flask-Admin's default ModelView, in order to override the
    method determining whether an admin view is accessible to the logged-in user.
    """

    def is_accessible(self):
        """
        Allow access to this view only for users with the role "Admin".
        """
        return current_user.has_role('Admin')
