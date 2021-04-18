import re
import json

def convert_tsv_to_json(tsv_path='paraphrase_data/ID_Quora_Paraphrasing_train.tsv',
						json_path='paraphrase_data/ID_Quora_Paraphrasing_train.json'):

	temp_dict = {}
	with open(tsv_path,'r') as f:
		for line in f:
			line_list = line.split('\t')
			temp_dict[line_list[0]] = {}
			temp_dict[line_list[0]]['question_1'] = line_list[1]
			temp_dict[line_list[0]]['question_2'] = re.sub('\n','',line_list[2])


	with open(json_path,'w') as f_out:
		for key,values in temp_dict.items():
			json.dump(values,f_out)
			f_out.write('\n')


if __name__ == '__main__':
	convert_tsv_to_json(tsv_path='paraphrase_data/ID_Quora_Paraphrasing_val.tsv',
						json_path='paraphrase_data/ID_Quora_Paraphrasing_val.json')
