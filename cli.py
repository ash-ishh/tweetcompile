import argparse
import datetime
import os 
import sys

from scrape import Scrape
from template import TweetsTemplate
from pdf import PDF

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATE_DIR = "templates"
TEMPLATES_PATH = os.path.join(DIR_PATH, TEMPLATE_DIR)
TEMPLATE_NAME = "tweets.html"
OUTPUT_DIR = "output"
STATIC_DIR = "static"
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

def prepare_user_dir(username):
    global DIR_PATH, OUTPUT_DIR
    directory = os.path.join(DIR_PATH, OUTPUT_DIR , username)
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        # clean it up exept old pdfs
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if (os.path.isfile(file_path) or os.path.islink(file_path)) and (not file_path.endswith('pdf')):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    return directory

def main():
    args = options()
    username = args.username
    keywords = args.keywords
    user_output_dir = prepare_user_dir(username)

    # prepare scraped jsons
    for keyword in keywords:
        if keyword:
            scrape = Scrape(username=username, keyword=keyword)
            json_name = f"{username}-{keyword}.json"
        else:
            # in case of no keywords [''] is the value of keywords
            scrape = Scrape(username=username)
            json_name = f"{username}.json"
        
        json_path = os.path.join(user_output_dir, json_name)

        if os.path.exists(json_path):
            os.remove(json_path) # delelet file is already exists since twint appends it

        scrape.save_json(json_path=json_path)

    # Get HTML of scraped tweets
    template = TweetsTemplate(
        template_path=TEMPLATES_PATH,
        template_name=TEMPLATE_NAME,
        static_base=STATIC_BASE,
        output_dir=user_output_dir
    )
    html_path = template.save_html(username, keywords)

    # Generate PDF
    output_pdf_name = f"{username}-{'-'.join(keywords)}.pdf"
    output_pdf_path = os.path.join(user_output_dir, output_pdf_name)
    pdf_instance = PDF(
        html_path=html_path,
        output_file_path=output_pdf_path
    )
    pdf_instance.save_pdf()

if __name__ == "__main__":
    main()
