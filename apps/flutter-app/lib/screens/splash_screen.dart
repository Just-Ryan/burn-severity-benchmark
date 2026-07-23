import 'package:flutter/material.dart';
import 'package:burn_ai2/config/theme.dart';
import 'package:burn_ai2/screens/home/home_screen.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeIn),
    );

    _controller.forward().then((_) {
      Future.delayed(const Duration(seconds: 1), () {
        Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (_) => const HomeScreen()),
        );
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [
              AppTheme.primaryBlue,
              AppTheme.primaryBlue.withOpacity(0.7),
              AppTheme.white,
            ],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: FadeTransition(
              opacity: _fadeAnimation,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(
                    Icons.local_hospital_rounded,
                    size: 80,
                    color: AppTheme.white,
                  ),
                  const SizedBox(height: 24),
                  Text(
                    'BurnAi',
                    style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                          color: AppTheme.white,
                          fontWeight: FontWeight.bold,
                        ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Burn severity assessment',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          color: AppTheme.white.withOpacity(0.9),
                        ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
