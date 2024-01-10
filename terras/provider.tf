# GCP Provider
provider "google"{
    credentials = file("terraforminfo.json")

    project = "testingpythonclouddep"
    region  = "us-central1"
}