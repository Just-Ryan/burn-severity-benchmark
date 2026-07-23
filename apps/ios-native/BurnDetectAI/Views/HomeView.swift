import SwiftUI

struct HomeView: View {
    @EnvironmentObject private var viewModel: BurnDetectionViewModel
    @State private var showingProcessing = false
    @State private var showingResults = false
    @State private var showingInfo = false
    
    var body: some View {
        ZStack {
            // Enhanced gradient background with animated circles
            Theme.gradientBackground
                .ignoresSafeArea()
            
            GeometryReader { proxy in
                let size = proxy.size
                
                // Animated background elements
                Circle()
                    .fill(Theme.accent1.opacity(0.05))
                    .frame(width: size.width * 0.8)
                    .blur(radius: 50)
                    .offset(x: -size.width * 0.2, y: -size.height * 0.2)
                
                Circle()
                    .fill(Theme.accent3.opacity(0.05))
                    .frame(width: size.width * 0.9)
                    .blur(radius: 50)
                    .offset(x: size.width * 0.4, y: size.height * 0.4)
            }
            
            ScrollView {
                VStack(spacing: 30) {
                    // Header section
                    HStack {
                        VStack(alignment: .leading, spacing: 8) {
                            Text("BurnDetect")
                                .font(.system(size: 34, weight: .heavy))
                            Text("AI")
                                .font(.system(size: 30, weight: .bold))
                        }
                        .foregroundStyle(Theme.gradientAccent)
                        
                        Spacer()
                        
                        Button(action: { showingInfo = true }) {
                            Image(systemName: "info.circle.fill")
                                .font(.system(size: 24))
                                .foregroundStyle(Theme.gradientAccent)
                        }
                    }
                    .padding(.horizontal)
                    .padding(.top, 20)
                    
                    // Tagline
                    Text("Fast, AI-powered burn detection")
                        .font(.system(size: 16, weight: .medium))
                        .foregroundColor(.white.opacity(0.7))
                        .padding(.bottom, 20)
                    
                    // Image container with enhanced glass effect
                    VStack {
                        if let image = viewModel.selectedImage {
                            Image(uiImage: image)
                                .resizable()
                                .scaledToFit()
                                .frame(height: 300)
                                .clipShape(RoundedRectangle(cornerRadius: 25))
                        } else {
                            // Enhanced placeholder
                            VStack(spacing: 20) {
                                ZStack {
                                    Circle()
                                        .fill(.ultraThinMaterial)
                                        .frame(width: 100, height: 100)
                                    
                                    Image(systemName: "camera.viewfinder")
                                        .font(.system(size: 40))
                                        .foregroundStyle(Theme.gradientAccent)
                                }
                                
                                Text("Take or select a photo")
                                    .font(.headline)
                                    .foregroundColor(.white.opacity(0.8))
                                
                                Text("For best results, ensure good lighting\nand clear view of the affected area")
                                    .font(.caption)
                                    .foregroundColor(.white.opacity(0.6))
                                    .multilineTextAlignment(.center)
                            }
                            .frame(height: 300)
                        }
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 20)
                    .background(
                        RoundedRectangle(cornerRadius: 25)
                            .fill(.ultraThinMaterial)
                            .shadow(
                                color: Theme.accent1.opacity(0.2),
                                radius: 15,
                                x: 0,
                                y: 8
                            )
                    )
                    .overlay(
                        RoundedRectangle(cornerRadius: 25)
                            .stroke(Theme.gradientAccent.opacity(0.1), lineWidth: 1)
                    )
                    .padding(.horizontal)
                    
                    // Enhanced action buttons
                    VStack(spacing: 16) {
                        ActionButton(
                            icon: "camera.fill",
                            title: "Take Photo",
                            subtitle: "Use camera to capture",
                            gradient: [Theme.accent1, Theme.accent2]
                        ) {
                            viewModel.checkCameraAccess()
                        }
                        
                        ActionButton(
                            icon: "photo.on.rectangle",
                            title: "Choose Photo",
                            subtitle: "Select from library",
                            gradient: [Theme.accent2, Theme.accent3]
                        ) {
                            viewModel.showingImagePicker = true
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.bottom, 30)
            }
        }
        .sheet(isPresented: $showingInfo) {
            InfoView()
        }
        .sheet(isPresented: $viewModel.showingCamera) {
            ImagePicker(image: $viewModel.selectedImage, sourceType: .camera)
        }
        .sheet(isPresented: $viewModel.showingImagePicker) {
            ImagePicker(image: $viewModel.selectedImage, sourceType: .photoLibrary)
        }
        .fullScreenCover(isPresented: $showingProcessing) {
            ProcessingView()
        }
        .fullScreenCover(isPresented: $showingResults) {
            ResultView()
        }
        .onChange(of: viewModel.selectedImage) { oldValue, newValue in
            if newValue != nil {
                showingProcessing = true
            }
        }
        .onChange(of: viewModel.isProcessing) { oldValue, newValue in
            if !newValue && viewModel.processedImage != nil {
                showingResults = true
            }
        }
        .alert("Error", isPresented: $viewModel.showingError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(viewModel.errorMessage)
        }
    }
}

// Enhanced button style
struct ActionButton: View {
    let icon: String
    let title: String
    let subtitle: String
    let gradient: [Color]
    let action: () -> Void
    
    var body: some View {
        Button(action: action) {
            HStack(spacing: 15) {
                ZStack {
                    Circle()
                        .fill(.white.opacity(0.1))
                        .frame(width: 46, height: 46)
                    
                    Image(systemName: icon)
                        .font(.system(size: 20, weight: .semibold))
                }
                
                VStack(alignment: .leading, spacing: 2) {
                    Text(title)
                        .font(.system(size: 17, weight: .semibold))
                    Text(subtitle)
                        .font(.system(size: 13, weight: .medium))
                        .opacity(0.8)
                }
                
                Spacer()
                
                Image(systemName: "chevron.right")
                    .font(.system(size: 14, weight: .semibold))
                    .opacity(0.7)
            }
            .frame(maxWidth: .infinity)
            .padding(.horizontal, 20)
            .padding(.vertical, 16)
            .background(
                LinearGradient(colors: gradient, startPoint: .leading, endPoint: .trailing)
                    .opacity(0.8)
            )
            .foregroundColor(.white)
            .clipShape(RoundedRectangle(cornerRadius: 20))
            .shadow(color: gradient[0].opacity(0.3), radius: 8, x: 0, y: 4)
        }
    }
} 