import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ScheduleClassScreen extends StatefulWidget {
  const ScheduleClassScreen({super.key});

  @override
  State<ScheduleClassScreen> createState() => _ScheduleClassScreenState();
}

class _ScheduleClassScreenState extends State<ScheduleClassScreen> {
  final TextEditingController courseNameController = TextEditingController();
  final TextEditingController instructorIdController = TextEditingController(); // You can later fetch this from login context/token
  final TextEditingController locationLatController = TextEditingController();
  final TextEditingController locationLngController = TextEditingController();
  final TextEditingController startTimeController = TextEditingController();
  final TextEditingController endTimeController = TextEditingController();

  Future<void> scheduleSession() async {
    final uri = Uri.parse('http://<YOUR_LOCAL_IP>:8002/create-session');

    try {
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          "course_name": courseNameController.text,
          "instructor_id": instructorIdController.text,
          "location_lat": double.tryParse(locationLatController.text),
          "location_lng": double.tryParse(locationLngController.text),
          "start_time": startTimeController.text,
          "end_time": endTimeController.text,
        }),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Class session scheduled successfully")),
        );
        Navigator.pop(context);
      } else {
        final err = jsonDecode(response.body);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Failed: ${err['detail']}")),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Schedule Class")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ListView(
          children: [
            TextField(controller: courseNameController, decoration: InputDecoration(labelText: "Course Name")),
            TextField(controller: instructorIdController, decoration: InputDecoration(labelText: "Instructor ID")),
            TextField(controller: locationLatController, decoration: InputDecoration(labelText: "Latitude")),
            TextField(controller: locationLngController, decoration: InputDecoration(labelText: "Longitude")),
            TextField(controller: startTimeController, decoration: InputDecoration(labelText: "Start Time (e.g. 2025-06-23T10:00:00)")),
            TextField(controller: endTimeController, decoration: InputDecoration(labelText: "End Time (e.g. 2025-06-23T12:00:00)")),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: scheduleSession,
              child: Text("Create Class Session"),
            ),
          ],
        ),
      ),
    );
  }
}
