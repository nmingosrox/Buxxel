## 🌐 Buxxel

Decentralized marketplace for products, services, and skills. Built for creator autonomy, mobile deployment, and system clarity.

---

### 📦 Project Structure

```
Buxxel/
├── src/
│   ├── app/
│   │   ├── auth/          # User signup/login blueprint
│   │   ├── marketplace/   # Product listing and discovery
│   │   ├── dashboard/     # Seller dashboards
│   │   ├── models.py
│   │   └── __init__.py
│   ├── templates/
│   ├── static/
│   ├── config.py
│   └── run.py
├── requirements.txt
```

---

### 📲 Setup Instructions (Termux-ready)

To run Buxxel on any mobile device with Termux and Git access:

#### 1. **Install Termux dependencies**
```bash
pkg update && pkg upgrade
pkg install git python clang libffi openssl
```

#### 2. **Clone the project**
```bash
git clone https://github.com/nmingosrox/Buxxel.git
cd Buxxel/src
```

#### 3. **Set up virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 4. **Install dependencies**
```bash
pip install -r ../requirements.txt
```

#### 5. **Run the app**
```bash
export FLASK_APP=run.py
flask run
```
