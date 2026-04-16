import requests  
# library used to make HTTP requests to GitHub API

import os  
# used to check if cache file exists in local system

import pickle  
# used to store and load cached GitHub results from file

from config import GITHUB_API, TOP_K  
# imports GitHub API URL and number of repositories to retrieve


CACHE_FILE = "github_cache.pkl"  
# name of the local file used to store cached GitHub results


def load_cache():
    # function used to load cached GitHub results from local file

    if os.path.exists(CACHE_FILE):
        # checks whether cache file already exists

        with open(CACHE_FILE, "rb") as f:
            # opens cache file in read-binary mode

            return pickle.load(f)
            # loads cached data from file and returns it

    return {}
    # if cache file does not exist, return empty dictionary



def save_cache(cache):
    # function used to save GitHub results into cache file

    with open(CACHE_FILE, "wb") as f:
        # opens cache file in write-binary mode

        pickle.dump(cache, f)
        # stores cache dictionary into file



def search_github(query):
    # function used to search repositories from GitHub based on user query

    cache = load_cache()
    # loads existing cached GitHub results


    # return cached result if already searched
    if query in cache:
        # checks whether the same query was searched before

        return cache[query]
        # returns cached repositories instead of calling API again


    search_query = f"{query} in:name,description"
    # modifies search query to search in repository name and description


    params = {
        # parameters sent to GitHub API

        "q": search_query,
        # search keyword

        "sort": "stars",
        # sort repositories by number of stars

        "order": "desc",
        # highest starred repositories first

        "per_page": TOP_K
        # limit number of repositories retrieved
    }


    try:
        # try block used to handle API errors safely

        response = requests.get(
            # sends GET request to GitHub API

            GITHUB_API,
            # GitHub search API endpoint

            params=params,
            # search parameters

            timeout=10
            # wait maximum 10 seconds for response
        )


        data = response.json()
        # converts API response into python dictionary


        repos = []
        # empty list used to store repository information


        for repo in data.get("items", []):
            # iterates through retrieved repositories
            # data["items"] contains list of repositories

            repos.append({
                # stores required repository details

                "name": repo["name"],
                # repository name

                "url": repo["html_url"],
                # repository GitHub link

                "description": repo["description"] or ""
                # repository description
                # if description is None, store empty string
            })


        # store in cache
        cache[query] = repos
        # saves retrieved repositories in cache dictionary


        save_cache(cache)
        # saves updated cache into local file


        return repos
        # returns list of repositories


    except:
        # handles API failure or network issues

        return []
        # returns empty list if GitHub request fails