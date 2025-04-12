🎌 Anime Recommendation System
A full-stack, production-ready hybrid anime recommendation system that combines content-based and collaborative filtering techniques. Built with Flask, Docker, Jenkins, and deployed on Google Cloud Platform (GCP) using Kubernetes. Features a modern UI, trailer previews, and personalized recommendations.

<!-- Replace with your actual architecture image path -->

🚀 Features
Hybrid Recommendation Engine: Combines content-based filtering (e.g., genres, synopsis) and collaborative filtering (user ratings) for accurate suggestions.

CI/CD Pipeline: Automated builds and deployments using Jenkins and Docker.

Data Version Control: Utilizes DVC to manage datasets and model versions.

Cloud Deployment: Scalable deployment on GCP with Kubernetes.

Interactive UI: Clean, responsive interface with trailer previews and anime posters.

Poster Strip Generator: Automatically generates anime poster strips for enhanced visuals.

🧠 Recommendation Model
The hybrid model integrates:

Content-Based Filtering: Uses TF-IDF vectorization on anime metadata (genres, synopsis) to find similar anime.

Collaborative Filtering: Employs user rating data to identify patterns and suggest anime liked by similar users.

This combination ensures personalized and diverse recommendations, addressing the cold-start problem effectively.

🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS, JavaScript

Machine Learning: Scikit-learn, Pandas, NumPy

Data Versioning: DVC

Containerization: Docker

CI/CD: Jenkins

Cloud Platform: Google Cloud Platform (GCP)

Orchestration: Kubernetes

⚙️ CI/CD Pipeline
The Jenkins pipeline automates the following steps:

Clone Repository: Fetches the latest code from GitHub.

Set Up Environment: Creates a virtual environment and installs dependencies.

Data Retrieval: Pulls datasets and models using DVC.

Build & Push Docker Image: Builds the Docker image and pushes it to Google Container Registry (GCR).

Deploy to Kubernetes: Applies Kubernetes configurations to deploy the application.

🚀 Deployment
To deploy the application manually:
kubectl apply -f deployment.yaml

![image](https://github.com/user-attachments/assets/ce98654b-9bc4-46d7-a331-252730c7711c)

📄 License
This project is licensed under the MIT License.

🙌 Acknowledgments
MyAnimeList for providing anime data.
Kaggle for additional datasets.
Scikit-learn for machine learning tools.
Thanking Krish Naik who helped me navigate me through this project by referring toh Krish Naik's MLOPS course
