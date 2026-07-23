import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:burn_ai2/config/theme.dart';
import 'package:burn_ai2/screens/processing/image_processing_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  Future<void> _handleImageSelection(BuildContext context, ImageSource source) async {
    final picker = ImagePicker();
    try {
      final XFile? image = await picker.pickImage(source: source);
      if (image != null && context.mounted) {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => ImageProcessingScreen(imagePath: image.path),
          ),
        );
      }
    } catch (e) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Failed to pick image')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              AppTheme.primaryBlue.withOpacity(0.1),
              AppTheme.white,
            ],
          ),
        ),
        child: SafeArea(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'BurnAi',
                      style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                            fontWeight: FontWeight.bold,
                          ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      'Burn severity assessment',
                      style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                            color: AppTheme.grey,
                          ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 32),
              Expanded(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(24.0),
                        decoration: BoxDecoration(
                          color: AppTheme.white,
                          borderRadius: BorderRadius.circular(20),
                          boxShadow: [
                            BoxShadow(
                              color: Colors.black.withOpacity(0.1),
                              blurRadius: 10,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: Column(
                          children: [
                            const Icon(
                              Icons.local_hospital_rounded,
                              size: 48,
                              color: AppTheme.primaryBlue,
                            ),
                            const SizedBox(height: 16),
                            Text(
                              'Get Started',
                              style: Theme.of(context).textTheme.titleLarge?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Take or select a photo of the burn area to assess its severity',
                              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: AppTheme.grey,
                                  ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 32),
                            ElevatedButton.icon(
                              onPressed: () => _handleImageSelection(context, ImageSource.camera),
                              icon: const Icon(Icons.camera_alt),
                              label: const Text('Capture Image'),
                              style: ElevatedButton.styleFrom(
                                minimumSize: const Size(double.infinity, 56),
                              ),
                            ),
                            const SizedBox(height: 16),
                            OutlinedButton.icon(
                              onPressed: () => _handleImageSelection(context, ImageSource.gallery),
                              icon: const Icon(Icons.photo_library),
                              label: const Text('Select from Gallery'),
                              style: OutlinedButton.styleFrom(
                                minimumSize: const Size(double.infinity, 56),
                                side: BorderSide(color: AppTheme.primaryBlue),
                              ),
                            ),
                          ],
                        ),
                      ),
                      const SizedBox(height: 32),
                      Container(
                        padding: const EdgeInsets.all(24.0),
                        decoration: BoxDecoration(
                          color: AppTheme.primaryBlue.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'How it works',
                              style: Theme.of(context).textTheme.titleMedium?.copyWith(
                                    fontWeight: FontWeight.bold,
                                  ),
                            ),
                            const SizedBox(height: 16),
                            _buildInfoStep(
                              context,
                              icon: Icons.camera_alt,
                              title: '1. Capture or Select',
                              description: 'Take a clear photo of the burn area or select from gallery',
                            ),
                            const SizedBox(height: 16),
                            _buildInfoStep(
                              context,
                              icon: Icons.center_focus_strong,
                              title: '2. Analysis',
                              description: 'The burn region is segmented and its severity is classified',
                            ),
                            const SizedBox(height: 16),
                            _buildInfoStep(
                              context,
                              icon: Icons.assessment,
                              title: '3. Get Results',
                              description: 'View detailed results and recommended actions',
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildInfoStep(
    BuildContext context, {
    required IconData icon,
    required String title,
    required String description,
  }) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: AppTheme.primaryBlue.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(
            icon,
            color: AppTheme.primaryBlue,
            size: 24,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: Theme.of(context).textTheme.titleSmall?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 4),
              Text(
                description,
                style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                      color: AppTheme.grey,
                    ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
