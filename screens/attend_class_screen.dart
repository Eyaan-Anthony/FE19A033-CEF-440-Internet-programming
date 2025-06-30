import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:location/location.dart';
import 'package:http/http.dart' as http;

class StudentAttendanceScreen extends StatefulWidget {
  const StudentAttendanceScreen({super.key});

  @override
  State<StudentAttendanceScreen> createState() => _StudentAttendanceScreenState();
}

class _StudentAttendanceScreenState extends State<StudentAttendanceScreen> {
  final TextEditingController studentIdController = TextEditingController();
  final TextEditingController sessionIdController = TextEditingController();
  final TextEditingController startTimeController = TextEditingController();
  File? _imageFile;
  LocationData? _location;

  Future<void> pickImage() async {
    final picker = ImagePicker();
    final picked = await picker.pickImage(source: ImageSource.camera);

    if (picked != null) {
      setState(() {
        _imageFile = File(picked.path);
      });
    }
  }

  Future<void> getLocation() async {
    Location location = Location();
    bool _serviceEnabled = await location.serviceEnabled();
    if (!_serviceEnabled) _serviceEnabled = await location.requestService();

    PermissionStatus _permissionGranted = await location.hasPermission();
    if (_permissionGranted == PermissionStatus.denied) {
      _permissionGranted = await location.requestPermission();
    }

    if (_permissionGranted == PermissionStatus.granted) {
      final loc = await location.getLocation();
      setState(() {
        _location = loc;
      });
    }
  }

  Future<void> submitAttendance() async {
    if (_imageFile == null || _location == null) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Image and location are required")));
      return;
    }

    final bytes = await _imageFile!.readAsBytes();
    final base64Image = base64Encode(bytes);

    final uri = Uri.parse('http://<YOUR_LOCAL_IP>:8003/mark-attendance');
    final response = await http.post(
      uri,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        "student_id": studentIdController.text,
        "session_id": sessionIdController.text,
        "image_data": base64Image,
        "student_lat": _location!.latitude,
        "student_long": _location!.longitude,
        "class_lat": _location!.latitude, // You may want to replace with session data
        "class_long": _location!.longitude,
        "start_time": startTimeController.text, // Should be ISO8601 UTC
      }),
    );

    final decoded = jsonDecode(response.body);
    if (response.statusCode == 200 && decoded["success"] == true) {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(decoded["reason"])));
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: ${decoded["reason"]}")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Attend Class")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            TextField(controller: studentIdController, decoration: InputDecoration(labelText: "Student ID")),
            TextField(controller: sessionIdController, decoration: InputDecoration(labelText: "Session ID")),
            TextField(controller: startTimeController, decoration: InputDecoration(labelText: "Start Time (e.g. 2025-06-24T09:00:00Z)")),

            const SizedBox(height: 16),
            ElevatedButton(onPressed: pickImage, child: Text("Take Selfie")),
            _imageFile != null ? Image.file(_imageFile!, height: 100) : SizedBox(),

            const SizedBox(height: 16),
            ElevatedButton(onPressed: getLocation, child: Text("Get Location")),
            _location != null ? Text("Lat: ${_location!.latitude}, Long: ${_location!.longitude}") : SizedBox(),

            const SizedBox(height: 24),
            ElevatedButton(onPressed: submitAttendance, child: Text("Mark Attendance")),
          ],
        ),
      ),
    );
  }
}
