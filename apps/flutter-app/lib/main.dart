import 'package:flutter/material.dart';
import 'package:burn_ai2/config/theme.dart';
import 'package:burn_ai2/screens/splash_screen.dart';

void main() => runApp(const BurnAIApp());

class BurnAIApp extends StatelessWidget {
  const BurnAIApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BurnAi',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: const SplashScreen(),
    );
  }
}
