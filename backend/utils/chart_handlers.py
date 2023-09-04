import json
from abc import ABC, abstractmethod

class HandleCharts(ABC):

    def __init__(self, file_name: str, x_axis: str, y_axis: str) -> None:
        self.file_name = file_name
        self.x_axis = x_axis
        self.y_axis = y_axis

    # @abstractmethod
    # def handle_pie(self):
    #     pass

    # @abstractmethod
    # def handle_bar(self):
    #     pass

    # @abstractmethod
    # def handle_line(self):
    #     pass


class PieChart(HandleCharts):

    def handle_pie(self):
        with open(r'C:\Users\theek\dev\S2T.ai\backend\data\file_1.json', 'r') as json_file:
            data = json.load(json_file)
            return data
    
    def get_pie_chart_data(self):
        data = self.handle_pie()

        pie_chart_data = []
        for obj in data:
            pie_chart_data.append({
                "name": obj[self.x_axis],
                "y": obj[self.y_axis]
            })
        
        data = {
            "name": self.y_axis,
            "colorByPoint": True,
            "data": pie_chart_data
        }
        return data


class BarChart(HandleCharts):

    def handle_bar(self):
        with open(r'C:\Users\theek\dev\S2T.ai\backend\data\file_1.json', 'r') as json_file:
            data = json.load(json_file)
            return data
    
    def get_bar_chart_data(self):
        data = self.handle_bar()
        bar_chart_data = []

        for obj in data:
            bar_chart_data.append({
                "name": obj[self.x_axis],
                "y": obj[self.y_axis]
            })
        
        data = {
            "name": self.y_axis,
            "colorByPoint": True,
            "data": bar_chart_data
        }
        return data
    
class LineChart(HandleCharts):
    def handle_line(self):
        with open(r'C:\Users\theek\dev\S2T.ai\backend\data\file_2.json', 'r') as json_file:
            data = json.load(json_file)
            return data
    

    def get_line_chart_data(self):
        return_data = []
        data = self.handle_line()
        for item in data:
            if item.get("name") == self.y_axis:
                return_data.append(item)
        return return_data