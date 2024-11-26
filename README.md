# Diet_Recipe_Finder
This Flask-based web application allows users to search for recipes either by uploading an image or manually searching for a recipe by name. The system matches the uploaded image with pre-stored recipes and provides the recipe details, including ingredients, procedure, and category. 

diet-recipe-finder/
 ├── food-11/
 │   ├── Evaluation/
 │   │   └── images.jpg
 ├── recipe1M/
 │   ├── ingredient_reduc.csv
 │   ├── recipes.json
 │   └── recipe_match.csv
 ├── templates/
 │   ├── index.html
 │   ├── upload.html
 │   └── manual.html
 ├── app.py
 └── requirements.txt

 Steps to run:
 python -m venv venv
 .\venv\Scripts\activate
 pip install -r requirements.txt
python app.py

