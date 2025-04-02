import os
import google.generativeai as genai

genai.configure(api_key= os.environ.get("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

PROMPT = "Generate a title and description for this image in JSON format with keys 'title' and 'description'"

def generate_image_description(image_uri):
  print(f"Generating image ${image_uri}")
  response = model.generate_content( contents=[image_uri, PROMPT] )
  print(f"response:: {response.text}")
  return response.text