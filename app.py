import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import re

# ==============================================================================
# 1. إعداد الصفحة الأساسي بنسق عريض متناسق متكامل مع هوية آبل البصرية
# ==============================================================================
st.set_page_config(
    page_title="إستبرق الدولية - منظومة الرقابة المالية وإدارة الشحنات الموحدة",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. حقن التنسيقات الفاخرة المخصصة واجهات ستريمليت بالكامل (Premium CSS Styling)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap');

/* إعادة صياغة الخطوط والاتجاهات بمفهوم آبل ولمسات البرونز الفخمة */
html, body, [data-testid="stSidebar"], .stApp {
    font-family: 'Cairo', sans-serif;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f8fafc;
    color: #0f172a;
}

.stHeading, .stMarkdown, p, div, label, span, h1, h2, h3, h4, h5, h6 {
    text-align: right !important;
    direction: rtl !important;
}

/* تخصيص مظهر الحقول المخصصة للإدخال لتتوافق مع اللغة العربية */
input, textarea, select, .stSelectbox {
    direction: rtl !important;
    text-align: right !important;
}

/* إخفاء عناصر ستريمليت الافتراضية للارتقاء بواجهة المستخدم للمظهر التجاري */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
[data-testid="stHeader"] {background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(12px); border-bottom: 1px solid #e2e8f0;}

/* تخصيص مظهر القائمة الجانبية الفاخرة بالتدرج اللوني لشركة إستبرق */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #091e14 0%, #112a1f 100%) !important;
    border-left: 1px solid rgba(255, 255, 255, 0.05);
}
[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}

/* بطاقات الموقف المالي الراقية (Responsive Premium Cards) */
.kpi-container {
    display: flex;
    gap: 18px;
    flex-wrap: wrap;
    margin-bottom: 25px;
    direction: rtl !important;
}
.kpi-card {
    flex: 1;
    min-width: 250px;
    background: #ffffff;
    padding: 24px;
    border-radius: 20px;
    border: 1px solid rgba(226, 232, 240, 0.8);
    box-shadow: 0 8px 30px rgba(148, 163, 184, 0.04);
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(17, 42, 31, 0.08);
    border-color: rgba(17, 42, 31, 0.15);
}
.kpi-card h5 { 
    margin: 0 0 10px 0 !important; 
    color: #64748b !important; 
    font-size: 13px !important; 
    font-weight: 800 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.5px;
}
.kpi-card h2 { 
    margin: 0 !important; 
    font-size: 28px !important; 
    font-weight: 900 !important; 
    color: #112a1f !important; 
}
.kpi-card p { 
    margin: 8px 0 0 0 !important; 
    font-size: 11.5px !important; 
    color: #94a3b8 !important; 
}

/* تصميم الجداول الذكية المستقرة والراقية المتوافقة تماماً مع شاشات الجوال */
.enterprise-table-container {
    width: 100%;
    overflow-x: auto;
    direction: rtl !important;
    margin: 20px 0;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.01);
}
table.corporate-data-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl !important;
    text-align: right !important;
}
table.corporate-data-table th {
    background-color: #112a1f !important;
    color: #ffffff !important;
    padding: 16px 20px;
    font-weight: 800;
    font-size: 14px;
    border-bottom: 2px solid #091e14;
    white-space: nowrap;
    text-align: right !important;
}
table.corporate-data-table td {
    padding: 14px 20px;
    text-align: right !important;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
    font-size: 13.5px;
    font-weight: 600;
    white-space: nowrap;
}
table.corporate-data-table tr:nth-child(even) { background-color: #f8fafc; }
table.corporate-data-table tr:hover { background-color: #f1f5f9; }

/* أزرار الإجراءات والتحكم بتصميم Apple الراقي بلمسات ذهبية تفاعلية */
div.stButton > button:first-child {
    background-color: #112a1f !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    width: 100% !important;
    border-radius: 14px !important;
    height: 48px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    font-size: 14.5px !important;
    box-shadow: 0 6px 20px rgba(17, 42, 31, 0.15) !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div.stButton > button:hover { 
    background-color: #1a3f2f !important; 
    border-color: #c5a880 !important;
    transform: translateY(-2px);
    box-shadow: 0 12px 30px rgba(17, 42, 31, 0.25) !important;
}

/* شارات الحالة الملونة الحديثة */
.status-badge { padding: 5px 12px; border-radius: 10px; font-size: 11.5px; font-weight: 800; display: inline-block; }
.status-green { background-color: #d1fae5; color: #065f46; }
.status-red { background-color: #fee2e2; color: #991b1b; }
.status-orange { background-color: #fef3c7; color: #92400e; }

/* تحسين تجاوب علامات التبويب واستغلال المساحات */
div[data-testid="stTabBar"] {
    background-color: #ffffff;
    padding: 6px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
div[data-testid="stTabBar"] button {
    font-size: 14px !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
}
div[data-testid="stTabBar"] button[aria-selected="true"] {
    background-color: #112a1f !important;
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. الوظائف والمساعدات الحسابية والبرمجية الذكية (Smart General Helpers)
# ==============================================================================
def safe_float(val):
    """تحويل القيم المدخلة إلى قيم عشرية بطريقة آمنة تتجنب الانهيار والأخطاء الكامنة"""
    try:
        if pd.isna(val) or val is None:
            return 0.0
        # معالجة النصوص المنظفة من العملات والرموز المزعجة
        if isinstance(val, str):
            val = val.replace('$', '').replace('د.ل', '').replace(',', '').strip()
        return float(val)
    except (ValueError, TypeError):
        return 0.0

def parse_any_date(date_val):
    """دالة ذكية لقراءة التواريخ وصياغتها بنسق موحد YYYY-MM-DD لمطابقة المدخلات العشوائية"""
    if pd.isna(date_val) or date_val is None or str(date_val).strip() == "":
        return datetime.now().strftime('%Y-%m-%d')
    if isinstance(date_val, datetime):
        return date_val.strftime('%Y-%m-%d')
    if hasattr(date_val, 'strftime'):
        return date_val.strftime('%Y-%m-%d')
    
    date_str = str(date_val).strip()
    # تجربة صيغ التحليل والتحويل الممكنة
    formats = ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d', '%d-%m-%Y', '%Y-%m-%d %H:%M:%S']
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
            
    # إذا تعذر تحليلها بالكامل، يتم تنظيف الصيغة أو إرجاع التاريخ الحالي كخيار افتراضي آمن
    return date_str

def to_excel(df):
    """تصدير وتحويل مخرجات كشوف الحساب النشطة حالياً إلى ملف إكسل رسمي"""
    output = io.BytesIO()
    clean_df = df.copy()
    
    # استبعاد الأعمدة البرمجية الداخلية والتقنية قبل عملية التصدير للزبون
    internal_cols = ['selector_label', 'selector_text', 'profit_usd', 'id']
    clean_df.drop(columns=[col for col in internal_cols if col in clean_df.columns], errors='ignore', inplace=True)
    
    # إعادة تسمية الأعمدة للمسميات الرسمية الفاخرة
    translation_dict = {
        'customer_name': 'اسم الزبون',
        'container_number': 'رقم الحاوية',
        'bl_number': 'رقم البوليصة',
        'shipment_date': 'التاريخ',
        'do_number': 'رقم إذن التسليم DO',
        'do_value_lyd': 'قيمة أمر التسليم (د.ل)',
        'agency_freight_usd': 'شحن الوكالة ($)',
        'final_freight_usd': 'الشحن النهائي للزبون ($)',
        'amount': 'المبلغ المقبوض',
        'currency': 'العملة',
        'receipt_date': 'تاريخ السند',
        'notes': 'ملاحظات السند'
    }
    clean_df.rename(columns=translation_dict, errors='ignore', inplace=True)
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        clean_df.to_excel(writer, index=False, sheet_name='كشف الحساب الرسمي')
        workbook  = writer.book
        worksheet = writer.sheets['كشف الحساب الرسمي']
        # ضبط محاذاة البيانات لتكون من اليمين إلى اليسار تلقائياً
        worksheet.right_to_left()
        
    return output.getvalue()

# ==============================================================================
# 4. إدارة الاتصال بقاعدة البيانات السحابية مع نظام المحاكاة الاحتياطي المستقر
# ==============================================================================
def get_db_connection():
    if "postgres" not in st.secrets:
        return None
    try:
        db_url = st.secrets["postgres"]["url"]
        return psycopg2.connect(db_url, cursor_factory=DictCursor)
    except Exception:
        return None

def init_db():
    conn = get_db_connection()
    if conn is None:
        # تهيئة البيانات الافتراضية في الذاكرة (Session State) للمحاكاة الفورية والتشغيل المستقر
        if "mock_db" not in st.session_state:
            st.session_state["mock_db"] = {
                "customers": [
                    {"id": 1, "name": "أحمد فايد"},
                    {"id": 2, "name": "الهادي الأحول"},
                    {"id": 3, "name": "مجموعة الوفاق للاستيراد"}
                ],
                "shipments": [
                    {"id": 1, "customer_name": "أحمد فايد", "container_number": "MSKU8831920", "bl_number": "MBL-77123", "shipment_date": "2026-06-15", "do_number": "DO-9012", "do_value_lyd": 1905.00, "agency_freight_usd": 1200.00, "final_freight_usd": 1450.00},
                    {"id": 2, "customer_name": "أحمد فايد", "container_number": "MSKU1120491", "bl_number": "MBL-77123", "shipment_date": "2026-06-15", "do_number": "DO-9013", "do_value_lyd": 0.00, "agency_freight_usd": 1200.00, "final_freight_usd": 0.00},
                    {"id": 3, "customer_name": "الهادي الأحول", "container_number": "SUDU4491029", "bl_number": "MBL-88124", "shipment_date": "2026-06-20", "do_number": "DO-8831", "do_value_lyd": 21212.00, "agency_freight_usd": 1800.00, "final_freight_usd": 2100.00},
                    {"id": 4, "customer_name": "مجموعة الوفاق للاستيراد", "container_number": "CMAU7718290", "bl_number": "MBL-99120", "shipment_date": "2026-06-25", "do_number": "", "do_value_lyd": 3400.00, "agency_freight_usd": 1500.00, "final_freight_usd": 1750.00}
                ],
                "receipts": [
                    {"id": 1, "customer_name": "أحمد فايد", "amount": 1000.00, "currency": "دولار أمريكي USD", "receipt_date": "2026-06-18", "notes": "دفعة نقدية بالدولار"},
                    {"id": 2, "customer_name": "الهادي الأحول", "amount": 15000.00, "currency": "دينار ليبي LYD", "receipt_date": "2026-06-22", "notes": "حوالة مصرفية جارية"}
                ]
            }
        return

    try:
        with conn.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    id SERIAL PRIMARY KEY, 
                    customer_name TEXT, 
                    container_number TEXT, 
                    bl_number TEXT,
                    shipment_date TEXT, 
                    do_number TEXT, 
                    do_value_lyd DOUBLE PRECISION DEFAULT 0.0,
                    agency_freight_usd DOUBLE PRECISION DEFAULT 0.0, 
                    final_freight_usd DOUBLE PRECISION DEFAULT 0.0
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS receipts (
                    id SERIAL PRIMARY KEY, 
                    customer_name TEXT, 
                    amount DOUBLE PRECISION DEFAULT 0.0,
                    currency TEXT, 
                    receipt_date TEXT, 
                    notes TEXT
                )
            """)
            conn.commit()
    except Exception as e:
        st.error(f"❌ خطأ في تهيئة جداول قاعدة البيانات: {e}")
    finally:
        conn.close()

# تهيئة قاعدة البيانات مباشرة مع إقلاع المنظومة
init_db()

# ==============================================================================
# 5. دوال جلب وتعديل البيانات الذكية لدمج قواعد البيانات والمحاكاة التلقائية
# ==============================================================================
def db_query(query, params=None, fetch=True):
    conn = get_db_connection()
    if conn is None:
        # توجيه الاستعلام تلقائياً إلى قاعدة البيانات المحلية في حالة غياب الاتصال السحابي
        if "SELECT * FROM customers" in query:
            return st.session_state["mock_db"]["customers"]
        elif "SELECT * FROM shipments" in query:
            return st.session_state["mock_db"]["shipments"]
        elif "SELECT * FROM receipts" in query:
            return st.session_state["mock_db"]["receipts"]
        elif "SELECT id FROM shipments" in query and params:
            # معالج التحقق من وجود الحاوية لمنع التكرار جراء الاستيراد المجمع
            container, bl = params[0], params[1]
            return [s for s in st.session_state["mock_db"]["shipments"] if s["container_number"] == container and s["bl_number"] == bl]
        return []
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if fetch:
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            conn.commit()
            return True
    except Exception as e:
        st.error(f"❌ خطأ في الاستعلام السحابي: {e}")
        return []
    finally:
        conn.close()

def db_execute(query, params=None):
    conn = get_db_connection()
    if conn is None:
        # معالجة حركات الإدخال والتعديل والحذف يدوياً داخل هيكل المحاكاة
        if "INSERT INTO customers" in query:
            new_id = len(st.session_state["mock_db"]["customers"]) + 1
            # التحقق من عدم التكرار
            if not any(c['name'] == params[0] for c in st.session_state["mock_db"]["customers"]):
                st.session_state["mock_db"]["customers"].append({"id": new_id, "name": params[0]})
        elif "INSERT INTO shipments" in query:
            new_id = len(st.session_state["mock_db"]["shipments"]) + 1
            st.session_state["mock_db"]["shipments"].insert(0, {
                "id": new_id, "customer_name": params[0], "container_number": params[1], "bl_number": params[2],
                "shipment_date": params[3], "do_number": params[4], "do_value_lyd": params[5],
                "agency_freight_usd": params[6], "final_freight_usd": params[7]
            })
        elif "INSERT INTO receipts" in query:
            new_id = len(st.session_state["mock_db"]["receipts"]) + 1
            st.session_state["mock_db"]["receipts"].insert(0, {
                "id": new_id, "customer_name": params[0], "amount": params[1], "currency": params[2],
                "receipt_date": params[3], "notes": params[4]
            })
        elif "UPDATE shipments SET" in query:
            for s in st.session_state["mock_db"]["shipments"]:
                if s["id"] == params[-1]:
                    s["container_number"] = params[0]
                    s["bl_number"] = params[1]
                    s["shipment_date"] = params[2]
                    s["do_number"] = params[3]
                    s["do_value_lyd"] = params[4]
                    s["agency_freight_usd"] = params[5]
                    s["final_freight_usd"] = params[6]
        elif "UPDATE receipts SET" in query:
            for r in st.session_state["mock_db"]["receipts"]:
                if r["id"] == params[-1]:
                    r["amount"] = params[0]
                    r["currency"] = params[1]
                    r["receipt_date"] = params[2]
                    r["notes"] = params[3]
        elif "UPDATE customers" in query:
            for c in st.session_state["mock_db"]["customers"]:
                if c["name"] == params[1]: c["name"] = params[0]
            for s in st.session_state["mock_db"]["shipments"]:
                if s["customer_name"] == params[1]: s["customer_name"] = params[0]
            for r in st.session_state["mock_db"]["receipts"]:
                if r["customer_name"] == params[1]: r["customer_name"] = params[0]
        elif "DELETE FROM shipments WHERE id" in query:
            st.session_state["mock_db"]["shipments"] = [s for s in st.session_state["mock_db"]["shipments"] if s["id"] != params[0]]
        elif "DELETE FROM receipts WHERE id" in query:
            st.session_state["mock_db"]["receipts"] = [r for r in st.session_state["mock_db"]["receipts"] if r["id"] != params[0]]
        elif "DELETE FROM customers" in query:
            st.session_state["mock_db"]["customers"] = [c for c in st.session_state["mock_db"]["customers"] if c["name"] != params[0]]
            st.session_state["mock_db"]["shipments"] = [s for s in st.session_state["mock_db"]["shipments"] if s["customer_name"] != params[0]]
            st.session_state["mock_db"]["receipts"] = [r for r in st.session_state["mock_db"]["receipts"] if r["customer_name"] != params[0]]
        elif "TRUNCATE" in query:
            st.session_state["mock_db"]["shipments"] = []
            if len(params) > 0 and params[0] is True:
                st.session_state["mock_db"]["receipts"] = []
                st.session_state["mock_db"]["customers"] = []
        return True

    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            return True
    except Exception as e:
        st.error(f"❌ خطأ في تنفيذ الإجراء السحابي: {e}")
        return False
    finally:
        conn.close()

# ==============================================================================
# 6. بناء وتصميم واجهة شبكة العرض الفاخرة للبيانات (Data Grid Layout)
# ==============================================================================
def render_premium_html_grid(df, show_internal_profit=False):
    headers = [
        "اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", 
        "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)", "مؤشر الربحية"
    ]
    if show_internal_profit: 
        headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
        
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    tr_html = ""
    
    for _, row in df.iterrows():
        final_fr = safe_float(row.get('final_freight_usd', 0))
        agency_fr = safe_float(row.get('agency_freight_usd', 0))
        
        if final_fr > agency_fr:
            profit_indicator = "<span class='status-badge status-green'>مربح</span>"
        elif final_fr < agency_fr:
            profit_indicator = "<span class='status-badge status-red'>🚨 خسارة</span>"
        else:
            profit_indicator = "<span class='status-badge status-orange'>غير مسعر</span>"
            
        tr_html += (
            f"<tr>"
            f"<td>{row['customer_name']}</td>"
            f"<td>{row['bl_number']}</td>"
            f"<td>{row['container_number']}</td>"
            f"<td>{row['shipment_date']}</td>"
            f"<td>{row['do_number']}</td>"
            f"<td>{safe_float(row['do_value_lyd']):,.2f} د.ل</td>"
            f"<td>${final_fr:,.2f}</td>"
            f"<td>{profit_indicator}</td>"
        )
        if show_internal_profit:
            profit = final_fr - agency_fr
            tr_html += (
                f"<td>${agency_fr:,.2f}</td>"
                f"<td>${profit:,.2f}</td>"
            )
        tr_html += "</tr>"
        
    st.markdown(
        f'<div class="enterprise-table-container">'
        f'<table class="corporate-data-table">'
        f'<thead><tr>{th_html}</tr></thead>'
        f'<tbody>{tr_html}</tbody>'
        f'</table></div>', 
        unsafe_allow_html=True
    )

# ==============================================================================
# 7. شريط التنقل الجانبي المطور والمنظم (Sleek Apple-style Department Selector)
# ==============================================================================
st.sidebar.markdown(
    """
    <div style='text-align: center; padding: 15px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 25px;'>
        <span style='font-size: 38px;'>🚢</span>
        <h2 style='color: #ffffff; font-weight: 900; margin: 10px 0 2px 0; font-size: 21px; letter-spacing: 0.5px;'>إستبرق الدولية</h2>
        <p style='color: #c5a880; font-size: 11.5px; font-weight: 700; margin: 0; letter-spacing: 1px; text-transform: uppercase;'>منظومة الرقابة المالية وإدارة الشحنات</p>
    </div>
    """, 
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "🎯 حدد القطاع التشغيلي المطلوب للعمل:",
    [
        "📊 الإدارة والتقرير المالي العام",
        "🚢 حركة الحاويات والشحنات",
        "💵 الخزينة والتحصيلات المالية",
        "⚙️ شؤون الزبائن وصيانة النظام"
    ]
)

st.sidebar.markdown(
    """
    <div style='position: fixed; bottom: 15px; text-align: center; width: 220px; font-size: 11px; color: #64748b; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 10px;'>
        النسخة الاحترافية العالمية للشركة © 2026
    </div>
    """, 
    unsafe_allow_html=True
)

# ==============================================================================
# البوابة الأولى: الإدارة والتقرير المالي العام + محرك فحص النواقص
# ==============================================================================
if menu == "📊 الإدارة والتقرير المالي العام":
    tab_reports, tab_audit = st.tabs(["📊 الميزان المالي العام وكشوف الحساب", "🔍 محرك فحص وتدقيق البيانات الناقصة"])
    
    customers_list = db_query("SELECT * FROM customers ORDER BY name ASC")
    shipments_list = db_query("SELECT * FROM shipments ORDER BY id DESC")
    receipts_list = db_query("SELECT * FROM receipts ORDER BY id DESC")
    
    customers_df = pd.DataFrame(customers_list) if customers_list else pd.DataFrame(columns=['id', 'name'])
    shipments_all = pd.DataFrame(shipments_list) if shipments_list else pd.DataFrame(columns=['id', 'customer_name', 'container_number', 'bl_number', 'shipment_date', 'do_number', 'do_value_lyd', 'agency_freight_usd', 'final_freight_usd'])
    receipts_all = pd.DataFrame(receipts_list) if receipts_list else pd.DataFrame(columns=['id', 'customer_name', 'amount', 'currency', 'receipt_date', 'notes'])

    # التهيئة المسبقة والآمنة لمتغير التصدير تلافياً لأخطاء المحاذاة البرمجية
    df_export_target = pd.DataFrame()
    target_customer = "الكل"

    # --- علامة التبويب الأولى: التقارير وكشوف الحساب ---
    with tab_reports:
        st.subheader("📊 لوحة التقارير والموازنات الجارية والذمم المجمعة")
        
        if customers_df.empty:
            st.warning("⚠️ لا توجد حسابات زبائن مسجلة حالياً بالمنظومة.")
        else:
            t_cont = len(shipments_all)
            t_lyd = shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0
            t_usd = shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
            
            st.markdown(
                f'<div class="kpi-container">'
                f'<div class="kpi-card"><h5>📦 حجم الحاويات المعالجة</h5><h2>{t_cont} شحنة جارية</h2><p>إجمالي القيود الجمركية المدرجة بالمنظومة</p></div>'
                f'<div class="kpi-card"><h5>💵 ذمم أوامر التسليم الكلية</h5><h2>{t_lyd:,.2f} د.ل</h2><p>قيمة الدفعات المحلية وتخليص الأوراق جمركياً</p></div>'
                f'<div class="kpi-card"><h5>💵 نولون الشحن الدولي المعتمد</h5><h2>${t_usd:,.2f}</h2><p>ذمم نولون الشحن الخارجي بالدولار للعملاء</p></div>'
                f'</div>', 
                unsafe_allow_html=True
            )
            
            with st.expander("⚙️ محرك تحديد هيكلية التقارير وعمليات الفرز الذكي والتعديل", expanded=True):
                c_filter1, c_filter2, c_filter3 = st.columns(3)
                with c_filter1: 
                    report_scope = st.radio("1. نطاق كشف الحساب الحالي:", ["كل زبائن المنظومة", "زبون محدد فردي"])
                with c_filter2: 
                    report_structure = st.radio("2. نوع وثيقة الكشف المالية المعروضة:", ["كشف مالي إجمالي عام", "كشف حساب تفصيلي"])
                with c_filter3: 
                    display_profit = st.checkbox("إظهار قيم شحن الوكالة وصافي الأرباح للشركة")
                    
                if report_scope == "زبون محدد فردي":
                    target_customer = st.selectbox("🎯 اختر اسم حساب الزبون المستهدف بالفرز المالي الموحد:", customers_df['name'].tolist())
                else:
                    target_customer = "الكل"

            req_l, paid_l, req_u, paid_u = 0.0, 0.0, 0.0, 0.0
            
            if report_scope == "كل زبائن المنظومة" and not customers_df.empty:
                if report_structure == "كشف مالي إجمالي عام":
                    st.subheader("📋 كشف ملخص أرصاد الحسابات لكافة الزبائن")
                    
                    if not shipments_all.empty:
                        ship_grp = shipments_all.groupby('customer_name').agg(
                            total_containers=('id', 'count'),
                            required_lyd=('do_value_lyd', 'sum'),
                            required_usd=('final_freight_usd', 'sum')
                        ).reset_index()
                    else:
                        ship_grp = pd.DataFrame(columns=['customer_name', 'total_containers', 'required_lyd', 'required_usd'])
                    
                    if not receipts_all.empty:
                        rec_lyd = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD'].groupby('customer_name')['amount'].sum().reset_index(name='paid_lyd')
                        rec_usd = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD'].groupby('customer_name')['amount'].sum().reset_index(name='paid_usd')
                        rec_grp = pd.merge(rec_lyd, rec_usd, on='customer_name', how='outer').fillna(0.0)
                    else:
                        rec_grp = pd.DataFrame(columns=['customer_name', 'paid_lyd', 'paid_usd'])
                        
                    df_export_target = pd.merge(customers_df, ship_grp, left_on='name', right_on='customer_name', how='left')
                    df_export_target = pd.merge(df_export_target, rec_grp, left_on='name', right_on='customer_name', how='left')
                    df_export_target.drop(columns=['customer_name_x', 'customer_name_y', 'name'], errors='ignore', inplace=True)
                    df_export_target.rename(columns={'name': 'customer_name'}, errors='ignore', inplace=True)
                    if 'customer_name' not in df_export_target.columns:
                        df_export_target.insert(0, 'customer_name', customers_df['name'])
                        
                    df_export_target.fillna(0.0, inplace=True)
                    df_export_target['remaining_lyd'] = df_export_target['required_lyd'] - df_export_target['paid_lyd']
                    df_export_target['remaining_usd'] = df_export_target['required_usd'] - df_export_target['paid_usd']
                    
                    th_html = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي الجاري (د.ل)", "نولون الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                    tr_html = ""
                    for _, r in df_export_target.iterrows():
                        tr_html += (
                            f"<tr>"
                            f"<td><b>{r['customer_name']}</b></td>"
                            f"<td>{int(r['total_containers'])}</td>"
                            f"<td>{r['required_lyd']:,.2f} د.ل</td>"
                            f"<td>{r['paid_lyd']:,.2f} د.ل</td>"
                            f"<td style='color:#991b1b; font-weight:bold;'>{r['remaining_lyd']:,.2f} د.ل</td>"
                            f"<td>${r['required_usd']:,.2f}</td>"
                            f"<td>${r['paid_usd']:,.2f}</td>"
                            f"<td style='color:#991b1b; font-weight:bold;'>${r['remaining_usd']:,.2f}</td>"
                            f"</tr>"
                        )
                    st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)
                    
                    req_l = shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0
                    req_u = shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
                    paid_l = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD']['amount'].sum() if not receipts_all.empty else 0.0
                    paid_u = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD']['amount'].sum() if not receipts_all.empty else 0.0
                else:
                    st.subheader("📋 كشف السجل التفصيلي الموحد لجميع الزبائن")
                    df_export_target = shipments_all.copy()
                    df_export_target['profit_usd'] = df_export_target['final_freight_usd'] - df_export_target['agency_freight_usd']
                    render_premium_html_grid(df_export_target, show_internal_profit=display_profit)
                    
                    req_l = df_export_target['do_value_lyd'].sum()
                    req_u = df_export_target['final_freight_usd'].sum()
                    paid_l = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD']['amount'].sum() if not receipts_all.empty else 0.0
                    paid_u = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD']['amount'].sum() if not receipts_all.empty else 0.0
            elif not customers_df.empty:
                df_cust_s = shipments_all[shipments_all['customer_name'] == target_customer].copy() if not shipments_all.empty else pd.DataFrame()
                df_cust_r = receipts_all[receipts_all['customer_name'] == target_customer].copy() if not receipts_all.empty else pd.DataFrame()
                
                req_l = df_cust_s['do_value_lyd'].sum() if not df_cust_s.empty else 0.0
                req_u = df_cust_s['final_freight_usd'].sum() if not df_cust_s.empty else 0.0
                paid_l = df_cust_r[df_cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not df_cust_r.empty else 0.0
                paid_u = df_cust_r[df_cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not df_cust_r.empty else 0.0
                
                if report_structure == "كشف مالي إجمالي عام":
                    st.subheader(f"📋 ملخص الموقف الحسابي العام لحساب: {target_customer}")
                    df_export_target = df_cust_s.copy()
                    render_premium_html_grid(df_export_target, show_internal_profit=display_profit)
                else:
                    st.subheader(f"📋 كشف الحاويات والقيود التفصيلي المعتمد لحساب: {target_customer}")
                    if not df_cust_s.empty:
                        df_cust_s['profit_usd'] = df_cust_s['final_freight_usd'] - df_cust_s['agency_freight_usd']
                    df_export_target = df_cust_s.copy()
                    render_premium_html_grid(df_export_target, show_internal_profit=display_profit)

            # تفعيل وتصحيح معالجة التصدير التلقائية
            if not df_export_target.empty:
                st.write("")
                st.download_button(
                    label="📥 تحميل كشف الحساب النشط حالياً بصيغة Excel معتمد للشركة", 
                    data=to_excel(df_export_target), 
                    file_name=f"istabraq_statement_{target_customer.replace(' ', '_')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

                # --- وثيقة تصديق الطباعة المعزولة تماماً والخالية من الفراغات لورق A4 ---
                st.write("---")
                st.markdown("### 🖨️ وثيقة تصديق ومطابقة كشوفات الحساب الرسمية للطباعة:")
                
                rows_html_p = ""
                if report_structure == "كشف مالي إجمالي عام" and report_scope == "كل زبائن المنظومة":
                    table_headers = "<th>اسم الزبون</th><th>عدد الحاويات</th><th>المطلوب (د.ل)</th><th>المدفوع (د.ل)</th><th>المتبقي الجاري (د.ل)</th><th>الشحن ($)</th><th>المدفوع ($)</th><th>المتبقي الجاري ($)</th>"
                    doc_type_text = "كشف الميزان والأرصاد المالي الإجمالي المجمع لكافة حسابات العملاء"
                    for _, r in df_export_target.iterrows():
                        rows_html_p += (
                            f"<tr><td>{r['customer_name']}</td><td>{int(r['total_containers'])}</td>"
                            f"<td>{r['required_lyd']:,.2f} د.ل</td><td>{r['paid_lyd']:,.2f} د.ل</td><td><b>{r['remaining_lyd']:,.2f} د.ل</b></td>"
                            f"<td>${r['required_usd']:,.2f}</td><td>${r['paid_usd']:,.2f}</td><td><b>${r['remaining_usd']:,.2f}</b></td></tr>"
                        )
                else:
                    th_agency_print = "<th>شحن الوكالة</th>" if display_profit else ""
                    th_profit_print = "<th>صافي الربح</th>" if display_profit else ""
                    table_headers = f"<th>اسم الزبون</th><th>رقم البوليصة</th><th>رقم الحاوية</th><th>تاريخ الاستلام</th><th>رقم D.O</th><th>قيمة أمر التسليم</th><th>الشحن النهائي</th>{th_agency_print}{th_profit_print}"
                    doc_type_text = f"كشف الحاويات التفصيلي المعتمد والمصفى جمركياً"
                    for _, r in df_export_target.iterrows():
                        agency_td_p = f"<td>${r['agency_freight_usd']:,.2f}</td>" if display_profit else ""
                        profit_val = r['final_freight_usd'] - r['agency_freight_usd']
                        profit_td_p = f"<td>${profit_val:,.2f}</td>" if display_profit else ""
                        rows_html_p += (
                            f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td>"
                            f"<td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{safe_float(r['do_value_lyd']):,.2f} د.ل</td>"
                            f"<td>${r['final_freight_usd']:,.2f}</td>{agency_td_p}{profit_td_p}</tr>"
                        )

                summary_table_html = f"""
                <table class="print-totals-table">
                    <thead>
                        <tr>
                            <th>العملة والبيان الحسابي للتحصيل الرسمي والذمة الجارية</th>
                            <th>إجمالي القيمة المطلوبة بذمته</th>
                            <th>إجمالي القيمة المدفوعة والمستلمة بالخزينة</th>
                            <th>صافي الرصيد المتبقي (الجاري معلق)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>حساب أوامر التسليم والتخليص الجمركي (LYD)</b></td>
                            <td>{req_l:,.2f} د.ل</td>
                            <td style="color:#112a1f;">{paid_l:,.2f} د.ل</td>
                            <td style="color:#991b1b; font-weight:bold;">{req_l - paid_l:,.2f} د.ل</td>
                        </tr>
                        <tr>
                            <td><b>حساب نولون وأرصاد الشحن الدولي (USD)</b></td>
                            <td>${req_u:,.2f}</td>
                            <td style="color:#112a1f;">${paid_u:,.2f}</td>
                            <td style="color:#991b1b; font-weight:bold;">${req_u - paid_u:,.2f}</td>
                        </tr>
                    </tbody>
                </table>"""

                # بناء نسخة طباعة معزولة تتجاوز عقبات Popups بالمتصفحات
                st.write("")
                st.info("ℹ️ اضغط على الزر أدناه لفتح واجهة الطباعة المتوافقة مع طابعات A4.")
                st.download_button(
                    label="🖨️ تحميل نسخة ملف الطباعة المباشرة بصيغة HTML المستقلة",
                    data=f"""
                    <!DOCTYPE html>
                    <html dir="rtl" lang="ar">
                    <head>
                        <meta charset="UTF-8">
                        <title>طباعة كشف الحساب الرسمي - إستبرق الدولية</title>
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;800&display=swap');
                            body {{ font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; padding: 40px; color: #000; }}
                            .header {{ text-align: center; border-bottom: 3px double #000; padding-bottom: 12px; margin-bottom: 25px; }}
                            .header h1 {{ font-size: 24px; margin: 0; font-weight: 800; }}
                            .header p {{ font-size: 14px; margin: 6px 0 0 0; font-weight: 700; color: #334155; }}
                            .meta-table {{ width: 100%; margin-bottom: 25px; font-size: 14px; font-weight: 700; border-collapse: collapse; }}
                            .meta-table td {{ padding: 8px; }}
                            .data-table {{ width: 100%; border-collapse: collapse; font-size: 13px; margin-top: 15px; }}
                            .data-table th {{ background-color: #f1f5f9; border: 1px solid #000; padding: 12px; text-align: right; font-weight: 800; }}
                            .data-table td {{ border: 1px solid #000; padding: 12px; font-weight: 700; }}
                            .print-totals-table {{ width: 100%; border-collapse: collapse; margin-top: 30px; }}
                            .print-totals-table th {{ background-color: #f1f5f9; border: 1px solid #000; padding: 12px; text-align: center; font-weight: 800; }}
                            .print-totals-table td {{ border: 1px solid #000; padding: 12px; text-align: center; font-weight: bold; }}
                            .signatures {{ margin-top: 80px; display: flex; justify-content: space-between; font-size: 14px; font-weight: 800; }}
                            @media print {{
                                body {{ padding: 20px; }}
                                .no-print {{ display: none; }}
                            }}
                        </style>
                    </head>
                    <body onload="window.print()">
                        <div class="header">
                            <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1>
                            <p>مصراتة - ليبيا | الهاتف: 0912185571 - 0912185569 | الحسابات المركزية المعتمدة</p>
                        </div>
                        <table class="meta-table">
                            <tr>
                                <td><b>مسمى كشف الحساب:</b> {target_customer if report_scope == 'زبون محدد فردي' else 'كافة عملاء المنظومة'}</td>
                                <td style="text-align: left;"><b>تاريخ وتوقيت الطباعة:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                            <tr>
                                <td><b>نوع وثيقة كشف الموقف المالي:</b> {doc_type_text}</td>
                                <td style="text-align: left;"><b>حصر القيود المدرجة:</b> {len(df_export_target)} سجل فعال جاري</td>
                            </tr>
                        </table>
                        <table class="data-table">
                            <thead><tr>{table_headers}</tr></thead>
                            <tbody>{rows_html_p}</tbody>
                        </table>
                        {summary_table_html}
                        <div class="signatures">
                            <div>توقيع واعتماد الحسابات المركزية: .........................</div>
                            <div>خِتم وتصديق إدارة الشركة رسميًا: .........................</div>
                        </div>
                    </body>
                    </html>
                    """,
                    file_name=f"print_statement_{datetime.now().strftime('%Y%m%d%H%M')}.html",
                    mime="text/html"
                )

    # --- علامة التبويب الثانية: محرك فحص وتدقيق البيانات الناقصة ---
    with tab_audit:
        st.subheader("🔍 محرك حصر ومتابعة الشحنات ناقصة البيانات المفقودة")
        st.markdown("يساعدك هذا المحرك التفاعلي الذكي في رصد الحاويات التي ينقصها أي جزء من البيانات الهامة كالأسعار أو البوالص وتعديلها فوراً.")
        
        if shipments_all.empty:
            st.success("🎉 قاعدة البيانات خالية تماماً من الشحنات حالياً.")
        else:
            with st.expander("⚙️ محدد شروط وفلاتر تدقيق البيانات الناقصة", expanded=True):
                fc1, fc2 = st.columns([1, 2])
                with fc1:
                    selected_cust_filter = st.selectbox("تصفية لزبون محدد:", ["كل زبائن المنظومة"] + customers_df['name'].tolist())
                with fc2:
                    incomplete_criteria = st.multiselect(
                        "اختر النواقص التي ترغب في تصفيتها ورصدها بالحاويات المفتوحة:",
                        [
                            "رقم الحاوية مفقود / فارغ",
                            "رقم البوليصة مفقود / فارغ",
                            "تاريخ الاستلام غير محدد",
                            "رقم إذن التسليم (D.O) مفقود / فارغ",
                            "قيمة أمر التسليم غير مدخلة (صفر)",
                            "شحن الوكالة غير مسعر ($0)",
                            "الشحن النهائي للزبون غير مسعر ($0)"
                        ],
                        default=[
                            "رقم الحاوية مفقود / فارغ",
                            "رقم البوليصة مفقود / فارغ",
                            "قيمة أمر التسليم غير مدخلة (صفر)",
                            "الشحن النهائي للزبون غير مسعر ($0)"
                        ]
                    )
            
            df_audit = shipments_all.copy()
            if selected_cust_filter != "كل زبائن المنظومة":
                df_audit = df_audit[df_audit['customer_name'] == selected_cust_filter]
                
            masks = []
            if incomplete_criteria:
                if "رقم الحاوية مفقود / فارغ" in incomplete_criteria:
                    masks.append(df_audit['container_number'].isna() | (df_audit['container_number'].astype(str).str.strip() == ""))
                if "رقم البوليصة مفقود / فارغ" in incomplete_criteria:
                    masks.append(df_audit['bl_number'].isna() | (df_audit['bl_number'].astype(str).str.strip() == ""))
                if "تاريخ الاستلام غير محدد" in incomplete_criteria:
                    masks.append(df_audit['shipment_date'].isna() | (df_audit['shipment_date'].astype(str).str.strip() == ""))
                if "رقم إذن التسليم (D.O) مفقود / فارغ" in incomplete_criteria:
                    masks.append(df_audit['do_number'].isna() | (df_audit['do_number'].astype(str).str.strip() == ""))
                if "قيمة أمر التسليم غير مدخلة (صفر)" in incomplete_criteria:
                    masks.append(df_audit['do_value_lyd'].isna() | (df_audit['do_value_lyd'] <= 0.0))
                if "شحن الوكالة غير مسعر ($0)" in incomplete_criteria:
                    masks.append(df_audit['agency_freight_usd'].isna() | (df_audit['agency_freight_usd'] <= 0.0))
                if "الشحن النهائي للزبون غير مسعر ($0)" in incomplete_criteria:
                    masks.append(df_audit['final_freight_usd'].isna() | (df_audit['final_freight_usd'] <= 0.0))
                    
                if masks:
                    combined_mask = masks[0]
                    for m in masks[1:]:
                        combined_mask = combined_mask | m
                    df_audit = df_audit[combined_mask]
            
            if df_audit.empty:
                st.success("🎉 رائع! جميع الشحنات مطابقة وكاملة البيانات حالياً.")
            else:
                st.warning(f"⚠️ تم رصد {len(df_audit)} حاويات / شحنات بها نواقص معلقة:")
                
                th_html = "".join(f"<th>{h}</th>" for h in ["الزبون", "البوليصة", "رقم الحاوية", "تاريخ الاستلام", "رقم D.O", "أمر التسليم", "شحن الوكالة", "الشحن للزبون"])
                tr_html = ""
                for _, row in df_audit.iterrows():
                    cust = row['customer_name']
                    bl = row['bl_number'] if (row['bl_number'] and str(row['bl_number']).strip()) else "<span style='color:#991b1b; font-weight:bold;'>⚠️ ناقص</span>"
                    cont = row['container_number'] if (row['container_number'] and str(row['container_number']).strip()) else "<span style='color:#991b1b; font-weight:bold;'>⚠️ ناقص</span>"
                    sdate = row['shipment_date'] if (row['shipment_date'] and str(row['shipment_date']).strip()) else "<span style='color:#991b1b; font-weight:bold;'>⚠️ ناقص</span>"
                    donum = row['do_number'] if (row['do_number'] and str(row['do_number']).strip()) else "<span style='color:#991b1b; font-weight:bold;'>⚠️ ناقص</span>"
                    
                    doval = f"{row['do_value_lyd']:,.2f} د.ل" if row['do_value_lyd'] > 0 else "<span style='color:#991b1b; font-weight:bold;'>⚠️ 0.00 د.ل</span>"
                    agency = f"${row['agency_freight_usd']:,.2f}" if row['agency_freight_usd'] > 0 else "<span style='color:#991b1b; font-weight:bold;'>⚠️ $0.00</span>"
                    final = f"${row['final_freight_usd']:,.2f}" if row['final_freight_usd'] > 0 else "<span style='color:#991b1b; font-weight:bold;'>⚠️ $0.00</span>"
                    
                    tr_html += f"<tr><td><b>{cust}</b></td><td>{bl}</td><td>{cont}</td><td>{sdate}</td><td>{donum}</td><td>{doval}</td><td>{agency}</td><td>{final}</td></tr>"
                
                st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)
                
                # الاستكمال السريع للحاويات مباشرة من نفس الصفحة
                st.write("---")
                st.subheader("📝 التحديث المباشر والاستكمال السريع للشحنة المحددة:")
                df_audit['selector_label'] = df_audit['customer_name'] + " | بوليصة: " + df_audit['bl_number'].astype(str) + " | حاوية: " + df_audit['container_number'].astype(str)
                selected_audit_opt = st.selectbox("اختر الشحنة المستهدفة بالاستكمال والترقيد المالي السريع:", df_audit['selector_label'].tolist())
                selected_audit_row = df_audit[df_audit['selector_label'] == selected_audit_opt].iloc[0]
                audit_id = int(selected_audit_row['id'])
                
                with st.form("quick_audit_update_form"):
                    ac1, ac2, ac3 = st.columns(3)
                    with ac1:
                        st.text_input("اسم حساب العميل (مغلق ومحمي جمركياً):", value=selected_audit_row['customer_name'], disabled=True)
                    with ac2:
                        audit_container_num = st.text_input("رقم الحاوية / الحاويات المفتوحة:", value=selected_audit_row['container_number'])
                    with ac3:
                        audit_bl_num = st.text_input("رقم البوليصة الرئيسي:", value=selected_audit_row['bl_number'])
                        
                    ac4, ac5, ac6 = st.columns(3)
                    with ac4:
                        audit_date_val = st.text_input("تاريخ الاستلام والتقييد (YYYY-MM-DD):", value=selected_audit_row['shipment_date'])
                    with ac5:
                        audit_do_num_val = st.text_input("رقم إذن / أمر التسليم (D.O):", value=selected_audit_row['do_number'])
                    with ac6:
                        audit_do_value_val = st.number_input("قيمة أمر التسليم الفعالة (بالدينار LYD):", value=float(selected_audit_row['do_value_lyd']))
                        
                    ac7, ac8 = st.columns(2)
                    with ac7:
                        audit_agency_val = st.number_input("تكلفة شحن ونولون الوكالة الكلية (بالدولار USD):", value=float(selected_audit_row['agency_freight_usd']))
                    with ac8:
                        audit_final_val = st.number_input("سعر الشحن النهائي المقيد على العميل (بالدولار USD):", value=float(selected_audit_row['final_freight_usd']))
                        
                    if st.form_submit_button("🚀 حفظ وتأكيد استكمال البيانات ومزامنتها بالخادم"):
                        db_execute(
                            'UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s',
                            (
                                audit_container_num.strip().upper(),
                                audit_bl_num.strip().upper(),
                                parse_any_date(audit_date_val),
                                audit_do_num_val.strip(),
                                audit_do_value_val,
                                audit_agency_val,
                                audit_final_val,
                                audit_id
                            )
                        )
                        st.success("🎉 تم استكمال وتحديث بيانات الشحنة بنجاح في قاعدة البيانات!")
                        st.rerun()

# ==============================================================================
# البوابة الثانية: حركة الحاويات والشحنات ومستورد الإكسل والتعديل السريع
# ==============================================================================
elif menu == "🚢 حركة الحاويات والشحنات":
    tab_manual, tab_excel_u, tab_modify = st.tabs(["➕ إضافة بوليصة جديدة يدوياً", "📥 رفع وتحميل ملف إكسل", "📝 مراجعة وتعديل وحذف الشحنات"])
    
    customers_list = db_query("SELECT * FROM customers ORDER BY name ASC")
    shipments_list = db_query("SELECT * FROM shipments ORDER BY id DESC")
    
    customers_df = pd.DataFrame(customers_list) if customers_list else pd.DataFrame(columns=['id', 'name'])
    shipments = pd.DataFrame(shipments_list) if shipments_list else pd.DataFrame(columns=['id', 'customer_name', 'container_number', 'bl_number', 'shipment_date', 'do_number', 'do_value_lyd', 'agency_freight_usd', 'final_freight_usd'])

    # --- إضافة بوليصة يدوياً ---
    with tab_manual:
        st.subheader("➕ إضافة بوليصة / شحنة جمركية يدوية تابعة لزبون")
        if customers_df.empty:
            st.warning("⚠️ يرجى تسجيل وإضافة زبون واحد على الأقل أولاً لتتمكن من ربط الشحنات الجمركية بحسابه المالي.")
        else:
            num_containers = st.number_input("حدد كم حاوية تابعة لهذه البوليصة المستهدفة بالتقييد:", min_value=1, max_value=50, value=1, step=1)
            with st.form("manual_shipment_form_v2", clear_on_submit=True):
                sc1, sc2 = st.columns(2)
                with sc1: 
                    s_cust = st.selectbox("ارتباط باسم الزبون المسجل بالمنظومة:", customers_df['name'])
                with sc2: 
                    s_bl = st.text_input("رقم البوليصة الرئيسي (MBL / HBL):")
                    
                container_inputs = []
                st.write("📝 أدخل أرقام الحاويات الخاصة بهذه البوليصة في الحقول أدناه:")
                grid_cols_num = min(num_containers, 4)
                c_cols = st.columns(grid_cols_num)
                for i in range(num_containers):
                    col_idx = i % grid_cols_num
                    with c_cols[col_idx]:
                        container_inputs.append(st.text_input(f"رقم الحاوية {i+1}:", key=f"manual_container_input_{i}"))
                        
                sc4, sc5, sc6 = st.columns(3)
                with sc4: 
                    s_date = st.date_input("تاريخ الاستلام الفعلي بالميناء:", datetime.now())
                with sc5: 
                    s_do_num = st.text_input("رقم إذن / أمر التسليم (D.O):")
                with sc6: 
                    s_do_val = st.number_input("قيمة أمر التسليم الإجمالية المحسوبة (بالدينار LYD):", min_value=0.0, step=100.0)
                    
                sc7, sc8 = st.columns(2)
                with sc7: 
                    s_agency = st.number_input("قيمة شحن الوكالة الكلية للشحنة (بالدولار USD):", min_value=0.0, step=50.0)
                with sc8: 
                    s_final = st.number_input("سعر نولون الشحن النهائي المقيد على الزبون (بالدولار USD):", min_value=0.0, step=50.0)
                    
                if st.form_submit_button("🚀 حفظ وإضافة الشحنة والبوليصة الجمركية"):
                    valid_containers = [c.strip().upper() for c in container_inputs if c.strip()]
                    if not valid_containers:
                        st.error("❌ خطأ: يرجى كتابة رقم حاوية واحد على الأقل لإدراج الشحنة بنجاح.")
                    elif s_bl.strip() == "":
                        st.error("❌ خطأ: يجب إدخال رقم البوليصة الرئيسي لربط الحاويات.")
                    else:
                        combined_containers_string = " , ".join(valid_containers)
                        db_execute(
                            'INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                            (s_cust, combined_containers_string, s_bl.strip().upper(), s_date.strftime('%Y-%m-%d'), s_do_num.strip(), s_do_val, s_agency, s_final)
                        )
                        st.success("🎉 تم حفظ البوليصة الجمركية الجديدة بنجاح وتم مزامنتها مع الموقف المالي للعميل!")
                        st.rerun()

    # --- استيراد الإكسل ---
    with tab_excel_u:
        st.subheader("📥 معالج رفع البيانات تلقائياً وتوطينها من ملف Excel")
        st.info("ℹ️ تأكد من تطابق ترويسة الحقول أو قم بمطابقتها يدوياً عبر محرك الربط الذكي بالأسفل.")
        uploaded_file = st.file_uploader("يرجى اختيار ملف الإكسل المستهدف للرفع والدمج السحابي:", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success("🎉 تم تحميل وقراءة ملف الإكسل بنجاح! يرجى مطابقة أعمدة الملف بأعمدة المنظومة:")
                
                all_cols = list(df.columns)
                c1, c2, c3, c4 = st.columns(4)
                with c1: 
                    col_cust = st.selectbox("عمود اسم الزبون الفعلي", all_cols, index=0)
                with c2: 
                    col_cont = st.selectbox("عمود رقم الحاوية", all_cols, index=min(1, len(all_cols)-1))
                with c3: 
                    col_bl = st.selectbox("عمود رقم البوليصة الجمركي", all_cols, index=min(2, len(all_cols)-1))
                with c4: 
                    col_date = st.selectbox("عمود تاريخ الاستلام والتقييد", all_cols, index=min(3, len(all_cols)-1))
                    
                c5, c6, c7, c8 = st.columns(4)
                with c5: 
                    col_donum = st.selectbox("عمود رقم إذن / أمر التسليم D.O", all_cols, index=min(4, len(all_cols)-1))
                with c6: 
                    col_dovald = st.selectbox("عمود قيمة أمر التسليم (بالدينار LYD)", all_cols, index=min(5, len(all_cols)-1))
                with c7: 
                    col_agency = st.selectbox("عمود نولون شحن الوكالة (بالدولار USD)", all_cols, index=min(6, len(all_cols)-1))
                with c8: 
                    col_final = st.selectbox("عمود الشحن النهائي للزبون (بالدولار USD)", all_cols, index=min(7, len(all_cols)-1))
                    
                st.write("🔍 **معاينة سريعة لأول 3 صفوف من الملف المرفوع:**")
                st.dataframe(df.head(3), use_container_width=True)
                
                if st.button("🚀 بدء دمج البيانات والمطابقة الذكية بقاعدة البيانات أونلاين"):
                    insert_count, update_count = 0, 0
                    for index, row in df.iterrows():
                        cust_name = str(row[col_cust]).strip() if not pd.isnull(row[col_cust]) else ""
                        if cust_name == "": 
                            continue
                        db_execute("INSERT INTO customers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (cust_name,))
                        
                        bl = str(row[col_bl]).strip().upper() if not pd.isnull(row[col_bl]) else ""
                        raw_date = row[col_date]
                        date_str = parse_any_date(raw_date)
                        
                        new_do_num = str(row[col_donum]).strip() if not pd.isnull(row[col_donum]) else ""
                        new_do_val = safe_float(row[col_dovald])
                        new_agency = safe_float(row[col_agency])
                        new_final = safe_float(row[col_final])
                        
                        raw_containers = str(row[col_cont]).strip() if not pd.isnull(row[col_cont]) else ""
                        container_list = re.split(r'[,/؛;\s\n]+', raw_containers)
                        container_list = [c.strip().upper() for c in container_list if c.strip()]
                        if not container_list: 
                            container_list = [""]
                            
                        for container in container_list:
                            existing = db_query("SELECT id FROM shipments WHERE container_number = %s AND bl_number = %s", (container, bl))
                            if existing:
                                db_execute(
                                    'UPDATE shipments SET customer_name=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                    (cust_name, date_str, new_do_num, new_do_val, new_agency, new_final, existing[0]['id'])
                                )
                                update_count += 1
                            else:
                                db_execute(
                                    'INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                                    (cust_name, container, bl, date_str, new_do_num, new_do_val, new_agency, new_final)
                                )
                                insert_count += 1
                    st.success(f"🎉 تكللت عملية التوطين السحابي بالنجاح! تم إدراج {insert_count} بوليصة جديدة وتحديث {update_count} بوليصة جارية.")
                    st.rerun()
            except Exception as e:
                st.error(f"❌ حدث خطأ فني أثناء قراءة ومعالجة الملف: {e}")

    # --- مراجعة وتعديل وحذف الشحنات الفردية ---
    with tab_modify:
        st.subheader("📝 مراجعة وتحديث القيود والشحنات الفردية المفتوحة")
        if shipments.empty:
            st.info("ℹ️ لا توجد شحنات مسجلة بالدفاتر حالياً.")
        else:
            search_query = st.text_input("🔍 صندوق البحث الذكي (ابحث برقم الحاوية، رقم البوليصة، أو اسم الزبون):")
            filtered_df = shipments.copy()
            if search_query.strip():
                q = search_query.strip().lower()
                filtered_df = shipments[
                    shipments['container_number'].astype(str).str.lower().str.contains(q, na=False) | 
                    shipments['bl_number'].astype(str).str.lower().str.contains(q, na=False) | 
                    shipments['customer_name'].astype(str).str.lower().str.contains(q, na=False)
                ]
                
            if filtered_df.empty:
                st.warning("⚠️ لم يسفر البحث عن أي نتائج مطابقة.")
            else:
                filtered_df['selector_text'] = (
                    "بوليصة جمركية: " + filtered_df['bl_number'].astype(str) + 
                    " | حاوية رقم: " + filtered_df['container_number'].astype(str) + 
                    " (" + filtered_df['customer_name'] + ")"
                )
                selected_option = st.selectbox("اختر الشحنة الدقيقة المستهدفة بالتعديل أو الإلغاء الكامل:", filtered_df['selector_text'].tolist())
                selected_row = filtered_df[filtered_df['selector_text'] == selected_option].iloc[0]
                shipment_id = int(selected_row['id'])
                
                with st.form("edit_ship_form_v2"):
                    ec1, ec2, ec3 = st.columns(3)
                    with ec1: 
                        edit_cust = st.text_input("اسم حساب العميل المرتبط (مغلق ومحمي جمركياً)", value=selected_row['customer_name'], disabled=True)
                    with ec2: 
                        edit_cont = st.text_input("أرقام الحاوية / الحاويات التابعة:", value=selected_row['container_number'])
                    with ec3: 
                        edit_bl = st.text_input("رقم البوليصة الرئيسي:", value=selected_row['bl_number'])
                        
                    ec4, ec5, ec6 = st.columns(3)
                    with ec4: 
                        edit_date = st.text_input("تاريخ الدخول والتقييد (صيغة YYYY-MM-DD):", value=selected_row['shipment_date'])
                    with ec5: 
                        edit_do_num = st.text_input("رقم أمر التسليم (D.O):", value=selected_row['do_number'])
                    with ec6: 
                        edit_do_val = st.number_input("قيمة أمر التسليم المعتمدة (بالدينار LYD):", value=float(selected_row['do_value_lyd']))
                        
                    ec7, ec8 = st.columns(2)
                    with ec7: 
                        edit_agency = st.number_input("تكلفة شحن ونولون الوكالة الكلية (بالدولار USD):", value=float(selected_row['agency_freight_usd']))
                    with ec8: 
                        edit_final = st.number_input("سعر الشحن النهائي المفتوح للزبون (بالدولار USD):", value=float(selected_row['final_freight_usd']))
                        
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.form_submit_button("💾 حفظ وتأكيد مزامنة البيانات المعدلة"):
                            db_execute(
                                'UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                (edit_cont.strip().upper(), edit_bl.strip().upper(), parse_any_date(edit_date), edit_do_num.strip(), edit_do_val, edit_agency, edit_final, shipment_id)
                            )
                            st.success("🎉 تم تعديل وحفظ بيانات الشحنة بنجاح بالمخدم السحابي!")
                            st.rerun()
                    with b2:
                        if st.form_submit_button("🗑️ حذف وإلغاء هذه الشحنة تماماً من الدفاتر"):
                            db_execute("DELETE FROM shipments WHERE id=%s", (shipment_id,))
                            st.success("🚨 تم حذف البوليصة والشحنة بالكامل وبصورة لا رجعة فيها.")
                            st.rerun()

# ==============================================================================
# البوابة الثالثة: الخزينة والتحصيلات المالية وسندات القبض
# ==============================================================================
elif menu == "💵 الخزينة والتحصيلات المالية":
    tab_add_rec, tab_edit_rec = st.tabs(["💰 تسجيل إيصال قبض جديد", "✏️ تعديل وحذف إيصالات الخزينة"])
    
    customers_list = db_query("SELECT * FROM customers ORDER BY name ASC")
    receipts_list = db_query("SELECT * FROM receipts ORDER BY id DESC")
    
    customers_df = pd.DataFrame(customers_list) if customers_list else pd.DataFrame(columns=['id', 'name'])
    receipts_all = pd.DataFrame(receipts_list) if receipts_list else pd.DataFrame(columns=['id', 'customer_name', 'amount', 'currency', 'receipt_date', 'notes'])

    # --- تسجيل إيصال قبض جديد بالخزينة ---
    with tab_add_rec:
        st.subheader("💰 إدارة المدفوعات المباشرة وإيداع الخزينة")
        if customers_df.empty:
            st.warning("⚠️ يرجى إضافة حساب زبون مسجل واحد على الأقل أولاً لتتمكن من إدراج المبالغ المالية.")
        else:
            st.write("➕ تحرير وتسجيل إيصال سداد مالي جديد")
            with st.form("receipt_form", clear_on_submit=True):
                rc1, rc2, rc3 = st.columns(3)
                with rc1: 
                    r_cust = st.selectbox("قبض من الزبون المسجل بالمنظومة:", customers_df['name'])
                with rc2: 
                    r_amount = st.number_input("قيمة المبلغ المقبوض بالكامل:", min_value=0.0, step=100.0, format="%.2f")
                with rc3: 
                    r_curr = st.selectbox("تحديد عملة التحصيل الرسمي:", ["دينار ليبي LYD", "دولار أمريكي USD"])
                    
                rc4, rc5 = st.columns([1, 2])
                with rc4: 
                    r_date = st.date_input("تاريخ القبض والتقييد المالي للجلسة الحالية:", datetime.now())
                with rc5: 
                    r_notes = st.text_input("رقم الإيصال اليدوي الموثق أو ملاحظات السند والبيان العام:")
                    
                if st.form_submit_button("💾 حفظ وإيداع الإيصال بقاعدة البيانات السحابية"):
                    if r_amount <= 0:
                        st.error("❌ خطأ: لا يمكن تقييد إيصال مالي بقيمة صفر أو قيمة سالبة.")
                    else:
                        db_execute(
                            'INSERT INTO receipts (customer_name, amount, currency, receipt_date, notes) VALUES (%s, %s, %s, %s, %s)', 
                            (r_cust, r_amount, r_curr, r_date.strftime('%Y-%m-%d'), r_notes.strip())
                        )
                        st.success(f"🎉 تم تسجيل وإيداع مبلغ {r_amount:,.2f} ({r_curr}) بحساب الزبون [{r_cust}] بنجاح بالخزينة!")
                        st.rerun()

    # --- مراجعة وتعديل وإلغاء إيصالات السداد ---
    with tab_edit_rec:
        st.subheader("✏️ مراجعة والتحكم في إيصالات وسندات المقبوضات الجارية")
        if receipts_all.empty:
            st.info("ℹ️ الخزينة فارغة من القيود والسندات المالية حالياً.")
        else:
            search_receipt = st.text_input("🔍 ابحث في الإيصالات (عبر اسم الزبون الملتزم أو ملاحظات السند ورقم الإيصال):")
            filtered_r = receipts_all.copy()
            if search_receipt.strip():
                sr = search_receipt.strip().lower()
                filtered_r = receipts_all[
                    receipts_all['customer_name'].str.lower().str.contains(sr, na=False) | 
                    receipts_all['notes'].str.lower().str.contains(sr, na=False)
                ]
                
            if filtered_r.empty:
                st.warning("⚠️ لم يتم العثور على أي نتائج تطابق عملية البحث الحالية.")
            else:
                filtered_r['selector_text'] = (
                    filtered_r['customer_name'] + 
                    " | قيمة المبلغ: " + filtered_r['amount'].astype(str) + 
                    " (" + filtered_r['currency'] + ") | التاريخ: " + 
                    filtered_r['receipt_date'] + " | البيان: " + filtered_r['notes']
                )
                selected_receipt_opt = st.selectbox("اختر الإيصال المستهدف للتعديل الفوري أو الإزالة من الخادم:", filtered_r['selector_text'])
                selected_r_row = filtered_r[filtered_r['selector_text'] == selected_receipt_opt].iloc[0]
                receipt_id = int(selected_r_row['id'])
                
                with st.form("edit_r_form"):
                    rec_c1, rec_c2, rec_c3 = st.columns(3)
                    with rec_c1: 
                        edit_r_cust = st.text_input("اسم حساب الزبون (مغلق ومحمي للسلامة الحسابية)", value=selected_r_row['customer_name'], disabled=True)
                    with rec_c2: 
                        edit_r_amount = st.number_input("تعديل قيمة المبلغ المالي للسند المختار:", value=float(selected_r_row['amount']))
                    with rec_c3: 
                        edit_r_curr = st.selectbox("تعديل عملة القيد المودعة المعتمدة:", ["دينار ليبي LYD", "دولار أمريكي USD"], index=0 if "LYD" in selected_r_row['currency'] else 1)
                        
                    rec_c4, rec_c5 = st.columns(2)
                    with rec_c4: 
                        edit_r_date = st.text_input("تاريخ القيد المالي للسند (صيغة YYYY-MM-DD):", value=selected_r_row['receipt_date'])
                    with rec_c5: 
                        edit_r_notes = st.text_input("تحديث ملاحظات / رقم الإيصال اليدوي والمستند:", value=selected_r_row['notes'])
                        
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.form_submit_button("💾 حفظ تعديلات الإيصال وتأكيد المزامنة بالدفاتر"):
                            db_execute(
                                'UPDATE receipts SET amount=%s, currency=%s, receipt_date=%s, notes=%s WHERE id=%s', 
                                (edit_r_amount, edit_r_curr, parse_any_date(edit_r_date), edit_r_notes.strip(), receipt_id)
                            )
                            st.success("🎉 تم تحديث ومزامنة بيانات الإيصال المالي بنجاح في الخزينة!")
                            st.rerun()
                    with b2:
                        if st.form_submit_button("🗑️ حذف السند المالي نهائياً وإلغاء القيد"):
                            db_execute("DELETE FROM receipts WHERE id=%s", (receipt_id,))
                            st.success("🚨 تم مسح السند المالي وشطبه بالكامل من الدفاتر السحابية للشركة.")
                            st.rerun()

# ==============================================================================
# البوابة الرابعة: شؤون الزبائن وصيانة قاعدة البيانات وتصفير النظام المجمع
# ==============================================================================
elif menu == "⚙️ شؤون الزبائن وصيانة النظام":
    tab_crm, tab_system = st.tabs(["👥 إدارة وحسابات الزبائن CRM", "💥 تصفير وصيانة المنظومة المجمعة"])
    
    customers_list = db_query("SELECT * FROM customers ORDER BY name ASC")
    customers_df = pd.DataFrame(customers_list) if customers_list else pd.DataFrame(columns=['id', 'name'])

    # --- إدارة حسابات الزبائن CRM ---
    with tab_crm:
        st.subheader("👥 التحكم الكامل والرقابة في قائمة الزبائن المعتمدين")
        tab1, tab2, tab3 = st.tabs(["➕ إضافة زبون جديد", "✏️ تعديل اسم حساب جاري", "❌ حذف وتصفية زبون"])
        
        with tab1:
            new_cust = st.text_input("أدخل الاسم الكامل للزبون أو الكيان التجاري لإدراجه:")
            if st.button("تأكيد تسجيل وإدراج العميل بالمنظومة"):
                if new_cust.strip():
                    db_execute("INSERT INTO customers (name) VALUES (%s)", (new_cust.strip(),))
                    st.success("🎉 تم تسجيل الزبون بنجاح بجدول الحسابات الرسمي للشركة!")
                    st.rerun()
                else:
                    st.error("❌ لا يمكن ترك حقل الاسم فارغاً.")
                    
        with tab2:
            if not customers_df.empty:
                cust_to_edit = st.selectbox("اختر حساب الزبون المراد تعديل مسماه بالكامل وتصحيحه:", customers_df['name'])
                new_name = st.text_input("أدخل الاسم الجديد المصحح والمطابق تماماً للحساب المالي:")
                if st.button("تأكيد تعديل ومزامنة المسمى بجميع الجداول التابعة"):
                    if new_name.strip():
                        db_execute("UPDATE customers SET name = %s WHERE name = %s", (new_name.strip(), cust_to_edit))
                        st.success("🎉 تم تعديل الاسم المالي ومزامنة كافة السجلات التابعة للعميل بنجاح!")
                        st.rerun()
            else:
                st.info("لا توجد حسابات زبائن مسجلة حالياً.")
                
        with tab3:
            if not customers_df.empty:
                cust_to_del = st.selectbox("اختر اسم حساب العميل لإزالته وشطب سجلاته نهائياً:", customers_df['name'])
                st.warning(f"🚨 تحذير: هذا الخيار سيقوم بحذف حساب [{cust_to_del}] بالكامل وشطب كافة حاوياته وإيصالاته التابعة من النظام السحابي!")
                if st.button("موافق، تأكيد الحذف النهائي الشامل لحسابه وملفاته"):
                    db_execute("DELETE FROM customers WHERE name = %s", (cust_to_del,))
                    st.success(f"🚨 تم مسح وإغلاق حساب [{cust_to_del}] مع كافة قيوده المالية نهائياً.")
                    st.rerun()
            else:
                st.info("لا توجد حسابات زبائن مسجلة حالياً.")

    # --- صيانة وتصفير المنظومة المجمعة كلياً ---
    with tab_system:
        st.subheader("🗑️ محرك تصفير المنظومة والشطب المجمع لقاعدة البيانات للشركة")
        tab_del_cust, tab_reset_all = st.tabs(["👤 مسح شحنات زبون معين بالكامل", "💥 تصفير كلي ونهائي للنظام الموحد"])
        
        with tab_del_cust:
            if customers_df.empty:
                st.info("لا توجد حسابات زبائن مسجلة حالياً.")
            else:
                target_cust = st.selectbox("اختر اسم حساب العميل المراد إزالة شحناته بالكامل وشطبها:", customers_df['name'], key="bulk_del_select")
                cust_shipments = db_query("SELECT id, container_number, bl_number, do_number FROM shipments WHERE customer_name = %s", (target_cust,))
                
                if not cust_shipments:
                    st.info(f"لا توجد حالياً أي حاويات جارية أو شحنات مسجلة باسم الزبون [{target_cust}].")
                else:
                    shipment_options = {f"📦 حاوية: {r['container_number']} | بوليصة: {r['bl_number']} | إذن رقم: {r['do_number']}": r['id'] for r in cust_shipments}
                    select_all = st.checkbox("🔄 تحديد وتظليل كافة حاويات هذا العميل المسجلة أعلاه لشطبها")
                    default_selection = list(shipment_options.keys()) if select_all else []
                    selected_labels = st.multiselect("اختر الشحنات المستهدفة بالشطب والإزالة الكلية للعميل المذكور:", options=list(shipment_options.keys()), default=default_selection)
                    
                    if selected_labels:
                        confirm_word = st.text_input("لتأكيد تنفيذ عملية الشطب المحددة، اكتب كلمة (حذف) صراحة أدناه للتأكيد الفوري:")
                        if st.button("🗑️ تنفيذ تصفية وحذف الحاويات المحددة وشطبها"):
                            if confirm_word.strip() == "حذف":
                                for label in selected_labels:
                                    s_id = shipment_options[label]
                                    db_execute("DELETE FROM shipments WHERE id = %s", (s_id,))
                                st.success("🚨 تم شطب ومسح الحاويات المحددة للعميل بنجاح وبسرعة!")
                                st.rerun()
                            else:
                                st.error("❌ الكلمة التأكيدية المدخلة غير صحيحة، يرجى المحاولة بدقة.")
                                
        with tab_reset_all:
            st.warning("⚠️ خطر للغاية! هذا القسم يقوم بمسح المنظومة بالكامل والعودة للصفر وتصفير كافة سجلات الزبائن والتحصيلات المالية!")
            clear_financials = st.checkbox("الموافقة على مسح وتصفير كافة إيصالات الخزينة وسجل أسماء الزبائن أيضاً كلياً للبداية من جديد")
            confirm_all = st.text_input("لتأكيد التصفير السحابي المجمع والشامل والنهائي، اكتب العبارة التأكيدية (Core-Reset) صراحة أدناه:")
            
            if st.button("💥 بدء التصفير الشامل والنهائي لقواعد البيانات والعودة للصفر"):
                if confirm_all == "Core-Reset":
                    db_execute("TRUNCATE TABLE shipments RESTART IDENTITY", (clear_financials,))
                    st.success("💥 تم تصفير قاعدة البيانات السحابية بالكامل وتجهيزها للبدء من جديد بنجاح وتطهير كافة الملفات!")
                    st.rerun()
                else:
                    st.error("❌ العبارة التأكيدية المكتوبة غير متطابقة، تم رفض شطب النظام.")
