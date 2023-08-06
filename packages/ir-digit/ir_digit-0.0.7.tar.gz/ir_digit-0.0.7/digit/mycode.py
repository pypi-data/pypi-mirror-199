from .code import Code
class MyCode(Code):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def get_guide(self):
        return 'TEST: This is a guide for MyCode'

    def preprocessing(self):
        print("TEST：未进行任何数据预处理")
        return self.data