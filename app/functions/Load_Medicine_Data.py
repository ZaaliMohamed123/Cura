import pandas as pd
import os

def load_medicines():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Points to 'functions' folder 

    # Go up two levels to reach the root project folder, then into 'data'
    project_root = os.path.dirname(os.path.dirname(current_dir))  # Goes up from 'functions' to 'app', then to root 
  
    file_path = os.path.join(project_root, 'data', 'ref-des-medicaments-cnops-2014.xlsx')  # Builds path: root + 'data/medicines.xlsx' 
    
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Extract medicine names (assuming column name is 'MedicineName')
    medicines = df['NOM'].dropna().tolist()

    return medicines

