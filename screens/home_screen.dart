import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  final String userRole; // either 'student' or 'instructor'

  const HomeScreen({super.key, required this.userRole});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Welcome'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Choose an action:',
              style: TextStyle(fontSize: 20),
            ),
            const SizedBox(height: 24),
            if (userRole == 'instructor') ...[
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/schedule-class'),
                child: const Text('Schedule a Class'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/instructor-stats'),
                child: const Text('View Attendance Stats'),
              ),
            ] else if (userRole == 'student') ...[
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/available-sessions'),
                child: const Text('View Available Sessions'),
              ),
              ElevatedButton(
                onPressed: () => Navigator.pushNamed(context, '/student-stats'),
                child: const Text('My Attendance Stats'),
              ),
            ] else
              const Text('Unknown role. Please log in again.'),
          ],
        ),
      ),
    );
  }
}