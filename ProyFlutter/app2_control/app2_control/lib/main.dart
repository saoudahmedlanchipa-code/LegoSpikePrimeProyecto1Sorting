import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_joystick/flutter_joystick.dart';
import 'package:flutter_ble_keyboard/flutter_ble_keyboard.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark(),
      home: const ControlPage(),
    );
  }
}

class ControlPage extends StatefulWidget {
  const ControlPage({super.key});

  @override
  State<ControlPage> createState() => _ControlPageState();
}

class _ControlPageState extends State<ControlPage> {
  bool connected = false;
  String status = "Desconectado";

  final keyboard = FlutterBleKeyboard();

  Color sensorColor = Colors.grey;

  // ---------------------------
  // INICIAR TECLADO BLUETOOTH
  // ---------------------------
  Future<void> startKeyboard() async {
    try {
      await keyboard.start();
      setState(() {
        connected = true;
        status = "Conectado ✔ (Teclado Bluetooth)";
      });
    } catch (e) {
      setState(() {
        status = "Error: $e";
      });
    }
  }

  // ENVIAR TECLA AL PC
  Future<void> sendKey(String key) async {
    if (!connected) return;

    try {
      await keyboard.sendText(key);
    } catch (e) {
      debugPrint("Error enviando: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          children: [
            // ---------------- TOP BAR ----------------
            Row(
              children: [
                Expanded(
                  child: Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: connected ? Colors.green : Colors.red,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      status,
                      textAlign: TextAlign.center,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),

                const SizedBox(width: 12),

                ElevatedButton(
                  onPressed: connected ? null : startKeyboard,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    padding:
                        const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                  ),
                  child: Text(connected ? "CONECTADO" : "CONECTAR"),
                ),
              ],
            ),

            const Spacer(),

            // ---------- MAIN AREA ----------
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // -------- LEFT BUTTONS --------
                Column(
                  children: [
                    ElevatedButton(
                      onPressed: () => sendKey("w"),
                      style: ElevatedButton.styleFrom(
                        minimumSize: const Size(100, 80),
                      ),
                      child: const Text("L1 → w",
                          style: TextStyle(fontSize: 24)),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton(
                      onPressed: () => sendKey("s"),
                      style: ElevatedButton.styleFrom(
                        minimumSize: const Size(100, 80),
                      ),
                      child: const Text("R1 → s",
                          style: TextStyle(fontSize: 24)),
                    ),
                  ],
                ),

                // -------- COLOR BOX (decorativo) --------
                Container(
                  width: 150,
                  height: 150,
                  decoration: BoxDecoration(
                    color: sensorColor,
                    borderRadius: BorderRadius.circular(20),
                    border: Border.all(color: Colors.white, width: 3),
                  ),
                ),

                // -------- JOYSTICK --------
                SizedBox(
                  width: 220,
                  height: 220,
                  child: Joystick(
                    mode: JoystickMode.all,
                    listener: (details) {
                      // Usa WASD para movimientos
                      if (details.y < -0.5) sendKey("w");
                      else if (details.y > 0.5) sendKey("s");

                      if (details.x < -0.5) sendKey("a");
                      else if (details.x > 0.5) sendKey("d");
                    },
                  ),
                ),
              ],
            ),

            const Spacer(),
          ],
        ),
      ),
    );
  }
}