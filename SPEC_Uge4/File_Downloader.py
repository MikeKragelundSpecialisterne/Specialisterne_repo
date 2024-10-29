import kagglehub

# Download latest version
path = kagglehub.dataset_download("namigabbasov/consumer-complaint-dataset")

print("Path to dataset files:", path)