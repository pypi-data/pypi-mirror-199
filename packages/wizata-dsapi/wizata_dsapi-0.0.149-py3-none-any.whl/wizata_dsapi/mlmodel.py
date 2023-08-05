import json
import uuid
from flask import jsonify
from .api_dto import ApiDto


class MLModel(ApiDto):

    def __init__(self, model_id=None):
        if model_id is None:
            model_id = uuid.uuid4()
        self.model_id = model_id

        self.generatedById = None
        self.status = 'draft'
        self.needExactColumnNumbers = True
        self.needExactColumnNames = True
        self.input_columns = []
        self.output_columns = []
        self.has_anomalies = False
        self.label_counts = 0
        self.has_target_feat = False

        self.trained_model = None
        self.scaler = None

    def api_id(self) -> str:
        return str(self.model_id).upper()

    def endpoint(self) -> str:
        return "MLModels"

    def to_json(self):
        obj = {"id": str(self.model_id),
               "status": str(self.status),
               "needExactColumnNames": str(self.needExactColumnNames),
               "needExactColumnNumbers": str(self.needExactColumnNumbers),
               "hasAnomalies": str(self.has_anomalies),
               "hasTargetFeat": str(self.has_target_feat),
               "labelCount": str(self.label_counts)
               }
        if self.generatedById is not None:
            obj["generatedById"] = str(self.generatedById)
        if self.input_columns is not None:
            obj["inputColumns"] = json.dumps(list(self.input_columns))
        if self.output_columns is not None:
            obj["outputColumns"] = json.dumps(list(self.output_columns))
        return obj

    def from_json(self, obj):
        if "id" in obj.keys():
            self.model_id = obj["id"]
        if "status" in obj.keys():
            self.status = str(obj["status"]).lower()
        if "inputColumns" in obj.keys():
            self.input_columns = json.loads(obj["inputColumns"])
        if "outputColumns" in obj.keys():
            self.output_columns = json.loads(obj["outputColumns"])
        if "labelCount" in obj.keys():
            self.label_counts = int(obj["labelCount"])
        if "hasAnomalies" in obj.keys():
            self.has_anomalies = bool(obj["hasAnomalies"])
        if "hasTargetFeat" in obj.keys():
            self.has_target_feat = bool(obj["hasTargetFeat"])
        if "needExactColumnNumbers" in obj.keys():
            self.needExactColumnNumbers = bool(obj["needExactColumnNumbers"])
        if "needExactColumnNames" in obj.keys():
            self.needExactColumnNames = bool(obj["needExactColumnNames"])

    def get_sample_payload(self):
        pl_columns = {"timestamp": "[timestamp]"}
        for hardwareId in self.input_columns:
            pl_columns[hardwareId] = "[" + hardwareId + "]"
        pl_json = {
            "id": str(self.model_id),
            "dataset": pl_columns
        }
        return pl_json

