import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  static const primaryBlue = Color(0xFF4A90E2);
  static const white = Color(0xFFFFFFFF);
  static const grey = Color(0xFF9E9E9E);
  static const darkGrey = Color(0xFF424242);
  static const orange = Color(0xFFFFA726);
  static const green = Color(0xFF66BB6A);

  static final ThemeData lightTheme = ThemeData(
    primaryColor: primaryBlue,
    scaffoldBackgroundColor: white,
    colorScheme: ColorScheme.light(
      primary: primaryBlue,
      secondary: orange,
      surface: white,
      background: white,
      error: Colors.red.shade700,
    ),
    textTheme: GoogleFonts.poppinsTextTheme(),
    elevatedButtonTheme: ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        elevation: 0,
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
        backgroundColor: primaryBlue,
        foregroundColor: white,
      ),
    ),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: Colors.grey.shade100,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide.none,
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide(color: primaryBlue),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(15),
        borderSide: BorderSide(color: Colors.red.shade700),
      ),
      contentPadding: EdgeInsets.symmetric(horizontal: 20, vertical: 16),
    ),
  );
}
