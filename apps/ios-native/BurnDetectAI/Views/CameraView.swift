import SwiftUI
import AVFoundation

struct CameraView: View {
    @StateObject private var cameraManager = CameraManager()
    @State private var showResult = false
    @State private var burnResult: BurnResult?
    @State private var isProcessing = false
    @State private var errorMessage: String?
    
    var body: some View {
        ZStack {
            CameraPreview(session: cameraManager.session)
                .ignoresSafeArea()
            
            VStack {
                if isProcessing {
                    ProgressView("Analyzing burn...")
                        .padding()
                        .background(.ultraThinMaterial)
                        .cornerRadius(10)
                }
                
                if let error = errorMessage {
                    Text(error)
                        .foregroundColor(.red)
                        .padding()
                        .background(.ultraThinMaterial)
                        .cornerRadius(10)
                }
                
                Spacer()
                
                Button(action: {
                    captureAndAnalyze()
                }) {
                    Image(systemName: "camera.circle.fill")
                        .font(.system(size: 72))
                        .foregroundColor(.white)
                }
                .padding(.bottom, 30)
                .disabled(isProcessing)
            }
        }
        .sheet(isPresented: $showResult) {
            if let result = burnResult {
                BurnResultView(result: result)
            }
        }
        .onAppear {
            cameraManager.checkPermissions()
        }
    }
    
    private func captureAndAnalyze() {
        isProcessing = true
        errorMessage = nil
        
        cameraManager.capturePhoto { image in
            guard let image = image else {
                errorMessage = "Failed to capture image"
                isProcessing = false
                return
            }
            
            // Convert image to JPEG data
            guard let imageData = image.jpegData(compressionQuality: 0.8) else {
                errorMessage = "Failed to process image"
                isProcessing = false
                return
            }
            
            // Create multipart form data
            let boundary = UUID().uuidString
            var request = URLRequest(url: URL(string: "http://localhost:5000/analyze")!)
            request.httpMethod = "POST"
            request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
            
            var body = Data()
            
            // Add image data
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"image\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
            body.append(imageData)
            body.append("\r\n".data(using: .utf8)!)
            body.append("--\(boundary)--\r\n".data(using: .utf8)!)
            
            request.httpBody = body
            
            // Send request
            URLSession.shared.dataTask(with: request) { data, response, error in
                DispatchQueue.main.async {
                    isProcessing = false
                    
                    if let error = error {
                        errorMessage = "Network error: \(error.localizedDescription)"
                        return
                    }
                    
                    guard let data = data else {
                        errorMessage = "No data received"
                        return
                    }
                    
                    do {
                        let result = try JSONDecoder().decode(BurnAnalysisResponse.self, from: data)
                        burnResult = BurnResult(
                            severity: result.severity,
                            confidence: result.confidence,
                            timestamp: Date()
                        )
                        showResult = true
                    } catch {
                        errorMessage = "Failed to parse response: \(error.localizedDescription)"
                    }
                }
            }.resume()
        }
    }
}

class CameraManager: ObservableObject {
    @Published var session = AVCaptureSession()
    private var photoOutput = AVCapturePhotoOutput()
    
    func checkPermissions() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            setupCamera()
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
                if granted {
                    DispatchQueue.main.async {
                        self?.setupCamera()
                    }
                }
            }
        default:
            break
        }
    }
    
    private func setupCamera() {
        guard let device = AVCaptureDevice.default(.builtInWideAngleCamera, for: .video, position: .back),
              let input = try? AVCaptureDeviceInput(device: device) else {
            return
        }
        
        if session.canAddInput(input) {
            session.addInput(input)
        }
        
        if session.canAddOutput(photoOutput) {
            session.addOutput(photoOutput)
        }
        
        DispatchQueue.global(qos: .userInitiated).async {
            self.session.startRunning()
        }
    }
    
    func capturePhoto(completion: @escaping (UIImage?) -> Void) {
        let settings = AVCapturePhotoSettings()
        photoOutput.capturePhoto(with: settings, delegate: PhotoCaptureDelegate(completion: completion))
    }
}

struct CameraPreview: UIViewRepresentable {
    let session: AVCaptureSession
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView(frame: UIScreen.main.bounds)
        let previewLayer = AVCaptureVideoPreviewLayer(session: session)
        previewLayer.frame = view.frame
        previewLayer.videoGravity = .resizeAspectFill
        view.layer.addSublayer(previewLayer)
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {}
}

class PhotoCaptureDelegate: NSObject, AVCapturePhotoCaptureDelegate {
    private let completion: (UIImage?) -> Void
    
    init(completion: @escaping (UIImage?) -> Void) {
        self.completion = completion
    }
    
    func photoOutput(_ output: AVCapturePhotoOutput, didFinishProcessingPhoto photo: AVCapturePhoto, error: Error?) {
        if let error = error {
            print("Error capturing photo: \(error.localizedDescription)")
            completion(nil)
            return
        }
        
        guard let imageData = photo.fileDataRepresentation(),
              let image = UIImage(data: imageData) else {
            completion(nil)
            return
        }
        
        completion(image)
    }
}

struct BurnResultView: View {
    let result: BurnResult
    @Environment(\.dismiss) private var dismiss
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Image(systemName: "exclamationmark.triangle.fill")
                    .font(.system(size: 60))
                    .foregroundColor(.orange)
                
                Text("Burn Detected")
                    .font(.title)
                    .bold()
                
                Text("Severity: \(result.severity.description)")
                    .font(.headline)
                
                Text("Confidence: \(Int(result.confidence * 100))%")
                    .font(.subheadline)
                
                Text("Timestamp: \(result.timestamp.formatted())")
                    .font(.subheadline)
                
                Spacer()
                
                Button("Close") {
                    dismiss()
                }
                .buttonStyle(.borderedProminent)
                .padding()
            }
            .padding()
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                }
            }
        }
    }
}

// Preview with camera preview
struct CameraView_Previews: PreviewProvider {
    static var previews: some View {
        CameraView()
            .previewDisplayName("Camera View")
    }
}

#Preview {
    CameraView()
} 