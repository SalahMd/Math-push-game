class Json:
    def __init__(self,json_data,rows=None,cols=None,cells=None):
        self.json_data = json_data
        self.rows = json_data["rows"]
        self.cols = json_data["cols"]
        self.cells = json_data["cells"]
        