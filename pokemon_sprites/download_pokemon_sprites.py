import requests
import os

"""
Downloads the front_default sprite for a given pokemon using the PokeAPI.
"""
def download_pokemon_sprite(pokemon_name_or_id: int | str, output_dir: str = ".", prefix: str = "") -> None:
    
    # 1. Fetch pokemon data from the API
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}"
    print(f"Fetching API data for '{pokemon_name_or_id}' from {api_url}...")
    
    response = requests.get(api_url)
    if response.status_code != 200:
        print(f"Error: Failed to retrieve data. Status code: {response.status_code}")
        return
        
    data = response.json()
    
    # 2. Extract the front_default sprite URL
    sprite_url = data.get("sprites", {}).get("front_default")
    if not sprite_url:
        print(f"Error: No front_default sprite found for '{pokemon_name_or_id}'.")
        return
        
    print(f"Sprite found at: {sprite_url}")
    print("Downloading image...")
    
    # 3. Download the specific image
    img_response = requests.get(sprite_url)
    if img_response.status_code == 200:
        # Make sure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        pokemon_name = data.get("name", str(pokemon_name_or_id))
        filename = os.path.join(output_dir, f"{prefix}_{pokemon_name}.png")
        
        # Save the image to disk
        with open(filename, 'wb') as f:
            f.write(img_response.content)
            
        print(f"Successfully saved {pokemon_name} sprite to {filename}")
    else:
        print(f"Error: Failed to download the image. Status code: {img_response.status_code}")

if __name__ == "__main__":
    # Example usage downloading Ditto (ID 132) and Pikachu
    download_pokemon_sprite('meowstic-female', output_dir="./", prefix="677")
    # download_pokemon_sprite("pikachu", output_dir="pokemon_sprites")
    for i in range(1, 1026):
        #skipping meowstic-male, same issue as tyrunt, but another version is available
        if i == 677:
            continue
        download_pokemon_sprite(i, output_dir="./", prefix=str(i))
