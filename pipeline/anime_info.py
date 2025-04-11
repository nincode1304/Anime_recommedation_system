import requests 
import random
def get_anime_info(anime_name):
    # 1. Search for the anime
    search_url = f"https://api.jikan.moe/v4/anime?q={anime_name}&limit=1"
    response = requests.get(search_url)
    
    if response.status_code !=200:
        return None 
    
    data = response.json()
    
    if not data['data']:
        return None 

    anime = data['data'][0]
    mal_id = anime['mal_id']    
    
    reviews_url = f"https://api.jikan.moe/v4/anime/{mal_id}/reviews"
    reviews_response = requests.get(reviews_url).json()
    all_reviews = reviews_response.get("data", [])
    selected_reviews = random.sample(all_reviews, min(6, len(all_reviews)))    
    review_list = [{
        "user": review['user']['username'],
        "score": review['score'],
        "review": review['review'][:350] + ("..." if len(review['review']) > 500 else "")
    } for review in selected_reviews]
    
    recommendation_url = f"https://api.jikan.moe/v4/anime/{mal_id}/recommendations"
    rec_response = requests.get(recommendation_url).json()
    rec_data = rec_response.get("data", [])[:6]  # Limit to 6 recommendations

    similar_anime = [{
        "title": rec['entry']['title'],
        "image_url": rec['entry']['images']['jpg']['image_url'],
        "mal_id": rec['entry']['mal_id']
    } for rec in rec_data]

    return {
        'title': anime.get('title'),
        'synopsis': anime.get('synopsis'),
        'rating': anime.get('score'),
        'genres': [genre['name'] for genre in anime.get('genres', [])],
        'poster': anime['images']['jpg']['large_image_url'],
        'mal_url': anime['url'],
        'trailer_url': anime.get('trailer', {}).get('url'),
        'reviews': review_list ,
        'similar': similar_anime
    } 
