enabled_services=$(gcloud services list --enabled --format="value(config.name)")

for service in $enabled_services; do
    echo "Disabling $service..."
    gcloud services disable $service --quiet
done
echo "Bulk disabling completed."
