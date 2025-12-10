# AI Auto-Fix Pipeline

Pipeline CI/CD dengan AI Auto-Fix menggunakan Jenkins, Gemini AI, dan ML Classifier untuk otomatis memperbaiki error pada build.

## 🏗️ Arsitektur

```
┌─────────────────────────────────────────────────────────────────────┐
│                         JENKINS PIPELINE                            │
├─────────────────────────────────────────────────────────────────────┤
│  1. Checkout → 2. Install Dependencies → 3. Run Tests              │
│                                                 ↓                   │
│                                          [Test Failed?]            │
│                                                 ↓                   │
│  4. ML Classifier (Python) → 5. LLM Patch Server (Node.js)         │
│                                                 ↓                   │
│  6. Apply Patch → 7. Create PR on GitHub                           │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Ubuntu 20.04 / 22.04 LTS (fresh install)
- Akun GitHub dengan Personal Access Token
- Gemini API Key (dari Google AI Studio)

---

## 🚀 Panduan Instalasi Lengkap

### Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Install Java (OpenJDK 17)

Jenkins membutuhkan Java untuk berjalan.

```bash
# Install OpenJDK 17
sudo apt install -y openjdk-17-jdk

# Verifikasi instalasi
java -version
```

### Step 3: Install Jenkins

```bash
# Tambahkan Jenkins repository key
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

# Tambahkan repository Jenkins
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install -y jenkins

# Start dan enable Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Cek status
sudo systemctl status jenkins
```

### Step 4: Install Node.js (v18+)

```bash
# Install NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs

# Verifikasi instalasi
node --version
npm --version
```

### Step 5: Install Python 3 dan pip

```bash
# Install Python3 dan pip
sudo apt install -y python3 python3-pip python3-venv

# Verifikasi instalasi
python3 --version
pip3 --version
```

### Step 6: Install Git

```bash
sudo apt install -y git

# Verifikasi
git --version
```

### Step 7: Install Tools Tambahan

```bash
# Install curl, jq (untuk parsing JSON), dan patch
sudo apt install -y curl jq patch
```

---

## ⚙️ Konfigurasi Jenkins

### Step 1: Akses Jenkins Web UI

1. Buka browser dan akses: `http://<IP_SERVER>:8080`
2. Dapatkan password awal:
   ```bash
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Paste password tersebut di halaman Jenkins
4. Pilih **"Install suggested plugins"**
5. Buat admin user

### Step 2: Install Jenkins Plugins

Pergi ke **Manage Jenkins → Plugins → Available plugins**, install:

- **Pipeline** (biasanya sudah terinstall)
- **Git plugin**
- **GitHub plugin**
- **Credentials Binding Plugin**

Restart Jenkins setelah install plugins:
```bash
sudo systemctl restart jenkins
```

### Step 3: Konfigurasi Credentials

Pergi ke **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**

#### A. GitHub Token
1. Klik **"Add Credentials"**
2. Kind: **Secret text**
3. Secret: *Paste GitHub Personal Access Token*
4. ID: `GITHUB_TOKEN`
5. Description: `GitHub Token for PR creation`
6. Klik **Create**

> **Cara membuat GitHub Token:**
> 1. Buka https://github.com/settings/tokens
> 2. Klik "Generate new token (classic)"
> 3. Berikan scope: `repo` (full control)
> 4. Copy token yang dihasilkan

#### B. Gemini API Key
1. Klik **"Add Credentials"**
2. Kind: **Secret text**
3. Secret: *Paste Gemini API Key*
4. ID: `GEMINI_API_KEY`
5. Description: `Gemini API Key for AI patch generation`
6. Klik **Create**

> **Cara mendapatkan Gemini API Key:**
> 1. Buka https://aistudio.google.com/apikey
> 2. Klik "Create API key"
> 3. Copy API key

### Step 4: Berikan Akses Jenkins ke Folder

```bash
# Berikan ownership folder yang diperlukan
sudo chown -R jenkins:jenkins /var/lib/jenkins

# Pastikan jenkins user bisa menjalankan Python
sudo usermod -aG sudo jenkins
```

---

## 📂 Setup Project Pipeline

### Step 1: Fork/Clone Repository

```bash
# Fork repository ini ke akun GitHub kamu, lalu clone
git clone https://github.com/AryakaLeorgi/tkti-pipeline-2.git
cd tkti-pipeline-2
```

### Step 2: Update Jenkinsfile

Edit `Jenkinsfile` dan ganti `GH_REPO` dengan repository kamu:

```groovy
environment {
    NODE_ENV = "ci"
    GH_REPO = "<USERNAME>/tkti-pipeline-2"  // Ganti dengan repo kamu
}
```

Push perubahan:
```bash
git add Jenkinsfile
git commit -m "Update GH_REPO"
git push origin main
```

### Step 3: Buat Pipeline Job di Jenkins

1. Di dashboard Jenkins, klik **"New Item"**
2. Masukkan nama: `ai-auto-fix-pipeline`
3. Pilih **"Pipeline"** → Klik **OK**
4. Di bagian **Pipeline**, pilih:
   - Definition: **Pipeline script from SCM**
   - SCM: **Git**
   - Repository URL: `https://github.com/<USERNAME>/tkti-pipeline-2.git`
   - Credentials: Pilih atau tambah GitHub credentials
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
5. Klik **Save**

