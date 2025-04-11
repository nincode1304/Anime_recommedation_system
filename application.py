from flask import Flask, render_template, request, redirect
from pipeline.prediction_pipeline import hybrid_recommendation
from pipeline.anime_info import get_anime_info
import requests
app = Flask(__name__)

# Route for recommendations
@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None

    if request.method == 'POST':
        mode = request.form.get('mode')

        try:
            if mode == 'recommend':
                user_id = int(request.form['userID'])
                titles = hybrid_recommendation(user_id)
                print(titles)
                recommendations = []

                for title in titles:
                    try:
                        jikan_url = f"https://api.jikan.moe/v4/anime?q={title}&limit=1"
                        res = requests.get(jikan_url).json()
                        anime_data = res.get("data", [])[0]
                        recommendations.append({
                            "title": anime_data["title"],
                            "image_url": anime_data["images"]["jpg"]["image_url"]
                        })
                    except Exception as fetch_err:
                        print(f"Could not fetch image for {title}: {fetch_err}")
                        recommendations.append({
                            "title": title,
                            "image_url": "/static/images/placeholder.jpg"
                        })

        except Exception as e:
            print("Error:", e)

    return render_template('index.html', recommendations=recommendations)




# Route for anime search result
@app.route('/search', methods=['GET', 'POST'])
def search_anime():
    anime_name = request.args.get('anime_name') or request.form.get('animeName')
    
    if not anime_name:
        return redirect('/')
    
    try:
        anime_info = get_anime_info(anime_name)
        if anime_info is None:
            return render_template('search_result.html', error="Anime not found!")
        return render_template('search_result.html', anime_info=anime_info)
    except Exception as e:
        print("Search Error:", e)
        return render_template('search_result.html', error="Something went wrong during the search.")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
