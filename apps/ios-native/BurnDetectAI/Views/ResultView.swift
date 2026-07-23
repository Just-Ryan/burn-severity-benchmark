import SwiftUI

struct ResultView: View {
    @EnvironmentObject private var viewModel: BurnDetectionViewModel
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Original Image
                if let image = viewModel.selectedImage {
                    Image(uiImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(maxHeight: 300)
                        .clipShape(RoundedRectangle(cornerRadius: 15))
                }
                
                // Visualization Image
                if let visualization = viewModel.visualizationImage {
                    Image(uiImage: visualization)
                        .resizable()
                        .scaledToFit()
                        .frame(maxHeight: 300)
                        .clipShape(RoundedRectangle(cornerRadius: 15))
                }
                
                // Classification Result
                if let result = viewModel.classificationResult {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Burn Classification")
                            .font(.title2)
                            .bold()
                        
                        HStack {
                            Text(result)
                                .font(.title3)
                                .foregroundColor(Theme.accent1)
                            
                            if let confidence = viewModel.confidenceScore {
                                Text("\(Int(confidence))% confidence")
                                    .font(.subheadline)
                                    .foregroundColor(.gray)
                            }
                        }
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 15)
                            .fill(.ultraThinMaterial)
                    )
                }
                
                // Severity Description
                if let description = viewModel.severityDescription {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Severity Description")
                            .font(.title2)
                            .bold()
                        
                        Text(description)
                            .font(.body)
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 15)
                            .fill(.ultraThinMaterial)
                    )
                }
                
                // Treatment Advice
                if let advice = viewModel.treatmentAdvice {
                    VStack(alignment: .leading, spacing: 10) {
                        Text("Treatment Advice")
                            .font(.title2)
                            .bold()
                        
                        ForEach(advice, id: \.self) { item in
                            HStack(alignment: .top, spacing: 10) {
                                Image(systemName: "checkmark.circle.fill")
                                    .foregroundColor(Theme.accent1)
                                
                                Text(item)
                                    .font(.body)
                            }
                        }
                    }
                    .padding()
                    .background(
                        RoundedRectangle(cornerRadius: 15)
                            .fill(.ultraThinMaterial)
                    )
                }
                
                // Probability Chart
                if let chart = viewModel.probabilityChart {
                    Image(uiImage: chart)
                        .resizable()
                        .scaledToFit()
                        .frame(maxHeight: 200)
                        .clipShape(RoundedRectangle(cornerRadius: 15))
                }
                
                // Reset Button
                Button(action: {
                    viewModel.reset()
                }) {
                    Text("Analyze Another Image")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Theme.gradientAccent)
                        .clipShape(RoundedRectangle(cornerRadius: 15))
                }
                .padding(.top)
            }
            .padding()
        }
        .background(Theme.gradientBackground.ignoresSafeArea())
        .navigationTitle("Analysis Results")
        .navigationBarTitleDisplayMode(.inline)
    }
}

#Preview {
    ResultView()
        .environmentObject(BurnDetectionViewModel())
} 