---

## ▶️ Menjalankan Pipeline

### Cara 1: Manual Build

1. Buka job `ai-auto-fix-pipeline`
2. Klik **"Build Now"**
3. Lihat progress di **"Console Output"**

### Cara 2: Trigger via GitHub Webhook (Opsional)

1. Di GitHub repository, pergi ke **Settings → Webhooks → Add webhook**
2. Payload URL: `http://<JENKINS_IP>:8080/github-webhook/`
3. Content type: `application/json`
4. Events: Pilih **"Just the push event"**
5. Klik **Add webhook**

---

## 🔍 Memahami Alur Pipeline

### Stage-stage Pipeline:

| Stage | Deskripsi |
|-------|-----------|
| **Checkout** | Clone repository dari GitHub |
| **Check Python** | Verifikasi Python3 dan pip tersedia |
| **Install Dependencies** | `npm install` di folder `src/` |
| **Start AI Patch Server** | Jalankan server Node.js untuk patch AI (port 3000) |
| **Start ML Classifier** | Jalankan server Python ML classifier (port 3001) |
| **Run Tests** | Jalankan `node test.js` |
| **Post (failure)** | Jika test gagal, jalankan AI Auto-Fix |

### Alur AI Auto-Fix (saat test gagal):

1. **ML Classification**: Error log dikirim ke ML Classifier untuk menentukan kategori error
2. **LLM Patch**: Jika error bisa di-fix, kirim ke Gemini AI untuk generate patch
3. **Apply Patch**: Coba apply patch dengan berbagai strategi
4. **Create PR**: Buat Pull Request dengan fix yang dihasilkan

---

## 🐛 Troubleshooting

### Error: "Python3 not found"

```bash
sudo apt install python3 python3-pip python3-venv
```

### Error: "npm command not found"

```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

### Error: "Permission denied" di Jenkins

```bash
sudo chown -R jenkins:jenkins /var/lib/jenkins
sudo chmod -R 755 /var/lib/jenkins
```

### Error: "jq command not found"

```bash
sudo apt install -y jq
```

### Error: Port 3000/3001 sudah digunakan

```bash
# Cari proses yang menggunakan port
sudo lsof -i :3000
sudo lsof -i :3001

# Kill proses jika diperlukan
sudo kill -9 <PID>
```

### Error: "Patch server failed to start"

```bash
# Cek log
cat /var/lib/jenkins/workspace/<JOB_NAME>/patch_server.log

# Pastikan GEMINI_API_KEY sudah dikonfigurasi dengan benar
```

### Error: "ML Classifier failed to start"

```bash
# Cek log
cat /var/lib/jenkins/workspace/<JOB_NAME>/ml_classifier.log

# Coba jalankan manual untuk debug
cd ml-classifier
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python train.py
python server.py
```

---

## 📁 Struktur Project

```
tkti-pipeline-2/
├── Jenkinsfile              # Pipeline definition
├── README.md                # Dokumentasi ini
├── requirements.txt         # Python dependencies (root)
│
├── src/                     # Source code utama
│   ├── auth.js              # Module autentikasi (contoh)
│   ├── test.js              # Test runner
│   └── package.json         # Node.js dependencies
│
├── explain-error/           # AI Patch Server (Gemini)
│   ├── patch-server.js      # Express server untuk AI patch
│   ├── explain.js           # Logic untuk explain error
│   └── package.json         # Dependencies
│
├── ml-classifier/           # ML Error Classifier
│   ├── server.py            # FastAPI server
│   ├── model.py             # ML model logic
│   ├── train.py             # Training script
│   ├── training_data.py     # Training data
│   └── requirements.txt     # Python dependencies
│
└── docs/                    # Dokumentasi tambahan
    └── paper.tex            # Paper LaTeX
```

---

## 🎯 Demo: Simulasi Error

Untuk testing pipeline dengan error yang bisa di-fix:

1. Edit `src/auth.js`, ubah `.test(` menjadi `.tset(` (typo)
2. Commit dan push
3. Pipeline akan detect error dan AI akan membuat fix PR

---

## 📜 License

MIT License - Silakan gunakan untuk keperluan edukasi.

---

## 👨‍💻 Author

Dibuat untuk Tugas Kuliah TKTI (Teknologi Komputasi Terapan dan Infrastruktur)
