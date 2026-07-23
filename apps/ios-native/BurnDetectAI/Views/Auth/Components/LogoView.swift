import SwiftUI

struct LogoView: View {
    var body: some View {
        VStack(spacing: 25) {
            ZStack {
                Circle()
                    .fill(.ultraThinMaterial)
                    .frame(width: 120, height: 120)
                
                Circle()
                    .stroke(Theme.gradientAccent, lineWidth: 2)
                    .frame(width: 120, height: 120)
                
                Image(systemName: "flame.fill")
                    .font(.system(size: 50))
                    .foregroundStyle(Theme.gradientAccent)
            }
            .shadow(color: Theme.accent1.opacity(0.3), radius: 20)
            
            VStack(spacing: 8) {
                Text("BurnDetect")
                    .font(.system(size: 36, weight: .heavy))
                Text("AI")
                    .font(.system(size: 32, weight: .bold))
            }
            .foregroundStyle(Theme.gradientAccent)
        }
    }
} 