import 'dart:io';
import 'package:flutter/material.dart';
import 'package:burn_ai2/config/theme.dart';

class ResultScreen extends StatelessWidget {
  final String imagePath;
  final String burnDegree;
  final double confidence;
  final String? segmentedImagePath;
  final List<String>? treatmentAdvice;
  final String? description;
  final Map<String, dynamic>? allProbabilities;

  const ResultScreen({
    super.key,
    required this.imagePath,
    required this.burnDegree,
    required this.confidence,
    this.segmentedImagePath,
    this.treatmentAdvice,
    this.description,
    this.allProbabilities,
  });

  Color _getBurnSeverityColor() {
    switch (burnDegree.toLowerCase()) {
      case 'first degree burn':
        return AppTheme.green;
      case 'second degree burn':
        return AppTheme.orange;
      case 'third degree burn':
        return Colors.red;
      default:
        return AppTheme.primaryBlue;
    }
  }

  String _getRecommendation() {
    // Use server-provided treatment advice if available
    if (treatmentAdvice != null && treatmentAdvice!.isNotEmpty) {
      return treatmentAdvice!.join('\n• ');
    }
    
    // Fallback to local recommendations
    switch (burnDegree.toLowerCase()) {
      case 'first degree burn':
        return 'Apply cool water for 10-20 minutes. Use over-the-counter pain relievers if needed. Monitor for changes.';
      case 'second degree burn':
        return 'Seek medical attention. Keep the burn clean and covered. Do not break blisters.';
      case 'third degree burn':
        return 'SEEK IMMEDIATE EMERGENCY MEDICAL ATTENTION. Do not remove clothing stuck to the burn.';
      default:
        return 'Please consult a medical professional for proper evaluation.';
    }
  }

  String _getBurnDescription() {
    // Use server-provided description if available
    if (description != null && description!.isNotEmpty) {
      return description!;
    }
    
    // Fallback to local descriptions
    switch (burnDegree.toLowerCase()) {
      case 'first degree burn':
        return 'First-degree burns affect only the outer layer of skin. The burn site is red, painful, and may have mild swelling. The skin is dry without blisters.';
      case 'second degree burn':
        return 'Second-degree burns affect both the outer and underlying layer of skin. The burn site appears red, blistered, and may be swollen and painful.';
      case 'third degree burn':
        return 'Third-degree burns extend into deeper tissues. The burn area may appear white, charred, or leathery. There might be little or no pain due to nerve damage.';
      default:
        return 'Burns are classified by severity and depth of skin damage.';
    }
  }

