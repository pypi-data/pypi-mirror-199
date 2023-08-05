import uuid
import pandas
from .api_dto import ApiDto


class DSDataFrame(ApiDto):
    """
    A DS Dataframe is a definition of a pandas Dataframe that can be stored and shared on Wizata.
    """

    def __init__(self, df_id=None):
        if df_id is None:
            self.df_id = uuid.uuid4()
        else:
            self.df_id = df_id
        self.generatedById = None
        self.dataframe = None

    def api_id(self) -> str:
        return str(self.df_id).upper()

    def endpoint(self) -> str:
        return "Dataframes"

    def from_json(self, obj):
        if "id" in obj.keys():
            self.df_id = uuid.UUID(obj["id"])
        if "generatedById" in obj.keys():
            self.generatedById = obj["generatedById"]

    def to_json(self):
        obj = {
            "id": str(self.df_id)
        }
        if self.generatedById is not None:
            obj["generatedById"] = str(self.generatedById)
        return obj

