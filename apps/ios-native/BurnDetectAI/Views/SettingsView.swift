import SwiftUI

struct SettingsView: View {
    @AppStorage("serverURL") private var serverURL = "http://localhost:5000"
    @AppStorage("useHighQuality") private var useHighQuality = true
    @AppStorage("saveHistory") private var saveHistory = true
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Server Configuration")) {
                    TextField("Server URL", text: $serverURL)
                        .keyboardType(.URL)
                        .autocapitalization(.none)
                }
                
                Section(header: Text("Detection Settings")) {
                    Toggle("High Quality Images", isOn: $useHighQuality)
                    Toggle("Save Detection History", isOn: $saveHistory)
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                }
            }
            .navigationTitle("Settings")
        }
    }
}

// Preview with settings
struct SettingsView_Previews: PreviewProvider {
    static var previews: some View {
        SettingsView()
            .previewDisplayName("Settings View")
    }
} 