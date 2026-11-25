import json 
from src.backend.elo import Competitor

def load_competitors(filename : str) -> list[Competitor]:
    """Takes the file located at data/tournaments/filename.json and loads each competitor.

    :param path: The name of the template
    :type path: str
    :return: A list of competitors.
    :rtype: list[Competitor]
    """

    #First, check if the filename exists, and if that file is json.
    if not filename.endswith(".json"):
        raise ValueError("Filename must be a JSON file.")
    
    #Get the file from data/tournaments/src
    resources = "data/tournaments/" + filename
    with open(resources, "r") as f:
        data = json.load(f)
    
    listed_competitors = data.get("competitors", [])
    returned_competitors = []
    for competitor in listed_competitors:
        name = competitor.get("name")
        elo = competitor.get("elo")
        returned_competitors.append(Competitor(name,elo))
    return returned_competitors


if __name__ == "__main__":
    #Try loading competitors
    competitors = load_competitors("tournament_template.json")
    print([competitor.name for competitor in competitors])
    