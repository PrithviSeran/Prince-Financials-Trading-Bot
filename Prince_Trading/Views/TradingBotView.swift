//
//  TradingBotView.swift
//  Prince_Trading
//
//  Created by PrithviSeran on 2024-01-06.
//

import SwiftUI

struct TradingBotView: View {
    @State private var botStatus = false
    
    var body: some View {
        VStack{
            HeaderView(title: "Console",
                       subtitle: "",
                       angle: 0,
                       background: .yellow)
            
            Spacer()
            
           
            if botStatus{
                ZStack{
                    Rectangle()
                        .foregroundColor(.clear)
                        .frame(width: 170, height: 70.21739)
                        .background(
                            EllipticalGradient(
                                stops: [
                                    Gradient.Stop(color: Color(red: 0.5, green: 1, blue: 0.5), location: 1),
                                    Gradient.Stop(color: Color(red: 0.0, green: 0.75, blue: 0.0), location: 1.00),
                                ],
                                center: UnitPoint(x: -0.11, y: -0.23)
                            )
                        )
                        .cornerRadius(14.24631)
                        .shadow(color: Color(red: 0.94, green: 0.63, blue: 0.71).opacity(0.4), radius: 8.90394, x: 0, y: 4.74877)
                    
                    Text("Bot is Active")
                        .foregroundColor(Color.white)
                }
                .offset(y: -350)
                TLButton(title: "DeActivate Bot", background: .blue){
                    //attempt to log in
                    //activateBot()
                    //makeAPICall(URLroute: "")
                    botStatus = false
                    
                }
                .frame(height: 100)
                .offset(y: -300)
                
                
            } else {
                ZStack{
                    Rectangle()
                        .foregroundColor(.clear)
                        .frame(width: 170, height: 70.21739)
                        .background(
                            EllipticalGradient(
                                stops: [
                                    Gradient.Stop(color: Color(red: 1, green: 0.5, blue: 0.5), location: 1),
                                    Gradient.Stop(color: Color(red: 0.75, green: 0.0, blue: 0.0), location: 1.00),
                                ],
                                center: UnitPoint(x: -0.11, y: -0.23)
                            )
                        )
                        .cornerRadius(14.24631)
                        .shadow(color: Color(red: 0.94, green: 0.63, blue: 0.71).opacity(0.4), radius: 8.90394, x: 0, y: 4.74877)
                    
                    Text("Bot is Not Active")
                        .foregroundColor(Color.white)
                }
                .offset(y: -350)
                TLButton(title: "Activate Bot", background: .blue){
                    //attempt to log in
                    //activateBot()
                    //makeAPICall(URLroute: "")
                    botStatus = true
                    
                }
                .frame(height: 100)
                .offset(y: -300)
            }
        }
    }
}

#Preview {
    TradingBotView()
}
