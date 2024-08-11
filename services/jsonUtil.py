from pathlib import Path
import json

class JsonUtil:
    @staticmethod
    def saveModelToJsonFile(model, folderPath, fileName):
        modelJson = model.model_dump_json()
        
        folderPath = Path(folderPath)
        filePath = folderPath/fileName
        if not filePath.exists() or  filePath.stat().st_size == 0:
            data = []
        else:
            with open(filePath, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        data.append(json.loads(modelJson))
        
        with open(filePath, 'w') as file:
            json.dump(data, file, indent=4)
            print(f'updated {filePath}')