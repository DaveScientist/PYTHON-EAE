from functions import load_files, test_results
import os 

os.chdir(os.path.dirname(__file__))
os.chdir(os.getcwd()+'/trabajos')

for archivo in os.listdir():
    if archivo[-3:] == 'zip':
        my_model0, df_test, info = load_files(os.getcwd()+'/'+archivo)
        test_results(my_model0, df_test, info)




