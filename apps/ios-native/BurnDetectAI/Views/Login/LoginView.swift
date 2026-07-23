import SwiftUI

struct LoginView: View {
    @State private var email = ""
    @State private var password = ""
    @State private var showSignUp = false
    @State private var showForgotPassword = false
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Logo
                Image(systemName: "flame.fill")
                    .font(.system(size: 60))
                    .foregroundStyle(Theme.gradientAccent)
                    .padding(.bottom, 30)
                
                // Email Field
                TextField("Email", text: $email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                
                // Password Field
                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.password)
                
                // Login Button
                Button(action: {
                    // TODO: Implement login
                }) {
                    Text("Login")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Theme.gradientAccent)
                        .cornerRadius(10)
                }
                .padding(.top, 10)
                
                // Forgot Password
                Button("Forgot Password?") {
                    showForgotPassword = true
                }
                .foregroundColor(.blue)
                
                Spacer()
                
                // Sign Up
                HStack {
                    Text("Don't have an account?")
                    Button("Sign Up") {
                        showSignUp = true
                    }
                    .foregroundColor(.blue)
                }
            }
            .padding()
            .navigationTitle("Welcome Back")
            .sheet(isPresented: $showSignUp) {
                SignUpView()
            }
            .sheet(isPresented: $showForgotPassword) {
                ForgotPasswordView()
            }
        }
    }
}

struct SignUpView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var email = ""
    @State private var password = ""
    @State private var confirmPassword = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                TextField("Email", text: $email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                
                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.newPassword)
                
                SecureField("Confirm Password", text: $confirmPassword)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.newPassword)
                
                Button(action: {
                    // TODO: Implement sign up
                }) {
                    Text("Sign Up")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Theme.gradientAccent)
                        .cornerRadius(10)
                }
                .padding(.top, 10)
            }
            .padding()
            .navigationTitle("Create Account")
            .navigationBarItems(trailing: Button("Cancel") {
                dismiss()
            })
        }
    }
}

struct ForgotPasswordView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var email = ""
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Enter your email address and we'll send you a link to reset your password.")
                    .multilineTextAlignment(.center)
                    .padding(.bottom)
                
                TextField("Email", text: $email)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .textContentType(.emailAddress)
                    .keyboardType(.emailAddress)
                    .autocapitalization(.none)
                
                Button(action: {
                    // TODO: Implement password reset
                }) {
                    Text("Reset Password")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .frame(height: 50)
                        .background(Theme.gradientAccent)
                        .cornerRadius(10)
                }
            }
            .padding()
            .navigationTitle("Forgot Password")
            .navigationBarItems(trailing: Button("Cancel") {
                dismiss()
            })
        }
    }
}

#Preview {
    LoginView()
} 