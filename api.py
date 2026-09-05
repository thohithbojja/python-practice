

import requests


main_url = "https://pokeapi.co/api/v2"


def get_pokemon_info(name):

	response = requests.get(f"{main_url}/pokemon/{name}")

	if response.status_code == 200:

		print("data retrieved")
	else:

	    	print("data not retrieved")




get_pokemon_info("pikachu")


get_pokemon_info("pikachu")









