import twint

class Scrape:
    def __init__(self, *args, **kwargs):
        self.username = kwargs.get("username",None)
        self.keyword = kwargs.get("keyword",None)

        self.c = twint.Config()
        self.c.Username = self.username

        if self.keyword:
            self.c.Search = self.keyword
            
        if not self.username:
            raise RuntimeError("Please provide username")

    def save_json(self, json_path):
        self.c.Store_json = True
        self.c.Output = json_path 
        twint.run.Search(self.c)