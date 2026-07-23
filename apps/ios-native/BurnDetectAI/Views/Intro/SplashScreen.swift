import SwiftUI

struct SplashScreen: View {
    @State private var isActive = false
    @State private var size = 0.7
    @State private var opacity = 0.3
    @State private var rotationAngle = -45.0
    
    var body: some View {
        if isActive {
            IntroScreen()
        } else {
            ZStack {
                Theme.gradientBackground
                    .ignoresSafeArea()
                
                // Animated background elements
                GeometryReader { proxy in
                    let size = proxy.size
                    
                    Circle()
                        .fill(Theme.accent1.opacity(0.1))
                        .frame(width: size.width * 0.8)
                        .blur(radius: 50)
                        .offset(x: -size.width * 0.2, y: -size.height * 0.2)
                    
                    Circle()
                        .fill(Theme.accent3.opacity(0.1))
                        .frame(width: size.width * 0.9)
                        .blur(radius: 50)
                        .offset(x: size.width * 0.4, y: size.height * 0.4)
                }
                
                VStack(spacing: 20) {
                    // Animated Logo
                    ZStack {
                        ForEach(0..<3) { index in
                            Circle()
                                .stroke(Theme.gradientAccent, lineWidth: 2)
                                .frame(width: 160 + CGFloat(index * 20),
                                       height: 160 + CGFloat(index * 20))
                                .opacity(0.5 - Double(index) * 0.15)
                                .rotationEffect(.degrees(rotationAngle))
                        }
                        
                        Circle()
                            .fill(.ultraThinMaterial)
                            .frame(width: 160, height: 160)
                        
                        Image(systemName: "flame.fill")
                            .font(.system(size: 70))
                            .foregroundStyle(Theme.gradientAccent)
                    }
                    .scaleEffect(size)
                }
                .opacity(opacity)
            }
            .onAppear {
                withAnimation(.easeOut(duration: 1.2)) {
                    self.size = 1.0
                    self.opacity = 1.0
                }
                
                withAnimation(.linear(duration: 4).repeatForever(autoreverses: false)) {
                    self.rotationAngle = 315
                }
                
                DispatchQueue.main.asyncAfter(deadline: .now() + 2.0) {
                    withAnimation(.easeInOut(duration: 0.7)) {
                        self.isActive = true
                    }
                }
            }
        }
    }
} 