import json 
from src.backend.elo import Competitor
from PIL import Image, ImageOps
from pathlib import Path
    
class Loader():
    def __init__(self, filename: str):
        #First, check if the filename exists, and if that file is json.
        if not filename.endswith(".json"):
            raise ValueError("Filename must be a JSON file.")
        
        #Get the file from data/tournaments/src
        resources = "data/" + filename
        with open(resources, "r") as f:
            self.data = json.load(f)
        
        self.competitors = self._load_competitors()
        self.images = self._load_images()
        print(self.images)
    
    def _load_images(self) -> dict[Competitor, Image.Image]:
        placeholder_image = Path("resources\\Assets\\Placeholder.jpg")
        image_path = self.data.get("image_path", None)
        directory = Path(image_path)
        images = {}
        if image_path is None:
            images = {}
            for competitor in self.competitors:
                with Image.open(placeholder_image) as img:
                    images[competitor] = img.resize((300,300))
            return images
        else:
            files = [f for f in directory.iterdir() if f.is_file()]
            for competitor in self.competitors:
                file = next((f for f in files if Path(f).stem.lower() == competitor.name.lower()), None)
                print(file)
                if file is None:
                    with Image.open(placeholder_image) as img:
                        images[competitor] = img.resize((300,300))
                else:
                    with Image.open(file) as img:
                        images[competitor] = img.resize((300,300))
            return images 


    def _load_competitors(self) -> list[Competitor]:
        """Takes the file located at data/tournaments/filename.json and loads each competitor.
        :return: A list of competitors.
        :rtype: list[Competitor]
        """
        listed_competitors = self.data.get("competitors", [])
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
