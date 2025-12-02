import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_reactive_ble/flutter_reactive_ble.dart';
import 'package:flutter_joystick/flutter_joystick.dart';
import 'dart:async'; 

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.landscapeLeft,
    DeviceOrientation.landscapeRight,
  ]);
  runApp(const SorterApp());
}

class SorterApp extends StatelessWidget {
  const SorterApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ControlScreen(),
    );
  }
}

class ControlScreen extends StatefulWidget {
  const ControlScreen({super.key});

  @override
  State<ControlScreen> createState() => _ControlScreenState();
}

class _ControlScreenState extends State<ControlScreen> {
  final flutterBlue = FlutterReactiveBle();
  StreamSubscription<DiscoveredDevice>? _scanSubscription;
  StreamSubscription<ConnectionStateUpdate>? _connectionSubscription;

  bool scanning = false;
  bool connected = false;

  late QualifiedCharacteristic? uartTx;

  // *** CAMBIO CRUCIAL: VOLVER AL SERVICIO NORDIC UART (NUS) ***
  final uartService = Uuid.parse("6e400001-b5a3-f393-e0a9-e50e24dcca9e");
  // Usamos el 6e400003-b5a3-f393-e0a9-e50e24dcca9e (RX) para enviar datos desde el móvil (TX)
  final uartTxChar = Uuid.parse("6e400003-b5a3-f393-e0a9-e50e24dcca9e"); 

  @override
  void dispose() {
    _scanSubscription?.cancel();
    _connectionSubscription?.cancel();
    super.dispose();
  }

  // Enviar texto al robot
  void send(String msg) async {
    if (!connected || uartTx == null) {
      print("No conectado o caracteristica no disponible.");
      return;
    }

    // Agregar el caracter de nueva línea para que Pybricks lo procese como comando completo
    final message = '$msg\n'; 
    final data = message.codeUnits;

    try {
      await flutterBlue.writeCharacteristicWithoutResponse(
        uartTx!,
        value: data,
      );
      print("Mensaje enviado: $msg");
    } catch (e) {
      print("Error al enviar mensaje: $e");
    }
  }

  // Buscar HUB (usando el Service UUID NUS)
  void scanForDevice() async {
    if (scanning) return;
    setState(() {
      scanning = true;
      connected = false;
    });

    print("Iniciando escaneo con servicio NUS...");

    // 1. Escanear solo por dispositivos que anuncian el servicio NUS
    _scanSubscription = flutterBlue.scanForDevices(withServices: [uartService]).listen((d) async {
      // 2. Filtrar por el nombre del Hub
      if (d.name.contains("Hub") || d.name == "PYBRICKS HUB") {
        print("Dispositivo encontrado: ${d.name} (${d.id})");
        
        _scanSubscription?.cancel();
        setState(() => scanning = false);

        // 3. Conectar al dispositivo
        try {
          _connectionSubscription = flutterBlue.connectToDevice(
            id: d.id,
            connectionTimeout: const Duration(seconds: 15),
          ).listen((state) async {
            if (state.connectionState == DeviceConnectionState.connected) {
              print("Conectado al dispositivo: ${d.id}");
              await discovered(d.id);
            } else if (state.connectionState == DeviceConnectionState.disconnected) {
              print("Desconectado.");
              setState(() => connected = false);
              _connectionSubscription?.cancel();
            }
          });
        } catch (e) {
          print("Error de conexión: $e");
          setState(() => scanning = false); 
        }
      }
    }, onError: (e) {
      print("Error durante el escaneo: $e");
      setState(() => scanning = false);
    });

    // Timeout para el escaneo si no encuentra nada
    Timer(const Duration(seconds: 10), () {
      if (scanning && !connected) {
        _scanSubscription?.cancel();
        setState(() => scanning = false);
        print("Escaneo terminado por timeout. Dispositivo no encontrado.");
      }
    });
  }

  // Descubrir servicios y encontrar la característica de escritura NUS
  Future<void> discovered(String id) async {
    try {
      final services = await flutterBlue.discoverServices(id);
      
      for (var s in services) {
        if (s.serviceId == uartService) {
          print("Servicio NUS encontrado.");
          for (var c in s.characteristics) {
            if (c.characteristicId == uartTxChar) {
              print("Característica NUS TX (RX del robot) encontrada.");
              uartTx = QualifiedCharacteristic(
                characteristicId: uartTxChar,
                deviceId: id,
                serviceId: uartService,
              );

              setState(() => connected = true);
              print("Conexión y descubrimiento exitosos.");
              return;
            }
          }
        }
      }
      print("Error: Característica NUS TX no encontrada.");
      setState(() => connected = false);
    } catch (e) {
      print("Error al descubrir servicios: $e");
      setState(() => connected = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          // IZQUIERDA: ESTADO + SCAN
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                connected ? "Conectado" : (scanning ? "Buscando..." : "Desconectado"),
                style: TextStyle(
                  color: connected ? Colors.green : (scanning ? Colors.yellow : Colors.red),
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: connected ? null : (scanning ? null : scanForDevice), 
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue,
                  padding: const EdgeInsets.all(20),
                ),
                child: Text(
                  scanning ? "Buscando..." : "Buscar SP-1",
                  style: const TextStyle(fontSize: 22),
                ),
              ),
            ],
          ),

          // CENTRO: JOYSTICK
          Joystick(
            mode: JoystickMode.horizontal,
            listener: (details) {
              if (!connected) return; 
              
              if (details.x > 0.3) {
                send("pos_right");
              } else if (details.x < -0.3) {
                send("pos_left");
              } else {
                send("pos_stop");
              }
            },
            base: Container(
              width: 200,
              height: 200,
              decoration: BoxDecoration(
                color: const Color.fromARGB(255, 0, 0, 0),
                shape: BoxShape.circle,
              ),
            ),
            stick: Container(
              width: 90,
              height: 90,
              decoration: const BoxDecoration(
                color: Colors.blue,
                shape: BoxShape.circle,
              ),
            ),
          ),

          // DERECHA: BOTONES L1 / R1
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ElevatedButton(
                onPressed: connected ? () => send("push_left") : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.amber,
                  minimumSize: const Size(120, 80),
                ),
                child: const Text("L1", style: TextStyle(fontSize: 26)),
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: connected ? () => send("push_right") : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.lightBlue,
                  minimumSize: const Size(120, 80),
                ),
                child: const Text("R1", style: TextStyle(fontSize: 26)),
              ),
            ],
          ),
        ],
      ),
    );
  }
}