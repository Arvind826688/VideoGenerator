# video_generation.py

import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from gtts import gTTS
from moviepy.editor import *
from diffusers import StableDiffusionPipeline
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Function to generate script from input text
def generate_script(topic):
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2").cuda()  # Use GPU with .cuda()
    prompt = f"Create a short tutorial script on {topic}."
    inputs = tokenizer.encode(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(inputs, max_length=150, do_sample=True)
    script = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return script

# Function to generate image prompts from the script
def generate_image_prompts(script):
    doc = nlp(script)
    prompts = [sent.text for sent in doc.sents]
    return prompts[:20]

# Function to convert text script into audio using gTTS
def text_to_speech(script, filename="audio.mp3"):
    tts = gTTS(script)
    tts.save(filename)

# Function to generate images from prompts using Stable Diffusion
def generate_images(prompts, num_images=2):
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")
    images = []
    for prompt in prompts:
        for i in range(num_images):
            image = pipe(prompt).images[0]
            image_path = f"generated_images/{prompt[:10]}_{i}.png"
            images.append(image_path)
            image.save(image_path)
    return images

# Function to create video from images and audio
def create_video(image_files, audio_file, output_file="tutorial_video.mp4"):
    images = [ImageClip(img).set_duration(3) for img in image_files]
    audio = AudioFileClip(audio_file)
    video = concatenate_videoclips(images, method="compose")
    video = video.set_audio(audio)
    video.write_videofile(output_file, fps=24)

# Function to run the complete video generation process
def generate_video_from_topic(topic):
    # Step 1: Generate script
    script = generate_script(topic)
    
    # Step 2: Convert script to audio
    audio_file = "audio.mp3"
    text_to_speech(script, audio_file)
    
    # Step 3: Generate prompts and images
    prompts = generate_image_prompts(script)
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")
    image_files = generate_images(prompts)
    
    # Step 4: Generate video
    create_video(image_files, audio_file, "tutorial_video.mp4")
