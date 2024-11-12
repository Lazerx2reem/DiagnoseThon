import os 
import re
from bs4 import BeautifulSoup
import requests

from constants import SYSTEM_PROMPT, HOUSE_SEASON_1_TITLES, BASE_URL

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class ParsedObject: 
    """
        Reads content from website page and structures the text read
    """
    PARSED_MODE = 0 
    FULL_TEXT_MODE = 1

    def __init__(self, url) -> None:
        
        self.recap_contents = None 
        self.zebra_factor = None 
        self.zebra_factor_contents = None 
        
        self.url = url 

        self.parsed_contents = self.parse_url(self.url)
        self.mode = ParsedObject.PARSED_MODE
        try:
            self.get_individual_contents()
        except BaseException as error:
            print(error)
            print(f"Parsing failed for {url} ; Using the entire content for LLM prompt generation.")       
            self.mode = ParsedObject.FULL_TEXT_MODE 

    def get_individual_contents(self):

        self.recap_contents = self.get_contents_between(data=self.parsed_contents,
                                                        s1="Recap\[\]",
                                                        s2="[Clinic Patient\[\]|Clinic Patients\[\]]")    
            
        self.zebra_factor = int(re.findall("(?<=Zebra Factor[: ])(.*?)(?=/10\[\])", self.parsed_contents)[0])
        
        self.zebra_factor_contents = self.get_contents_between(data=self.parsed_contents,
                                                               s1="Zebra Factor [0-9]+/10\[\]", 
                                                               s2="[Trivia and cultural references\[\]|Trivia and Cultural References[]|Title\[\]]")
    
    def parse_url(self, url):
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        return soup.get_text()        

    def get_contents_between(self, data, s1, s2):
        y = re.findall(f'{s1}[\S\s]*{s2}', data)
        return y[0]
    
    def get_prompt(self):
        prompt = None 
        if self.mode == ParsedObject.PARSED_MODE:
            prompt = f""" Use the information from RECAP and ZEBRA FACTOR for creating your LLM prompt, required medical answer, and the disease name
            ### RECAP ### 
            {self.recap_contents}
            ### ZEBRA FACTOR ### 
            {self.zebra_factor_contents}
            """
        else:
            prompt = f"""Use details in INFORMATION for creating your LLM prompt, required medical answer, and the disease name  
            ### INFORMATION ### 
            {self.parsed_contents}
            """
        return prompt


def openAIPayLoadHelper(prompt, api_key, gpt_system_prompt):
    """
        Helper function to construct the header and body of the OpenAI API call
    """
    
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
        "role": "system", 
        "content": f"{gpt_system_prompt}"
        },
        {
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"{prompt}"
            },
        ]
        }
    ],
    "max_tokens": 1024
    }

    return (headers, payload)
    

def parseOpenAIRespone(response):
    """
        Parses the response from openAI API call and returns the output 
    """
    json_dict = response.json()
    target_output = json_dict["choices"][0]["message"]["content"]
    return target_output

def main():

    parsed_objs = []
    print(" === Collecting data ===")

    # collect all urls
    for i, episode_name in enumerate(HOUSE_SEASON_1_TITLES):
        url = f"{BASE_URL}{episode_name.replace(' ', '_')}" 
        print(f"{episode_name} ::: {url}")
        try:
            x = ParsedObject(url)
            parsed_objs += [x]
        except BaseException as error:
            print(error)
            print(f"{url} skipped. ")

    print(" === Generating medical question and answer ===")
    # call the api 
    for x in parsed_objs:
        prompt = x.get_prompt()
        # format the api payload
        (headers, payload) = openAIPayLoadHelper(prompt, OPENAI_API_KEY, SYSTEM_PROMPT)
        # make the post api call
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        parsedOutput = parseOpenAIRespone(response)
        print(parsedOutput)


if __name__ == "__main__":
    main()
