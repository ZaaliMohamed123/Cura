import torch
import torch.nn as nn
import torch.nn.functional as F
import requests
import numpy as np
from rdkit import Chem
from rdkit.Chem.AllChem import GetMorganGenerator
import os
from dotenv import load_dotenv
import google.generativeai as genai

# --- Your Local ML Model Definition ---
class DDI_MLP(nn.Module):
    def __init__(self):
        super(DDI_MLP, self).__init__()
        self.fc1 = nn.Linear(2048, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.dropout1 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(512, 128)
        self.bn2 = nn.BatchNorm1d(128)
        self.dropout2 = nn.Dropout(0.3)
        self.out = nn.Linear(128, 1)

    def forward(self, x):
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.out(x)
        return torch.sigmoid(x).squeeze(1)

# --- Initialize Morgan fingerprint generator ---
morgan_gen = GetMorganGenerator(radius=2, fpSize=1024)

# --- Load your local ML model ---
# IMPORTANT: Adjust the path if 'funtions' is not in the same root as a 'model' dir
# Assuming your Flask app.py is in the root, and you have:
# root/
# |- app.py
# |- funtions/
# |  |- ddi_model_utilities.py
# |- model/
# |  |- ddi_mlp_model.pth

# Construct the path to the model relative to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
model_path = os.path.join(project_root, 'model', 'ddi_mlp_model.pth')

model = DDI_MLP() # This is your local model instance
if os.path.exists(model_path):
    try:
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        print("Loaded pre-trained local DDI model.")
    except Exception as e:
        print(f"Error loading local DDI model: {e}. Using a randomly initialized model.")
else:
    print(f"Local DDI model file not found at {model_path}. Using a randomly initialized model.")
model.eval()


# --- LLM Configuration ---
load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('GOOGLE_API_KEY')
llm_model = None
if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        llm_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        print("Google Generative AI SDK configured successfully with gemini-1.5-flash-latest.")
    except Exception as e:
        print(f"Error configuring Google Generative AI SDK: {e}")
else:
    print("GOOGLE_API_KEY not found. LLM DDI checks will be skipped.")


def get_smiles(drug_name):
    safe_drug_name = requests.utils.quote(drug_name)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{safe_drug_name}/property/IsomericSMILES/TXT"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SMILES for {drug_name}: {e}")
    return None

def smiles_to_fp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"Could not parse SMILES: {smiles}")
        return None
    fp = morgan_gen.GetFingerprint(mol)
    return np.array(fp, dtype=np.int8)

def predict_interaction_with_local_model(drug_name1, drug_name2, local_ml_model_instance, threshold=0.35):
    smiles1 = get_smiles(drug_name1)
    smiles2 = get_smiles(drug_name2)
    if not smiles1: return "SMILES Error", 0.0, f"Could not get SMILES for {drug_name1}."
    if not smiles2: return "SMILES Error", 0.0, f"Could not get SMILES for {drug_name2}."

    fp1 = smiles_to_fp(smiles1)
    fp2 = smiles_to_fp(smiles2)
    if fp1 is None: return "FP Error", 0.0, f"Fingerprint failed for {drug_name1}."
    if fp2 is None: return "FP Error", 0.0, f"Fingerprint failed for {drug_name2}."

    combined_fp = np.concatenate((fp1, fp2))
    combined_fp_tensor = torch.FloatTensor(combined_fp).unsqueeze(0)
    with torch.no_grad():
        probability = local_ml_model_instance(combined_fp_tensor).item()
    prediction_label = "Interaction" if probability > threshold else "No Interaction"
    return prediction_label, probability, None

def get_patient_friendly_ddi_alert(drug1_name, drug2_name, local_model_prediction, local_model_confidence):
    if not llm_model:
        return f"Note: Advanced AI check for {drug1_name} and {drug2_name} is currently unavailable."

    # Refined prompt for patient-friendly output
    prompt = f"""
    A patient is taking {drug1_name} and {drug2_name}.
    A basic computer model predicted: "{local_model_prediction}" with a confidence of {local_model_confidence:.2f}.

    Based on established medical knowledge, is there a significant interaction between {drug1_name} and {drug2_name} that this patient should be aware of?

    If YES, provide a brief, easy-to-understand alert for the patient (1-2 sentences). Start with "Alert:" or "Important:"
    Explain the potential risk in simple terms and strongly advise them to discuss this combination with their doctor or pharmacist. Do NOT give medical advice beyond telling them to consult a professional.

    If NO significant interaction is generally expected, or if the interaction is minor and generally managed, state that clearly and briefly. For example: "Good news: {drug1_name} and {drug2_name} are generally considered safe to take together, but always follow your doctor's advice."

    Focus on clarity and directness for a patient. Avoid overly technical jargon.
    Example of a good alert: "Alert: Taking {drug1_name} and {drug2_name} together might increase [simple risk, e.g., 'drowsiness' or 'bleeding risk']. Please talk to your doctor or pharmacist about this combination soon."
    """
    try:
        response = llm_model.generate_content(prompt)
        # Simple cleaning: remove potential markdown or extra newlines from LLM response
        patient_message = response.text.strip().replace("*","")
        return patient_message
    except Exception as e:
        print(f"Error querying LLM for patient alert ({drug1_name}, {drug2_name}): {e}")
        return f"Important: We recommend discussing the combination of {drug1_name} and {drug2_name} with your doctor, as an advanced check could not be completed."