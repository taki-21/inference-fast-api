from datetime import datetime
import uuid


class ObjectKey():
    @classmethod
    def make_object_key(cls, extension: str, file_name: str = None) -> str:
        if file_name is None:
            file_name_key = str(uuid.uuid4())
        else:
            file_name_key = file_name

        today = datetime.now()
        return f'{today.strftime("%Y/%m/%d")}/{file_name_key}.{extension}'
