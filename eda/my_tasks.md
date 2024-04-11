# 0. Create training script for both models (POC's and enhanced)
- Adapt create_model.py script to train both model versions
- Set some arguments for this script to make it easier to use
- Create Makefile command for training

# 1. Create Kubernetes manifests
- Configure basic HPA

# 2. Create GitLab actions config
- Create jobs for testing, linting and Kubernetes deployment

# 3. Create slides
    - First version (simple)
    - Improve scalling with Keda
    - Improve demographic data retrieval with Redis
    - Improve MLOps 
        - Create proper training pipeline
        - Instantiate MLFlow
        - Configure experiment tracking
        - Configure Model Registry
        - Improve API loading model from MLFlow during build or during runtime
    - Further improve delivery using ArgoCD
    - Further improve API by using some ML framkework such as NVidia Triton