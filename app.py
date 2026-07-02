import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import re
import plotly.graph_objects as go
import plotly.express as px

# ==============================================================================
# 1. إعداد الصفحة الأساسي بنسق عريض رصين وراقٍ
# ==============================================================================
st.set_page_config(
    page_title="إستبرق الدولية - منظومة إدارة الشحنات والرقابة المالية",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. حزمة الـ CSS العالمية المتطورة لثبات الـ RTL والطباعة الاحترافية المعزولة
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800&display=swap');

/* تنسيق الواجهة العامة */
html, body, [data-testid="stSidebar"], .stApp {
    font-family: 'Cairo', sans-serif;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f8fafc;
    color: #1e293b;
}

/* محاذاة النصوص والقوائم */
.stHeading, .stMarkdown, p, div, label, span, h1, h2, h3, h4, h5, h6 {
    text-align: right !important;
    direction: rtl !important;
}

/* بطاقات المؤشرات المالية الفاخرة (ERP Metric Cards) */
.kpi-container {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-bottom: 25px;
    direction: rtl !important;
}
.kpi-card {
    flex: 1;
    min-width: 240px;
    background: #ffffff;
    padding: 20px;
    border-radius: 12px;
    border-right: 5px solid #1b4332;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    transition: transform 0.2s ease;
}
.kpi-card:hover {
    transform: translateY(-2px);
}
.kpi-card h5 { 
    margin: 0 0 8px 0 !important; 
    color: #64748b !important; 
    font-size: 13px !important; 
    font-weight: 700 !important; 
    text-transform: uppercase;
}
.kpi-card h2 { 
    margin: 0 !important; 
    font-size: 26px !important; 
    font-weight: 800 !important; 
    color: #1b4332 !important; 
}
.kpi-card p { 
    margin: 6px 0 0 0 !important; 
    font-size: 11px !important; 
    color: #94a3b8 !important; 
}

/* هندسة جداول البيانات الفاخرة المعتمدة */
.enterprise-table-container {
    width: 100%;
    overflow-x: auto;
    direction: rtl !important;
    margin: 20px 0;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    background: #ffffff;
}
table.corporate-data-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl !important;
    text-align: right !important;
}
table.corporate-data-table th {
    background-color: #1b4332 !important;
    color: #ffffff !important;
    padding: 14px 16px;
    font-weight: 700;
    font-size: 14px;
    border-bottom: 3px solid #112a1f;
    white-space: nowrap;
    text-align: right !important;
}
table.corporate-data-table td {
    padding: 12px 16px;
    text-align: right !important;
    border-bottom: 1px solid #f1f5f9;
    color: #334155;
    font-size: 13.5px;
    font-weight: 500;
}
table.corporate-data-table tr:nth-child(even) { background-color: #f8fafc; }
table.corporate-data-table tr:hover { background-color: #f1f5f9; }

/* عناصر التحكم والمدخلات */
div.stButton > button:first-child {
    background-color: #1b4332 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    width: 100% !important;
    border-radius: 8px !important;
    height: 44px !important;
    border: none !important;
    font-size: 15px !important;
    box-shadow: 0 4px 6px -1px rgba(27, 67, 50, 0.2) !important;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover { 
    background-color: #2d6a4f !important; 
    transform: translateY(-1px);
}

/* الشارات الملونة للحالات */
.status-badge { 
    padding: 4px 10px; 
    border-radius: 6px; 
    font-size: 11.5px; 
    font-weight: 700; 
    display: inline-block;
}
.status-green { background-color: #d8f3dc; color: #1b4332; }
.status-red { background-color: #fee2e2; color: #991b1b; }
.status-orange { background-color: #fef3c7; color: #92400e; }

/* تخصيص مظهر الـ Sidebar */
[data-testid="stSidebar"] {
    background-color: #112a1f !important;
}
[data-testid="stSidebar"] * {
    color: #f8fafc !important;
}
[data-testid="stSidebar"] .stRadio label {
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ==============================================================================
 * 📜 هيكلية الطباعة المعزولة كلياً والمضمونة (Anti-Overlap Isolation CSS)
 * ============================================================================== */
.official-print-document { display: none; }

@media print {
    /* إخفاء واجهة تطبيق ستريمليت بالكامل بطريقة التمويه المرئي المضمون */
    body * {
        visibility: hidden !important;
    }
    
    /* حصر وإظهار وثيقة كشف الحساب الرسمية لوحدها فقط */
    .official-print-document, .official-print-document * {
        visibility: visible !important;
    }
    
    .official-print-document {
        display: block !important;
        position: absolute !important;
        left: 0 !important;
        top: 0 !important;
        width: 100% !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 10mm 10mm !important;
        direction: rtl !important;
        text-align: right !important;
    }

    @page { 
        size: A4 portrait; 
        margin: 15mm 10mm; 
    }
    
    .document-corporate-header {
        border-bottom: 3px double #000000;
        padding-bottom: 12px;
        margin-bottom: 20px;
        text-align: center !important;
    }
    .document-corporate-header h1 {
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 0 0 5px 0 !important;
        text-align: center !important;
    }
    .document-corporate-header p {
        font-size: 12px !important;
        margin: 0 !important;
        text-align: center !important;
    }
    
    .document-meta-table {
        width: 100% !important;
        margin-bottom: 20px !important;
        font-size: 12px !important;
    }
    .document-meta-table td {
        padding: 5px !important;
        border: none !important;
    }

    table.print-invoice-table { 
        width: 100% !important; 
        border-collapse: collapse !important; 
        margin-top: 15px !important; 
        font-size: 11px !important; 
    }
    table.print-invoice-table th { 
        background-color: #f1f5f9 !important; 
        color: #000000 !important; 
        border: 1px solid #475569 !important; 
        padding: 8px !important; 
        font-weight: bold !important; 
        text-align: right !important; 
        -webkit-print-color-adjust: exact; 
    }
    table.print-invoice-table td { 
        border: 1px solid #cbd5e1 !important; 
        padding: 8px !important; 
        text-align: right !important; 
        color: #000000 !important; 
    }
    table.print-invoice-table tr { 
        page-break-inside: avoid !important; 
    }
    
    table.print-totals-table { 
        width: 100% !important; 
        border-collapse: collapse !important; 
        margin-top: 20px !important; 
        page-break-inside: avoid !important; 
    }
    table.print-totals-table th { 
        background-color: #e2e8f0 !important; 
        border: 1px solid #475569 !important; 
        padding: 10px !important; 
        font-weight: bold !important; 
        text-align: center !important; 
        -webkit-print-color-adjust: exact; 
    }
    table.print-totals-table td { 
        border: 1px solid #cbd5e1 !important; 
        padding: 10px !important; 
        text-align: center !important; 
        font-weight: 700 !important; 
    }
    
    .print-signatures-block { 
        margin-top: 40px !important; 
        width: 100% !important; 
        display: flex !important; 
        justify-content: space-between !important; 
        font-size: 12px !important;
        font-weight: bold !important; 
        page-break-inside: avoid !important; 
    }
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. محرك إدارة والتحكم باتصالات قواعد البيانات السحابية (Safe Context Manager)
# ==============================================================================
def get_db_connection():
    """تأسيس اتصال آمن بقاعدة البيانات مع تفعيل معالجة الاستثناءات"""
    try:
        db_url = st.secrets["postgres"]["url"]
        return psycopg2.connect(db_url, cursor_factory=DictCursor)
    except Exception as e:
        st.error(f"🔴 خطأ في الاتصال بقاعدة البيانات السحابية: {e}")
        st.stop()


def init_db():
    """تهيئة الجداول الجمركية والمالية مع الفهارس المناسبة لسرعة الاستعلام"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # جدول أسماء الزبائن الرئيسي
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    id SERIAL PRIMARY KEY, 
                    name TEXT NOT NULL UNIQUE
                )
            """)
            # جدول الشحنات والحاويات المطور
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
            # جدول إيصالات تحصيل الخزينة
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
        st.error(f"❌ خطأ في إعداد قاعدة البيانات السحابية: {e}")
    finally:
        conn.close()

# تهيئة قاعدة البيانات تلقائياً
init_db()


# ==============================================================================
# 4. الدوال والوظائف المساعدة (Utility Functions)
# ==============================================================================
def safe_float(val):
    """تحويل القيم بطريقة آمنة لتفادي الأخطاء الصفرية"""
    if pd.isnull(val): 
        return 0.0
    try: 
        return float(val)
    except (ValueError, TypeError): 
        return 0.0


def to_excel(df):
    """توليد ملفات إكسل رسمية معزولة ومعتمدة"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='كشف الحساب الرسمي')
    return output.getvalue()


def parse_any_date(date_val):
    """معالجة مرنة لمختلف صيغ التواريخ اليدوية والآلية وتوحيدها"""
    if isinstance(date_val, (datetime, pd.Timestamp)):
        return date_val.strftime('%Y-%m-%d')
    date_str = str(date_val).strip()
    for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y'):
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return datetime.now().strftime('%Y-%m-%d')


def render_premium_html_grid(df, show_internal_profit=False):
    """تصميم عارض الجداول الذكية التفاعلية على واجهة الشاشة"""
    headers = [
        "اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", 
        "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)", "مؤشر الربحية"
    ]
    if show_internal_profit: 
        headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
        
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    tr_html = ""
    
    for _, row in df.iterrows():
        # مؤشر ربحية الحاوية
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
# 5. واجهة التحكم الجانبية وأقسام المنظومة
# ==============================================================================
st.sidebar.markdown(
    "<h1 style='text-align: center; color: #d8f3dc; font-weight:800; font-size:24px; margin-bottom:20px;'>"
    "🚢 إستبرق الدولية"
    "</h1>", 
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "لوحة تحكم المنظومة الموحدة:", 
    [
        "📊 لوحة التحكم والتقارير", 
        "🔍 الشحنات ناقصة البيانات", 
        "💰 إيصالات القبض والمالية", 
        "✏️ تعديل وحذف الإيصالات", 
        "➕ إضافة شحنة جديدة (يدوي/LCL)", 
        "📥 رفع ملف إكسل", 
        "👥 إدارة الزبائن", 
        "📝 تعديل وحذف الشحنات", 
        "🗑️ مسح البيانات دفعة واحدة"
    ]
)


# ==============================================================================
# القسم الأول: لوحة التحكم والتقارير المالية المدمجة
# ==============================================================================
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 مركز التقارير والرقابة المالية والموازنات الجارية")
    
    conn = get_db_connection()
    try:
        customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
        shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
        receipts_all = pd.read_sql_query("SELECT * FROM receipts ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب التقارير: {e}")
    finally:
        conn.close()
        
    if customers_df.empty:
        st.warning("⚠️ لا توجد أي حسابات زبائن أو شحنات مسجلة حالياً في النظام.")
    else:
        # حساب إحصائيات الموقف المالي العام بصورة فورية وسريعة
        t_cont = len(shipments_all)
        t_lyd = shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0
        t_usd = shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
        
        # عرض بطاقات الـ KPI الفاخرة
        st.markdown(
            f'<div class="kpi-container">'
            f'<div class="kpi-card"><h5>📦 حجم الحاويات المعالجة</h5><h2>{t_cont} شحنة جارية</h2><p>إجمالي القيود الجمركية</p></div>'
            f'<div class="kpi-card"><h5>💵 ذمم أوامر التسليم الكلية</h5><h2>{t_lyd:,.2f} د.ل</h2><p>قيمة الدفعات المحلية المفتوحة</p></div>'
            f'<div class="kpi-card"><h5>💵 نولون الشحن الدولي المعتمد</h5><h2>${t_usd:,.2f}</h2><p>ذمم النقل الخارجي بالدولار</p></div>'
            f'</div>', 
            unsafe_allow_html=True
        )
        
        # محرك التصفية الجمركي والمالي المطور
        with st.expander("⚙️ محرك تحديد هيكلية التقارير وعمليات الفرز الذكي", expanded=True):
            c_filter1, c_filter2, c_filter3 = st.columns(3)
            with c_filter1: 
                report_scope = st.radio("1. نطاق كشف الحساب:", ["كل زبائن المنظومة", "زبون محدد فردي"])
            with c_filter2: 
                report_structure = st.radio("2. نوع وثيقة الكشف المالية:", ["كشف مالي إجمالي عام", "كشف حساب تفصيلي"])
            with c_filter3: 
                display_profit = st.checkbox("إظهار قيم شحن الوكالة وصافي الأرباح (خاص بالإدارة)")
                
            if report_scope == "زبون محدد فردي":
                target_customer = st.selectbox("🎯 اختر اسم حساب الزبون المستهدف بالفرز المالي:", customers_df['name'].tolist())
            else:
                target_customer = "الكل"

        # تحضير ومعالجة البيانات بناءً على الفلاتر بطريقة الـ Vectorization السريعة
        df_export_target = pd.DataFrame()
        req_l, paid_l, req_u, paid_u = 0.0, 0.0, 0.0, 0.0
        
        if report_scope == "كل زبائن المنظومة":
            # معالجة بيانات المجموع الكلي للعملاء دفعة واحدة (ميزان مراجعة مالي مبسط)
            if report_structure == "كشف مالي إجمالي عام":
                st.subheader("📋 كشف ملخص أرصاد الحسابات لكافة الزبائن")
                
                # تجميع سريع للشحنات
                if not shipments_all.empty:
                    ship_grp = shipments_all.groupby('customer_name').agg(
                        total_containers=('id', 'count'),
                        required_lyd=('do_value_lyd', 'sum'),
                        required_usd=('final_freight_usd', 'sum')
                    ).reset_index()
                else:
                    ship_grp = pd.DataFrame(columns=['customer_name', 'total_containers', 'required_lyd', 'required_usd'])
                
                # تجميع سريع للمتحصلات
                if not receipts_all.empty:
                    rec_lyd = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD'].groupby('customer_name')['amount'].sum().reset_index(name='paid_lyd')
                    rec_usd = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD'].groupby('customer_name')['amount'].sum().reset_index(name='paid_usd')
                    rec_grp = pd.merge(rec_lyd, rec_usd, on='customer_name', how='outer').fillna(0.0)
                else:
                    rec_grp = pd.DataFrame(columns=['customer_name', 'paid_lyd', 'paid_usd'])
                    
                # بناء ميزان الأرصدة
                df_export_target = pd.merge(customers_df, ship_grp, left_on='name', right_on='customer_name', how='left')
                df_export_target = pd.merge(df_export_target, rec_grp, left_on='name', right_on='customer_name', how='left')
                df_export_target.drop(columns=['customer_name_x', 'customer_name_y', 'name'], errors='ignore', inplace=True)
                df_export_target.rename(columns={'name': 'customer_name'}, errors='ignore', inplace=True)
                if 'customer_name' not in df_export_target.columns:
                    df_export_target.insert(0, 'customer_name', customers_df['name'])
                    
                df_export_target.fillna(0.0, inplace=True)
                df_export_target['remaining_lyd'] = df_export_target['required_lyd'] - df_export_target['paid_lyd']
                df_export_target['remaining_usd'] = df_export_target['required_usd'] - df_export_target['paid_usd']
                
                # عرض الجدول المالي التفاعلي
                th_html = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي المعلق (د.ل)", "نولون الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
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
                
                # رسم بياني توضيحي لميزان الحسابات - حل مشكلة bmode السابقة إلى barmode
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_export_target['customer_name'], 
                    y=df_export_target['remaining_lyd'], 
                    name='متبقي الدينار (د.ل)', 
                    marker_color='#1b4332'
                ))
                fig.add_trace(go.Bar(
                    x=df_export_target['customer_name'], 
                    y=df_export_target['remaining_usd'], 
                    name='متبقي الدولار ($)', 
                    marker_color='#d8f3dc'
                ))
                fig.update_layout(
                    title='📈 ميزان الأرصاد المعلقة والذمم المالية الجارية لكافة الزبائن معاً', 
                    template='plotly_white', 
                    font=dict(family="Cairo"), 
                    barmode='group'  # تم تصحيح المشكلة الموضحة في image_93d083.png بنجاح
                )
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                # كشف حساب تفصيلي للكل
                st.subheader("📋 كشف السجل التفصيلي الموحد لجميع الزبائن")
                df_export_target = shipments_all.copy()
                df_export_target['profit_usd'] = df_export_target['final_freight_usd'] - df_export_target['agency_freight_usd']
                render_premium_html_grid(df_export_target, show_internal_profit=display_profit)
                
                req_l = df_export_target['do_value_lyd'].sum()
                req_u = df_export_target['final_freight_usd'].sum()
                paid_l = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD']['amount'].sum() if not receipts_all.empty else 0.0
                paid_u = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD']['amount'].sum() if not receipts_all.empty else 0.0
                
        else:
            # معالجة بيانات زبون محدد بشكل آمن وفوري
            df_cust_s = shipments_all[shipments_all['customer_name'] == target_customer].copy()
            df_cust_r = receipts_all[receipts_all['customer_name'] == target_customer].copy()
            
            req_l = df_cust_s['do_value_lyd'].sum() if not df_cust_s.empty else 0.0
            req_u = df_cust_s['final_freight_usd'].sum() if not df_cust_s.empty else 0.0
            paid_l = df_cust_r[df_cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not df_cust_r.empty else 0.0
            paid_u = df_cust_r[df_cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not df_cust_r.empty else 0.0
            
            if report_structure == "كشف مالي إجمالي عام":
                st.subheader(f"📋 ملخص الموقف الحسابي العام لحساب: {target_customer}")
                # عرض إجمالي مجمع للزبون المختار
                df_export_target = df_cust_s.copy()
                render_premium_html_grid(df_export_target, show_internal_profit=display_profit)
            else:
                st.subheader(f"📋 كشف الحاويات والقيود التفصيلي المعتمد لحساب: {target_customer}")
                df_cust_s['profit_usd'] = df_cust_s['final_freight_usd'] - df_cust_s['agency_freight_usd']
                df_export_target = df_cust_s.copy()
                render_premium_html_grid(df_export_target, show_internal_profit=display_profit)

        # زر تحميل كشف الحساب الحالي بصيغة إكسل
        if not df_export_target.empty:
            st.write("")
            st.download_button(
                label="📥 تحميل كشف الحساب النشط حالياً بصيغة Excel معتمد للشركة", 
                data=to_excel(df_export_target), 
                file_name=f"istabraq_statement_{target_customer.replace(' ', '_')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # ==============================================================================
        # محرك الطباعة الجمركية المعتمد والمعزول (A4 Portrait Layout)
        # ==============================================================================
        st.write("---")
        st.markdown("### 🖨️ وثيقة تصديق ومطابقة كشوفات الحساب الرسمية الجاهزة للطباعة:")
        
        if st.button("🖨️ تأكيد معالجة وتوليد وثيقة كشف الحساب للطباعة الفورية"):
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
                        <td style="color:#1b4332;">{paid_l:,.2f} د.ل</td>
                        <td style="color:#991b1b; font-weight:bold;">{req_l - paid_l:,.2f} د.ل</td>
                    </tr>
                    <tr>
                        <td><b>حساب نولون وأرصاد الشحن الدولي (USD)</b></td>
                        <td>${req_u:,.2f}</td>
                        <td style="color:#1b4332;">${paid_u:,.2f}</td>
                        <td style="color:#991b1b; font-weight:bold;">${req_u - paid_u:,.2f}</td>
                    </tr>
                </tbody>
            </table>"""

            # حجر الأساس لبناء الطباعة المعزولة تماماً بدون تداخل
            html_document_payload = f"""
            <div class='official-print-document'>
                <div class='document-corporate-header'>
                    <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1>
                    <p>المكتب الرئيسي: مصراتة - ليبيا | الحسابات المركزية المعتمدة والتسويات المالية</p>
                </div>
                <table class='document-meta-table'>
                    <tr>
                        <td><b>كشف حساب جاري للعميل:</b> {target_customer if report_scope == 'زبون محدد فردي' else 'كافة عملاء المنظومة'}</td>
                        <td style='text-align: left;'><b>تاريخ استخراج الوثيقة:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                    </tr>
                    <tr>
                        <td><b>نوع وثيقة كشف الموقف المالي:</b> {doc_type_text}</td>
                        <td style='text-align: left;'><b>حصر القيود المدرجة:</b> {len(df_export_target)} سجل جاري فعال</td>
                    </tr>
                </table>
                <table class='print-invoice-table'>
                    <thead><tr>{table_headers}</tr></thead>
                    <tbody>{rows_html_p}</tbody>
                </table>
                {summary_table_html}
                <div class='print-signatures-block'>
                    <div>توقيع واعتماد الحسابات المركزية: .........................</div>
                    <div>خِتم وتصديق إدارة الشركة رسميًا: .........................</div>
                </div>
            </div>"""
            
            st.markdown(html_document_payload, unsafe_allow_html=True)
            st.success("🎉 تكللت العملية بالنجاح! يمكنك الآن الضغط على مفاتيح الكيبورد [ Ctrl + P ] لبدء الطباعة المعزولة والآمنة فوراً.")


# ==============================================================================
# القسم الثاني: محرك حصر ومتابعة الشحنات ناقصة البيانات (البديل المطور لأعمار الديون)
# ==============================================================================
elif menu == "🔍 الشحنات ناقصة البيانات":
    st.title("🔍 محرك حصر ومتابعة الشحنات ناقصة البيانات (Data Auditor)")
    st.markdown("يساعدك هذا القسم في فلترة وتحديد كافة بوالص الحاويات التي تفتقر لمعلومات أساسية مثل (التواريخ، أرقام البوالص، قيم الشحن، أرقام الحاويات) لتسهيل استكمالها.")
    
    conn = get_db_connection()
    try:
        customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
        shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"خطأ في جلب البيانات: {e}")
    finally:
        conn.close()
        
    if shipments_all.empty:
        st.success("🎉 قاعدة البيانات خالية تماماً من الشحنات حالياً.")
    else:
        # لوحة الفرز والتدقيق الذكي
        with st.expander("⚙️ محدد شروط تدقيق وفحص البيانات الناقصة", expanded=True):
            fc1, fc2 = st.columns([1, 2])
            with fc1:
                selected_cust_filter = st.selectbox("تصفية لزبون محدد:", ["كل زبائن المنظومة"] + customers_df['name'].tolist())
            with fc2:
                incomplete_criteria = st.multiselect(
                    "اختر النواقص التي ترغب في حصرها:",
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
        
        # فلترة البيانات بناء على العميل أولاً
        df_audit = shipments_all.copy()
        if selected_cust_filter != "كل زبائن المنظومة":
            df_audit = df_audit[df_audit['customer_name'] == selected_cust_filter]
            
        # تطبيق مرشحات النواقص المختارة
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
                
            # دمج المرشحات باستخدام المعامل المنطقي OR لتظهر أي حاوية بها نقص واحد على الأقل
            if masks:
                combined_mask = masks[0]
                for m in masks[1:]:
                    combined_mask = combined_mask | m
                df_audit = df_audit[combined_mask]
        
        if df_audit.empty:
            st.success("🎉 ممتاز! لا توجد أي شحنات ناقصة البيانات بناءً على شروط الفحص المحددة.")
        else:
            st.warning(f"⚠️ تم رصد {len(df_audit)} شحنة / حاوية ببيانات ناقصة وغير مكتملة:")
            
            # عرض الجدول الملون مع إبراز الأخطاء
            th_html = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم D.O", "قيمة إذن التسليم", "شحن الوكالة", "الشحن النهائي"])
            tr_html = ""
            for _, row in df_audit.iterrows():
                # تلوين النواقص باللون الأحمر لتنبيه المدخل
                cust = row['customer_name']
                bl = row['bl_number'] if (row['bl_number'] and str(row['bl_number']).strip()) else "<span style='color:#ef4444; font-weight:bold;'>⚠️ ناقص</span>"
                cont = row['container_number'] if (row['container_number'] and str(row['container_number']).strip()) else "<span style='color:#ef4444; font-weight:bold;'>⚠️ ناقص</span>"
                sdate = row['shipment_date'] if (row['shipment_date'] and str(row['shipment_date']).strip()) else "<span style='color:#ef4444; font-weight:bold;'>⚠️ ناقص</span>"
                donum = row['do_number'] if (row['do_number'] and str(row['do_number']).strip()) else "<span style='color:#ef4444; font-weight:bold;'>⚠️ ناقص</span>"
                
                doval = f"{row['do_value_lyd']:,.2f} د.ل" if row['do_value_lyd'] > 0 else "<span style='color:#ef4444; font-weight:bold;'>⚠️ 0.0 د.ل</span>"
                agency = f"${row['agency_freight_usd']:,.2f}" if row['agency_freight_usd'] > 0 else "<span style='color:#ef4444; font-weight:bold;'>⚠️ $0.0</span>"
                final = f"${row['final_freight_usd']:,.2f}" if row['final_freight_usd'] > 0 else "<span style='color:#ef4444; font-weight:bold;'>⚠️ $0.0</span>"
                
                tr_html += (
                    f"<tr>"
                    f"<td><b>{cust}</b></td>"
                    f"<td>{bl}</td>"
                    f"<td>{cont}</td>"
                    f"<td>{sdate}</td>"
                    f"<td>{donum}</td>"
                    f"<td>{doval}</td>"
                    f"<td>{agency}</td>"
                    f"<td>{final}</td>"
                    f"</tr>"
                )
                
            st.markdown(
                f'<div class="enterprise-table-container">'
                f'<table class="corporate-data-table">'
                f'<thead><tr>{th_html}</tr></thead>'
                f'<tbody>{tr_html}</tbody>'
                f'</table></div>', 
                unsafe_allow_html=True
            )
            
            # ==============================================================================
            # محرك تعديل سريع ومباشر للحاويات ناقصة البيانات
            # ==============================================================================
            st.write("---")
            st.subheader("📝 الاستكمال والتعديل السريع للحاوية المحددة:")
            st.info("تسمح لك هذه اللوحة باختيار الشحنة الناقصة مباشرة من الجدول وتحديث معلوماتها فوراً دون تشتيت.")
            
            df_audit['selector_label'] = (
                df_audit['customer_name'] + 
                " | بوليصة: " + df_audit['bl_number'].astype(str) + 
                " | حاوية: " + df_audit['container_number'].astype(str)
            )
            
            selected_audit_opt = st.selectbox("اختر الشحنة المستهدفة بالاستكمال والترقيد المالي:", df_audit['selector_label'].tolist())
            selected_audit_row = df_audit[df_audit['selector_label'] == selected_audit_opt].iloc[0]
            audit_id = int(selected_audit_row['id'])
            
            with st.form("quick_audit_update_form"):
                ac1, ac2, ac3 = st.columns(3)
                with ac1:
                    audit_cust_name = st.text_input("اسم حساب العميل (مغلق ومحمي):", value=selected_audit_row['customer_name'], disabled=True)
                with ac2:
                    audit_container_num = st.text_input("رقم الحاوية / الحاويات:", value=selected_audit_row['container_number'])
                with ac3:
                    audit_bl_num = st.text_input("رقم البوليصة الرئيسي:", value=selected_audit_row['bl_number'])
                    
                ac4, ac5, ac6 = st.columns(3)
                with ac4:
                    audit_date_val = st.text_input("تاريخ الدخول والتقييد (YYYY-MM-DD):", value=selected_audit_row['shipment_date'])
                with ac5:
                    audit_do_num_val = st.text_input("رقم إذن / أمر التسليم (D.O):", value=selected_audit_row['do_number'])
                with ac6:
                    audit_do_value_val = st.number_input("قيمة أمر التسليم الفعالة (بالدينار LYD):", value=float(selected_audit_row['do_value_lyd']))
                    
                ac7, ac8 = st.columns(2)
                with ac7:
                    audit_agency_val = st.number_input("تكلفة شحن الوكالة الكلية (بالدولار USD):", value=float(selected_audit_row['agency_freight_usd']))
                with ac8:
                    audit_final_val = st.number_input("سعر الشحن النهائي المقيد على العميل (بالدولار USD):", value=float(selected_audit_row['final_freight_usd']))
                    
                if st.form_submit_button("🚀 حفظ وتأكيد استكمال البيانات ومزامنتها"):
                    conn = get_db_connection()
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(
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
                            conn.commit()
                        st.success("🎉 تم استكمال وتحديث بيانات الشحنة بنجاح في النظام السحابي!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ أثناء الحفظ الفوري للبيانات: {e}")
                    finally:
                        conn.close()


# ==============================================================================
# القسم الثالث: إدارة المدفوعات وإيصالات القبض والمالية
# ==============================================================================
elif menu == "💰 إيصالات القبض والمالية":
    st.title("💰 إدارة المدفوعات وإيصالات تحصيل وإيداع الخزينة")
    
    conn = get_db_connection()
    try:
        customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    except Exception as e:
        st.error(f"خطأ في الاتصال: {e}")
    finally:
        conn.close()
        
    if customers_df.empty:
        st.warning("⚠️ يرجى إضافة حساب زبون مسجل واحد على الأقل عبر قسم (إدارة الزبائن) لتتمكن من إدراج المبالغ المالية.")
    else:
        st.subheader("➕ تحرير وتسجيل إيصال سداد مالي جديد")
        with st.form("receipt_form", clear_on_submit=True):
            rc1, rc2, rc3 = st.columns(3)
            with rc1: 
                r_cust = st.selectbox("قبض من الزبون المسجل:", customers_df['name'])
            with rc2: 
                r_amount = st.number_input("قيمة المبلغ المقبوض بالكامل:", min_value=0.0, step=100.0, format="%.2f")
            with rc3: 
                r_curr = st.selectbox("تحديد العملة المحصلة:", ["دينار ليبي LYD", "دولار أمريكي USD"])
                
            rc4, rc5 = st.columns([1, 2])
            with rc4: 
                r_date = st.date_input("تاريخ القبض والتقييد المالي:", datetime.now())
            with rc5: 
                r_notes = st.text_input("رقم الإيصال اليدوي أو ملاحظات السند والبيان:")
                
            if st.form_submit_button("💾 حفظ وإيداع الإيصال بقاعدة البيانات"):
                if r_amount <= 0:
                    st.error("❌ خطأ: لا يمكن تقييد إيصال مالي بقيمة صفر أو قيمة سالبة.")
                else:
                    conn = get_db_connection()
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                'INSERT INTO receipts (customer_name, amount, currency, receipt_date, notes) VALUES (%s, %s, %s, %s, %s)', 
                                (r_cust, r_amount, r_curr, r_date.strftime('%Y-%m-%d'), r_notes.strip())
                            )
                            conn.commit()
                        st.success(f"🎉 تم تسجيل وإيداع مبلغ {r_amount:,.2f} ({r_curr}) بحساب الزبون [{r_cust}] بنجاح!")
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء حفظ الإيصال: {e}")
                    finally:
                        conn.close()


# ==============================================================================
# القسم الرابع: تعديل وحذف إيصالات القبض الجارية
# ==============================================================================
elif menu == "✏️ تعديل وحذف الإيصالات":
    st.title("✏️ التحكم وإدارة إيصالات القبض والتحصيلات المالية (تعديل / حذف)")
    
    conn = get_db_connection()
    try:
        receipts_all = pd.read_sql_query("SELECT * FROM receipts ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"خطأ: {e}")
    finally:
        conn.close()
        
    if receipts_all.empty:
        st.info("ℹ️ الخزينة خالية تماماً ولا توجد إيصالات مسجلة حالياً.")
    else:
        search_receipt = st.text_input("🔍 ابحث في الإيصالات (عبر اسم الزبون أو ملاحظات السند):")
        filtered_r = receipts_all.copy()
        
        if search_receipt.strip():
            sr = search_receipt.strip().lower()
            filtered_r = receipts_all[
                receipts_all['customer_name'].str.lower().str.contains(sr, na=False) | 
                receipts_all['notes'].str.lower().str.contains(sr, na=False)
            ]
            
        if filtered_r.empty:
            st.warning("⚠️ لم يتم العثور على أي نتائج تطابق عملية البحث.")
        else:
            filtered_r['selector_text'] = (
                filtered_r['customer_name'] + 
                " | قيمة المبلغ: " + filtered_r['amount'].astype(str) + 
                " (" + filtered_r['currency'] + ") | التاريخ: " + 
                filtered_r['receipt_date'] + " | البيان: " + filtered_r['notes']
            )
            
            selected_receipt_opt = st.selectbox("اختر الإيصال المستهدف للتعديل أو الإزالة السحابية:", filtered_r['selector_text'])
            selected_r_row = filtered_r[filtered_r['selector_text'] == selected_receipt_opt].iloc[0]
            receipt_id = int(selected_r_row['id'])
            
            with st.form("edit_r_form"):
                rec_c1, rec_c2, rec_c3 = st.columns(3)
                with rec_c1: 
                    edit_r_cust = st.text_input("اسم حساب الزبون (غير قابل للتغيير من هنا)", value=selected_r_row['customer_name'], disabled=True)
                with rec_c2: 
                    edit_r_amount = st.number_input("تعديل قيمة المبلغ المالي:", value=float(selected_r_row['amount']))
                with rec_c3: 
                    edit_r_curr = st.selectbox("تعديل العملة المودعة:", ["دينار ليبي LYD", "دولار أمريكي USD"], index=0 if "LYD" in selected_r_row['currency'] else 1)
                    
                rec_c4, rec_c5 = st.columns(2)
                with rec_c4: 
                    edit_r_date = st.text_input("تاريخ القيد المالي (صيغة YYYY-MM-DD):", value=selected_r_row['receipt_date'])
                with rec_c5: 
                    edit_r_notes = st.text_input("ملاحظات / رقم الإيصال اليدوي والمستند:", value=selected_r_row['notes'])
                    
                b1, b2 = st.columns(2)
                with b1:
                    if st.form_submit_button("💾 حفظ تعديلات الإيصال وتأكيد المزامنة"):
                        conn = get_db_connection()
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    'UPDATE receipts SET amount=%s, currency=%s, receipt_date=%s, notes=%s WHERE id=%s', 
                                    (edit_r_amount, edit_r_curr, parse_any_date(edit_r_date), edit_r_notes.strip(), receipt_id)
                                )
                                conn.commit()
                            st.success("🎉 تم تحديث ومزامنة بيانات الإيصال المالي بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"خطأ في الحفظ السحابي: {e}")
                        finally:
                            conn.close()
                with b2:
                    if st.form_submit_button("🗑️ حذف السند المالي نهائياً"):
                        conn = get_db_connection()
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute("DELETE FROM receipts WHERE id=%s", (receipt_id,))
                                conn.commit()
                            st.success("🚨 تم مسح السند المالي وشطبه بالكامل من الدفاتر السحابية.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"خطأ في الحذف: {e}")
                        finally:
                            conn.close()


# ==============================================================================
# القسم الخامس: إضافة شحنة جديدة يدوياً أو بنسق LCL
# ==============================================================================
elif menu == "➕ إضافة شحنة جديدة (يدوي/LCL)":
    st.title("➕ إضافة بوليصة / شحنة جمركية جديدة يدويًا بدعم الحاويات المتعددة")
    
    conn = get_db_connection()
    try:
        customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    except Exception as e:
        st.error(f"خطأ: {e}")
    finally:
        conn.close()
        
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
            
            # عرض حقول الحاويات ديناميكياً لتوزيع ذكي
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
                    conn = get_db_connection()
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                'INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                                (s_cust, combined_containers_string, s_bl.strip().upper(), s_date.strftime('%Y-%m-%d'), s_do_num.strip(), s_do_val, s_agency, s_final)
                            )
                            conn.commit()
                        st.success("🎉 تم حفظ البوليصة الجمركية الجديدة بنجاح وتم مزامنتها مع الموقف المالي للعميل!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ جراء الحفظ: {e}")
                    finally:
                        conn.close()


# ==============================================================================
# القسم السادس: رفع البيانات من ملفات إكسل بصورة آلية ومطابقة ذكية
# ==============================================================================
elif menu == "📥 رفع ملف إكسل":
    st.title("📥 معالج رفع البيانات تلقائياً وتوطينها من ملف Excel")
    
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
                col_cont = st.selectbox("عمود رقم الحاوية (يقبل حاويات مدمجة بالخلية)", all_cols, index=min(1, len(all_cols)-1))
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
                conn = get_db_connection()
                try:
                    with conn.cursor() as cursor:
                        insert_count, update_count = 0, 0
                        
                        for index, row in df.iterrows():
                            cust_name = str(row[col_cust]).strip()
                            if cust_name == "" or pd.isnull(row[col_cust]): 
                                continue
                                
                            # إدراج اسم الزبون تلقائياً بجدول الحسابات في حال لم يكن مسجلاً سابقاً
                            cursor.execute("INSERT INTO customers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (cust_name,))
                            
                            bl = str(row[col_bl]).strip().upper()
                            raw_date = row[col_date]
                            date_str = parse_any_date(raw_date)
                            
                            new_do_num = str(row[col_donum]).strip()
                            new_do_val = safe_float(row[col_dovald])
                            new_agency = safe_float(row[col_agency])
                            new_final = safe_float(row[col_final])
                            
                            raw_containers = str(row[col_cont]).strip()
                            # تكسير وفصل الحاويات الجارية المكتوبة بنص واحد عبر المعالج الذكي
                            container_list = re.split(r'[,/؛;\s\n]+', raw_containers)
                            container_list = [c.strip().upper() for c in container_list if c.strip()]
                            
                            if not container_list: 
                                container_list = [""]
                                
                            for container in container_list:
                                # فحص وجود الشحنة مسبقاً لمنع التكرار وتحديثها إن وجدت
                                cursor.execute("SELECT id FROM shipments WHERE container_number = %s AND bl_number = %s", (container, bl))
                                existing = cursor.fetchone()
                                
                                if existing:
                                    cursor.execute(
                                        'UPDATE shipments SET customer_name=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                        (cust_name, date_str, new_do_num, new_do_val, new_agency, new_final, existing['id'])
                                    )
                                    update_count += 1
                                else:
                                    cursor.execute(
                                        'INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                                        (cust_name, container, bl, date_str, new_do_num, new_do_val, new_agency, new_final)
                                    )
                                    insert_count += 1
                                    
                        conn.commit()
                        st.success(f"🎉 تكللت عملية التوطين السحابي بالنجاح الملوكي! تم إدراج {insert_count} بوليصة جديدة وتحديث {update_count} بوليصة جارية.")
                except Exception as e:
                    st.error(f"❌ حدث خطأ غير متوقع أثناء الدمج السحابي للبيانات: {e}")
                finally:
                    conn.close()
        except Exception as e:
            st.error(f"❌ حدث خطأ فني أثناء قراءة ومعالجة بنية ملف الإكسل: {e}")


# ==============================================================================
# القسم السابع: إدارة وتحديث أسماء وحسابات الزبائن (CRM)
# ==============================================================================
elif menu == "👥 إدارة الزبائن":
    st.title("👥 التحكم الكامل والرقابة في قائمة وحسابات زبائن الشركة")
    
    conn = get_db_connection()
    try:
        tab1, tab2, tab3 = st.tabs(["➕ إضافة زبون جديد لحسابات الشركة", "✏️ تعديل ومطابقة اسم حساب جاري", "❌ حذف وتصفية حساب زبون"])
        
        with tab1:
            new_cust = st.text_input("أدخل الاسم الكامل للزبون أو الكيان التجاري:")
            if st.button("تأكيد تسجيل وإدراج العميل"):
                if new_cust.strip():
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute("INSERT INTO customers (name) VALUES (%s)", (new_cust.strip(),))
                            conn.commit()
                        st.success("🎉 تم تسجيل الزبون بنجاح بجدول الحسابات الرسمي!")
                        st.rerun()
                    except Exception:
                        st.error("⚠️ خطأ: هذا الزبون أو الحساب مسجل مسبقاً بقاعدة البيانات.")
                else:
                    st.error("❌ لا يمكن ترك حقل الاسم فارغاً.")
                    
        with tab2:
            customers = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
            if not customers.empty:
                cust_to_edit = st.selectbox("اختر حساب الزبون المراد تعديل مسماه بالكامل:", customers['name'])
                new_name = st.text_input("أدخل الاسم الجديد المصحح والمطابق:")
                if st.button("تأكيد تعديل ومزامنة المسمى بجميع الجداول"):
                    if new_name.strip():
                        try:
                            with conn.cursor() as cursor:
                                # تعديل الاسم بجدول العملاء وجدول الحاويات وجدول الإيصالات للمحافظة على تماسك البيانات ورابطة العزل
                                cursor.execute("UPDATE customers SET name = %s WHERE name = %s", (new_name.strip(), cust_to_edit))
                                cursor.execute("UPDATE shipments SET customer_name = %s WHERE customer_name = %s", (new_name.strip(), cust_to_edit))
                                cursor.execute("UPDATE receipts SET customer_name = %s WHERE customer_name = %s", (new_name.strip(), cust_to_edit))
                                conn.commit()
                            st.success("🎉 تم تعديل الاسم المالي ومزامنة كافة السجلات التابعة للعميل بنجاح!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"خطأ أثناء التعديل: {e}")
            else:
                st.info("لا توجد حسابات زبائن حالياً.")
                
        with tab3:
            if not customers.empty:
                cust_to_del = st.selectbox("اختر اسم حساب العميل لإزالته وشطب سجلاته نهائياً:", customers['name'])
                st.warning(f"🚨 تحذير: هذا الخيار سيقوم بحذف حساب [{cust_to_del}] بالكامل وشطب كافة حاوياته وإيصالاته التابعة من النظام!")
                if st.button("موافق، تأكيد الحذف النهائي والنهائي"):
                    try:
                        with conn.cursor() as cursor:
                            cursor.execute("DELETE FROM customers WHERE name = %s", (cust_to_del,))
                            cursor.execute("DELETE FROM shipments WHERE customer_name = %s", (cust_to_del,))
                            cursor.execute("DELETE FROM receipts WHERE customer_name = %s", (cust_to_del,))
                            conn.commit()
                        st.success(f"🚨 تم مسح وإغلاق حساب [{cust_to_del}] مع كافة قيوده المالية نهائياً.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"خطأ أثناء الحذف: {e}")
            else:
                st.info("لا توجد حسابات زبائن حالياً.")
    finally:
        conn.close()


# ==============================================================================
# القسم الثامن: محرك البحث المتقدم والتحكم الفردي في الشحنات
# ==============================================================================
elif menu == "📝 تعديل وحذف الشحنات":
    st.title("📝 محرك البحث المتقدم والتحكم الفردي والميداني في الحاويات والشحنات")
    
    conn = get_db_connection()
    try:
        shipments = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    except Exception as e:
        st.error(f"خطأ: {e}")
    finally:
        conn.close()
        
    if shipments.empty:
        st.info("ℹ️ لا توجد شحنات مسجلة بالدفاتر حالياً.")
    else:
        search_query = st.text_input("🔍 صندوق البحث الذكي (ابحث برقم الحاوية، رقم البوليصة، أو اسم حساب الزبون):")
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
                    edit_cust = st.text_input("اسم حساب العميل المرتبط (مغلق ومحمي)", value=selected_row['customer_name'], disabled=True)
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
                        conn = get_db_connection()
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    'UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                    (edit_cont.strip().upper(), edit_bl.strip().upper(), parse_any_date(edit_date), edit_do_num.strip(), edit_do_val, edit_agency, edit_final, shipment_id)
                                )
                                conn.commit()
                            st.success("🎉 تم تعديل وحفظ بيانات الشحنة بنجاح بالمخدم السحابي!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"حدث خطأ جراء التعديل: {e}")
                        finally:
                            conn.close()
                with b2:
                    if st.form_submit_button("🗑️ حذف وإلغاء هذه الشحنة تماماً"):
                        conn = get_db_connection()
                        try:
                            with conn.cursor() as cursor:
                                cursor.execute("DELETE FROM shipments WHERE id=%s", (shipment_id,))
                                conn.commit()
                            st.success("🚨 تم حذف البوليصة والشحنة بالكامل وبصورة لا رجعة فيها.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"خطأ أثناء الحذف الفردي: {e}")
                        finally:
                            conn.close()


# ==============================================================================
# القسم التاسع: شطب وتصفير كافة محتويات قاعدة البيانات أو أرصدة عميل محدد
# ==============================================================================
elif menu == "🗑️ مسح البيانات دفعة واحدة":
    st.title("🗑️ محرك تصفير المنظومة والشطب المجمع لقاعدة البيانات")
    
    conn = get_db_connection()
    try:
        customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
        tab1, tab2 = st.tabs(["👤 مسح وحذف الحاويات التابعة لعميل معين", "💥 تصفير كلي ونهائي للنظام"])
        
        with tab1:
            if customers_df.empty:
                st.info("لا توجد حسابات مسجلة حالياً.")
            else:
                target_cust = st.selectbox("اختر اسم حساب العميل المراد إزالة شحناته بالكامل:", customers_df['name'], key="bulk_del_select")
                
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, container_number, bl_number, do_number FROM shipments WHERE customer_name = %s", (target_cust,))
                    cust_shipments = cursor.fetchall()
                    
                if not cust_shipments:
                    st.info(f"لا توجد حالياً أي حاويات جارية أو شحنات مسجلة باسم الزبون [{target_cust}].")
                else:
                    shipment_options = {f"📦 حاوية: {r['container_number']} | بوليصة: {r['bl_number']} | إذن رقم: {r['do_number']}": r['id'] for r in cust_shipments}
                    select_all = st.checkbox("🔄 تحديد وتظليل كافة حاويات هذا العميل المسجلة أعلاه")
                    default_selection = list(shipment_options.keys()) if select_all else []
                    
                    selected_labels = st.multiselect("اختر الشحنات المستهدفة بالشطب والإزالة الكلية:", options=list(shipment_options.keys()), default=default_selection)
                    
                    if selected_labels:
                        confirm_word = st.text_input("لتأكيد تنفيذ عملية الشطب المحددة، اكتب كلمة (حذف) صراحة أدناه:")
                        if st.button("🗑️ تنفيذ تصفية وحذف الحاويات المحددة"):
                            if confirm_word.strip() == "حذف":
                                ids_to_delete = [shipment_options[lbl] for lbl in selected_labels]
                                placeholders = ', '.join(['%s'] * len(ids_to_delete))
                                
                                with conn.cursor() as cursor:
                                    cursor.execute(f"DELETE FROM shipments WHERE id IN ({placeholders})", ids_to_delete)
                                    conn.commit()
                                st.success("🚨 تم شطب ومسح الحاويات المحددة للعميل بنجاح!")
                                st.rerun()
                            else:
                                st.error("❌ الكلمة التأكيدية غير صحيحة.")
                                
        with tab2:
            st.warning("⚠️ خطر للغاية! هذا القسم يقوم بمسح المنظومة بالكامل والعودة للصفر وتصفير كافة سجلات الزبائن والتحصيلات المالية!")
            clear_financials = st.checkbox("الموافقة على مسح وتصفير كافة إيصالات الخزينة وسجل أسماء الزبائن أيضاً")
            confirm_all = st.text_input("لتأكيد التصفير السحابي المجمع والشامل، اكتب العبارة التأكيدية (Core-Reset) أدناه:")
            
            if st.button("💥 بدء التصفير الشامل والنهائي لقواعد البيانات"):
                if confirm_all == "Core-Reset":
                    with conn.cursor() as cursor:
                        cursor.execute("TRUNCATE TABLE shipments RESTART IDENTITY")
                        if clear_financials:
                            cursor.execute("TRUNCATE TABLE receipts RESTART IDENTITY")
                            cursor.execute("TRUNCATE TABLE customers RESTART IDENTITY")
                        conn.commit()
                    st.success("💥 تم تصفير قاعدة البيانات السحابية بالكامل وتجهيزها للبدء من جديد بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ العبارة التأكيدية غير متطابقة.")
    finally:
        conn.close()
