import SwiftUI

struct AuthTextField: View {
    @Binding var text: String
    let placeholder: String
    let icon: String
    var isSecure: Bool = false
    
    var body: some View {
        HStack(spacing: 15) {
            Image(systemName: icon)
                .font(.system(size: 18))
                .foregroundStyle(Theme.gradientAccent)
            
            Group {
                if isSecure {
                    SecureField(placeholder, text: $text)
                } else {
                    TextField(placeholder, text: $text)
                }
            }
            .textInputAutocapitalization(.never)
            .autocorrectionDisabled()
        }
        .padding()
        .background(.ultraThinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Theme.gradientAccent.opacity(0.2), lineWidth: 1)
        )
    }
} 