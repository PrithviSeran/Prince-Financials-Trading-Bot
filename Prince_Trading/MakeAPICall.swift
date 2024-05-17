//
//  MakeAPICall.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-06.
//

import Foundation

func makeAPICall(URLroute: String) {
    guard let url = URL(string: URLroute) else {
        print("Invalid URL")
        return
    }

    var request = URLRequest(url: url)
    request.httpMethod = "GET"

    let task = URLSession.shared.dataTask(with: request) { data, response, error in
        if let error = error {
            print("Error: \(error)")
            return
        }

        guard let data = data else {
            print("No data received")
            return
        }

        if let resultString = String(data: data, encoding: .utf8) {
            print("API Response: \(resultString)")
        } else {
            print("Failed to convert data to string")
        }
    }

    task.resume()
}
