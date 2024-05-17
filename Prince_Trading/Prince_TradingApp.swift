//
//  Prince_TradingApp.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-05.
//

import SwiftUI
import FirebaseCore

@main
struct Prince_TradingApp: App {
    
    init(){
        FirebaseApp.configure()
    }
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
