#### vChatGPT
vChatGPT allows users to communicate verbally with ChatGPT.

#### Demo screenshot
Input: Your voice through a microphone  
Output: Speech sound from speakers + text  
![alt text](https://github.com/ywatanabe1989/vChatGPT/blob/main/docs/vChatGPT_demo.png?raw=true)

#### Installation
``` bash
$ python -m venv .vChatGPT
$ source .vChatGPT/bin/activate
$ git clone git@github.com:ywatanabe1989/vChatGPT.git
$ cd vChatGPT
$ pip install -r requirements.txt
# $ pip install git+https://github.com/openai/whisper.git
```

#### How to execute verbal ChatGPT
``` bash
$ export OPENAI_API_KEY="52-DIGIT-YOUR_API_KEY" # Available on https://platform.openai.com/account/api-keys
$ cd ./src/vChatGPT
$ python ./scripts/main.py
```

#### TODO
- [ ] pip install vChatGPT
