//
//  RegisterView.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-05.
//

import SwiftUI

struct RegisterView: View {
    @StateObject var viewModel = RegisterViewViewModel()
    @State private var showInfo = false
    
    
    var body: some View {

        VStack{
            HeaderView(title: "Register Now",
                       subtitle: "Start Earning",
                       angle: -15,
                       background: .orange
            )
            
            Form{
                TextField("Full Name", text: $viewModel.name)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocorrectionDisabled()
                TextField("Email Address", text: $viewModel.email)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocapitalization(/*@START_MENU_TOKEN@*/.none/*@END_MENU_TOKEN@*/)
                    .autocorrectionDisabled()
                SecureField("Password", text: $viewModel.password)
                    .textFieldStyle(DefaultTextFieldStyle())
                TextField("Oanda Account ID", text: $viewModel.accountId)
                    .textFieldStyle(DefaultTextFieldStyle())
                    .autocapitalization(/*@START_MENU_TOKEN@*/.none/*@END_MENU_TOKEN@*/)
                    .autocorrectionDisabled()
                Button("Done have an Oanda Account ID?") {
                    showInfo = true
                }
                .alert(isPresented: $showInfo) {
                    Alert(
                        title: Text("Create an Oanda Trading account"),
                        message: Text("To start using Prince Trading, please create a trading account in Oanda and please enter the account ID."),
                        dismissButton: .default(Text("OK"))
                    )
                }
            
                TLButton(
                    title: "Next",
                    background: .green
                ) {
                    viewModel.register()
                        
                }
            }.offset(y: -50)
            
            Spacer()
            
        }
    }
}

#Preview {
    RegisterView()
}
