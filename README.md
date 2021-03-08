# Inoa Challenge
This project was made as a part of Inoa's internship process.
## Specification
For the challenge, it was required that a system be made to track B3's assets, to assist an investor in his buying/selling choices. To achieve this, the following functionalities were necessary:
- Obtain, at a configurable periodicity, the price of assets from some public source and store them for later consultation.
- Display a web interface to consult stored prices, configure the assets to be monitored and their lower and upper limit prices.
- Send an email to the investor suggesting to buy whenever the price of a monitored asset crosses its lower limit, and suggest to sell whenever the price of a monitored asset crosses its upper limit.

It was also required that the system be made in Python with Django.

## Install


```bash
git clone https://username@github.com/viniciusth/inoa-challenge.git
cd inoa-challenge
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
```

## Run

To run the app, `docker` and `docker-compose` must be installed on your system. For installation
instructions refer to the Docker [docs](https://docs.docker.com/compose/install/). 

#### Compose
The app can be run in development mode using Django's built in web server simply by executing

```bash
docker-compose up
```

To remove all containers in the cluster use

```bash
docker-compose down
```

## Functionalities
#### Home Page
In this page there isn't much, just a text welcoming the user and the sidebar where more functionalities can be found.
#### Registering account
To register an account simply fill in the needed data and click on "Register account"
#### Logging in
After registering, put in your username and password at the "Login" page to login.
#### Viewing profile
If you're logged in, there will be an option "Profile". in this page you can look at your account data and edit your email/password. 
#### Viewing all assets
Being logged in or not you can click on the "Assets" option to view all B3 assets, including a search bar to find the asset you want easily.
#### Viewing your tracked assets
If you're logged in, there will be an option "My Assets". In this page you can look at your currently tracked assets, track new ones and untrack previously tracked assets. To track a new asset you must enter a valid B3 asset ticker and a valid lower/upper limit price.
#### Extra information about specific asset
In both the "All Assets" and "My Assets" page, you can click at the ticker of an asset you want to get extra information about. In this extra page you will find an graph containing the today's price of the asset plotted, with an option to plot different periods. 
## Data
A list containing all of B3 assets couldn't be found easily on their website, to overcome this i generated my own list via 10 days of data about [open positions](http://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/consultas/boletim-diario/arquivos-para-download/), which, together, contained almost 600 different assets. To get the value of these assets [yfinance](https://pypi.org/project/yfinance/) was used, a python library which gets historical market data from [Yahoo! finance](https://finance.yahoo.com/).
## Updating prices
The project updates the value of tracked assets every 45 seconds, to do this it utilizes [django-workers](https://pypi.org/project/django-workers/), a Django extension which adds simple background tasks to Django. To change the amount of time you need to change the task function decorator.
