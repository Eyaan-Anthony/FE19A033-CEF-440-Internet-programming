import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  Future<void> login() async {
    final url = Uri.parse('http://0.0.0.0:8000/log-in'); 

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'email': emailController.text.trim(),
          'password': passwordController.text.trim(),
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final String role = data['role'];
        final String token = data['access_token'];
        final String message = data['message'];

        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));

        if (role == 'student') {
          Navigator.pushReplacementNamed(context, '/home-student');
        } else if (role == 'instructor') {
          Navigator.pushReplacementNamed(context, '/home-instructor');
        } else {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Unknown role")));
        }
      } else {
        final error = jsonDecode(response.body)['detail'] ?? "Login failed";
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(error)));
      }
    } catch (e) {
      print("Login error: $e");
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text("Login failed: $e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Login")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Form(
          key: _formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              TextFormField(
                controller: emailController,
                decoration: const InputDecoration(labelText: 'Email'),
              ),
              TextFormField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Password'),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: login,
                child: const Text("Login"),
              ),
              TextButton(
                  onPressed: () {
                    Navigator.pushNamed(context, '/signin');
                  },
                  child: Text("Don't have an account? Sign up"),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
