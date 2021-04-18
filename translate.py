# Reference: https://github.com/Wikidepia/indonesian_datasets/tree/master/paraphrase/paws

import pandas as pd
from google_trans_new import google_translator
import concurrent.futures as confu

input_data_path = "paraphrase_data/Quora_Paraphrasing_val.csv"
output_data_path = "paraphrase_data/ID_Quora_Paraphrasing_val.tsv"

try:
    translated_id = pd.read_csv(output_data_path,sep='\t',usecols=['id'])
    translated_id = translated_id['id'].astype(str).to_list()
    print(translated_id)
except Exception as e:
    print(e)
    translated_id = []


def translate(row):
    sentence1 = row["question1"]
    sentence2 = row["question2"]
    sentence_id = row['id']

    if str(sentence_id) not in translated_id:
        print(sentence_id)
        # Append all sentences and use separator to reduce API usage and prevent block from Google
        cat_sentence = sentence1 + " [<=>] " + sentence2
        translated_sentence = translator.translate(cat_sentence, lang_src="en", lang_tgt="id")
        translated_sentence = translated_sentence.split("[<=>]")
        print(translated_sentence)
        translated_datas = open(output_data_path, "a")

        translated_datas.write(f'{sentence_id}\t{translated_sentence[0].strip()}\t{translated_sentence[1].strip()}\n')

        return translated_sentence


if __name__ == "__main__":
    # Use rotating proxy to prevent "429 Too Many Request"
    # Find free proxy from here: https://free-proxy-list.net/
    translator = google_translator(
        proxies={"http": "203.150.113.93:8080", "https": "203.150.113.93:8080"}
        )
    df = pd.read_csv(input_data_path)  
    df['id'] = df.index

    if len(translated_id) == len(df):
        print('Done!')
    else:
        with confu.ThreadPoolExecutor(8) as executor:
            futures = [executor.submit(translate, row) for _, row in df.iterrows()]
            for future in confu.as_completed(futures):
                try:
                    pass
                except ValueError as e:
                    print(e)