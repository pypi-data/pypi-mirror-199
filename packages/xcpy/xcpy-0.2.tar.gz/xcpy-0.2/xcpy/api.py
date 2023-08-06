import requests
import os

class xcpy:
    def __init__(self, api_key):
        self.base_url = "https://www.xeno-canto.org/api/2"
        self.api_key = api_key
    
    def search_recordings(self, query="", species="", author="", country="", type="", page=1):
        """
        Search for recordings by keyword(s), bird species, author, country, and/or song type.

        Parameters:
            query (str): The search query string (optional).
            species (str): The common or scientific name of the bird species (optional).
            author (str): The name of the author of the recording (optional).
            country (str): The two-letter country code of the location of the recording (optional).
            type (str): The type of vocalization in the recording (optional).
            page (int): The page number of the search results (optional, default=1).

        Returns:
            A dictionary containing the search results.
        """
        url = f"{self.base_url}/recordings"
        params = {
            "query": query,
            "species": species,
            "recorder": author,
            "country": country,
            "type": type,
            "page": page,
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_recording_by_id(self, recording_id):
        """
        Get a recording by its Xeno Canto ID.

        Parameters:
            recording_id (int): The Xeno Canto ID of the recording.

        Returns:
            A dictionary containing the recording information.
        """
        url = f"{self.base_url}/recordings/{recording_id}"
        params = {
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()
    
    def get_species_by_id(self, species_id):
        """
        Get a species by its Xeno Canto ID.

        Parameters:
            species_id (int): The Xeno Canto ID of the species.

        Returns:
            A dictionary containing the species information.
        """
        url = f"{self.base_url}/species/{species_id}"
        params = {
            "key": self.api_key
        }
        response = requests.get(url, params=params)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def download_audio(self, recordings, download_dir):
    """
    Download audio files from a list of Recording objects to the specified directory.

    Parameters:
    recordings (list): A list of Recording objects returned by the XenoCantoAPI.search_recordings method.
    download_dir (str): The directory where audio files should be downloaded to.

    Returns:
    None
    """

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    for recording in recordings:
        audio_url = recording.file
        audio_filename = os.path.basename(audio_url)

        response = requests.get(audio_url)

        if response.status_code == 200:
            audio_file_path = os.path.join(download_dir, audio_filename)

            with open(audio_file_path, 'wb') as f:
                f.write(response.content)

            print(f'Downloaded {audio_file_path}')
        else:
            print(f'Error downloading audio file for Recording {recording.id}')