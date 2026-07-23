import 'dart:io';
import 'dart:math';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:burn_ai2/config/theme.dart';
import 'package:burn_ai2/screens/processing/result_screen.dart';
import 'package:burn_ai2/services/burn_analyzer_service.dart';
import 'package:burn_ai2/services/burn_result.dart';

class ImageProcessingScreen extends StatefulWidget {
  final String imagePath;

  const ImageProcessingScreen({
    super.key,
    required this.imagePath,
  });

  @override
  State<ImageProcessingScreen> createState() => _ImageProcessingScreenState();
}

class _ImageProcessingScreenState extends State<ImageProcessingScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _progressAnimation;
  final List<String> _processingSteps = [
    'Connecting to server...',
    'Uploading image...',
    'Detecting burn regions...',
    'Assessing burn severity...',
    'Generating recommendations...',
  ];
  int _currentStep = 0;
  bool _isProcessing = true;
  String? _errorMessage;
  final BurnAnalyzerService _burnAnalyzer = BurnAnalyzerService();

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 5),
      vsync: this,
    );

    _progressAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _controller.addListener(() {
      setState(() {
        _currentStep = (_controller.value * _processingSteps.length).floor();
        if (_currentStep >= _processingSteps.length) {
          _currentStep = _processingSteps.length - 1;
        }
      });
    });

    _initializeAndProcess();
  }

  Future<void> _initializeAndProcess() async {
    try {
      // Start the animation
      _controller.forward();
      
      // Initialize the burn analyzer service
      await _burnAnalyzer.initialize();
      
      // Process the image
      final result = await _burnAnalyzer.analyzeBurn(widget.imagePath);
      final burnResult = BurnResult.fromMap(result);
      
      if (burnResult.success) {
        // Wait for animation to complete if it hasn't already
        if (_controller.value < 1.0) {
          await _controller.forward(from: _controller.value).orCancel;
        }
        
        // Navigate to result screen
        if (mounted) {
          Navigator.of(context).pushReplacement(
            MaterialPageRoute(
              builder: (_) => ResultScreen(
                imagePath: widget.imagePath,
                burnDegree: burnResult.burnDegree!,
                confidence: burnResult.confidence!,
                segmentedImagePath: burnResult.segmentedImagePath,
                treatmentAdvice: burnResult.treatmentAdvice,
                description: burnResult.description,
                allProbabilities: burnResult.allProbabilities,
              ),
            ),
          );
        }
      } else {
        setState(() {
          _isProcessing = false;
          _errorMessage = burnResult.error ?? 'An unknown error occurred';
        });
      }
    } on SocketException {
      setState(() {
        _isProcessing = false;
        _errorMessage = 'Failed to connect to server. Please check your internet connection.';
      });
    } on HttpException {
      setState(() {
        _isProcessing = false;
        _errorMessage = 'Failed to upload image. Please try again.';
      });
    } catch (e) {
      setState(() {
        _isProcessing = false;
        _errorMessage = e.toString();
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          // Background image with blur
          Container(
            decoration: BoxDecoration(
              image: DecorationImage(
                image: FileImage(File(widget.imagePath)),
                fit: BoxFit.cover,
              ),
            ),
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
              child: Container(
                color: Colors.black.withOpacity(0.5),
              ),
            ),
          ),
          // Content
          SafeArea(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Preview of the selected image
                Container(
                  width: 200,
                  height: 200,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.3),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(20),
                    child: Image.file(
                      File(widget.imagePath),
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                const SizedBox(height: 40),
                
                if (_isProcessing) ...[
                  // Processing animation
                  Container(
                    width: 80,
                    height: 80,
                    decoration: BoxDecoration(
                      color: AppTheme.white,
                      borderRadius: BorderRadius.circular(40),
                      boxShadow: [
                        BoxShadow(
                          color: AppTheme.primaryBlue.withOpacity(0.3),
                          blurRadius: 20,
                          spreadRadius: 5,
                        ),
                      ],
                    ),
                    child: AnimatedBuilder(
                      animation: _controller,
                      builder: (context, child) {
                        return Transform.rotate(
                          angle: _controller.value * 4 * pi,
                          child: const Icon(
                            Icons.auto_awesome,
                            size: 40,
                            color: AppTheme.primaryBlue,
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 32),
                  // Processing step text
                  AnimatedSwitcher(
                    duration: const Duration(milliseconds: 500),
                    child: Text(
                      _processingSteps[_currentStep],
                      key: ValueKey<int>(_currentStep),
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            color: AppTheme.white,
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  // Progress indicator
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 40),
                    child: LinearProgressIndicator(
                      value: _progressAnimation.value,
                      backgroundColor: AppTheme.white.withOpacity(0.2),
                      valueColor: AlwaysStoppedAnimation<Color>(AppTheme.primaryBlue),
                      borderRadius: BorderRadius.circular(10),
                      minHeight: 8,
                    ),
                  ),
                ] else if (_errorMessage != null) ...[
                  // Error message
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Column(
                      children: [
                        const Icon(
                          Icons.error_outline,
                          color: Colors.red,
                          size: 48,
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Error',
                          style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                color: Colors.red,
                                fontWeight: FontWeight.bold,
                              ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _errorMessage!,
                          textAlign: TextAlign.center,
                          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                color: AppTheme.white,
                              ),
                        ),
                        const SizedBox(height: 24),
                        ElevatedButton(
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppTheme.white,
                            foregroundColor: AppTheme.primaryBlue,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 32,
                              vertical: 12,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(30),
                            ),
                          ),
                          child: const Text('Go Back'),
                        ),
                        const SizedBox(height: 16),
                        TextButton(
                          onPressed: () {
                            setState(() {
                              _isProcessing = true;
                              _errorMessage = null;
                              _controller.reset();
                              _controller.forward();
                            });
                            _initializeAndProcess();
                          },
                          child: Text(
                            'Try Again',
                            style: TextStyle(
                              color: AppTheme.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        ],
      ),
    );
  }
}
