
def file_to_str(file_name):
    with open(file_name, 'r') as file:
        a = file.read().replace('\n', "\\n")
    return a

def str_to_py(file_name,string):
    line="def string():\n"+\
            "    a="+"'"+string+"'"+\
            "\n    return a"
    file=open(file_name,"w")
    file.write(line)

def file_to_py(input_file_name,output_file_name):
    string=file_to_str(input_file_name)
    str_to_py(output_file_name,string)

def read_csv(dir_='./Trained_model'):
    suffixes=['','_gamma','_omega','_stability']
    
    #read csv
    for suffix in suffixes:
        input_file_name=dir_+'/NN'+suffix+'_norm_factor.csv'
        output_file_name=input_file_name[:-4]+'.py'
        file_to_py(input_file_name,output_file_name)

def read_weight(dir_='./Trained_model'):
    suffixes=['','_gamma','_omega','_stability']
    
    #read weight
    for suffix in suffixes:
        input_file_name=dir_+'/SLiM_NN'+suffix+'.h5'
        output_file_name=input_file_name[:-3]+'.py'
        file_to_py(input_file_name,output_file_name)

def read_model(dir_='./Trained_model'):
    read_csv(dir_)
    read_weight(dir_)

if __name__ == "__main__":
    read_model(dir_='./Trained_model')