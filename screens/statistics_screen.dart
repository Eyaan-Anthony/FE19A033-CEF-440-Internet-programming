import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class StatisticsScreen extends StatefulWidget {
  final String role; // 'student' or 'instructor'

  const StatisticsScreen({super.key, required this.role});

  @override
  State<StatisticsScreen> createState() => _StatisticsScreenState();
}

class _StatisticsScreenState extends State<StatisticsScreen> {
  final TextEditingController _sessionIdController = TextEditingController();
  Map<String, dynamic> _stats = {};
  bool _loading = false;

  Future<void> fetchStats({String? sessionId}) async {
    setState(() {
      _loading = true;
    });

    final uri = sessionId == null || sessionId.isEmpty
        ? Uri.parse("http://<YOUR_LOCAL_IP>:8003/stats")
        : Uri.parse("http://<YOUR_LOCAL_IP>:8003/stats?session_id=$sessionId");

    try {
      final response = await http.get(uri);
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _stats = data['data'] ?? {};
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Failed to load stats")));
      }
    } catch (e) {
      print("Stats error: $e");
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Error: $e")));
    }

    setState(() {
      _loading = false;
    });
  }

  @override
  void initState() {
    super.initState();
    if (widget.role == 'instructor') {
      fetchStats();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Attendance Statistics")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            if (widget.role == 'student') ...[
              TextField(
                controller: _sessionIdController,
                decoration: InputDecoration(labelText: "Enter Session ID"),
              ),
              const SizedBox(height: 10),
              ElevatedButton(
                onPressed: () => fetchStats(sessionId: _sessionIdController.text),
                child: const Text("Get My Stats"),
              ),
            ],
            const SizedBox(height: 20),
            _loading
                ? const CircularProgressIndicator()
                : _stats.isEmpty
                    ? const Text("No data available")
                    : Expanded(
                        child: ListView.builder(
                          itemCount: _stats.length,
                          itemBuilder: (context, index) {
                            final sessionId = _stats.keys.elementAt(index);
                            final studentIds = List<String>.from(_stats[sessionId]);
                            return Card(
                              child: ListTile(
                                title: Text("Session ID: $sessionId"),
                                subtitle: Text("Present Students: ${studentIds.length}"),
                              ),
                            );
                          },
                        ),
                      ),
          ],
        ),
      ),
    );
  }
}
