# Face Recognition Attendance System 🧠📷

A real-time face recognition attendance system built using Python, OpenCV, and Firebase. It captures live video, identifies faces, and records attendance securely on the cloud.

## 🚀 Features

- Real-time face detection and recognition using `face_recognition`
- Cloud-based attendance management with Firebase Realtime Database
- Excel export for attendance reports (`pandas`)
- Simple UI with OpenCV overlays
- Automatic duplicate prevention using timestamp checks

## 📁 Project Structure

```
├── EncodeGenerator.py        # Encode and store student face data
├── main.py                   # Main real-time recognition logic
├── AddDataToDatabase.py      # Upload student data to Firebase
├── Resources/                # Background and mode display images
├── Images/                   # Training images for face encoding
├── requirements.txt          # Python package dependencies
```

## 🛠️ Tech Stack

- **Python**
- **OpenCV**
- **face_recognition**
- **Firebase (Realtime DB + Storage)**
- **NumPy, Pandas, Pickle**

## 🔐 Security Note

⚠️ **DO NOT upload `SecretKey.json`** (contains Firebase credentials). Keep it in `.gitignore`.

## 📦 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Face-Recognition-Attendance-System.git
   cd Face-Recognition-Attendance-System
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Add your `SecretKey.json` to the root directory.

4. Run the encoder:
   ```bash
   python EncodeGenerator.py
   ```

5. Start the attendance system:
   ```bash
   python main.py
   ```

## ✍️ Author

**Tashvi Aggarwal**  
📫 [LinkedIn](https://www.linkedin.com/in/tashvi-aggarwal/)  
📘 Author of [*My Entangled Thoughts*](https://amazon.in/...)  

---

## 📜 License

This project is for educational purposes only.