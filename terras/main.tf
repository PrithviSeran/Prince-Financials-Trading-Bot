resource "google_storage_bucket" "buffer" {
   name = "YOUR GOOGLE CLOUD STORAGE BUCKET NAME"
   location = "US"
}

resource "google_storage_bucket_object" "static_site_src"{
    name = "Trading_Bot.zip"
    source = "THE ABSOLUTE PATH OF THE ZIPPED FILE OF 'Files_to_be_Imported"
    bucket = google_storage_bucket.buffer.name
}
