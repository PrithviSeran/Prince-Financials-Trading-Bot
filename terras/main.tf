resource "google_storage_bucket" "buffer" {
   name = "lets_test_twice"
   location = "US"
}

resource "google_storage_bucket_object" "static_site_src"{
    name = "Trading_Bot.zip"
    source = "/Users/prithviseran/Documents/Forex_Trading_Bot_Server/Trading_Bot.zip"
    bucket = google_storage_bucket.buffer.name
}