  @override
  Widget build(BuildContext context) {
    final burnColor = _getBurnSeverityColor();
    final recommendation = _getRecommendation();
    final burnDescription = _getBurnDescription();

    return Scaffold(
      body: CustomScrollView(
        slivers: [
          SliverAppBar(
            expandedHeight: 300.0,
            floating: false,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: Stack(
                fit: StackFit.expand,
                children: [
                  Image.file(
                    File(imagePath),
                    fit: BoxFit.cover,
                  ),
                  Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                        colors: [
                          Colors.transparent,
                          Colors.black.withOpacity(0.7),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
            leading: IconButton(
              icon: const Icon(Icons.arrow_back),
              onPressed: () => Navigator.of(context).pop(),
            ),
            actions: [
              IconButton(
                icon: const Icon(Icons.share),
                onPressed: () {
                  // TODO: Implement share functionality
                },
              ),
            ],
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        decoration: BoxDecoration(
                          color: burnColor.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Icon(
                              Icons.local_fire_department,
                              color: burnColor,
                              size: 20,
                            ),
                            const SizedBox(width: 8),
                            Text(
                              burnDegree,
                              style: TextStyle(
                                color: burnColor,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ],
                        ),
                      ),
                      const Spacer(),
                      Text(
                        'Confidence: ${(confidence * 100).toInt()}%',
                        style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              color: AppTheme.grey,
                            ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 24),
                  
                  // Burn Description
                  Text(
                    'Burn Assessment',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: burnColor.withOpacity(0.05),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: burnColor.withOpacity(0.3),
                        width: 1,
                      ),
                    ),
                    child: Text(
                      burnDescription,
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            height: 1.5,
                          ),
                    ),
                  ),
                  const SizedBox(height: 24),
                  
                  // Image Analysis Section
                  Text(
                    'Image Analysis',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 16),
                  
                  // Original and Segmented Images
                  Container(
                    height: 180,
                    decoration: BoxDecoration(
                      color: Colors.grey.shade100,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Row(
                      children: [
                        // Original Image
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text(
                                'Original',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: ClipRRect(
                                    borderRadius: BorderRadius.circular(8),
                                    child: Image.file(
                                      File(imagePath),
                                      fit: BoxFit.cover,
                                    ),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                        
                        // Segmented Image
                        Expanded(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Text(
                                'Detected Region',
                                style: TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(8.0),
                                  child: segmentedImagePath != null
                                      ? ClipRRect(
                                          borderRadius: BorderRadius.circular(8),
                                          child: Image.file(
                                            File(segmentedImagePath!),
                                            fit: BoxFit.cover,
                                          ),
                                        )
                                      : Container(
                                          decoration: BoxDecoration(
                                            color: Colors.grey.shade300,
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: const Center(
                                            child: Text('No segmentation available'),
                                          ),
                                        ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 32),
                  Text(
                    'Recommended Actions',
                    style: Theme.of(context).textTheme.titleLarge?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: burnColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            Icon(
                              Icons.medical_services,
                              color: burnColor,
                            ),
                            const SizedBox(width: 12),
                            Text(
                              'Medical Advice',
                              style: Theme.of(context)
                                  .textTheme
                                  .titleMedium
                                  ?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                            ),
                          ],
                        ),
                        const SizedBox(height: 12),
                        treatmentAdvice != null && treatmentAdvice!.isNotEmpty
                            ? Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  for (var advice in treatmentAdvice!)
                                    Padding(
                                      padding: const EdgeInsets.only(bottom: 8.0),
                                      child: Row(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          const Text('• ', style: TextStyle(fontWeight: FontWeight.bold)),
                                          Expanded(
                                            child: Text(
                                              advice,
                                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                                    height: 1.5,
                                                  ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),
                                ],
                              )
                            : Text(
                                recommendation,
                                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                      height: 1.5,
                                    ),
                              ),
                      ],
                    ),
                  ),
                  
                  // Probabilities section if available
                  if (allProbabilities != null && allProbabilities!.isNotEmpty) ...[
                    const SizedBox(height: 32),
                    Text(
                      'Confidence Levels',
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.grey.shade100,
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Column(
                        children: [
                          ...allProbabilities!.entries.map((entry) {
                            final double value = (entry.value as num).toDouble();
                            final String label = entry.key.toString().contains('Degree') 
                                ? entry.key 
                                : '${entry.key} Degree Burn';
                            
                            return Padding(
                              padding: const EdgeInsets.only(bottom: 12.0),
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                    children: [
                                      Text(
                                        label,
                                        style: const TextStyle(fontWeight: FontWeight.w500),
                                      ),
                                      Text(
                                        '${value.toStringAsFixed(1)}%',
                                        style: TextStyle(
                                          color: value > 50 ? burnColor : AppTheme.grey,
                                          fontWeight: value > 50 ? FontWeight.bold : FontWeight.normal,
                                        ),
                                      ),
                                    ],
                                  ),
                                  const SizedBox(height: 4),
                                  LinearProgressIndicator(
                                    value: value / 100,
                                    backgroundColor: Colors.grey.shade300,
                                    valueColor: AlwaysStoppedAnimation<Color>(
                                      value > 50 ? burnColor : AppTheme.primaryBlue.withOpacity(0.5),
                                    ),
                                    minHeight: 8,
                                    borderRadius: BorderRadius.circular(4),
                                  ),
                                ],
                              ),
                            );
                          }).toList(),
                        ],
                      ),
                    ),
                  ],
                  
                  const SizedBox(height: 32),
                  Text(
                    'Disclaimer',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'This app provides preliminary assessment only. Always consult a healthcare professional for proper medical evaluation and treatment.',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppTheme.grey,
                          height: 1.5,
                        ),
                  ),
                  const SizedBox(height: 32),
                  ElevatedButton.icon(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.camera_alt),
                    label: const Text('Analyze Another Image'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppTheme.primaryBlue,
                      foregroundColor: AppTheme.white,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 24,
                        vertical: 16,
                      ),
                      minimumSize: const Size(double.infinity, 56),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
