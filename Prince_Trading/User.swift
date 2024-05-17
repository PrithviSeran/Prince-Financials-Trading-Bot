//
//  User.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-06.
//

import Foundation

struct User: Codable {
    let id: String
    let name: String
    let email: String
    let accountId: String
    let joined: TimeInterval
}
