from google.cloud import texttospeech
import os
import sys  # Add this line to import the sys module
 
# Set the path to your service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./google.json"

# Initialize TTS client
client = texttospeech.TextToSpeechClient()
 
# Define text-to-speech function
def text_to_speech(text,gender_choice, output_file="output.mp3"):
    synthesis_input = texttospeech.SynthesisInput(text=text)

    if gender_choice.lower() == 'male':
        gender = texttospeech.SsmlVoiceGender.MALE
        voice_name = "en-US-Neural2-D"  # Realistic male voice
    elif gender_choice.lower() == 'female':
        gender = texttospeech.SsmlVoiceGender.FEMALE
        voice_name = "en-US-Neural2-C"  # Realistic female voice
    else:
        gender = texttospeech.SsmlVoiceGender.NEUTRAL
        voice_name = "en-US-Wavenet-A"  # Neutral voice
   
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=gender,
        name=voice_name  # Use realistic female voice model
    )
   
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
   
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
   
    # Save the output
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print("Audio content written to output_file")
    return output_file if os.path.exists(output_file) else None
 
# Check for command-line input and run the TTS function
if __name__ == "__main__":
    if len(sys.argv) > 2:
        text = sys.argv[1]
        gender = sys.argv[2]
        text_to_speech(text,gender)
    else:
        print("Please provide text input for speech synthesis.")
