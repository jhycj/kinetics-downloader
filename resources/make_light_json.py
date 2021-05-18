import json 
import itertools 
import argparse 

def read_json_file(json_file): 
    with open(json_file, 'r') as f: 
        video_dict = json.load(f)     
    return video_dict 

def minimize_dict(video_dict, size): 

    video_dict = dict(itertools.islice(video_dict.items(), size))
    return video_dict


def filter_given_class(video_dict, classes): 
    
    new_dict = dict() 


    for key in video_dict.keys(): 
        metadata = video_dict[key] 
        annotations = metadata["annotations"] 
        for class_name  in classes: 
            if annotations["label"].lower() == class_name.lower():
                new_dict[key] = metadata
              
    return new_dict
 
def count_data_by_class(video_dict) : 

    ret_dict = dict()



    for key in video_dict.keys(): 
        metadata = video_dict[key] 
        annotations = metadata["annotations"] 
        class_name = annotations["label"].lower()  

        if class_name in ret_dict.keys(): 
            ret_dict[class_name] +=1
        else: 
            ret_dict[class_name] = 1 

    return ret_dict 


def main(parsed): 

    data_type = parsed.data_type
    classes = parsed.classes 
    #print(data_type) 
    #print(classes)
      
    video_dict = read_json_file(json_file=f'./kinetics_{data_type}.json')
    filtered_dict = filter_given_class(video_dict, classes)
    
    dict_size = len(list(filtered_dict.keys())) 
    #new_size = int(dict_size*1)

    output_dict = minimize_dict(filtered_dict, dict_size)  
    output_path = f'./small_kinetics_{data_type}.json' 

    with open(output_path, 'w') as of: 
        json.dump(output_dict, of, indent=4) 

    data_num_info = count_data_by_class(output_dict) 
    print(data_num_info) 
    

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description= 'custmoize dataset') 
    parser.add_argument('--classes', type=str, nargs='+', help= 'classes which you want to get') 
    parser.add_argument('--data_type', type=str, help = 'train or valid')  

    #data_type='train' 
    #classes = ['petting cat', 'robot dancing', 'playing chess']

    parsed = parser.parse_args()
    main(parsed)

