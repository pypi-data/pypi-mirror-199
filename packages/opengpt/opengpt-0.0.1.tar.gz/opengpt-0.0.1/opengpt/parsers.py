import pandas as pd
from io import StringIO
import re

def csv_parser(data, prompt_config, row, config):
    r''' Try to load the output into a dataframe, if it fails we skip.
    '''
    answer = None
    try:
        df = pd.read_csv(StringIO(data), sep=';;;;', engine='python')
    except Exception as e:
        print("Skipping an example as the output could not be parsed.")
        print(e)

    if df is not None and all([col in df.columns for col in ['ID', 'Question', 'Answer']]):
        # Strip everything
        df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        ref_col = prompt_config.get('reference_column_to_append', None)
        if ref_col and ref_col in row and row[ref_col]:
            # Means we want to append a reference at the end of each Answer
            to_append = f"\nReferences:\n- {row[ref_col]}"
            df['Answer'] = df['Answer'] + to_append
        df['Question'] += f' {config.special_tokens.eos}' # Every Q/A pair is independent
        df['Answer'] += f' {config.special_tokens.eos} {config.special_tokens.eod}'
        answer = [f'{config.special_tokens.user} {q.strip()} {config.special_tokens.ai} {a.strip()}' for q,a in df[['Question', 'Answer']].values]

    elif df is not None:
        print("The dataframe did not have all the required columns.")
        print("Dataframe size: ", len(df))
        print("Dataframe columns: ", df.columns)

    return answer


def medical_conversation_parser(data, prompt_config, row, config):
    answer = None

    # Merge the extractions into one conversation
    if data:
        # I'm sure there is a better way to split the output
        data = re.findall(r'(Patient:|AI-Assistant:) (.+(\n.+)*)', data)
        if len(data) > 0:
            answer = ""
            to_append = None

            ref_col = prompt_config.get('reference_column_to_append', None)
            if ref_col and ref_col in row and row[ref_col]:
                # Means we want to append a reference at the end of each Answer
                to_append = f"\nReferences:\n- {row[ref_col]}"

            for pieces in data:
                if pieces[0] == 'Patient:' and len(pieces) > 1:
                    answer += f'{config.special_tokens.user} {pieces[1].strip()}'
                elif pieces[0] == 'AI-Assistant:' and len(pieces) > 1:
                    answer += f'{config.special_tokens.ai} {pieces[1].strip()}'
                    if to_append is not None and to_append:
                        answer += to_append
                else:
                    print("Skipping a generated example because it does not have the correct actors.")
                    print(pieces)
                    answer = None
                    break
                answer += f" {config.special_tokens.eos} "
            if answer:
                # Make into an array, as parsers have to return arrays
                answer = answer.strip() + f" {config.special_tokens.eod}"
                answer = [answer.strip()]
    return answer