import joblib
import os
from django.conf import settings

class SalaryPredictor:
    def __init__(self):
        try:
            model_path = os.path.join(settings.BASE_DIR, 'static', 'models', 'ai_salaryprediction')
            self.model = joblib.load(os.path.join(model_path, 'salary_prediction_model.joblib'))
            self.encoders = joblib.load(os.path.join(model_path, 'label_encoders.joblib'))
        except Exception as e:
            print(f"Error cargando los modelos: {str(e)}")
            print(f"Ruta buscada: {model_path}")
            raise
    
    def predict(self, experience_level, job_title, company_location, company_size):
        try:
            # Codificar las entradas en el orden correcto
            job_encoded = self.encoders['job'].transform([job_title])[0]
            size_encoded = self.encoders['size'].transform([company_size])[0]
            loc_encoded = self.encoders['location'].transform([company_location])[0]
            exp_encoded = self.encoders['experience'].transform([experience_level])[0]
            
            # Hacer la predicción
            features = [[job_encoded, size_encoded, loc_encoded, exp_encoded]]
            predicted_salary = self.model.predict(features)[0]
            
            return float(predicted_salary * 1000)  # Convertir a salario anual
        except Exception as e:
            raise ValueError(f"Error en la predicción: {str(e)}")

# Crear instancia global
predictor = SalaryPredictor()