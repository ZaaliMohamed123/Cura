# Cura - Medical Management System

MediMate is a comprehensive Flask-based web application designed for managing patient medications, pathologies, appointments, and providing drug-drug interaction (DDI) analysis using machine learning and AI. The system includes features for medication tracking, mentor-patient relationships, pharmacy management, and intelligent medication safety checks.

## 🌟 Features

- **User Management**: Patient and mentor registration with role-based access
- **Medication Management**: Add, edit, and track medications with dosage and frequency
- **Drug-Drug Interaction (DDI) Analysis**: AI-powered interaction detection using:
  - Local machine learning model with molecular fingerprints
  - Google Gemini AI for patient-friendly safety alerts
- **Pathology Tracking**: Manage and monitor patient medical conditions
- **Appointment Scheduling**: Schedule and manage medical appointments
- **Pharmacy Management**: Store and manage pharmacy information
- **Medication Reminders**: Set up automated medication reminders
- **Medication Logging**: Track medication intake and effects
- **Mentorship System**: Connect patients with mentors for support
- **Inspirational Quotes**: Daily motivational content for patient wellbeing

## 🏗️ Project Structure

```
MediMate/
├── app/
│   ├── app.py              # Flask application factory
│   ├── config.py           # Configuration settings
│   ├── models.py           # Database models (SQLAlchemy)
│   ├── routes.py           # Application routes
│   ├── run.py              # Application entry point
│   ├── .env                # Environment variables
│   ├── functions/          # Utility functions
│   │   ├── ddi_model_utilities.py    # DDI ML model utilities
│   │   ├── MedicineAutocomplete.py   # Medicine search autocomplete
│   │   ├── GetNextDoseTime.py        # Medication timing utilities
│   │   └── Load_Medicine_Data.py     # Medicine data loader
│   ├── instance/
│   │   └── MediMateDB.db   # SQLite database
│   ├── migrations/         # Database migration files
│   └── model/
│       └── ddi_mlp_model.pth # Pre-trained DDI ML model
├── data/
│   ├── inspiration.csv     # Inspirational quotes dataset
│   └── ref-des-medicaments-cnops-2014_translated_meds.csv # Medicine reference data
├── static/                 # CSS, JavaScript, images, fonts
├── templates/              # HTML templates
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Prerequisites

- **Python 3.8 or higher**
- **SQLite** (included with Python)
- **Git**
- **Google API Key** (it's free you can get your api key from https://aistudio.google.com/apikey)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ZaaliMohamed123/Cura.git
cd Cura
```

### 2. Create and Activate Virtual Environment

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

The application uses environment variables for configuration. A `.env` file is already included in the `app/` directory with default values:

```env
SECRET_KEY=fb4af99da33dc69ea80b9efcb73fcbaa62641683f8a1ef613d1f00911e473cf2
DATABASE_URL=sqlite:///./MediMateDB.db
GOOGLE_API_KEY="your_google_api_key_here"
```

**Important**: For production use, generate a new secret key:
```python
import secrets
print(secrets.token_hex(32))
```

### 5. Database Setup

Initialize the database with Flask-Migrate:

```bash
cd app
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the Application

```bash
python app/run.py
```

The application will be available at `http://127.0.0.1:5000/`

## 🔑 Key Dependencies

### Core Framework
- **Flask 3.1.0**: Web framework
- **Flask-SQLAlchemy 3.1.1**: Database ORM
- **Flask-Migrate 4.1.0**: Database migrations
- **Flask-Login 0.6.3**: User session management
- **Flask-Bcrypt 1.0.1**: Password hashing

### Machine Learning & AI
- **torch 2.7.0**: PyTorch for ML model
- **rdkit 2025.3.2**: Chemical informatics for molecular fingerprints
- **google-generativeai 0.8.5**: Google Gemini AI integration
- **numpy 2.2.6**: Numerical computing

