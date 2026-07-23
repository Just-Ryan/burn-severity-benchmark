import SwiftUI

class AuthViewModel: ObservableObject {
    @Published var isAuthenticated = false
    @Published var isLoading = false
    @Published var errorMessage = ""
    @Published var showError = false
    
    func signIn(email: String, password: String) {
        isLoading = true
        
        // Simulate network delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
            guard let self = self else { return }
            // TODO: Implement actual authentication
            if !email.isEmpty && !password.isEmpty {
                self.isAuthenticated = true
            } else {
                self.errorMessage = "Invalid credentials"
                self.showError = true
            }
            self.isLoading = false
        }
    }
    
    func signUp(email: String, password: String, confirmPassword: String) {
        guard password == confirmPassword else {
            errorMessage = "Passwords don't match"
            showError = true
            return
        }
        
        isLoading = true
        
        // Simulate network delay
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
            guard let self = self else { return }
            // TODO: Implement actual registration
            if !email.isEmpty && !password.isEmpty {
                self.isAuthenticated = true
            } else {
                self.errorMessage = "Invalid input"
                self.showError = true
            }
            self.isLoading = false
        }
    }
    
    func signOut() {
        isAuthenticated = false
    }
} 