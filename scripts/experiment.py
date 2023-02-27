import math as m 
import json
from tqdm import tqdm

BATCH_SIZE = 5
MAX_NEW_TOKENS = 140
TEMPERATURE = 0.5
TOP_K = 40

def run_inference(input_list, output_file_path, tokenizer, model, stop_token, do_sample):

  n_batches = m.ceil(len(input_list) / BATCH_SIZE)

  for n in tqdm(range(n_batches)):
    with open(output_file_path, "a") as output_file:
      for prompt in input_list[n*BATCH_SIZE:(n+1)*BATCH_SIZE]:
        input_tokenized = tokenizer(prompt, return_tensors="pt")["input_ids"].cuda()
        if do_sample:
          outputs = model.generate(input_tokenized, 
                                  max_new_tokens=MAX_NEW_TOKENS, 
                                  eos_token_id=stop_token, 
                                  do_sample=do_sample, 
                                  temperature=TEMPERATURE, 
                                  top_k=TOP_K)
        else:
          outputs = model.generate(input_tokenized, 
                                  max_new_tokens=MAX_NEW_TOKENS, 
                                  eos_token_id=stop_token, 
                                  do_sample=do_sample)
        output_text = tokenizer.decode(outputs[0])
        output_text = output_text.replace(prompt, "")
        output_text = output_text.replace("\n\nA:", "")
        pred = {"generated answer": output_text}
        json.dump(pred, output_file)
        output_file.write("\n")