import json
import uuid
import dill
import types
from .api_dto import ApiDto


class Script(ApiDto):

    def __init__(self, script_id=None):

        # Id
        if script_id is None:
            script_id = uuid.uuid4()
        self.script_id = script_id

        # Properties
        self.name = None
        self.description = None
        self.canGeneratePlot = False
        self.canGenerateModel = False
        self.canGenerateData = False
        self.status = "draft"
        self.needExactColumnNumbers = False
        self.needExactColumnNames = False
        self.inputColumns = []
        self.outputColumns = []

        # Function properties (code)
        self.function = None

    def api_id(self) -> str:
        return str(self.script_id).upper()

    def endpoint(self) -> str:
        return "Scripts"

    def to_json(self):
        obj = {
            "id": str(self.script_id),
            "name": str(self.name),
            "description": str(self.description),
            "canGeneratePlot": str(self.canGeneratePlot),
            "canGenerateModel": str(self.canGenerateModel),
            "canGenerateData": str(self.canGenerateData),
            "status": str(self.status),
            "needExactColumnNumbers": str(self.needExactColumnNumbers),
            "needExactColumnNames": str(self.needExactColumnNames),
            "inputColumns": json.dumps(list(self.inputColumns)),
            "outputColumns": json.dumps(list(self.outputColumns))
        }
        return obj

    def from_json(self, obj):
        if "id" in obj.keys():
            self.script_id = uuid.UUID(obj["id"])
        if "name" in obj.keys():
            self.name = obj["name"]
        if "description" in obj.keys():
            if obj["description"] != "None":
                self.description = obj["description"]
        if "canGeneratePlot" in obj.keys():
            self.canGeneratePlot = bool(obj["canGeneratePlot"])
        if "canGenerateModel" in obj.keys():
            self.canGenerateModel = bool(obj["canGenerateModel"])
        if "canGenerateData" in obj.keys():
            self.canGenerateData = bool(obj["canGenerateData"])
        if "status" in obj.keys():
            self.status = str(obj["status"]).lower()
        if "needExactColumnNumbers" in obj.keys():
            self.needExactColumnNumbers = bool(obj["needExactColumnNumbers"])
        if "needExactColumnNames" in obj.keys():
            self.needExactColumnNames = bool(obj["needExactColumnNames"])
        if "inputColumns" in obj.keys():
            self.inputColumns = json.loads(obj["inputColumns"])
        if "outputColumns" in obj.keys():
            self.outputColumns = json.loads(obj["outputColumns"])

    def copy(self, myfunction):
        self.function = Function()
        self.function.code = myfunction.__code__

        f_globals = myfunction.__globals__
        self.function.globals = []
        for k_global in f_globals:
            if isinstance(myfunction.__globals__[k_global], types.ModuleType):
                module = f_globals[k_global]
                self.function.globals.append({
                    "var": k_global,
                    "module": str(module.__name__)
                })


class Function:

    def __init__(self):
        self.code = None
        self.globals = None
