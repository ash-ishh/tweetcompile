import argparse
import os 
import sys
from scrape import Scrape
from template import Template 
from pdf import PDF

TEMPLATE_NAME = "tweets.html"
OUTPUT_DIR = "output"
STATIC_DIR = "static"
TEMPLATE_DIR = "templates"
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_PATH = os.path.join(DIR_PATH, TEMPLATE_DIR)
STATIC_BASE = os.path.join(DIR_PATH, OUTPUT_DIR, STATIC_DIR)

def options():
    parser = argparse.ArgumentParser(prog="tweetcompile",
                                     usage="python3 %(prog)s [options]",
                                     description="Generate PDF of tweet compilation for given user and keywords")
    parser.add_argument('-u','--username',
                        type=str,
                        help='twitter handle',
                        required='True')
    parser.add_argument('--keywords', nargs='+',default=[''])
    args = parser.parse_args()
    return args

def make_user_dir(username):
    global DIR_PATH, OUTPUT_DIR
    directory = os.path.join(DIR_PATH, OUTPUT_DIR , username)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def scrape_tweets(username, keywords, output_dir):
    global DIR_PATH
    for keyword in keywords:
        if keyword:
            scrape = Scrape(username=username,keyword=keyword)
        else:
            scrape = Scrape(username=username)
        json_path = os.path.join(output_dir,f"{username}-{keyword}.json")
        if os.path.exists(json_path):
            os.remove(json_path) #delelet file is already exists since twint appends it
        scrape.save_json(json_path=json_path)

def save_template(username, keywords, output_dir):
    global TEMPLATES_PATH, TEMPLATE_NAME, DIR_PATH
    html_path = os.path.join(output_dir,f"{username}.html")
    json_paths = [os.path.join(output_dir, f"{username}-{keyword}.json") for keyword in keywords]
    template = Template(templates_path=TEMPLATES_PATH)
    template.save_html(json_paths=json_paths,
                       template_name=TEMPLATE_NAME,
                       output_path=html_path,
                       static_base=STATIC_BASE,
                       keywords=keywords)
    return html_path

def main():
    args = options()
    username = args.username
    keywords = args.keywords
    output_dir = make_user_dir(username)

    scrape_tweets(username, keywords, output_dir)
    html_path = save_template(username, keywords, output_dir)

    output_pdf= os.path.join(output_dir,f"{username}.pdf")
    pdf_instance = PDF()
    pdf_instance.save_pdf(html_path, output_pdf)

if __name__ == "__main__":
    main()
