# 🚨 Ageisresponse

> **AI-Powered Intelligent Emergency Response, Incident Prioritization, and Disaster Management Platform.**

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Backend-black.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-blue.svg)
![JavaScript](https://img.shields.io/badge/Frontend-JavaScript-yellow.svg)
![AI](https://img.shields.io/badge/AI-OpenAI%20Vision-green.svg)
![Maps](https://img.shields.io/badge/Maps-Leaflet%20%7C%20OpenStreetMap-brightgreen.svg)
![Project](https://img.shields.io/badge/Project-CODE%20CLASH%202026-orange.svg)

**Tagline: Report Faster. Coordinate Smarter. Respond Better.**

---

## 📌 Problem Statement

During natural disasters, road accidents, fires, medical emergencies, and other critical situations, effective emergency reporting and rapid response coordination are essential to saving lives and minimizing damage. However, traditional emergency management systems face several challenges that delay response operations and reduce coordination efficiency.

1. **Manual Emergency Reporting and Communication Delays:** Traditional reporting systems depend heavily on users manually entering incident details. During stressful situations, injured individuals or people with limited ability to type may struggle to provide accurate information, resulting in delayed or incomplete emergency reports.

2. **Lack of Intelligent Incident Prioritization:** Existing reporting approaches often lack automated mechanisms to evaluate incident severity, the number of people affected, emergency category, and reporting time. Consequently, critical emergencies may not receive appropriate priority.

3. **Inefficient Emergency Resource Allocation:** Assigning suitable fire, medical, and rescue teams manually can cause delays. Without location-based recommendations and team availability management, identifying the nearest appropriate response team becomes difficult.

4. **Limited Incident Visibility and Coordination:** Emergency authorities may face difficulties monitoring multiple incidents, tracking response progress, identifying available teams, and understanding incident locations through a centralized interface.

5. **Insufficient Operational Analytics:** The absence of centralized statistical dashboards makes it challenging to analyze emergency patterns, monitor team availability, identify critical cases, and support informed resource allocation decisions.

**ResQSphere** addresses these challenges through an AI-assisted emergency response and disaster management platform. Its innovative photo-to-report feature analyzes uploaded incident photographs using AI vision technology to suggest emergency categories, estimate severity, and automatically populate relevant report fields.

The platform further integrates intelligent incident prioritization, emergency team management, location-based team recommendations, incident status tracking, interactive map visualization, and analytical dashboards.

By combining AI-assisted reporting with location-aware resource recommendations and centralized monitoring, ResQSphere aims to reduce reporting delays, improve emergency coordination, and support faster, more informed disaster response decisions.

---

## 🚀 Features

| Feature | Subsystem | Technical Mechanism | Output |
|---|---|---|---|
| **AI Photo-to-Report** | AI Vision Engine | OpenAI Vision API analyzes uploaded emergency photographs | Suggested title, description, category, and severity |
| **Intelligent Incident Prioritization** | Priority Engine | Rule-based scoring using severity, affected people, category, and elapsed time | Priority score (0–99) |
| **Emergency Team Management** | Team Management | Flask REST APIs and SQLite persistence | Team registration and availability management |
| **Nearest Suitable Team Assignment** | Location Engine | Haversine geographical distance calculation and category matching | Nearest available suitable team recommendation |
| **Incident Lifecycle Tracking** | Incident Management | Controlled status transitions | Reported, Assigned, In Progress, Resolved |
| **Interactive Emergency Map** | Map Visualization | Leaflet.js and OpenStreetMap | Incident and response-team location markers |
| **Operational Analytics Dashboard** | Analytics Engine | Database aggregation and category/severity counts | Emergency statistics and team availability |
| **Separate User and Admin Portals** | Web Interface | HTML, CSS, JavaScript, and Flask routing | Dedicated reporting and administration interfaces |
| **Assignment History** | Audit Records | SQLite assignment history table | Stored team assignment records and distances |
| **Photo Capture Support** | Camera Integration | Browser Media Capture and file upload | Camera-captured or uploaded emergency photographs |

---

## 🏗️ Technology Stack

### Frontend Client

| Component | Technology | Role in Architecture |
|---|---|---|
| HTML5 | HTML | Structure of user and admin portals |
| CSS3 | CSS | Responsive layouts and interface styling |
| JavaScript | JavaScript | Form handling, dashboard interaction, and API communication |
| Leaflet.js | Leaflet | Interactive incident and team maps |
| OpenStreetMap | OSM | Map tile and geographical visualization |
| Browser Geolocation API | JavaScript API | Obtaining user location coordinates |

### Backend Services

| Component | Technology | Role in Architecture |
|---|---|---|
| Python | Python 3.11+ | Primary application runtime |
| Flask | Flask | Web application framework and REST API |
| REST API | HTTP | Communication between frontend and backend |
| OpenAI Vision API | AI Vision | Emergency photograph analysis and report suggestions |
| Werkzeug | Password Hashing | Secure admin password hashing |
| Haversine Formula | Geospatial Algorithm | Calculating geographical distance between incidents and teams |

### Storage and Configuration

| Component | Technology | Role in Architecture |
|---|---|---|
| SQLite | SQLite Database | Persistent incident and team storage |
| Python SQLite Integration | SQLite3 | Database operations and queries |
| Environment Variables | `.env` / System Environment | API keys and application configuration |
| Local File Storage | Server Filesystem | Uploaded emergency photographs |

---

## 📂 Project Structure

```text
ResQSphere/
│
├── static/
│   ├── admin.js                  # Admin dashboard functionality,
│   │                             # incident management, team assignment,
│   │                             # status updates, and analytics
│   │
│   ├── app.css                   # Application styling, responsive
│   │                             # layouts, dashboards, and UI components
│   │
│   └── user.js                   # User portal functionality,
│                                 # emergency reporting, photo upload,
│                                 # camera capture, and form handling
│
├── templates/
│   ├── admin.html                # Administrator dashboard for
│   │                             # incident monitoring, team management,
│   │                             # assignments, maps, and analytics
│   │
│   └── user.html                 # Public emergency reporting interface
│                                 # with text, photo upload, and camera capture
│
├── .env.example                  # Environment variable template for
│                                 # API keys and application configuration
│
├── .gitignore                    # Excludes environment secrets,
│                                 # Python cache, and unnecessary files
│
├── aegisresponse.db              # SQLite database containing incidents,
│                                 # emergency teams, admin accounts,
│                                 # and assignment history
│
├── app.py                        # Main Flask backend application
│                                 # REST APIs, database operations,
│                                 # AI integration, priority calculation,
│                                 # team assignment, and incident tracking
│
├── README.md                     # Project documentation and
│                                 # installation instructions
│
├── requirements.txt              # Python dependency manifest
│
└── Start_AegisResponse.bat       # Windows launcher for installing
                                  # dependencies and starting Flask
```

---

## ⚙️ Installation & Setup

### Prerequisites

- **Python:** Version 3.11 or above.
- **Git:** Version 2.30 or above.
- **Web Browser:** Chrome, Edge, or Firefox.
- **OpenAI API Key:** Required only for AI photo analysis.
- **Internet Connection:** Required for API access and map tiles.

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/ResQSphere.git
cd ResQSphere
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Configure the following environment variables before launching:

```env
OPENAI_API_KEY=your_openai_api_key
ADMIN_PASSWORD=your_secure_admin_password
FLASK_SECRET_KEY=your_random_secret_key
```

Keep actual credentials private. Never upload API keys or `.env` files to GitHub.

### Step 5: Start the Application

**Windows automatic launcher:**

Double-click:

```text
Start_AegisResponse.bat
```

Alternatively, run Flask manually using the command configured for the application.

### Step 6: Access the Application

| Interface | URL |
|---|---|
| User Portal | http://127.0.0.1:5000/ |
| Admin Dashboard | http://127.0.0.1:5000/admin |
| Health Check | http://127.0.0.1:5000/health |

**Default Demo Admin Credentials:**

```text
Username: admin
Password: admin123
```

Change the default credentials before deployment.

---

## 🧠 How It Works

ResQSphere operates through five major stages:

```text
          RESQSPHERE PLATFORM
                   |
       +-----------+-----------+
       |                       |
   USER PORTAL             ADMIN PORTAL
       |                       |
  Emergency Report       Admin Dashboard
       |                       |
       +-----------+-----------+
                   |
             FLASK BACKEND
                   |
       +-----------+-----------+
       |           |           |
    AI Vision   Priority    Team Matching
    Analysis    Engine      Algorithm
       |           |           |
       +-----------+-----------+
                   |
             SQLITE DATABASE
                   |
       +-----------+-----------+
       |           |           |
    Incident    Assignment   Team
    Tracking     History    Management
       |           |           |
       +-----------+-----------+
                   |
          MAP & ANALYTICS
```

### 1. AI-Based Photo-to-Report Processing

1. The user opens the emergency reporting portal.
2. The user uploads an image or captures a photograph using the device camera.
3. The image is sent to the Flask backend.
4. The backend validates the image format and file size.
5. The OpenAI Vision API analyzes the photograph.
6. The AI generates suggested incident information:
   - Incident title.
   - Incident description.
   - Emergency category.
   - Estimated severity.
7. The suggested information automatically fills the report form.
8. The user reviews and corrects the suggestions before submitting.

**Supported image formats:** JPG, PNG, and WEBP.

**Maximum upload size:** 8 MB.

Photo analysis is optional and requires an OpenAI API key.

### 2. Intelligent Incident Prioritization

Every submitted emergency receives a priority score between 0 and 99.

The scoring mechanism considers four parameters:

- Emergency severity.
- Number of people affected.
- Emergency category.
- Time elapsed since reporting.

The system uses a rule-based scoring algorithm to rank reported incidents.

### 3. Location-Based Emergency Team Assignment

1. The admin selects an incident for assignment.
2. The backend retrieves available emergency teams.
3. Teams are filtered according to supported emergency categories.
4. The Haversine formula calculates the geographical distance between the incident and suitable teams.
5. The nearest suitable available team is selected.
6. The assigned team status changes to Busy.
7. The incident status changes to Assigned.
8. Assignment information is stored in the assignment history table.

If coordinates are unavailable, the system selects the first suitable available team and reports the distance as unavailable.

### 4. Incident Lifecycle Management

The platform maintains the following incident workflow:

```text
      REPORTED
          |
          v
      ASSIGNED
          |
          v
     IN PROGRESS
          |
          v
       RESOLVED
```

When an incident is marked as Resolved, its assigned team automatically becomes Available.

### 5. Map Visualization and Analytics

The admin dashboard provides:

- Incident location markers.
- Emergency response team locations.
- Assigned team information.
- Incident status monitoring.
- Category-wise incident statistics.
- Severity-wise incident statistics.
- Team availability information.
- Operational KPI summaries.

Leaflet.js and OpenStreetMap provide the geographical visualization.

---

## 🧮 Incident Prioritization Algorithm

ResQSphere uses a transparent rule-based scoring mechanism.

**Priority Score (0–99)**

```text
Priority Score =
    Severity Base Score
  + Affected People Points
  + Category Bonus
  + Elapsed Time Points
```

### Severity Base Scores

| Severity | Base Score |
|---|---:|
| Low | 15 |
| Medium | 35 |
| High | 65 |
| Critical | 85 |

### Additional Scoring Parameters

| Parameter | Scoring Mechanism |
|---|---|
| Affected People | Up to 15 points |
| Fire / Building Collapse | +8 points |
| Medical / Road Accident | +5 points |
| Elapsed Reporting Time | Up to 12 points |

The final score is bounded between 0 and 99.

The priority score is used to rank incidents and support administrative decisions.

**Note:** This is a prototype decision-support algorithm, not a clinically or operationally validated emergency triage model. Human responders must make final decisions.

---

## 📍 Nearest Suitable Team Algorithm

ResQSphere uses the Haversine formula to estimate geographical distance between an emergency incident and available response teams.

The Haversine formula is:

\[
a=\sin^2\left(\frac{\Delta\phi}{2}\right)+
\cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)
\]

\[
d=2R\arcsin(\sqrt{a})
\]

Where:

- \(d\) = Distance between two geographical points.
- \(R\) = Earth's mean radius (approximately 6371 km).
- \(\phi_1,\phi_2\) = Latitude coordinates.
- \(\lambda_1,\lambda_2\) = Longitude coordinates.

### Assignment Process

1. Retrieve available response teams.
2. Filter teams based on supported emergency categories.
3. Calculate geographical distances.
4. Sort suitable teams by distance.
5. Recommend the nearest available suitable team.
6. Update team availability to Busy.
7. Store assignment history.

**Important:** Haversine calculates straight-line distance, not actual road distance or travel time.

---

## 🗄️ Database Architecture

ResQSphere uses SQLite for persistent application storage.

### 1. Incidents Table

Stores emergency report information.

| Field | Description |
|---|---|
| id | Unique incident identifier |
| title | Incident title |
| description | Incident description |
| category | Emergency category |
| severity | Incident severity |
| people | Number of affected people |
| location | Incident location |
| latitude | Geographical latitude |
| longitude | Geographical longitude |
| contact | Reporter contact |
| status | Incident lifecycle status |
| priority_score | Calculated priority score |
| assigned_team_id | Assigned response team |
| photo_filename | Uploaded image filename |
| created_at | Reporting timestamp |
| updated_at | Last updated timestamp |
| resolved_at | Resolution timestamp |

### 2. Teams Table

Stores emergency response team information.

- Team ID.
- Team name.
- Response category.
- Supported categories.
- Latitude and longitude.
- Availability.
- Assigned incident ID.
- Creation and update timestamps.

### 3. Assignment History Table

Maintains emergency team assignment records.

- Incident ID.
- Team ID.
- Assignment action.
- Calculated distance.
- Assignment timestamp.

### 4. Admins Table

Stores administrator authentication information.

- Username.
- Hashed password.

Foreign keys and database indexes support data relationships and retrieval.

---

## 🔌 REST API Architecture

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/incidents` | Retrieve priority-ranked incidents |
| POST | `/api/incidents` | Create an emergency incident |
| GET | `/api/incidents/<id>` | Retrieve incident details |
| PATCH | `/api/incidents/<id>/status` | Update incident status |
| DELETE | `/api/incidents/<id>` | Delete an incident |
| GET / POST | `/api/teams` | Retrieve or create response teams |
| PATCH | `/api/teams/<id>` | Update team availability |
| POST | `/api/incidents/<id>/assign` | Assign nearest suitable team |
| GET | `/api/assignments` | Retrieve assignment history |
| GET | `/api/analytics` | Retrieve operational analytics |
| GET | `/api/map` | Retrieve map location data |
| POST | `/api/analyse-image` | Analyze uploaded emergency photographs |
| POST | `/api/admin/login` | Authenticate administrator |
| POST | `/api/admin/logout` | End admin session |
| GET | `/api/admin/session` | Check administrator login status |
| GET | `/health` | Application health check |

Administrative operations are protected by admin authentication.

---

## 🌟 Novelty & Innovation

### Core Innovation: AI-Powered Photo-to-Emergency Reporting

Traditional emergency reporting requires users to manually enter incident information.

ResQSphere introduces an AI-powered photo-to-report feature that allows users to upload or capture an emergency photograph and automatically generate suggested report details.

**Key innovation points:**

1. **Photo-Based Emergency Reporting:** Converts uploaded emergency photographs into structured report suggestions.
2. **Reduced Manual Input:** Helps people who cannot easily type during stressful emergency situations.
3. **Intelligent Priority Scoring:** Evaluates incident information using a transparent scoring algorithm.
4. **Location-Aware Team Recommendation:** Identifies the nearest suitable available response team.
5. **Centralized Emergency Monitoring:** Combines incident reporting, team management, maps, and analytics in one platform.

The combination of AI-assisted reporting, rule-based incident prioritization, and geographical team recommendations provides a unified emergency coordination approach.

---

## 💡 Feasibility

ResQSphere is designed as a lightweight hackathon prototype using accessible technologies.

- **Cost-Effective Architecture:** Flask and SQLite avoid the need for complex enterprise infrastructure.
- **Simple Deployment:** The Windows batch launcher simplifies local application startup.
- **Modular Components:** Separate user and admin interfaces provide organized application workflows.
- **Optional AI Integration:** The platform's main reporting and management functionality works without an OpenAI API key.
- **Open-Source Mapping:** Leaflet.js and OpenStreetMap support interactive map visualization.
- **Expandable Architecture:** The backend can be extended with more advanced databases, authentication, and external emergency-service integrations.

---

## ⚠️ Limitations & Future Enhancements

### Current Prototype Limitations

- Photo analysis requires an OpenAI API key and internet access.
- AI-generated incident details and severity suggestions require human verification.
- Team availability is based on application records, not verified live field availability.
- Haversine distance represents straight-line geographical distance.
- Map routes are straight-line polylines, not turn-by-turn road navigation.
- OpenStreetMap tiles require internet connectivity.
- The prototype does not directly dispatch emergency vehicles or contact emergency services.

### Future Enhancements

1. Real-time GPS tracking of emergency response vehicles.
2. Integration with authorized emergency service providers.
3. Advanced AI-based image classification and incident assessment.
4. SMS and mobile push notifications.
5. Live road routing and traffic-aware team recommendations.
6. Advanced disaster prediction and risk mapping.
7. Multi-language and voice-assisted emergency reporting.
8. Scalable cloud database and deployment infrastructure.
9. Advanced role-based access control and audit monitoring.

---

## 🔐 Ethical Use & Operational Disclaimer

ResQSphere is a hackathon prototype developed for emergency reporting, administrative coordination, and disaster management decision support.

- **Not an Official Emergency Dispatch System:** The application does not directly dispatch emergency services.
- **Human Verification:** AI-generated incident descriptions and severity suggestions must be reviewed by users and qualified responders.
- **Location Accuracy:** Browser-provided location coordinates may be inaccurate or unavailable.
- **Data Privacy:** Real-world deployment requires appropriate protection of personal information, uploaded photographs, and location data.
- **Security:** HTTPS, CSRF protection, rate limiting, secure session management, backups, and stronger access controls are required before production deployment.

In an actual emergency, contact the appropriate official emergency services directly. Do not rely on this prototype as a substitute.

---

## 📜 License

Choose and add an appropriate open-source license before publishing the repository.

---

## 🧩 Project Information

**Project Name:** ResQSphere

**Project Category:** AI-Based Emergency Response & Disaster Management

**Event:** CODE CLASH 2026 – Round 2

**Primary Innovation:** AI-Powered Photo-to-Emergency Reporting

**Technology:** Python, Flask, SQLite, HTML, CSS, JavaScript, OpenAI Vision API, Leaflet.js, and OpenStreetMap.

**Tagline:** Report Faster. Coordinate Smarter. Respond Better.