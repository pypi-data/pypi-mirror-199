from typing import Any, Dict
from . import settings
import requests
import argparse
import sys


class Generator:

    def __init__(self, prompt, language, filename) -> None:
        self.prompt = prompt
        self.language = language
        self.filename = filename

    @property
    def get_header(self) -> Dict[str, Any]:
        return {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + settings.API_KEY
        }

    @property
    def get_data(self) -> Dict[str, Any]:
        return {
            "model": "text-davinci-003",
            "prompt": f"Write {self.language} script to {self.prompt}. \
                Provide only code, no text.",
            "max_tokens": 100,
            "temperature": 0.5
        }

    def generate(self):
        response = requests.post(
            settings.API_ENDPOINT, headers=self.get_header, json=self.get_data)

        if response.status_code == 200:
            if self.filename:
                response_text = response.json()["choices"][0]["text"]
                with open(self.filename, "w") as file:
                    file.write(response_text)
                print(self.filename)
        else:
            print(f"Failed request {response.status_code}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--prompt", required=True,
                        help="Prompt to send to the OpenAI API")
    parser.add_argument("-f", "--filename", required=True,
                        help="The filename of output file")
    parser.add_argument("-l", "--language",
                        help="Language code (default=python)", default="python")
    args = parser.parse_args()
    Generator(**dict(args._get_kwargs())).generate()


if __name__ == "__main__":
    main()
