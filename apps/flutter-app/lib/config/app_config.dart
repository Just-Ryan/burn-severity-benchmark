class AppConfig {
  /// Base URL of the deployed inference API (Flask on Hugging Face Spaces).
  ///
  /// Override at build/run time without touching source:
  ///   flutter run --dart-define=BURN_API_BASE_URL=https://<user>-<space>.hf.space
  ///
  /// Hugging Face Spaces serve over HTTPS on port 443, so no port is needed.
  static const String apiBaseUrl = String.fromEnvironment(
    'BURN_API_BASE_URL',
    defaultValue: 'https://YOUR-SPACE.hf.space',
  );
}
