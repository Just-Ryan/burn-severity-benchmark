import SwiftUI

struct InfoView: View {
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationStack {
            ZStack {
                Theme.gradientBackground
                    .ignoresSafeArea()
                
                ScrollView {
                    VStack(spacing: 30) {
                        // App Info Section
                        InfoSection(
                            title: "About BurnDetect AI",
                            content: "BurnDetect AI is an advanced medical imaging tool designed to assist healthcare professionals in burn assessment and classification.",
                            icon: "info.circle.fill"
                        )
                        
                        // Features Section
                        InfoSection(
                            title: "Key Features",
                            content: [
                                "AI-Powered Analysis",
                                "Real-time Burn Detection",
                                "Medical-Grade Accuracy",
                                "HIPAA Compliant",
                                "Secure Data Handling"
                            ],
                            icon: "star.fill"
                        )
                        
                        // Usage Section
                        InfoSection(
                            title: "How to Use",
                            content: [
                                "1. Take or select a photo",
                                "2. Ensure good lighting",
                                "3. Keep the burn area in focus",
                                "4. Wait for AI analysis",
                                "5. Review the results"
                            ],
                            icon: "questionmark.circle.fill"
                        )
                        
                        // Legal Section
                        InfoSection(
                            title: "Legal",
                            content: "For medical professional use only. This app is not intended to replace professional medical judgment. Always verify results with standard medical practices.",
                            icon: "doc.text.fill"
                        )
                        
                        // Version Info
                        Text("Version 1.0")
                            .font(.caption)
                            .foregroundColor(.white.opacity(0.6))
                            .padding(.top)
                    }
                    .padding()
                }
            }
            .navigationTitle("Information")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                    .foregroundStyle(Theme.gradientAccent)
                }
            }
        }
    }
}

// Helper view for info sections
struct InfoSection: View {
    let title: String
    let content: Any
    let icon: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 15) {
            HStack(spacing: 12) {
                Image(systemName: icon)
                    .font(.title2)
                    .foregroundStyle(Theme.gradientAccent)
                
                Text(title)
                    .font(.title3)
                    .fontWeight(.bold)
                    .foregroundColor(.white)
            }
            
            if let stringContent = content as? String {
                Text(stringContent)
                    .font(.body)
                    .foregroundColor(.white.opacity(0.8))
                    .fixedSize(horizontal: false, vertical: true)
            } else if let arrayContent = content as? [String] {
                VStack(alignment: .leading, spacing: 10) {
                    ForEach(arrayContent, id: \.self) { item in
                        Text(item)
                            .font(.body)
                            .foregroundColor(.white.opacity(0.8))
                    }
                }
            }
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 15))
        .overlay(
            RoundedRectangle(cornerRadius: 15)
                .stroke(Theme.gradientAccent.opacity(0.2), lineWidth: 1)
        )
    }
}

#Preview {
    InfoView()
} 