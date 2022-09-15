import json
import os

from jinja2 import Environment, FileSystemLoader 

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

class TweetsTemplate:
    def __init__(self, *args, **kwargs):
        self.templates_path = kwargs.get("template_path","templates")
        self.template_name = kwargs.get("template_name", "tweets.html")
        self.static_base = kwargs.get("static_base")
        self.output_dir = kwargs.get("output_dir")
        self.file_loader = FileSystemLoader(self.templates_path)
        self.env = Environment(loader=self.file_loader)

    def save_html(self, username, keywords):
        json_paths = [os.path.join(self.output_dir, f"{username}-{keyword}.json") for keyword in keywords]

        compilation = []
        no_tweets_count = 0
    
        for keyword, json_path in zip(keywords,json_paths):
            if not os.path.exists(json_path):
                print(f"No tweets found for {keyword}")
                no_tweets_count += 1
                continue
            tweets = get_json_list(json_path)
            compilation.append({
                "keyword":keyword,
                "tweets":tweets
            })

        if no_tweets_count == len(keywords):
            raise Exception("No tweets found for any of the keywords.")

        template = self.env.get_template(self.template_name)
        output = template.render(compilation=compilation, static_base=self.static_base)
        rendered_html_path = os.path.join(self.output_dir, f"{username}.html")
        with open(rendered_html_path, "w") as output_file:
            output_file.write(output)
        return rendered_html_path