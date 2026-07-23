import SwiftUI

struct ProcessingView: View {
    @EnvironmentObject private var viewModel: BurnDetectionViewModel
    @Environment(\.dismiss) private var dismiss
    @State private var animationAmount = 1.0
    
    var body: some View {
        ZStack {
            // Animated gradient background
            Theme.gradientBackground
                .ignoresSafeArea()
            
            // Content
            VStack(spacing: 25) {
                // Custom loading animation
                ZStack {
                    Circle()
                        .stroke(
                            .linearGradient(
                                colors: [
                                    .white.opacity(0.2),
                                    .white.opacity(0.5)
                                ],
                                startPoint: .top,
                                endPoint: .bottom
                            ),
                            lineWidth: 8
                        )
                        .frame(width: 80, height: 80)
                    
                    Circle()
                        .trim(from: 0, to: 0.7)
                        .stroke(
                            Theme.gradientAccent,
                            style: StrokeStyle(
                                lineWidth: 8,
                                lineCap: .round
                            )
                        )
                        .frame(width: 80, height: 80)
                        .rotationEffect(Angle(degrees: animationAmount * 360))
                }
                
                VStack(spacing: 15) {
                    Text("Analyzing Image")
                        .font(.title2)
                        .fontWeight(.bold)
                        .foregroundColor(.white)
                    
                    Text("Using AI to detect and classify burn severity")
                        .font(.subheadline)
                        .foregroundColor(.white.opacity(0.8))
                        .multilineTextAlignment(.center)
                }
            }
            .padding(40)
            .background(.ultraThinMaterial)
            .clipShape(RoundedRectangle(cornerRadius: 30))
            .shadow(color: .black.opacity(0.2), radius: 20)
        }
        .onAppear {
            withAnimation(
                .linear(duration: 2)
                .repeatForever(autoreverses: false)
            ) {
                animationAmount = 2
            }
            viewModel.processImage()
        }
        .onChange(of: viewModel.isProcessing) { oldValue, newValue in
            if !newValue {
                dismiss()
            }
        }
    }
} 