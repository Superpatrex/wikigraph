# wikigraph

## webscrapper

In order to run the python web scrapper, you need to each install the required libraries. You can do this by running the following command:

```bash
cd webscrapper
pip install -r requirements.txt
```

If you do not have pip installed, you can create a virtual environment and install the required libraries by running the following commands:

```bash
cd webscrapper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Once you have installed the required libraries, you can run the web scrapper by running the following command:

```bash
python3 wikidataparser.py
```

This will run the web scrapper and generate a files within the `output` directory which contains the data that was scraped from the Wikipedia page. These files will include the rankings and values of the algorithms that were run on the data. `constants.js` contains all the data together in a single file.

`NOTE:` Data can change on the Wikipedia page, so the data that is scraped may not be the same as the data that is currently on the Wikipedia page or on the graph that is being displayed.

`NOTE:` The web scrapper and running of the various algorithms can take a while to run, so please be patient. 

## [wikigraph website](https://superpatrex.github.io/wikigraph/)

The website can be viewed by simply clicking on the following link that is already hosted: [wikigraph](https://superpatrex.github.io/wikigraph/)

`NOTE:` The website is hosted on github pages and may take a few seconds to load.

If you would like to run the website locally, you can do so by doing the following:

First ensure that you have `node` and `npm` installed on your machine. You can do this by running the following commands:

```bash
node -v
npm -v
```

`NOTE:` `node` v23.3.0 and `npm` 10.9.0 were used to create the website.

If you do not have `node` and `npm` installed, you can install them by following the instructions on the following website: [nodejs.org](https://nodejs.org/)

Once you have installed `node` and `npm`, you can run the following commands to run the website locally:

```bash
npm install
npm start
```

This will install the required libraries and start the website on `localhost:3000/wikigraph`.