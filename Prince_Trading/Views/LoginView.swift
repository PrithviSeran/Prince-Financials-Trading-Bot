//
//  LoginView.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-05.
//

import Foundation
import SwiftUI

struct LoginView: View {
    @StateObject var viewModel = LoginViewViewModel()
    
    var body: some View {
        NavigationView{
            VStack{
                HeaderView(title: "Prince Trading",
                           subtitle: "Become Royalty",
                           angle: 15,
                           background: .orange)
                
                Form{
                    if !viewModel.errorMessage.isEmpty {
                        Text(viewModel.errorMessage)
                            .foregroundStyle(Color.red)
                    }
                    
                    TextField("Email Address", text: $viewModel.email)
                        .textFieldStyle(DefaultTextFieldStyle())
                        .autocapitalization(/*@START_MENU_TOKEN@*/.none/*@END_MENU_TOKEN@*/)
                    SecureField("Password", text: $viewModel.password)
                        .textFieldStyle(DefaultTextFieldStyle())
                    
                    TLButton(title: "log in", background: .blue){
                        //attempt to log in
                        viewModel.login()
                    }
                }
                VStack{
                    Text("New Around Here?")
                    NavigationLink("Create An Account",
                    destination: RegisterView())
                }
                .padding(.bottom, 50)
                
                Spacer()
            }
        }
    }
}

struct LoginView_Previews: PreviewProvider{
    static var previews: some View{
        LoginView()
    }
}

