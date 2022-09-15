# tweetcompile

Generate tweet compilation PDF of given user.

## Getting Started

### Dependencies

* python3.6+

### Installation

* Create and activate virtual env
* Install packages from requirements.txt
* Install [wkhtmltopdf 0.12.6 (with patched qt)](https://wkhtmltopdf.org/downloads.html)

### Executing program

* Creating pdf of all the tweets
```
python cli.py -u ash_ishh_
```

* Creating pdf by filtering tweets with keywords
```
python cli.py -u elonmusk --keywords 'twitter' 'kanye'
```

### Output pdf

* Output pdf will be located in ./output/{user}/{user}{keywords}.pdf
