import SwiftUI
import AVFoundation

class BurnDetectionViewModel: ObservableObject {
    @Published var selectedImage: UIImage?
    @Published var processedImage: UIImage?
    @Published var visualizationImage: UIImage?
    @Published var probabilityChart: UIImage?
    @Published var classificationResult: String?
    @Published var confidenceScore: Double?
    @Published var treatmentAdvice: [String]?
    @Published var severityDescription: String?
    @Published var isProcessing: Bool = false
    @Published var showingImagePicker: Bool = false
    @Published var showingCamera: Bool = false
    @Published var showingError: Bool = false
    @Published var errorMessage: String = ""
    
    func processImage() {
        guard let image = selectedImage else {
            showError("No image selected")
            return
        }
        
        isProcessing = true
        
        ModelManager.shared.processImage(image) { [weak self] result in
            DispatchQueue.main.async {
                guard let self = self else { return }
                
                switch result {
                case .success(let analysisResult):
                    if analysisResult.success {
                        // Update UI with results
                        self.classificationResult = analysisResult.predictedClass
                        self.confidenceScore = analysisResult.classConfidence
                        self.treatmentAdvice = analysisResult.treatmentAdvice
                        self.severityDescription = analysisResult.description
                        
                        // Download and set images
                        if let visualizationURL = analysisResult.visualization {
                            self.downloadImage(from: visualizationURL) { image in
                                self.visualizationImage = image
                            }
                        }
                        
                        if let probabilityChartURL = analysisResult.probabilityChart {
                            self.downloadImage(from: probabilityChartURL) { image in
                                self.probabilityChart = image
                            }
                        }
                    } else {
                        self.showError(analysisResult.error ?? "Unknown error occurred")
                    }
                case .failure(let error):
                    self.showError(error.localizedDescription)
                }
                
                self.isProcessing = false
            }
        }
    }
    
    private func downloadImage(from urlString: String, completion: @escaping (UIImage) -> Void) {
        ModelManager.shared.downloadImage(from: urlString) { [weak self] result in
            DispatchQueue.main.async {
                switch result {
                case .success(let image):
                    completion(image)
                case .failure(let error):
                    self?.showError("Failed to download image: \(error.localizedDescription)")
                }
            }
        }
    }
    
    private func showError(_ message: String) {
        errorMessage = message
        showingError = true
    }
    
    func reset() {
        selectedImage = nil
        processedImage = nil
        visualizationImage = nil
        probabilityChart = nil
        classificationResult = nil
        confidenceScore = nil
        treatmentAdvice = nil
        severityDescription = nil
        isProcessing = false
        showingError = false
        errorMessage = ""
    }
    
    func checkCameraAccess() {
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized:
            showingCamera = true
        case .notDetermined:
            AVCaptureDevice.requestAccess(for: .video) { [weak self] granted in
                DispatchQueue.main.async {
                    if granted {
                        self?.showingCamera = true
                    } else {
                        self?.showError("Camera access denied")
                    }
                }
            }
        default:
            showError("Camera access required. Please enable it in Settings.")
        }
    }
} 