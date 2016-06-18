from PlagCheck.util.settings import PlagCheckSettings


class PlagCheckRouter(object):

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'PlagCheck':
            return PlagCheckSettings.database
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'PlagCheck':
            return PlagCheckSettings.database
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'PlagCheck' and obj2._meta.app_label == 'PlagCheck':
            return True
        elif 'PlagCheck' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, model):
        """
        Make sure only plagcheck migrations get applied on the plagcheck db
        and just there.
        """
        if db == PlagCheckSettings.database:
            if model._meta.app_label == 'PlagCheck':
                return True
            else:
                return False
        elif model._meta.app_label == 'PlagCheck':
            return False
        return None