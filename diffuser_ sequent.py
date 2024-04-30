#one by one
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from urllib.request import urlretrieve
from datetime import datetime

import argparse
import numpy as np
import torch
import pandas as pd
import os
import pytz

def generate_image(prompt, image_index):
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cpu")

    image = pipe(prompt).images[0]
    image.save(f"{image_index}.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    num_prompts = int(os.environ.get("NUM_PROMPTS", 1))
    parser.add_argument("--num_prompts", type=int, default=1, help="Number of prompts to process")
    args = parser.parse_args()

    table_url = f'https://huggingface.co/datasets/poloclub/diffusiondb/resolve/main/metadata.parquet'
    urlretrieve(table_url, 'metadata.parquet')

    metadata_df = pd.read_parquet('metadata.parquet')
    prompts = metadata_df['prompt']

    prompts = list(set(prompts))

    selected_prompts = prompts[:num_prompts]

    chicago_tz = pytz.timezone('US/Central')
    start_time = datetime.now(chicago_tz)
    print(f"Start time in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    for i, prompt in enumerate(selected_prompts, start=1):
        start_time = datetime.now(chicago_tz)
        print(f"Start image {i} in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        generate_image(prompt, i)
        end_time = datetime.now(chicago_tz)
        print(f"End image {i} in: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    end_time = datetime.now(chicago_tz)
    print(f"End time in : {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
