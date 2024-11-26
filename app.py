from flask import Flask, redirect, request, jsonify, render_template,send_from_directory, url_for

import os
from PIL import Image
import numpy as np

import pandas as pd
import json




#app = Flask(__name__)
app = Flask(__name__, static_folder='food-11')


# Path to the evaluation images
image_folder = 'food-11/evaluation'


# Load recipe match data
recipe_match_file = 'recipe1M/recipe_match.csv'
recipe_match_df = pd.read_csv(recipe_match_file)

# Load recipes data
recipes_file = 'recipe1M/recipes.json'
with open(recipes_file, 'r') as file:
    recipes_data = json.load(file)

def preprocess_image(image_path):
    img = Image.open(image_path).resize((299, 299))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def get_recipe_details(recipe_name):
    for recipe in recipes_data:
        if recipe['recipe_name'] == recipe_name:
            return recipe['ingredients'], recipe['procedure'], recipe['category']
        
    return None, None, None



@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('food-11', path)

@app.route('/food-11/evaluation/<path:filename>')
def serve_image(filename):
    return send_from_directory('food-11/evaluation', filename)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_image_page')
def upload_image_page():
    return render_template('upload.html')

@app.route('/manual_search_page')
def manual_search_page():
    return render_template('manual.html')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Route for handling form submission and storing data
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    # Path to the file where contact details will be stored
    file_path = os.path.join('contact_details.txt')

    # Write data to the file
    with open(file_path, 'a') as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Message: {message}\n")
        file.write(f"{'-'*30}\n")

    # Redirect back to the contact page or a success page
    return redirect(url_for('contact'))


@app.route('/upload_image', methods=['POST'])
def upload_image():
    selected_image = request.form.get('image_name')
    if not selected_image:
        return jsonify({'error': 'No image selected'}), 400 , "error is there in not selcted image"
    
    image_path = os.path.join(image_folder, selected_image)
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image file does not exist'}), 400
    
    

    # Get recipe from recipe match
    matched_recipe = recipe_match_df[recipe_match_df['image_name'] == selected_image]
    if matched_recipe.empty:
        return jsonify({'error': 'No matching recipe found'}), 404
    
    recipe_name = matched_recipe.iloc[0]['recipe_name']
    ingredients, procedure, category = get_recipe_details(recipe_name)
    
    if not ingredients or not procedure:
        return jsonify({'error': 'Recipe details not found'}), 404

    return jsonify({
        'recipe_name': recipe_name,
        'ingredients': ingredients,
        'procedure': procedure,
        'best_suitable_for': category,
        
        
    })

@app.route('/manual_search', methods=['POST'])
def manual_search():
    category = request.form.get('category')
    recipe_name = request.form.get('recipe_name')
    
    ingredients, procedure, category = get_recipe_details(recipe_name)
    if not ingredients or not procedure:
        return jsonify({'error': 'Recipe details not found'}), 404
    
    # Generate image URL without the static prefix
    image_row = recipe_match_df[recipe_match_df['recipe_name'] == recipe_name]
    if image_row.empty:
        return jsonify({'error': 'No image found for this recipe'}), 404
    
    image_name = image_row.iloc[0]['image_name']
    image_url =f'{ image_name}'  # Use this instead of /static/

    
    return jsonify({
        'recipe_name': recipe_name,
        'ingredients': ingredients,
        'procedure': procedure,
        'best_suitable_for': category,
        'image_url': image_url  # Return just the filename, the static route will handle the path
    }) 




@app.route('/search_recipe', methods=['GET'])
def search_recipe():
    category = request.args.get('category')
    if not category:
        return jsonify({'error': 'No category provided'}), 400
    
    matching_recipes = [recipe['recipe_name'] for recipe in recipes_data if recipe['category'] == category]
    return jsonify({'recipes': matching_recipes})

@app.route('/get_image_list', methods=['GET'])
def get_image_list():
    image_list = os.listdir(image_folder)
    return jsonify({'images': image_list})

if __name__ == '__main__':
    app.run(debug=True)