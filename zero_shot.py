
import json
from tqdm import tqdm
from transformers import pipeline, AutoModelWithLMHead, AutoTokenizer
from tqdm import tqdm
import torch
import os
torch.cuda.is_available()

def remove_bad(sentence,symbol):
    end_sentence = ''
    try:
        sentence_list = sentence.split(symbol)
        for tmp_sentence in sentence_list:
            end_sentence =end_sentence + tmp_sentence
    except:
        pass
    return end_sentence
def get_complete_sentence(sentence):
    
    remove_list = ['\n','&#8217','<br/>']
    
    for sample in remove_list:
        end_sentence = remove_bad(sentence,sample)
    return end_sentence
def use_zero_classification(en_list,user_input,classifier):
    all_results = {}
    all_results[user_input] = {}
    for sample in tqdm(en_list):
        results = classifier(sample, user_input)
        all_results[results['labels'][0]][results['sequence']] = results['scores'][0] 
    
    tmp_sample = all_results[user_input]
    tmp_sort_sample = sorted(tmp_sample.items(),key = lambda item:item[1],reverse=True)
    all_results[user_input] = tmp_sort_sample
    
    return all_results

def remove_douhao(sample):
    sentence = ''
    tmp_list = sample.split(',')
    for index in range(0,len(tmp_list)):
        sentence = sentence +' '+ tmp_list[index]       
    return sentence


def sort_get_sentence(user_input,classifier,topk):
    json_path = '/cloud/cloud_disk/users/huh/nlp/smart_home/script/yiya/cope_dataset/yiya_review.json'
    with open(json_path, 'r') as f:
        json_data = json.load(f)
    reviews_list = json_data['reviews']
    en_to_ch = {}
    en_list = []
    reviews_list = json_data['reviews']
    for product in reviews_list:
        reviews = product['reviews']
        for tmp_sample in reviews:
            en_title = tmp_sample['en_title']
            en_content = tmp_sample['en_content']   
            en_sentence = en_title +'     '+ en_content
            en_sentence = remove_douhao(en_sentence)
            ch_sentence = tmp_sample['ch_title'] + tmp_sample['ch_content']
            en_to_ch[en_sentence] = ch_sentence
            en_list.append(en_sentence)

    tmp_results = use_zero_classification(en_list,user_input,classifier)
    num = 0
    end_results = {}
    for sample in tmp_results[user_input]:
        num+=1
        if num>10:
            break
        else:
            end_results[sample[0]] = sample[1]

    return end_results


# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli",device = 1)
# end_results = sort_get_sentence('quality',classifier,10)
# print(len(end_results))