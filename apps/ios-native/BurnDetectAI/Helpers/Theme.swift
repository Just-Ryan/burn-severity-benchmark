import SwiftUI

// Helper for hex colors
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 3: // RGB (12-bit)
            (a, r, g, b) = (255, (int >> 8) * 17, (int >> 4 & 0xF) * 17, (int & 0xF) * 17)
        case 6: // RGB (24-bit)
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB (32-bit)
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

struct Theme {
    // Base Colors
    static let primary = Color(hex: "1A1A2E")       // Dark blue background
    static let secondary = Color(hex: "16213E")     // Slightly lighter blue
    static let accent1 = Color(hex: "FF4C29")       // Bright orange/red
    static let accent2 = Color(hex: "C84B31")       // Darker orange
    static let accent3 = Color(hex: "ECDBBA")       // Light cream
    
    // Text Colors
    static let textPrimary = Color.white
    static let textSecondary = Color.white.opacity(0.7)
    static let textAccent = Color(hex: "FF4C29")    // Bright orange/red
    
    // Gradients
    static let gradientBackground = LinearGradient(
        colors: [
            primary,
            secondary
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
    
    static let gradientAccent = LinearGradient(
        colors: [accent1, accent2],
        startPoint: .leading,
        endPoint: .trailing
    )
    
    static let gradientButton = LinearGradient(
        colors: [
            accent1,
            accent2.opacity(0.8)
        ],
        startPoint: .leading,
        endPoint: .trailing
    )
    
    static let gradientCard = LinearGradient(
        colors: [
            secondary.opacity(0.5),
            secondary.opacity(0.2)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
    
    // Shadows
    static let shadowColor = Color.black.opacity(0.3)
    static let shadowRadius: CGFloat = 15
    static let shadowX: CGFloat = 0
    static let shadowY: CGFloat = 8
    
    // Card Style
    static func cardStyle<V: View>(_ content: V) -> some View {
        content
            .background(
                RoundedRectangle(cornerRadius: 20)
                    .fill(gradientCard)
                    .background(.ultraThinMaterial)
                    .clipShape(RoundedRectangle(cornerRadius: 20))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 20)
                    .stroke(accent1.opacity(0.3), lineWidth: 1)
            )
            .shadow(
                color: shadowColor,
                radius: shadowRadius,
                x: shadowX,
                y: shadowY
            )
    }
    
    // Button Style
    static func buttonStyle<V: View>(_ content: V) -> some View {
        content
            .background(gradientButton)
            .foregroundColor(.white)
            .clipShape(RoundedRectangle(cornerRadius: 15))
            .shadow(color: accent1.opacity(0.5), radius: 10, x: 0, y: 5)
    }
} 