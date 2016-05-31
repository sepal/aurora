from AuroraProject.settings import PLAGCHECK as plagcheck_settings


class PlagCheckRouter(object):

    def db_for_read(self, model, **hints):
        #print("read app: %s" % model._meta.app_label)
        if model._meta.app_label == 'PlagCheck':
            #print("select PLAGCHECK db")
            return plagcheck_settings['database']
        return None

    def db_for_write(self, model, **hints):
        #print("write app: %s" % model._meta.app_label)
        if model._meta.app_label == 'PlagCheck':
            #print("select PLAGCHECK db")
            return plagcheck_settings['database']
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
        if db == plagcheck_settings['database']:
            if model._meta.app_label == 'PlagCheck':
                #print("Select PLAGCHECK for migration")
                return True
            else:
                #print("Don't Select PLAGCHECK for migration")
                return False
        elif model._meta.app_label == 'PlagCheck':
            #print("2 Don't Select PLAGCHECK for migration")
            return False
        return None