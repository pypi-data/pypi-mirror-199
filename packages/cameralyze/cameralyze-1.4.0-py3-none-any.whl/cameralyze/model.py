import requests
import filetype

from typing import Union
from uuid import uuid4


class Connect:
    def __init__(self, api_key: str = None):
        self.model = None
        self.endpoint = None
        self.background_job = None
        self.flow = None
        self.beautify = False
        self.get_response = True
        self.base_domain = "https://api.server.cameralyze.co"
        self.test_temporary_image_domain = "https://tmp.cameralyze.co"
        self.upload_url = "https://platform.api.cameralyze.com/temporary-file/generate"
        self.api_key = api_key
        
    def beautify_response(self):
        self.beautify = True
        
        return self
        
    def open_response(self):
        self.get_response = True
        
        return self
        
    def close_response(self):
        self.get_response = False
        
        return self
        
    def set_api_key(self, api_key: str):
        self.api_key = api_key
        
        return self
        
    def set_model(self, model: str):
        """
        Args:
            model (str): Model UUID or model alias name
        """
        self.model = model
        
        return self
        
    def set_flow(self, flow: str):
        """
        Args:
            flow (str): Flow UUID or flow alias name
        """
        self.flow = flow
        
        return self
        
    def __get_presigned_upload_url(self, file_type: str) -> str:
        return requests.post(self.upload_url, json={"fileType": file_type, "fileName": str(uuid4())}).json()["data"]        

    def read_file(self, path: str) -> str:
        file_type = filetype.guess(path).mime
        file = "{file_name}.{file_extension}".format(file_name=str(uuid4()), file_extension=path.split(".")[-1])

        self.__upload_file(path=path, file_type=file_type)

        return "{test_temporary_image_domain}/{file}".format(
            test_temporary_image_domain=self.test_temporary_image_domain, 
            file=file
        )

    def __upload_file(self, path: str, file_type: str):
        with open(path, 'rb') as local_file:
            local_file_body = local_file.read()

        requests.put(
            self.__get_presigned_upload_url(file_type=file_type), 
            data=local_file_body, 
            headers={'Content-Type': file_type, 'x-amz-acl': 'public-read'}
        )

    def __get_json(self, image: Union[str, tuple]) -> dict:
        json={"apiKey": self.api_key, "rawResponse": not self.beautify, "getResponse": self.get_response}

        if isinstance(image, tuple):
            json["fileId"] = image[0]
            json["fileType"] = image[1]
        elif image.startswith("http"):
            json["url"] = image
        else:
            json["image"] = image
            
        if self.endpoint:
            json["applicationUuid"] = self.endpoint
        
        if self.background_job:
            json["applicationUuid"] = self.background_job
        
        return json
    
    def __get_path(self) -> str:
        if self.flow:
            return "flow"
        
        return "model"
    
    def __get_unique_id(self) -> str:
        if self.flow:
            return self.flow
        
        return self.model

    def predict(self, image: Union[str, tuple]) -> dict:
        api_call = requests.post(
            "{base_domain}/{path}/{unique_id}".format(base_domain=self.base_domain, path=self.__get_path(), unique_id=self.__get_unique_id()),
            json=self.__get_json(image=image)
        )

        return api_call.json() 
