"""
Generic Views
"""
from flask.views import MethodView
from ms_utils import ViewGeneralMethods

ViewGeneralMethods.db = db
vmg = ViewGeneralMethods()


class GenericItemCrud(MethodView):
    """
    Generic Crud Class
    """
    init_every_request = False
    db = None
    model = None
    validator = None
    schema = None

    def __init__(self, db, model, validator, schema):
        self.db = db
        self.model = model
        self.validator = validator
        self.schema = schema
        ViewGeneralMethods.db = db

    vmg = ViewGeneralMethods()

    def get(self, object_id):
        """
        Component Type details
        :param object_id:
        :return:
        """
        return vmg.generic_details(self.model, self.schema, object_id)

    def patch(self, object_id):
        """
        Component Type update
        :param object_id:
        :return:
        """
        return vmg.generic_update_or_create(self.model, self.validator, object_id)

    def delete(self, object_id):
        """
        Component Type update
        :param object_id:
        :return:
        """
        return vmg.generic_delete(self.model, object_id)


class GenericGroupCrud(MethodView):
    """
    Generic Crud Class
    """
    init_every_request = False
    model = None
    validator = None
    schema = None

    def __init__(self, db, model, validator, schema):
        self.db = db
        self.model = model
        self.validator = validator
        self.schema = schema
        ViewGeneralMethods.db = db

    vmg = ViewGeneralMethods()

    # Component Type
    def get(self):
        """
        Component type list
        :return: jsonify
        """
        return vmg.generic_list(self.model, self.schema)

    def post(self):
        """
        Create component type
        :return: jsonfy
        """
        return vmg.generic_update_or_create(self.model, self.validator)


def register_api(app, model, name, validator, schema):
    """
    Register API method
    :param schema:
    :param validator:
    :param app:
    :param model:
    :param name:
    :return:
    """
    item = GenericItemCrud.as_view(f"{name}-item", model, validator, schema)
    group = GenericGroupCrud.as_view(f"{name}-group", model, validator, schema)
    app.add_url_rule(f"/{name}/<int:id>", view_func=item)
    app.add_url_rule(f"/{name}/", view_func=group)
