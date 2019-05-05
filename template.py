from jinja2 import Environment, FileSystemLoader 
import json

def get_json_list(json_path):
    """
    It return list of jsons fetched from
    each line of given json_path
    """
    data = []
    with open(json_path) as json_file:
        for line in json_file:
            data.append(json.loads(line)) 
    return data

class Template:
    def __init__(self, *args, **kwargs):
        self.templates_path = kwargs.get("template_path","templates")
        self.file_loader = FileSystemLoader(self.templates_path)
        self.env = Environment(loader=self.file_loader)

    def save_html(self, *args, **kwargs):
        template_name = kwargs.get("template_name", None)
        json_paths = kwargs.get("json_paths", None)
        output_path = kwargs.get("output_path", None)
        static_base = kwargs.get("static_base", None)
        keywords = kwargs.get("keywords", None)
        compilation = []

        for keyword, json_path in zip(keywords,json_paths):
            tweets = get_json_list(json_path)
            compilation.append({
                "name":keyword,
                "tweets":tweets
            })
        template = self.env.get_template(template_name)
        output = template.render(compilation=compilation,static_base=static_base)
        with open(output_path,"w") as output_file:
            output_file.write(output)