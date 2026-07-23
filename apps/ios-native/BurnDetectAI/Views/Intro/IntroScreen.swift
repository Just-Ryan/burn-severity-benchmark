import SwiftUI

struct IntroScreen: View {
    @State private var currentPage = 0
    @State private var showMainApp = false
    
    let pages = [
        IntroPage(
            title: "AI-Powered Analysis",
            description: "Advanced burn detection using state-of-the-art artificial intelligence",
            icon: "wand.and.stars"
        ),
        IntroPage(
            title: "Medical Grade Accuracy",
            description: "Precise burn classification to assist medical professionals",
            icon: "cross.case.fill"
        ),
        IntroPage(
            title: "Instant Results",
            description: "Get immediate analysis and classification of burn severity",
            icon: "bolt.fill"
        ),
        IntroPage(
            title: "HIPAA Compliant",
            description: "Secure and private handling of all medical data",
            icon: "lock.shield.fill"
        )
    ]
    
    var body: some View {
        ZStack {
            Theme.gradientBackground
                .ignoresSafeArea()
            
            VStack(spacing: 0) {
                // Logo Section
                LogoView()
                    .padding(.top, 60)
                
                // Carousel
                TabView(selection: $currentPage) {
                    ForEach(0..<pages.count, id: \.self) { index in
                        IntroPageView(page: pages[index])
                            .tag(index)
                    }
                }
                .tabViewStyle(.page(indexDisplayMode: .always))
                .frame(height: 400)
                
                // Buttons
                VStack(spacing: 16) {
                    Button(action: {
                        withAnimation {
                            showMainApp = true
                        }
                    }) {
                        Text("Get Started")
                            .font(.title3)
                            .fontWeight(.semibold)
                            .frame(maxWidth: .infinity)
                            .frame(height: 56)
                            .background(Theme.gradientAccent)
                            .foregroundColor(.white)
                            .clipShape(RoundedRectangle(cornerRadius: 16))
                    }
                    
                    // Version info
                    Text("Version 1.0")
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.6))
                }
                .padding(.horizontal, 30)
                .padding(.bottom, 30)
            }
        }
        .fullScreenCover(isPresented: $showMainApp) {
            ContentView()
        }
    }
}

// Helper types
struct IntroPage: Identifiable {
    let id = UUID()
    let title: String
    let description: String
    let icon: String
}

struct IntroPageView: View {
    let page: IntroPage
    
    var body: some View {
        VStack(spacing: 30) {
            ZStack {
                Circle()
                    .fill(.ultraThinMaterial)
                    .frame(width: 100, height: 100)
                
                Image(systemName: page.icon)
                    .font(.system(size: 40))
                    .foregroundStyle(Theme.gradientAccent)
            }
            
            VStack(spacing: 12) {
                Text(page.title)
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
                
                Text(page.description)
                    .font(.body)
                    .multilineTextAlignment(.center)
                    .foregroundColor(.white.opacity(0.8))
                    .padding(.horizontal)
            }
        }
    }
}

#Preview {
    IntroScreen()
} 