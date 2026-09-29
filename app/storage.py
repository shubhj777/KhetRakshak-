"""SQLite Persistence & In-Memory Store for KhetRakshak.
Tracks farmer accounts, farm profiles, scan timeline, alerts, and surveillance analytics.
"""

import sqlite3
import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.models import FarmProfile, SmartAlert

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "khetrakshak.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Farmers / Users Authentication table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_name TEXT NOT NULL,
            mobile_number TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            district TEXT NOT NULL,
            block TEXT,
            village TEXT,
            primary_crop TEXT NOT NULL,
            other_crops TEXT,
            land_area REAL,
            land_area_unit TEXT DEFAULT 'Acres',
            crop_stage TEXT,
            irrigation_type TEXT,
            soil_type TEXT,
            preferred_language TEXT DEFAULT 'hi',
            is_demo INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 2. Profile table (active farm snapshot)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_profile (
            id INTEGER PRIMARY KEY,
            farmer_name TEXT,
            district TEXT,
            village_block TEXT,
            crop TEXT,
            crop_stage TEXT,
            farm_size_acres REAL,
            irrigation_type TEXT,
            soil_type TEXT,
            latitude REAL,
            longitude REAL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 3. Scan timeline table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scan_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            crop TEXT,
            crop_stage TEXT,
            possible_issue TEXT,
            hindi_issue TEXT,
            confidence REAL,
            severity TEXT,
            overall_score INTEGER,
            risk_level TEXT,
            notes TEXT
        )
    """)

    # 4. Smart alerts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS smart_alerts (
            id TEXT PRIMARY KEY,
            title TEXT,
            title_hindi TEXT,
            category TEXT,
            severity TEXT,
            icon TEXT,
            reason TEXT,
            reason_hindi TEXT,
            recommended_action TEXT,
            recommended_action_hindi TEXT,
            district TEXT,
            crop TEXT,
            timestamp TEXT
        )
    """)

    conn.commit()

    # Pre-seed 5 realistic Bihar Demo Farmers
    cursor.execute("SELECT COUNT(*) FROM farmers")
    if cursor.fetchone()[0] == 0:
        demo_accounts = [
            (
                "Ramesh Kumar Yadav", "9800011111", "demo", "Purnia", "Kasba", "Madhavpur",
                "Maize", "Paddy, Mustard", 3.0, "Acres", "Flowering & Tasseling",
                "Borewell / Tube-well", "Sandy Loam Alluvium", "hi", 1
            ),
            (
                "Suresh Manjhi", "9800022222", "demo", "Gaya", "Bodh Gaya", "Bakror",
                "Wheat", "Gram, Mustard", 2.5, "Acres", "Vegetative (Jointing)",
                "Check Dam / Tube-well", "Old Alluvium / Red Sandy Silt", "hi", 1
            ),
            (
                "Arun Kumar Singh", "9800033333", "demo", "Bhagalpur", "Sabour", "Khanjarpur",
                "Paddy", "Maize, Jardalu Mango", 4.0, "Acres", "Tillering",
                "Canal / River Lift", "Fine Alluvial Silt Loam", "hi", 1
            ),
            (
                "Mukesh Chandra", "9800044444", "demo", "Muzaffarpur", "Mushahari", "Patahi",
                "Litchi", "Vegetables, Paddy", 5.0, "Acres", "Fruit Development",
                "Drip Irrigation", "Calcareous Alluvium (Lime-rich)", "hi", 1
            ),
            (
                "Dharmendra Rai", "9800055555", "demo", "Rohtas", "Nokha", "Baraon",
                "Paddy", "Wheat, Lentil", 6.0, "Acres", "Tillering & Growth",
                "Sone Canal Network", "Rich Sone Alluvium", "hi", 1
            )
        ]
        cursor.executemany("""
            INSERT INTO farmers
            (farmer_name, mobile_number, password, district, block, village, primary_crop, other_crops, land_area, land_area_unit, crop_stage, irrigation_type, soil_type, preferred_language, is_demo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_accounts)
        conn.commit()

    # Populate default demo profile if empty
    cursor.execute("SELECT COUNT(*) FROM farm_profile")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO farm_profile 
            (id, farmer_name, district, village_block, crop, crop_stage, farm_size_acres, irrigation_type, soil_type, latitude, longitude)
            VALUES (1, 'Ramesh Kumar Yadav', 'Purnia', 'Kasba Block', 'Maize', 'Flowering & Tasseling', 3.0, 'Borewell / Tube-well', 'Sandy Loam Alluvium', 25.7771, 87.4753)
        """)
        conn.commit()

    # Populate initial timeline history
    cursor.execute("SELECT COUNT(*) FROM scan_history")
    if cursor.fetchone()[0] == 0:
        now = datetime.now()
        cursor.executemany("""
            INSERT INTO scan_history 
            (timestamp, crop, crop_stage, possible_issue, hindi_issue, confidence, severity, overall_score, risk_level, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                (now - timedelta(days=3)).strftime("%d %b, %I:%M %p"),
                "Maize",
                "Vegetative (Knee-high)",
                "Healthy Maize",
                "स्वस्थ मक्का",
                0.94,
                "None",
                28,
                "LOW",
                "Crop growth normal, moisture balanced"
            ),
            (
                (now - timedelta(days=1)).strftime("%d %b, %I:%M %p"),
                "Maize",
                "Flowering & Tasseling",
                "Maydis Leaf Blight (Early)",
                "मेडीस लीफ ब्लाइट (प्रारंभिक)",
                0.86,
                "Moderate",
                58,
                "MODERATE",
                "Light rain showers, early leaf lesions appeared"
            )
        ])
        conn.commit()

    # Populate initial alerts
    cursor.execute("SELECT COUNT(*) FROM smart_alerts")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO smart_alerts 
            (id, title, title_hindi, category, severity, icon, reason, reason_hindi, recommended_action, recommended_action_hindi, district, crop, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            (
                "alert-101",
                "Flood & Waterlogging Alert",
                "बाढ़ एवं जलजमाव चेतावनी",
                "FLOOD",
                "CRITICAL",
                "🌊",
                "Heavy rainfall forecast (88.5 mm) in saturated Kosi catchment.",
                "कोसी जलग्रहण क्षेत्र में भारी बारिश (88.5 मिमी) का पूर्वानुमान।",
                "Halt scheduled irrigation and open perimeter drainage channels.",
                "सिंचाई तुरंत रोकें और खेत की जल निकासी नाली साफ रखें।",
                "Purnia",
                "Maize",
                "Today, 06:30 AM"
            ),
            (
                "alert-102",
                "Crop Disease Alert",
                "फसल रोग चेतावनी",
                "DISEASE",
                "WARNING",
                "🦠",
                "Maydis leaf blight symptoms detected in latest scan.",
                "नवीनतम स्कैन में पर्ण अंगमारी के लक्षण पाए गए।",
                "Inspect lower leaves. Prepare Mancozeb 75% WP spray once rainfall stops.",
                "निचली पत्तियों की जांच करें। बारिश रुकते ही मैंकोजेब का छिड़काव करें।",
                "Purnia",
                "Maize",
                "Today, 08:15 AM"
            ),
            (
                "alert-103",
                "Weather-to-Crop Advisory",
                "मौसम-फसल परामर्श",
                "ADVISORY",
                "WARNING",
                "🌦️",
                "Maize is in sensitive flowering phase; pollen wash risk high.",
                "मक्का अत्यंत संवेदनशील मंजर अवस्था में है; परागकण धुलने का जोखिम।",
                "Avoid chemical spraying during rainfall to prevent chemical runoff.",
                "बारिश के दौरान कीटनाशक न छिड़कें।",
                "Purnia",
                "Maize",
                "Yesterday, 04:00 PM"
            )
        ])
        conn.commit()

    conn.close()

# ----------------- Farmer Authentication & Profile Functions -----------------

def register_farmer(data: Dict[str, Any]) -> Dict[str, Any]:
    """Registers a new farmer in SQLite database."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    mobile = str(data.get("mobile_number", "")).strip()
    cursor.execute("SELECT id FROM farmers WHERE mobile_number = ?", (mobile,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise ValueError("Mobile number is already registered. Please login.")

    cursor.execute("""
        INSERT INTO farmers
        (farmer_name, mobile_number, password, district, block, village, primary_crop, other_crops, land_area, land_area_unit, crop_stage, irrigation_type, soil_type, preferred_language, is_demo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("farmer_name", "Farmer"),
        mobile,
        data.get("password", "123456"),
        data.get("district", "Purnia"),
        data.get("block", ""),
        data.get("village", ""),
        data.get("primary_crop", "Maize"),
        data.get("other_crops", ""),
        float(data.get("land_area", 2.5)),
        data.get("land_area_unit", "Acres"),
        data.get("crop_stage", "Flowering"),
        data.get("irrigation_type", "Borewell / Tube-well"),
        data.get("soil_type", "Alluvial Loam"),
        data.get("preferred_language", "hi"),
        0
    ))
    new_id = cursor.lastrowid
    conn.commit()

    # Also sync into current active farm_profile
    cursor.execute("""
        UPDATE farm_profile SET
            farmer_name=?, district=?, village_block=?, crop=?, crop_stage=?,
            farm_size_acres=?, irrigation_type=?, soil_type=?
        WHERE id=1
    """, (
        data.get("farmer_name"), data.get("district"),
        f"{data.get('block', '')} Block", data.get("primary_crop"),
        data.get("crop_stage"), float(data.get("land_area", 2.5)),
        data.get("irrigation_type"), data.get("soil_type")
    ))
    conn.commit()
    conn.close()

    return get_farmer_by_id(new_id)

def authenticate_farmer(mobile: str, password: str) -> Optional[Dict[str, Any]]:
    """Validates mobile and password against farmers table."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, farmer_name, mobile_number, password, district, block, village, primary_crop,
               other_crops, land_area, land_area_unit, crop_stage, irrigation_type,
               soil_type, preferred_language, is_demo
        FROM farmers
        WHERE mobile_number = ?
    """, (mobile.strip(),))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None

    stored_pwd = row[3] or ""
    is_demo = bool(row[15])
    input_pwd = password.strip()

    # Password validation: exact match, or standard demo passwords for demo accounts
    if stored_pwd != input_pwd:
        if not (is_demo and input_pwd in ["demo", "123456", "demo_password", "password123"]):
            return None

    farmer_dict = {
        "id": row[0],
        "farmer_name": row[1],
        "mobile_number": row[2],
        "district": row[4],
        "block": row[5],
        "village": row[6],
        "primary_crop": row[7],
        "other_crops": row[8],
        "land_area": row[9],
        "land_area_unit": row[10],
        "crop_stage": row[11],
        "irrigation_type": row[12],
        "soil_type": row[13],
        "preferred_language": row[14],
        "is_demo": bool(row[15])
    }

    # Sync into farm_profile
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE farm_profile SET
            farmer_name=?, district=?, village_block=?, crop=?, crop_stage=?,
            farm_size_acres=?, irrigation_type=?, soil_type=?
        WHERE id=1
    """, (
        farmer_dict["farmer_name"], farmer_dict["district"],
        f"{farmer_dict['block']} Block", farmer_dict["primary_crop"],
        farmer_dict["crop_stage"], farmer_dict["land_area"],
        farmer_dict["irrigation_type"], farmer_dict["soil_type"]
    ))
    conn.commit()
    conn.close()

    return farmer_dict

def get_farmer_by_id(farmer_id: int) -> Optional[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, farmer_name, mobile_number, district, block, village, primary_crop,
               other_crops, land_area, land_area_unit, crop_stage, irrigation_type,
               soil_type, preferred_language, is_demo
        FROM farmers WHERE id = ?
    """, (farmer_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    return {
        "id": row[0],
        "farmer_name": row[1],
        "mobile_number": row[2],
        "district": row[3],
        "block": row[4],
        "village": row[5],
        "primary_crop": row[6],
        "other_crops": row[7],
        "land_area": row[8],
        "land_area_unit": row[9],
        "crop_stage": row[10],
        "irrigation_type": row[11],
        "soil_type": row[12],
        "preferred_language": row[13],
        "is_demo": bool(row[14])
    }

def get_demo_farmers() -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, farmer_name, mobile_number, district, block, village, primary_crop,
               land_area, crop_stage
        FROM farmers WHERE is_demo = 1 ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "farmer_name": r[1],
            "mobile_number": r[2],
            "district": r[3],
            "block": r[4],
            "village": r[5],
            "primary_crop": r[6],
            "land_area": r[7],
            "crop_stage": r[8]
        }
        for r in rows
    ]

# ----------------- Active Profile Functions -----------------

def get_profile() -> FarmProfile:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT farmer_name, district, village_block, crop, crop_stage, farm_size_acres, irrigation_type, soil_type, latitude, longitude FROM farm_profile WHERE id=1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return FarmProfile(
            farmer_name=row[0],
            district=row[1],
            village_block=row[2],
            crop=row[3],
            crop_stage=row[4],
            farm_size_acres=row[5],
            irrigation_type=row[6],
            soil_type=row[7],
            latitude=row[8],
            longitude=row[9]
        )
    return FarmProfile()

def update_profile(p: FarmProfile) -> FarmProfile:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE farm_profile SET
            farmer_name=?, district=?, village_block=?, crop=?, crop_stage=?,
            farm_size_acres=?, irrigation_type=?, soil_type=?, latitude=?, longitude=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE id=1
    """, (p.farmer_name, p.district, p.village_block, p.crop, p.crop_stage, p.farm_size_acres, p.irrigation_type, p.soil_type, p.latitude, p.longitude))
    conn.commit()
    conn.close()
    return p

def add_scan_history(entry: Dict[str, Any]):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_history
        (timestamp, crop, crop_stage, possible_issue, hindi_issue, confidence, severity, overall_score, risk_level, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        entry.get("timestamp", datetime.now().strftime("%d %b, %I:%M %p")),
        entry.get("crop", "Maize"),
        entry.get("crop_stage", "Flowering"),
        entry.get("possible_issue", "Healthy"),
        entry.get("hindi_issue", "स्वस्थ"),
        entry.get("confidence", 0.9),
        entry.get("severity", "None"),
        entry.get("overall_score", 50),
        entry.get("risk_level", "MODERATE"),
        entry.get("notes", "")
    ))
    conn.commit()
    conn.close()

def get_scan_timeline() -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, crop, crop_stage, possible_issue, hindi_issue, confidence, severity, overall_score, risk_level, notes FROM scan_history ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "timestamp": r[0],
            "crop": r[1],
            "crop_stage": r[2],
            "possible_issue": r[3],
            "hindi_issue": r[4],
            "confidence": r[5],
            "severity": r[6],
            "overall_score": r[7],
            "risk_level": r[8],
            "notes": r[9]
        }
        for r in rows
    ]

