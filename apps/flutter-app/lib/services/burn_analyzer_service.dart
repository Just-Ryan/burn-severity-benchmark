import 'dart:io';
import 'package:flutter/material.dart';
import 'package:path_provider/path_provider.dart';
import 'package:http/http.dart' as http;
import 'package:dio/dio.dart';
import 'package:burn_ai2/config/app_config.dart';

/// A service that handles burn analysis by communicating with a Flask server.
/// This service sends images to the server for processing and receives analysis results.
class BurnAnalyzerService {
  // Single source of truth for the backend URL (see AppConfig; override via --dart-define)
  static const String serverUrl = AppConfig.apiBaseUrl;
  
  bool _isInitialized = false;
  final Dio _dio = Dio();
  
  final List<String> burnClasses = ['First Degree Burn', 'Second Degree Burn', 'Third Degree Burn'];
  
  // Singleton pattern
  static final BurnAnalyzerService _instance = BurnAnalyzerService._internal();
  
  factory BurnAnalyzerService() {
    return _instance;
  }
  
  BurnAnalyzerService._internal();
  
  /// Initialize the burn analyzer service
  /// This checks the server connection
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      // Check server connection
      final response = await _dio.get('$serverUrl/',
        options: Options(
          receiveTimeout: const Duration(seconds: 10),
          sendTimeout: const Duration(seconds: 10),
        ),
      );
      
      if (response.statusCode != 200) {
        throw Exception('Failed to connect to server: ${response.statusCode}');
      }
      
      _isInitialized = true;
      debugPrint('Burn Analyzer Service initialized successfully');
    } catch (e) {
      debugPrint('Error initializing Burn Analyzer Service: $e');
      rethrow;
    }
  }
  
  /// Analyze a burn image by sending it to the Flask server
  /// @param imagePath Path to the image file
  /// @return Map containing analysis results
  Future<Map<String, dynamic>> analyzeBurn(String imagePath) async {
    if (!_isInitialized) {
      try {
        await initialize();
      } catch (e) {
        return {
          'success': false,
          'error': 'Failed to connect to server: $e',
        };
      }
    }
    
    try {
      // Check if the image file exists
      final File imageFile = File(imagePath);
      if (!await imageFile.exists()) {
        throw Exception('Image file does not exist: $imagePath');
      }
      
      // Create form data with the image
      final formData = FormData.fromMap({
        'file': await MultipartFile.fromFile(
          imagePath,
          filename: imagePath.split('/').last,
        ),
      });
      
      // Send the image to the server
      final response = await _dio.post(
        '$serverUrl/analyze',
        data: formData,
        options: Options(
          receiveTimeout: const Duration(seconds: 60),
          sendTimeout: const Duration(seconds: 60),
        ),
      );
      
      if (response.statusCode != 200) {
        throw Exception('Server error: ${response.statusCode}');
      }
      
      final responseData = response.data;
      
      if (!responseData['success']) {
        throw Exception(responseData['error'] ?? 'Unknown server error');
      }
      
      // Save the segmented image if it exists
      String? segmentedImagePath;
      if (responseData['masked_image'] != null) {
        // Download the masked image
        final tempDir = await getTemporaryDirectory();
        final segmentedFile = File('${tempDir.path}/segmented_${DateTime.now().millisecondsSinceEpoch}.jpg');
        
        // Get the full URL for the masked image
        final String maskedImageUrl = '$serverUrl${responseData['masked_image']}';
        
        // Download the image
        final imageResponse = await http.get(Uri.parse(maskedImageUrl));
        await segmentedFile.writeAsBytes(imageResponse.bodyBytes);
        segmentedImagePath = segmentedFile.path;
      }
      
      // Map the predicted class to our format
      String burnDegree;
      switch (responseData['predicted_class']) {
        case 'First':
          burnDegree = 'First Degree Burn';
          break;
        case 'Second':
          burnDegree = 'Second Degree Burn';
          break;
        case 'Third':
          burnDegree = 'Third Degree Burn';
          break;
        default:
          burnDegree = '${responseData['predicted_class']} Degree Burn';
      }
      
      // Convert the result to the expected format
      return {
        'success': true,
        'originalImage': imagePath,
        'segmentedImage': segmentedImagePath,
        'burnDegree': burnDegree,
        'confidence': responseData['class_confidence'] is double 
            ? responseData['class_confidence'] / 100 
            : ((responseData['class_confidence'] as num?)?.toDouble() ?? 0) / 100,
        'segmentationConfidence': responseData['seg_confidence'] is double 
            ? responseData['seg_confidence'] / 100 
            : ((responseData['seg_confidence'] as num?)?.toDouble() ?? 0) / 100,
        'treatmentAdvice': responseData['treatment_advice'],
        'description': responseData['description'],
        'allProbabilities': responseData['all_probabilities'],
      };
    } catch (e) {
      debugPrint('Error analyzing burn: $e');
      return {
        'success': false,
        'error': e.toString(),
      };
    }
  }
  
  /// Clean up resources
  void dispose() {
    _isInitialized = false;
  }
}