### Data Processing
- **pandas 2.2.3**: Data manipulation
- **openpyxl 3.1.5**: Excel file processing
- **requests 2.32.3**: HTTP requests for external APIs

## 🧠 AI & Machine Learning Features

### Drug-Drug Interaction (DDI) Detection

MediMate uses a sophisticated two-tier approach for DDI analysis:

1. **Local ML Model**: 
   - Multi-layer perceptron (MLP) neural network
   - Uses Morgan molecular fingerprints from RDKit
   - Trained on drug interaction datasets
   - Provides probability scores for potential interactions

2. **AI-Enhanced Analysis**:
   - Google Gemini AI integration
   - Generates patient-friendly safety alerts
   - Provides contextual medical advice
   - Recommends consulting healthcare professionals

### Medicine Autocomplete

Advanced search functionality with:
- Prefix matching using trie data structure
- Substring matching for partial queries
- Fuzzy matching for typo tolerance
- Real-time suggestions from medicine database

## 🗃️ Database Schema

The application uses SQLAlchemy ORM with the following main models:

- **Users**: Patient and mentor information
- **Medications**: Medication details and prescriptions
- **Pathologies**: Medical conditions and diagnoses
- **Appointments**: Medical appointment scheduling
- **Pharmacies**: Pharmacy information
- **Mentorship**: Patient-mentor relationships
- **Medication_Reminders**: Automated reminders
- **Medication_Intake_Logging**: Medication tracking
- **AI_Adverse_Effect_Reports**: AI-generated safety reports

## 🔒 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **Session Management**: Flask-Login for user sessions
- **CSRF Protection**: Flask-Talisman for security headers
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 🌐 API Integration

### External APIs Used:
- **PubChem API**: For fetching molecular SMILES data
- **Google Generative AI**: For enhanced DDI analysis
- **Chemical Structure APIs**: For molecular fingerprint generation

## 🎨 Frontend Technologies

- **Bootstrap 5**: Responsive UI framework
- **Custom CSS**: Enhanced styling and animations
- **JavaScript**: Interactive features and AJAX requests
- **Boxicons**: Icon library for UI elements

## 📱 Usage Guide

### For Patients:
1. **Register** as a patient
2. **Add medications** with dosage and frequency
3. **Set up reminders** for medication times
4. **Track pathologies** and medical conditions
5. **Schedule appointments** with healthcare providers
6. **View DDI alerts** for medication safety
7. **Log medication intake** and effects

### For Mentors:
1. **Register** as a mentor
2. **Connect with patients** through mentorship system
3. **Monitor patient progress** and medication adherence
4. **Provide support** and guidance

## 🔧 Configuration Options

### Environment Variables:
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `GOOGLE_API_KEY`: Google AI API key (optional)

### Application Settings:
- Database: SQLite (default) or PostgreSQL/MySQL
- Debug mode: Enabled in development
- Host: 0.0.0.0 (accessible from network)
- Port: 5000 (default)

## 🚨 Troubleshooting

### Common Issues:

1. **Database Migration Errors**:
   ```bash
   flask db stamp head
   flask db migrate
   flask db upgrade
   ```

2. **Missing Dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Port Already in Use**:
   ```bash
   # Change port in app/run.py
   app.run(host='0.0.0.0', port=5001, debug=True)
   ```

4. **Google API Issues**:
   - Verify API key in `.env` file
   - Check API quotas and billing
   - DDI analysis will work with local model only if API fails

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

## ⚠️ Medical Disclaimer

**Important**: MediMate is a software tool designed to assist with medication management and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical decisions. The DDI analysis is for informational purposes only and should not be the sole basis for medication decisions.

## 🔮 Future Enhancements

- Mobile application development
- Integration with electronic health records (EHR)
- Advanced analytics and reporting
- Multi-language support
- Telemedicine integration
- Wearable device connectivity
- Enhanced AI models for drug interactions

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Developed with ❤️ for better healthcare management**