def get_alerts() -> List[Dict[str, Any]]:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, title_hindi, category, severity, icon, reason, reason_hindi, recommended_action, recommended_action_hindi, district, crop, timestamp FROM smart_alerts ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "title": r[1],
            "title_hindi": r[2],
            "category": r[3],
            "severity": r[4],
            "icon": r[5],
            "reason": r[6],
            "reason_hindi": r[7],
            "recommended_action": r[8],
            "recommended_action_hindi": r[9],
            "district": r[10],
            "crop": r[11],
            "timestamp": r[12]
        }
        for r in rows
    ]

def get_admin_metrics() -> Dict[str, Any]:
    """Provides simulated state-level surveillance statistics for Department of Agriculture / KVK / DMD Bihar."""
    return {
        "title": "Bihar Agricultural Risk Surveillance Dashboard",
        "jurisdiction": "Government of Bihar - Krishi Vibhag & Disaster Management Dept",
        "monitored_farms": 14250,
        "high_risk_districts_count": 8,
        "high_risk_districts": ["Purnia", "Darbhanga", "Saharsa", "Supaul", "Khagaria", "Kishanganj", "Gaya", "Nawada"],
        "active_flood_alerts_farms": 1240,
        "disease_outbreak_alerts": 486,
        "water_stress_drought_alerts": 318,
        "river_basins_alert": [
            {"river": "Kosi Basin (Birpur)", "status": "Near Warning Mark (High Discharge)", "risk": "HIGH"},
            {"river": "Kamla Balan (Jhanjharpur)", "status": "Above Danger Level (+0.42m)", "risk": "SEVERE"},
            {"river": "Bagmati (Benibad)", "status": "Rising Rapidly", "risk": "HIGH"},
            {"river": "Ganga (Patna/Bhagalpur)", "status": "Below Warning Level (Steady)", "risk": "MODERATE"},
            {"river": "Gandak (Valmiki Nagar)", "status": "Controlled Discharge", "risk": "MODERATE"},
            {"river": "Falgu (Gaya)", "status": "Dry Riverbed (Moisture Deficit)", "risk": "DROUGHT"}
        ],
        "crop_vulnerability_summary": [
            {"crop": "Maize", "acreage_at_risk_ha": 34500, "dominant_threat": "Waterlogging during flowering & Maydis Blight"},
            {"crop": "Paddy", "acreage_at_risk_ha": 48200, "dominant_threat": "Early submergence & Bacterial Blight in North Bihar; Drought in South Bihar"},
            {"crop": "Makhana", "acreage_at_risk_ha": 6800, "dominant_threat": "Pond water exchange & pest surveillance in Mithilanchal"},
            {"crop": "Sugarcane", "acreage_at_risk_ha": 18200, "dominant_threat": "Water stagnation root rot in West Champaran"}
        ],
        "disclaimer": "Prototype telemetry aggregated from participating KVK centers and farmer uploads for demonstration."
    }
