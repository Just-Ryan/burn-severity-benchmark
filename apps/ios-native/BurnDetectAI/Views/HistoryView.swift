import SwiftUI

struct HistoryView: View {
    @AppStorage("burnHistory") private var burnHistoryData: Data = Data()
    @State private var burnHistory: [BurnResult] = []
    
    var body: some View {
        NavigationView {
            Group {
                if burnHistory.isEmpty {
                    VStack(spacing: 20) {
                        Image(systemName: "clock")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        
                        Text("No burn detections yet")
                            .font(.title2)
                            .foregroundColor(.gray)
                        
                        Text("Use the camera to detect burns")
                            .font(.subheadline)
                            .foregroundColor(.gray)
                    }
                } else {
                    List {
                        ForEach(burnHistory) { result in
                            BurnHistoryRow(result: result)
                        }
                        .onDelete(perform: deleteItems)
                    }
                }
            }
            .navigationTitle("Detection History")
            .listStyle(.insetGrouped)
            .toolbar {
                if !burnHistory.isEmpty {
                    EditButton()
                }
            }
        }
        .onAppear {
            loadHistory()
        }
        .onChange(of: burnHistory) { _, _ in
            saveHistory()
        }
    }
    
    private func loadHistory() {
        if let decoded = try? JSONDecoder().decode([BurnResult].self, from: burnHistoryData) {
            burnHistory = decoded
        }
    }
    
    private func saveHistory() {
        if let encoded = try? JSONEncoder().encode(burnHistory) {
            burnHistoryData = encoded
        }
    }
    
    private func deleteItems(at offsets: IndexSet) {
        burnHistory.remove(atOffsets: offsets)
    }
}

struct BurnHistoryRow: View {
    let result: BurnResult
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(result.severity.description)
                    .font(.headline)
                
                Text("Confidence: \(Int(result.confidence * 100))%")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                
                Text(result.timestamp.formatted())
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            Image(systemName: severityIcon)
                .font(.title2)
                .foregroundColor(severityColor)
        }
        .padding(.vertical, 8)
    }
    
    private var severityIcon: String {
        switch result.severity {
        case .firstDegree:
            return "1.circle.fill"
        case .secondDegree:
            return "2.circle.fill"
        case .thirdDegree:
            return "3.circle.fill"
        }
    }
    
    private var severityColor: Color {
        switch result.severity {
        case .firstDegree:
            return .orange
        case .secondDegree:
            return .red
        case .thirdDegree:
            return .purple
        }
    }
}

// Preview with sample data
struct HistoryView_Previews: PreviewProvider {
    static var previews: some View {
        HistoryView()
            .previewDisplayName("Empty History")
        
        HistoryView()
            .previewDisplayName("With History")
            .onAppear {
                // Set up sample data for preview
                let sampleData = [
                    BurnResult(severity: .firstDegree, confidence: 0.85, timestamp: Date()),
                    BurnResult(severity: .secondDegree, confidence: 0.92, timestamp: Date().addingTimeInterval(-3600)),
                    BurnResult(severity: .thirdDegree, confidence: 0.78, timestamp: Date().addingTimeInterval(-7200))
                ]
                
                if let encoded = try? JSONEncoder().encode(sampleData) {
                    UserDefaults.standard.set(encoded, forKey: "burnHistory")
                }
            }
    }
} 