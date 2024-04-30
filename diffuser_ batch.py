#as a list
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from urllib.request import urlretrieve
from datetime import datetime
from torch.profiler import profile, record_function, ProfilerActivity

import argparse
import numpy as np
import torch
import pandas as pd
import os
import pytz
import torchvision.models as models

def generate_image(prompts, num_prompts):
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cpu")

    valid_prompts = []
    index = 0
    while len(valid_prompts) < num_prompts and index < len(prompts):
        prompt = prompts[index]
        token_length = len(pipe.tokenizer(prompt)['input_ids'])
        if token_length <= 77:
            valid_prompts.append(prompt)
        index += 1

    images = pipe(valid_prompts).images
    for i in range(len(valid_prompts)):
        image = images[i]
        image.save(f"image_{i}.png")

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

    chicago_tz = pytz.timezone('US/Central')
    start_time = datetime.now(chicago_tz)
    print(f"Start time in: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    generate_image(prompts, num_prompts)

    end_time = datetime.now(chicago_tz)
    print(f"End time in Chicago: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
