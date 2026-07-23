import Foundation

enum BurnSeverity: String, Codable, Equatable {
    case firstDegree = "first_degree"
    case secondDegree = "second_degree"
    case thirdDegree = "third_degree"
    
    var description: String {
        switch self {
        case .firstDegree:
            return "First Degree"
        case .secondDegree:
            return "Second Degree"
        case .thirdDegree:
            return "Third Degree"
        }
    }
}

struct BurnResult: Codable, Equatable, Identifiable {
    let id = UUID()
    let severity: BurnSeverity
    let confidence: Double
    let timestamp: Date
    
    enum CodingKeys: String, CodingKey {
        case severity
        case confidence
        case timestamp
    }
}

struct BurnAnalysisResponse: Codable {
    let severity: BurnSeverity
    let confidence: Double
} 