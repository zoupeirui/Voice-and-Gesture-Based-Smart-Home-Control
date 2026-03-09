# Voice-and-Gesture-Based-Smart-Home-Control
语音与手势融合的多模态人机交互系统
# Voice & Gesture Based Smart Home Control System

An edge-AI based smart home control system deployed on Jetson Nano, integrating speech recognition and gesture sensing for multimodal interaction.

## Project Overview

This project implements a multimodal human-computer interaction system for smart home control. 

The system integrates:

- **Speech Recognition** using Sherpa-ONNX
- **Gesture Recognition** using sensor-based smart glove
- **Natural Language Command Parsing**
- **Edge Deployment on NVIDIA Jetson Nano**

Users can control smart home devices using **voice commands or hand gestures**, improving accessibility and interaction efficiency.

## System Architecture

Voice Input → Speech Recognition → Command Parsing → Device Control  
Gesture Input → Sensor Processing → Command Mapping → Device Control

## Hardware Platform

- NVIDIA Jetson Nano 2GB
- Sensor-based smart glove
- Microphone module

## Software Stack

- Python
- Sherpa-ONNX
- ONNX Runtime
- Embedded Linux

## Features

- Real-time speech recognition on edge device
- Keyword-based command extraction
- Multimodal interaction (voice + gesture)
- Smart home device control

## Example Commands

## Demo

Demo video available in `/demo`.

## Future Work

- Improve speech command understanding
- Add LLM-based semantic parsing
- Integrate more smart home devices

-       Voice Input
          │
          ▼
   Speech Recognition
    (Sherpa-ONNX)
          │
          ▼
   Command Parsing
          │
          ▼
     Device Control
          │
          ▼
      Smart Home
          
          
      Gesture Glove
          │
          ▼
   Sensor Processing
          │
          ▼
     Command Mapping

