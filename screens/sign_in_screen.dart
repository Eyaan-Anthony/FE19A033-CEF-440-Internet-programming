import 'dart:io';
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'package:path/path.dart';

class SignInScreen extends StatefulWidget {
  const SignInScreen({super.key});

  @override
  State<SignInScreen> createState() => _SignInScreenState();
}

class _SignInScreenState extends State<SignInScreen> {
  final _formKey = GlobalKey<FormState>();
  final picker = ImagePicker();

  // Controllers
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController levelController = TextEditingController();
  final TextEditingController facultyController = TextEditingController();

  List<File> imageFiles = [];
  String selectedRole = 'student';

  Future<void> pickImages(BuildContext ctx) async {
    final List<XFile> picked = await picker.pickMultiImage();

    if (picked.length < 4) {
      ScaffoldMessenger.of(ctx).showSnackBar(
        SnackBar(content: Text("Please select at least 4 images")),
      );
      return;
    }

    setState(() {
      imageFiles = picked.map((xfile) => File(xfile.path)).toList().take(4).toList();
    });
  }

  Future<void> registerStudent(BuildContext ctx) async {
    if (imageFiles.length < 4) {
      ScaffoldMessenger.of(ctx).showSnackBar(
        SnackBar(content: Text("4 images required")),
      );
      return;
    }

    var uri = Uri.parse('http://0.0.0.0:8000:8000/sign-in/student');
    var request = http.MultipartRequest('POST', uri);

    request.fields['name'] = nameController.text;
    request.fields['email'] = emailController.text;
    request.fields['password'] = passwordController.text;
    request.fields['level'] = levelController.text;

    for (var image in imageFiles) {
      var stream = http.ByteStream(image.openRead());
      var length = await image.length();
      request.files.add(
        http.MultipartFile(
          'pictures',
          stream,
          length,
          filename: basename(image.path),
        ),
      );
    }

    try {
      var response = await request.send();
      var respStr = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = http.Response(respStr, response.statusCode);
        final decoded = jsonDecode(data.body);

        String token = decoded['access_token'];
        String message = decoded['message'];

        ScaffoldMessenger.of(ctx).showSnackBar(SnackBar(content: Text(message)));

        Navigator.pushReplacementNamed(ctx, '/home-student');
      } else {
        ScaffoldMessenger.of(ctx).showSnackBar(
          SnackBar(content: Text('Registration failed: $respStr')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(ctx).showSnackBar(
        SnackBar(content: Text("Something went wrong: $e")),
      );
    }
  }

  Future<void> registerInstructor(BuildContext ctx) async {
    var uri = Uri.parse('http://0.0.0.0:8000/sign-in/instructor');
    var request = http.MultipartRequest('POST', uri);

    request.fields['name'] = nameController.text;
    request.fields['email'] = emailController.text;
    request.fields['password'] = passwordController.text;
    request.fields['faculty'] = facultyController.text;

    try {
      var response = await request.send();
      var respStr = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final data = http.Response(respStr, response.statusCode);
        final decoded = jsonDecode(data.body);

        String token = decoded['access_token'];
        String message = decoded['message'];

        ScaffoldMessenger.of(ctx).showSnackBar(SnackBar(content: Text(message)));

        Navigator.pushReplacementNamed(ctx, '/home-instructor');
      } else {
        ScaffoldMessenger.of(ctx).showSnackBar(
          SnackBar(content: Text('Registration failed: $respStr')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(ctx).showSnackBar(
        SnackBar(content: Text("Something went wrong: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Sign Up")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              DropdownButtonFormField<String>(
                value: selectedRole,
                decoration: InputDecoration(labelText: "Select Role"),
                items: ['student', 'instructor']
                    .map((role) => DropdownMenuItem(value: role, child: Text(role)))
                    .toList(),
                onChanged: (value) {
                  setState(() {
                    selectedRole = value!;
                  });
                },
              ),
              const SizedBox(height: 10),
              TextFormField(controller: nameController, decoration: InputDecoration(labelText: "Name")),
              TextFormField(controller: emailController, decoration: InputDecoration(labelText: "Email")),
              TextFormField(
                  controller: passwordController,
                  decoration: InputDecoration(labelText: "Password"),
                  obscureText: true),
              if (selectedRole == 'student') ...[
                TextFormField(controller: levelController, decoration: InputDecoration(labelText: "Level")),
                const SizedBox(height: 10),
                ElevatedButton(
                  onPressed: () => pickImages(context),
                  child: Text("Pick 4 Pictures"),
                ),
                Text("Selected: ${imageFiles.length} images"),
              ],
              if (selectedRole == 'instructor')
                TextFormField(controller: facultyController, decoration: InputDecoration(labelText: "Faculty")),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: () {
                  if (selectedRole == 'student') {
                    registerStudent(context);
                  } else {
                    registerInstructor(context);
                  }
                },
                child: Text("Register"),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
