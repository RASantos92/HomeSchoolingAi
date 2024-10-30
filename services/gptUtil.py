from services.jsonUtil import JsonUtil
from models.AssesmentTest import AssesmentTest
from openai.types.chat.chat_completion import ChatCompletion
class GptUtil:
    # so far this cost a 2 cents to create a weeks worth of leactures
    @staticmethod
    def makeJsonAPICall(model, responseFormat : AssesmentTest, filePath = None, fileName = None) -> ChatCompletion:
        completion = model.client.beta.chat.completions.parse(
            messages = model.context,
            model = "gpt-4o-mini",
            response_format = responseFormat
        )
        # print("In makeJsonAPICall:\n", completion.choices[0].message.parsed)
        returnedModel = completion.choices[0].message.parsed
        if filePath:
            JsonUtil.saveModelToJsonFile(returnedModel, filePath, fileName)
        return completion
    
    @staticmethod
    def makeChatAPICall(model) -> ChatCompletion:
        completion = model.client.chat.completions.create(
            model='gpt-4o-mini',
            messages= model.context
        )
        message = completion.choices[0].message.content
        print(message, type(completion))
        return completion
    
    # cost 18 cents for a weeks worth of lectures.
    @staticmethod
    def makeJsonAPICallXL(model, responseFormat : AssesmentTest, filePath : str, fileName : str) -> ChatCompletion:
        completion = model.client.beta.chat.completions.parse(
            messages = model.context,
            model = "gpt-4o-2024-08-06",
            response_format = responseFormat
        )
        print("In makeJsonAPICall:\n", completion.choices[0].message.parsed)
        returnedModel = completion.choices[0].message.parsed
        JsonUtil.saveModelToJsonFile(returnedModel, filePath, fileName)
        return completion
    