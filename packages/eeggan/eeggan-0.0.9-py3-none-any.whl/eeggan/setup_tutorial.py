import pkg_resources
import shutil
import os

def setup_tutorial():
    
    def move_file(filename):
        #Find file within package
        stream = pkg_resources.resource_stream(__name__, filename)
        
        #Determine if folder exists within currentlocation
        if not os.path.exists(filename.split('/')[0]):
            os.mkdir(filename.split('/')[0]) #Create folder if it does not exist
            
        #Move file to folder
        shutil.copyfile(stream, os.getcwd() + filename)
        
    #Move the necessary files fo the tutorial
    move_file('data/gansEEGTrainingData.csv')
    move_file('data/gansEEGValidationData.csv')
    move_file('trained_models/gansEEGModel.pt')
    move_file('generated_samples/gansEEGSyntheticData.csv')