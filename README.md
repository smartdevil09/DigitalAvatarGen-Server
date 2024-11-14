Follow below steps to Configure the Server for DigitalAvatarGen:

**Step 1: Install Google-TTS**

* Set up a Google Cloud Project

  - Go to the Google Cloud Console.
  
  - Create a new project or select an existing project.

* Enable Google Cloud Text-to-Speech API

  - Navigate to the API & Services section.
  
  - Search for "Text-to-Speech API."
  
  - Enable the Google Cloud Text-to-Speech API.

* Set up Authentication (Service Account)

  - Go to IAM & Admin in the console.
  
  - Select Service Accounts, and click Create Service Account.
  
  - Set a name for your service account and assign it the Text-to-Speech API User role.
  
  - After creating the service account, download the JSON key file for authentication.

* Install Google Cloud SDK in your project

  - You can install the Google Cloud Text-to-Speech client library for Python.
  
    ```pip install google-cloud-texttospeech```
    
  -  Verify installation: ```pip show google-cloud-texttospeech```

**Step 2: Follow the installation steps for the SadTalker based on operating System: https://github.com/OpenTalker/SadTalker/tree/main**

**Step 3: Download our ```server.py```, ```inference.py``` and ```tts.py``` and save them in the SadTalker cloned working directory.**

**Step 4: Replace the code of file ```inference.py``` pulled from the SadTalker library with the our ```inference.py``` file.**

**Step 5: ```tts.py``` is the code for running up Google-TTS for converting text to speech. Replace ```google.json``` in the file with the path of your JSON key file.**

**Step 6: Run below command to start the server.**
  
  Command:```python server.py```
