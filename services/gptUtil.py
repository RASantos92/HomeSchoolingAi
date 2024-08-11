from services.jsonUtil import JsonUtil

class GptUtil:
    @staticmethod
    def makeJsonAPICall(model, responseFormat, filePath, fileName):
        completion = model.client.beta.chat.completions.parse(
            messages = model.context,
            model = "gpt-4o-mini",
            response_format = responseFormat
        )
        print("In makeJsonAPICall:\n", completion.choices[0].message.parsed)
        returnedModel = completion.choices[0].message.parsed
        JsonUtil.saveModelToJsonFile(returnedModel, filePath, fileName)
        return completion