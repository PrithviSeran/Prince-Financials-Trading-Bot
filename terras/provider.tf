# GCP Provider
provider "google"{
    credentials = file("terraforminfo.json")

    project = "GOOGLE CLOUD PROJECT ID"
    region  = "us-central1"
}
