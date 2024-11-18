
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
