import Foundation
import UIKit

enum BurnDegree: String {
    case first = "First Degree"
    case second = "Second Degree"
    case third = "Third Degree"
    case unknown = "Unknown"
}

struct AnalysisResult: Codable {
    let success: Bool
    let predictedClass: String?
    let classConfidence: Double?
    let segConfidence: Double?
    let processingTime: Double?
    let originalImage: String?
    let maskedImage: String?
    let visualization: String?
    let probabilityChart: String?
    let treatmentAdvice: [String]?
    let description: String?
    let allProbabilities: [String: Double]?
    let error: String?
    
    enum CodingKeys: String, CodingKey {
        case success
        case predictedClass = "predicted_class"
        case classConfidence = "class_confidence"
        case segConfidence = "seg_confidence"
        case processingTime = "processing_time"
        case originalImage = "original_image"
        case maskedImage = "masked_image"
        case visualization
        case probabilityChart = "probability_chart"
        case treatmentAdvice = "treatment_advice"
        case description
        case allProbabilities = "all_probabilities"
        case error
    }
}

class ModelManager {
    static let shared = ModelManager()
    
    private let baseURL = "http://127.0.0.1:5002" // Update this with your Flask server's IP
    private let session = URLSession.shared
    
    private init() {}
    
    func processImage(_ image: UIImage, completion: @escaping (Result<AnalysisResult, Error>) -> Void) {
        guard let imageData = image.jpegData(compressionQuality: 0.8) else {
            completion(.failure(NSError(domain: "ModelManager", code: -1, userInfo: [NSLocalizedDescriptionKey: "Failed to convert image to data"])))
            return
        }
        
        let boundary = UUID().uuidString
        var request = URLRequest(url: URL(string: "\(baseURL)/analyze")!)
        request.httpMethod = "POST"
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
        
        var body = Data()
        
        // Add the image data
        body.append("--\(boundary)\r\n".data(using: .utf8)!)
        body.append("Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n".data(using: .utf8)!)
        body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
        body.append(imageData)
        body.append("\r\n".data(using: .utf8)!)
        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        
        request.httpBody = body
        
        let task = session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data else {
                completion(.failure(NSError(domain: "ModelManager", code: -2, userInfo: [NSLocalizedDescriptionKey: "No data received"])))
                return
            }
            
            do {
                let result = try JSONDecoder().decode(AnalysisResult.self, from: data)
                completion(.success(result))
            } catch {
                completion(.failure(error))
            }
        }
        
        task.resume()
    }
    
    func downloadImage(from urlString: String, completion: @escaping (Result<UIImage, Error>) -> Void) {
        guard let url = URL(string: "\(baseURL)\(urlString)") else {
            completion(.failure(NSError(domain: "ModelManager", code: -3, userInfo: [NSLocalizedDescriptionKey: "Invalid URL"])))
            return
        }
        
        let task = session.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            guard let data = data, let image = UIImage(data: data) else {
                completion(.failure(NSError(domain: "ModelManager", code: -4, userInfo: [NSLocalizedDescriptionKey: "Failed to create image from data"])))
                return
            }
            
            completion(.success(image))
        }
        
        task.resume()
    }
} 