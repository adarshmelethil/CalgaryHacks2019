

gcloud beta container \
--project "hackathon-19" \
clusters create "standard-cluster-1" \
--zone "us-central1-a" \
--username "admin" \
--cluster-version "1.11.6-gke.2" \
--machine-type "n1-standard-1" \
--image-type "COS" \
--disk-type "pd-standard" \
--disk-size "100" \
--scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" \
--num-nodes "1" \
--enable-cloud-logging \
--enable-cloud-monitoring \
--no-enable-ip-alias \
--network "projects/hackathon-19/global/networks/default" \
--subnetwork "projects/hackathon-19/regions/us-central1/subnetworks/default" \
--addons HorizontalPodAutoscaling,HttpLoadBalancing \
--no-enable-autoupgrade \
--no-enable-autorepair