# Chicago Job Market Dashboard

A small project to analyze the Chicago job market using Python, Docker, and Tableau.

## Features
- Scrapes Chicago job listings (title, company, location, posted date, link)
- Cleans and stores data into a CSV
- Deployable pipeline with GitHub Actions + Docker
- Tableau dashboard showing trends

## Tech Stack
- Python (pandas, playwright)
- Docker
- GitHub Actions (CI/CD)
- Kubernetes (for container orchestration)
- Tableau (for visualization) (TBD)

## Setup

```bash
git clone https://github.com/camserr/job-board.git
cd job-board
pip install -r requirements.txt
python src/scraper.py
python src/clean_data.py
```

## Docker

Build and run the Docker container:

```bash
docker build -t job-scraper .
docker run --rm job-scraper
```

## Kubernetes

Deploy to a local Kubernetes cluster (e.g., Minikube):

1. Start Minikube:

```bash
minikube start
```

2. Apply the deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

3. Check pod status:

```bash
kubectl get pods
```

4. View logs:

```bash
kubectl logs <pod-name>
```

5. Optional: Open Minikube dashboard:

```bash
minikube dashboard
```

## CI/CD

The GitHub Actions pipeline builds and pushes the Docker image, and runs tests inside the container.

Make sure to add your Docker Hub credentials as GitHub secrets (`DOCKER_USERNAME` and `DOCKER_PASSWORD`).

---

For more details or help, please reach out!
