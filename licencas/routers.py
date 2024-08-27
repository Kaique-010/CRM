class LicencaRouter:
    def db_for_read(self, model, **hints):
        """Direciona operações de leitura para o banco de dados apropriado."""
        if model._meta.app_label == 'app_cliente_1':
            return 'save_cliente_1'
        return None

    def db_for_write(self, model, **hints):
        """Direciona operações de escrita para o banco de dados apropriado."""
        if model._meta.app_label == 'app_cliente_1':
            return 'save_cliente_1'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Permite relações entre modelos que estão no mesmo banco de dados."""
        if obj1._state.db == 'save_cliente_1' and obj2._state.db == 'save_cliente_1':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Permite ou impede a migração de modelos para bancos de dados específicos."""
        if app_label == 'app_cliente_1':
            return db == 'save_cliente_1'
        return None