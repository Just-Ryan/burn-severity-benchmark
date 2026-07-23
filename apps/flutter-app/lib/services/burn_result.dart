class BurnResult {
  final bool success;
  final String? error;
  final String originalImagePath;
  final String? segmentedImagePath;
  final String? burnDegree;
  final double? confidence;
  final double? segmentationConfidence;
  final List<String>? treatmentAdvice;
  final String? description;
  final Map<String, dynamic>? allProbabilities;

  BurnResult({
    required this.success,
    this.error,
    required this.originalImagePath,
    this.segmentedImagePath,
    this.burnDegree,
    this.confidence,
    this.segmentationConfidence,
    this.treatmentAdvice,
    this.description,
    this.allProbabilities,
  });

  factory BurnResult.fromMap(Map<String, dynamic> map) {
    return BurnResult(
      success: map['success'] ?? false,
      error: map['error'],
      originalImagePath: map['originalImage'] ?? '',
      segmentedImagePath: map['segmentedImage'],
      burnDegree: map['burnDegree'],
      confidence: map['confidence'],
      segmentationConfidence: map['segmentationConfidence'],
      treatmentAdvice: map['treatmentAdvice'] != null 
          ? List<String>.from(map['treatmentAdvice']) 
          : null,
      description: map['description'],
      allProbabilities: map['allProbabilities'],
    );
  }

  factory BurnResult.error(String errorMessage, String originalImagePath) {
    return BurnResult(
      success: false,
      error: errorMessage,
      originalImagePath: originalImagePath,
    );
  }
}
