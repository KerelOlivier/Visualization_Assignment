# JBI100 - Visualising the NYC Airbnb debate

This project is a dashboard to support the debate about the impact of AirBnbs in New York City. It is made for the Course JBI100-Visualization at the TU Eindhoven. 

## Requirements

* Python 3

## How to run this app

We suggest you to create a virtual environment for running this app with Python 3. Clone this repository 
and open your terminal/command prompt in the root folder.

open the command prompt
cd into the folder where you want to save the files and run the following commands:

```
> git clone https://gitlab.tue.nl/s146523/jbi100-2021-2022.git
> cd jbi100-2021-2022
> python -m venv venv

```
If python is not recognized use python3 instead

In Windows: 

```
> venv\Scripts\activate

```
In Unix system:
```
> source venv/bin/activate
```

(Instead of a python virtual environment you can also use an anaconda virtual environment.
 
Requirements:

• Anaconda (https://www.anaconda.com/) or Miniconda (https://docs.conda.io/en/latest/miniconda.html)

• The difference is that Anaconda has a user-friendly UI but requires a lot of space, and Miniconda is Command Prompt based, no UI, but requires considerably less space.

Then you should replace the lines: python -m venv venv and venv\Scripts\activate or source venv/bin/activate with the following:

```
> conda create -n yourenvname
> conda activate yourenvname
```
)

Install all required packages by running:
```
> pip install -r requirements.txt
```

Run this app locally with:
```
> python app.py
```
Initial loading of the webpage might take a bit due to a large dataset being rendered. Performance will improve when selecting a neighbourhood or neighbourhood group.
You will get a http link, open this in your browser to see the results. You can edit the code in any editor (e.g. Visual Studio Code) and if you save it you will see the results in the browser.
