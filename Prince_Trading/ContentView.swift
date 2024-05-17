//
//  ContentView.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-05.
//

import SwiftUI

struct ContentView: View {
    @StateObject var viewModel = ContentViewViewModel()
    
    var body: some View {
        
        if viewModel.isSignedIn, !viewModel.currentUserId.isEmpty{
            //trading bot page
            
        } else {
            LoginView()
        }
        
    }
}

#Preview {
    ContentView()
}
