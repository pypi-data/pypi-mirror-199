import pandas as pd
import math
import os
import json
import hashlib
from tqdm import tqdm
from opengpt import parsers
from opengpt.openai_api import ask_openai

def split_csv_by_max_len(datasets, max_len, tokenizer, base_path):
    for dataset in datasets:
        csv_path = dataset['path']
        name = dataset['name']
        print("Started processing: ", name)

        df = pd.read_csv(csv_path)
        cols = df.columns
        assert 'text' in cols, f'The CSV for dataset {name} has no "text" column.'

        new_data = [list(cols) + ['len', 'part']]
        for ind, row in df.iterrows():
            text = row['text']
            tokens = tokenizer.encode(text)

            for i in range(math.ceil(len(tokens) / max_len)):
                new_text = tokenizer.decode(tokens[i*max_len:(i+1)*max_len])
                new_data_row = [row[c] if c != 'text' else new_text for c in cols]
                new_data_row.append(len(tokens[i*max_len:(i+1)*max_len]))
                new_data_row.append(f'part_{i}')
                new_data.append(new_data_row)
        
        # Save
        new_df = pd.DataFrame(new_data[1:], columns=new_data[0])
        new_df.to_csv(os.path.join(base_path, name, 'data_split_by_length.csv'))
        print(f'Processing done, length before vs after: {len(df)} vs {len(new_df)}\n')

def create_dataset(config):
    prompt_db = json.load(open(config.path.prompt_db, 'rb'))
    data_columns = ['text', 'dataset', 'language', 'run', 'prompt_hash', 'prompt_text_hash']
    data = pd.DataFrame(None, columns=data_columns)
    data_path = os.path.join(config.base_path, f"generated_data_for_{config.name}.csv")
    if os.path.exists(data_path):
        data = pd.read_csv(data_path)
        print(f"Loading an existing openai generated dataset found at: {data_path}")
        print(f"There are already {len(data)} rows in the that dataset, the generation will continue from where last left off.")

    cnt = 0
    for prompt_config in config.prompts:
        prompt = [prompt for prompt in prompt_db if prompt['hash'] == prompt_config['hash']][0] # There must be one
        parser = getattr(parsers, prompt['parser'])

        for run in range(prompt_config.get('runs', 1)):
            parameters = prompt_config['extra_parameters']

            for language in prompt_config.get('languages', ['English']):
                parameters['language'] = language
                prompt_text_template = prompt['text']

                print(f"\nStarting prompt: {prompt_config['hash']}\nRun: {run}\nLanguage: {language}")
                for dataset_name in prompt_config['datasets']:
                    df = pd.read_csv(os.path.join(config.base_path, dataset_name, 'data_split_by_length.csv'))
                    for _, row in tqdm(df.iterrows(), desc=dataset_name, total=len(df)):
                        parameters['context'] = row['text']
                        prompt_text = prompt_text_template.format(**parameters)
                        # The hash is of everything that is used to generate the output
                        h = hashlib.sha256(prompt_text.encode("utf-8"))
                        h.update(str(run).encode("utf-8"))
                        h = h.hexdigest()

                        # Only get the output if this was not done already
                        if h not in data.prompt_text_hash.values:
                            # Get output from OpenAI and parse using parser, the parser returns a list of strings.
                            #The parser will append references and everything else needed.
                            openai_output = ask_openai(prompt_text, config)
                            output = parser(openai_output, prompt_config, row, config) if openai_output is not None else None

                            # Parser will return None if there is a mistake in the ChatGPT output, we just skip those
                            if output is not None and len(output):
                                # Concat the current output to the data dataframe
                                new_data = pd.DataFrame([[text, dataset_name, language, run, prompt_config['hash'], h] for text in output], columns=data_columns)
                                data = pd.concat([data, new_data], ignore_index=True)

                                cnt += 1
                                if cnt % config.data_generation_checkpoint_every == 0:
                                    print("Checkpointing the generated dataset.")
                                    data.to_csv(data_path, index=False)
    # Final save
    data.to_csv(data_path, index=False)
    return data