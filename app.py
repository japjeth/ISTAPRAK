import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import plotly.graph_objects as go

# ----------------- 1. إعدادات المنظومة الرسمية -----------------
st.set_page_config(page_title="إستبرق الدولية - منظومة إدارة الشحنات والمالية", layout="wide", initial_sidebar_state="expanded")

# ----------------- 2. حزمة التنسيق المتقدم والطباعة العمودية الممتدة A4 -----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap');
html, body, [data-testid="stSidebar"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #f8f9fa; }
.stHeading, .stMarkdown, p, div, label, span { text-align: right; direction: rtl; }

/* بطاقات المؤشرات المالية والتحليلات KPI Cards */
.analytics-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 25px; direction: rtl; }
.analytics-card { flex: 1; min-width: 240px; background: #ffffff; padding: 24px; border-radius: 8px; border-top: 4px solid #1e4620; box-shadow: 0 4px 12px rgba(0,0,0,0.02); }
.analytics-card h4 { margin: 0 0 10px 0; color: #7f8c8d; font-size: 14px; font-weight: 600; }
.analytics-card p { margin: 0; font-size: 24px; font-weight: 700; color: #1e4620; }

/* 📊 جداول البيانات الجمركية المفرودة RTL على الشاشة */
.enterprise-table-container { width: 100%; overflow-x: auto; direction: rtl; margin: 20px 0; border-radius: 8px; border: 1px solid #e2e8f0; background: #ffffff; }
table.corporate-data-table { width: 100%; border-collapse: collapse; direction: rtl; text-align: right; }
table.corporate-data-table th { background-color: #1e4620; color: #ffffff; padding: 14px 18px; font-weight: 600; font-size: 14px; border-bottom: 2px solid #143316; white-space: nowrap; text-align: right; }
table.corporate-data-table td { padding: 12px 18px; text-align: right; border-bottom: 1px solid #edf2f7; color: #2d3748; font-size: 14px; font-weight: 500; white-space: nowrap; }
table.corporate-data-table tr:nth-child(even) { background-color: #f7fafc; }
table.corporate-data-table tr:hover { background-color: #f0f4f1; }

/* 📜 وثيقة كشف الحساب المعتمدة الجاهزة للطباعة العمودية لعدة صفحات دون انقطاع */
.official-invoice-document { background-color: #ffffff !important; padding: 40px; border: 1px solid #1e4620; border-radius: 6px; direction: rtl; text-align: right; margin-top: 30px; color: #000000 !important; }
.invoice-corporate-header { text-align: center; border-bottom: 3px double #1e4620; padding-bottom: 15px; margin-bottom: 25px; }
.invoice-corporate-header h2 { color: #1e4620 !important; font-weight: 700; margin: 0; font-size: 24px; text-align: center; }
.invoice-meta-data { width: 100%; margin-bottom: 20px; font-size: 14px; color: #000000 !important; }
.invoice-meta-data td { padding: 5px; border: none !important; }

table.invoice-records-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; color: #000000 !important; }
table.invoice-records-table th { background-color: #f2f2f2 !important; color: #1e4620 !important; border: 1px solid #000000 !important; padding: 11px; font-weight: bold; text-align: right; }
table.invoice-records-table td { border: 1px solid #000000 !important; padding: 11px; text-align: right; color: #000000 !important; font-weight: 500; }

.invoice-summary-box { margin-top: 30px; padding: 18px; background-color: #fcfcf9; border: 1px solid #000000; border-radius: 6px; color: #000000 !important; }
.invoice-signatures-block { margin-top: 60px; width: 100%; display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; color: #000000 !important; }

/* 🖨️ محرك الرقابة الجمركي للطباعة العمودية الصارمة: تحرير تدفق الصفحات وحظر شوائب الموقع */
@media print {
    @page { size: A4 portrait; margin: 20mm 15mm; }
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stElementToolbar"],
    div.stButton, div.stForm, div.stSelectbox, div.stMultiSelect, div.stRadio, .stExpander, .print-instruction, .enterprise-table-container, .analytics-container, .no-print {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    [data-testid="stAppViewContainer"], .main, .block-container, [data-testid="stVerticalBlock"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        display: block !important;
        overflow: visible !important;
        height: auto !important;
    }
    .official-invoice-document {
        display: block !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        direction: rtl !important;
        overflow: visible !important;
        height: auto !important;
    }
    table.invoice-records-table { page-break-inside: auto !important; width: 100% !important; }
    table.invoice-records-table tr { page-break-inside: avoid !important; page-break-after: auto !important; }
    thead { display: table-header-group !important; }
}
</style>
""", unsafe_allow_html=True)

# ----------------- 3. إدارة الاتصال بقاعدة البيانات السحابية -----------------
def get_db_connection():
    try:
        db_url = st.secrets["postgres"]["url"]
        return psycopg2.connect(db_url, cursor_factory=DictCursor)
    except Exception as e:
        st.error(f"🔴 خطأ في الاتصال بقاعدة البيانات السحابية: {e}")
        st.stop()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE)')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shipments (
            id SERIAL PRIMARY KEY, customer_name TEXT, container_number TEXT,
            bl_number TEXT, shipment_date TEXT, do_number TEXT, do_value_lyd DOUBLE PRECISION,
            agency_freight_usd DOUBLE PRECISION, final_freight_usd DOUBLE PRECISION
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id SERIAL PRIMARY KEY, customer_name TEXT, amount DOUBLE PRECISION,
            currency TEXT, receipt_date TEXT, notes TEXT
        )
    ''')
    conn.commit()
    cursor.close(); conn.close()

init_db()

def safe_float(val):
    if pd.isnull(val): return 0.0
    try: return float(val)
    except: return 0.0

def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='كشف الحساب الجاري')
    return output.getvalue()

# دالة رندرة جداول الـ HTML المفرودة RTL لمنع مشاكل وانكماش الـ Canvas الافتراضي
def render_enterprise_html_grid(df, show_internal_profit=False):
    headers = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)"]
    if show_internal_profit:
        headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
        
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    tr_html = ""
    for _, row in df.iterrows():
        tr_html += "<tr>"
        tr_html += f"<td>{row['customer_name']}</td>"
        tr_html += f"<td>{row['bl_number']}</td>"
        tr_html += f"<td>{row['container_number']}</td>"
        tr_html += f"<td>{row['shipment_date']}</td>"
        tr_html += f"<td>{row['do_number']}</td>"
        tr_html += f"<td>{row['do_value_lyd']:,.2f} د.ل</td>"
        tr_html += f"<td>${row['final_freight_usd']:,.2f}</td>"
        if show_internal_profit:
            tr_html += f"<td>${row['agency_freight_usd']:,.2f}</td>"
            tr_html += f"<td>${row['profit_usd']:,.2f}</td>"
        tr_html += "</tr>"
        
    st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)

# ----------------- القائمة الجانبية الاحترافية -----------------
st.sidebar.markdown("<h2 style='text-align: center; color: #1e4620; font-weight:700;'>🚢 إستبرق الدولية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4caf50;'>🌐 نظام الرقابة والتحليل المالي</p>", unsafe_allow_html=True)
st.sidebar.write("---")
menu = st.sidebar.radio("قائمة تحكم المنظومة:", [
    "📊 لوحة التحكم والتقارير", 
    "⚠️ الحاويات غير المكتملة", 
    "💰 إيصالات القبض والمالية",
    "✏️ تعديل وحذف الإيصالات",
    "➕ إضافة شحنة جديدة (يدوي/LCL)",
    "📥 رفع ملف إكسل", 
    "👥 إدارة الزبائن", 
    "📝 تعديل وحذف الشحنات",
    "🗑️ مسح البيانات دفعة واحدة"
])

# ==================== 📊 لوحة التحكم والتقارير المحدثة بالكامل من الصفر ====================
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 مركز إدارة ومراقبة الأداء المالي اللوجستي")
    
    st.markdown("""
    <div class='print-instruction' style='background-color: #e8f5e9; padding: 15px; border-right: 5px solid #2e7d32; border-radius: 8px; margin-bottom: 15px;'>
    💡 <b>إرشادات الطباعة الرسمية:</b> قم بتحديد الفلاتر المطلوبة بالأسفل، ثم اضغط على زر <b>"🖨️ توليد مستند كشف الحساب للطباعة"</b>، ثم اضغط على <b>Ctrl + P</b> من لوحة المفاتيح. سيقوم النظام أوتوماتيكياً بتقسيم الجداول الممتدة على عدة صفحات عمودية A4 Portrait دون أي نقص أو تشويه.
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty:
        st.warning("لا توجد بيانات مسجلة في قاعدة البيانات حالياً.")
    else:
        # حساب وعرض الكتل المالية الكلية للشركة Dashboard KPIs
        t_cont = len(shipments_all)
        t_lyd = shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0
        t_usd = shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
        
        st.markdown(f"""
        <div class="analytics-container">
            <div class="analytics-card"><h4>📦 حجم الشحنات والحاويات المعالجة</h4><p>{t_cont} شحنة جارية</p></div>
            <div class="analytics-card"><h4>💵 إجمالي ذمم أوامر التسليم</h4><p>{t_lyd:,.2f} د.ل</p></div>
            <div class="analytics-card"><h4>💵 إجمالي مطلوب نولون الشحن الدولي</h4><p>${t_usd:,.2f}</p></div>
        </div>
        """, unsafe_allow_html=True)
        
        # محرك الفرز والاستخراج المطور
        with St_expander if 'St_expander' in locals() else st.expander("⚙️ محرك تحديد نطاق وهيكلية كشوفات الحساب", expanded=True):
            c_filter1, f_col2, f_col3 = st.columns(3)
            with c_filter1:
                report_scope = st.radio("1. نطاق البحث المالي:", ["كافة الحسابات الكلية", "حساب عميل محدد"], horizontal=True)
            with f_col2:
                report_structure = st.radio("2. هيكلية بيان المستند:", ["كشف مالي إجمالي مجمع", "تقرير سجل تفصيلي"], horizontal=True)
            with f_col3:
                display_profit = st.checkbox("إظهار قيم التكلفة الداخية وصافي الأرباح", value=False)
                
            st.write("---")
            if report_scope == "حساب عميل محدد":
                target_customer = st.selectbox("🎯 اختر اسم حساب الزبون المستهدف بالفرز:", customers_df['name'].tolist())
            else:
                target_customer = "الكل"

        st.write("---")

        df_export_target = pd.DataFrame()
        
        if report_scope == "كافة الحسابات الكلية":
            if report_structure == "كشف مالي إجمالي مجمع":
                st.subheader("📋 كشف أرصاد الموقف المالي العام لكافة عملاء الشركة")
                global_summary = []
                for cust in customers_df['name']:
                    cust_s = shipments_all[shipments_all['customer_name'] == cust]
                    cust_r = receipts_all[receipts_all['customer_name'] == cust]
                    r_lyd = cust_s['do_value_lyd'].sum() if not cust_s.empty else 0.0
                    r_usd = cust_s['final_freight_usd'].sum() if not cust_s.empty else 0.0
                    p_lyd = cust_r[cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not cust_r.empty else 0.0
                    p_usd = cust_r[cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not cust_r.empty else 0.0
                    
                    global_summary.append({
                        "customer_name": cust, "total_containers": len(cust_s), 
                        "required_lyd": r_lyd, "paid_lyd": p_lyd, "remaining_lyd": r_lyd - p_lyd, 
                        "required_usd": r_usd, "paid_usd": p_usd, "remaining_usd": r_usd - p_usd
                    })
                df_export_target = pd.DataFrame(global_summary)
                
                # رندرة جدول الإجمالي العام الموحد والمحمي تماماً ضد الـ KeyError
                th_html = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                tr_html = ""
                for _, r in df_export_target.iterrows():
                    tr_html += f"<tr><td>{r['customer_name']}</td><td>{r['total_containers']}</td><td>{r['required_lyd']:,.2f} د.ل</td><td>{r['paid_lyd']:,.2f} د.ل</td><td style='color:red; font-weight:bold;'>{r['remaining_lyd']:,.2f} د.ل</td><td>${r['required_usd']:,.2f}</td><td>${r['paid_usd']:,.2f}</td><td style='color:red; font-weight:bold;'>${r['remaining_usd']:,.2f}</td></tr>"
                st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)
                
                # استخدام مكتبة Plotly المتطورة للتحليلات الرسومية
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df_export_target['customer_name'], y=df_export_target['remaining_lyd'], name='المتبقي بالدينار د.ل', marker_color='#1e4620'))
                fig.update_layout(title='📈 ميزان الأرصاد المعلقة والذمم المالية الجارية للزبائن أونلاين', template='plotly_white', font=dict(family="Cairo"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.subheader("📋 كشف سجل الشحنات التفصيلي الشامل لكافة الزبائن")
                df_export_target = shipments_all.copy()
                df_export_target['profit_usd'] = df_export_target['final_freight_usd'] - df_export_target['agency_freight_usd']
                render_enterprise_html_grid(df_export_target, show_internal_profit=display_profit)
        else:
            # فرز حساب عميل محدد فردي
            df_cust_s = shipments_all[shipments_all['customer_name'] == target_customer].copy()
            df_cust_r = receipts_all[receipts_all['customer_name'] == target_customer]
            r_lyd = df_cust_s['do_value_lyd'].sum() if not df_cust_s.empty else 0.0
            r_usd = df_cust_s['final_freight_usd'].sum() if not df_cust_s.empty else 0.0
            p_lyd = df_cust_r[df_cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not df_cust_r.empty else 0.0
            p_usd = df_cust_r[df_cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not df_cust_r.empty else 0.0
            
            if report_structure == "كشف مالي إجمالي مجمع":
                st.subheader(f"📋 الموقف والملخص المالي الإجمالي لحساب: {target_customer}")
                k1, k2 = st.columns(2)
                with k1:
                    st.markdown(f"""<div class='metric-card' style='border-right-color: #2196f3;'>
                        <h5>💵 ذمم حساب أوامر التسليم (دينار ليبي):</h5>
                        <p>إجمالي المطلوب: <b>{r_lyd:,.2f} د.ل</b> | المدفوع: <b style='color:green;'>{p_lyd:,.2f} د.ل</b></p>
                        <p>المتبقي بذمته جاري: <b style='color:red;'>{r_lyd - p_lyd:,.2f} د.ل</b></p>
                    </div>""", unsafe_allow_html=True)
                with k2:
                    st.markdown(f"""<div class='metric-card' style='border-right-color: #4caf50;'>
                        <h5>💵 مطلوب حساب نولون الشحن الدولي (دولار أمريكي):</h5>
                        <p>إجمالي المطلوب: <b>${r_usd:,.2f}</b> | المدفوع: <b style='color:green;'>${p_usd:,.2f}</b></p>
                        <p>المتبقي بذمته جاري: <b style='color:red;'>${r_usd - p_usd:,.2f}</b></p>
                    </div>""", unsafe_allow_html=True)
                df_export_target = pd.DataFrame([{"اسم الزبون": target_customer, "المطلوب (د.ل)": r_lyd, "المدفوع (د.ل)": p_lyd, "المتبقي (د.ل)": r_lyd-p_lyd, "الشحن ($)": r_usd, "المدفوع ($)": p_usd, "المتبقي ($)": r_usd-p_usd}])
            else:
                st.subheader(f"📋 سجل الحاويات التفصيلي المفتوح لحساب: {target_customer}")
                df_cust_s['profit_usd'] = df_cust_s['final_freight_usd'] - df_cust_s['agency_freight_usd']
                df_export_target = df_cust_s.copy()
                render_enterprise_html_grid(df_export_target, show_internal_profit=display_profit)

        # محرك التصدير لملفات Excel الجاهزة والمعتمدة
        if not df_export_target.empty:
            st.write("")
            st.download_button(label="📥 تصدير وتحميل كشف الحساب النشط بصيغة Excel", data=to_excel(df_export_target), file_name=f"istabraq_statement_{datetime.now().strftime('%Y%m%d')}.xlsx")

        # ==================== 🖨️ محرك بناء مستندات الطباعة العمودية المتعددة الصفحات A4 Portrait ====================
        st.write("---")
        st.markdown("### 🖨️ محرك توليد وتصديق مستندات كشوفات الحساب الرسمية:")
        
        btn_print_trigger = st.button("🖨️ توليد واعتماد مستند كشف الحساب للطباعة")
        
        if btn_print_trigger:
            st.success("🎉 تم معالجة وتوليد مستند كشف الحساب بنجاح! اضغط الآن من لوحة المفاتيح على Ctrl + P لبدء الطباعة الفورية المتعددة الصفحات.")
            
            # احتساب مجاميع كشف الحساب المستخرج حالياً
            if report_structure == "كشف مالي إجمالي مجمع" and report_scope == "كافة الحسابات الكلية":
                p_total_lyd = df_export_target['required_lyd'].sum()
                p_total_usd = df_export_target['required_usd'].sum()
                
                rows_html_p = ""
                for _, r in df_export_target.iterrows():
                    rows_html_p += f"<tr><td>{r['customer_name']}</td><td>{r['total_containers']}</td><td>{r['required_lyd']:,.2f} د.ل</td><td>{r['paid_lyd']:,.2f} د.ل</td><td>{r['remaining_lyd']:,.2f} د.ل</td><td>${r['required_usd']:,.2f}</td><td>${r['paid_usd']:,.2f}</td><td>${r['remaining_usd']:,.2f}</td></tr>"
                    
                table_headers = "<th>اسم الزبون</th><th>عدد الحاويات</th><th>المطلوب (د.ل)</th><th>المدفوع (د.ل)</th><th>المتبقي (د.ل)</th><th>الشحن ($)</th><th>المدفوع ($)</th><th>المتبقي ($)</th>"
                doc_type_text = "كشف ميزان الأرصاد الإجمالي لكافة العملاء"
            else:
                p_total_lyd = df_export_target['do_value_lyd'].sum()
                p_total_usd = df_export_target['final_freight_usd'].sum()
                
                rows_html_p = ""
                for _, r in df_export_target.iterrows():
                    agency_td_p = f"<td>${r['agency_freight_usd']:,.2f}</td>" if display_profit else ""
                    profit_td_p = f"<td>${r['profit_usd']:,.2f}</td>" if display_profit else ""
                    rows_html_p += f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f} د.ل</td><td>${r['final_freight_usd']:,.2f}</td>{agency_td_p}{profit_td_p}</tr>"
                    
                th_agency_print = "<th>شحن الوكالة</th>" if display_profit else ""
                th_profit_print = "<th>صافي الربح</th>" if display_profit else ""
                table_headers = f"<th>اسم الزبون</th><th>رقم البوليصة</th><th>رقم الحاوية</th><th>التاريخ</th><th>رقم أمر التسليم</th><th>قيمة أمر التسليم</th><th>الشحن النهائي</th>{th_agency_print}{th_profit_print}"
                doc_type_text = "كشف سجل الحاويات التفصيلي المعتمد"

            # قالب الوثيقة الرسمية الصارم والجاهز للتدفق عبر عدد لا نهائي من الصفحات بدون قطع
            html_document_payload = "<div class='official-print-document'>"
            html_document_payload += "<div class='document-corporate-header'><h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1><p style='margin:5px 0 0 0; color:#444; font-size:14px;'>مصراتة - ليبيا | قسم الحسابات والرقابة المالية المركزية</p></div>"
            html_document_payload += "<table class='document-meta-table'>"
            html_document_payload += f"<tr><td><b>الحساب الجاري المستخرج:</b> {target_customer if report_scope == 'حساب عميل محدد' else 'كافة عملاء الحسابات الكلية'}</td><td style='text-align: left;'><b>تاريخ استخراج الوثيقة:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td></tr>"
            html_document_payload += f"<tr><td><b>تصنيف الوثيقة المعتمدة:</b> {doc_type_text}</td><td style='text-align: left;'><b>حصر عدد السجلات المدرجة:</b> {len(df_export_target)} سجل جاري مصفى</td></tr>"
            html_document_payload += "</table>"
            html_document_payload += f"<table class='document-items-table'><thead><tr>{table_headers}</tr></thead><tbody>{rows_html_p}</tbody></table>"
            html_document_payload += "<div class='document-totals-box'>"
            html_document_payload += f"<div style='width:100%; text-align:left; font-size:16px; margin-bottom:8px; color:#000;'><b>إجمالي ذمم أوامر التسليم الكلية المستحقة:</b> {p_total_lyd:,.2f} دينار ليبي</div>"
            html_document_payload += f"<div style='width:100%; text-align:left; font-size:16px; color:#000;'><b>إجمالي مطلوب نولون الشحن الدولي المستحق:</b> ${p_total_usd:,.2f} دولار أمريكي</div>"
            html_document_payload += "</div>"
            html_document_payload += "<div class='document-signatures-area'><div>توقيع واعتماد الإدارة المادية: .........................</div><div>خِتم وتصديق الشركة الرسمي: .........................</div></div>"
            html_document_payload += "</div>"
            
            st.markdown(html_document_payload, unsafe_allow_html=True)

# ----------------- باقي الأقسام اللوجستية والمالية للمنظومة -----------------
elif menu == "⚠️ الحاويات غير المكتملة":
    st.title("⚠️ محرك فحص وتحديد البيانات الناقصة في الحاويات")
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments", conn)
    conn.close()
    if shipments_all.empty: st.info("لا توجد شحنات.")
    else:
        with st.expander("🔍 خيارات تصفية نوع النقص الحسابي", expanded=True):
            fc1, fc2 = st.columns(2)
            with fc1: filter_cust = st.selectbox("تصفية لحساب زبون معين:", ["كل الزبائن"] + list(customers_df['name']))
            with fc2: missing_type = st.selectbox("نوع البيان المفقود المستهدف:", ["أي بيان ناقص بالكامل", "قيمة الشحن النهائي ناقصة", "قيمة أمر التسليم ناقصة"])
        df_filtered = shipments_all.copy()
        if filter_cust != "كل الزبائن": df_filtered = df_filtered[df_filtered['customer_name'] == filter_cust]
        if missing_type == "أي بيان ناقص بالكامل":
            cond = ((df_filtered['container_number'].isna()) | (df_filtered['container_number'] == "") | (df_filtered['bl_number'].isna()) | (df_filtered['bl_number'] == "") | (df_filtered['do_number'].isna()) | (df_filtered['do_number'] == "") | (df_filtered['do_value_lyd'] == 0) | (df_filtered['do_value_lyd'].isna()) | (df_filtered['final_freight_usd'] == 0) | (df_filtered['final_freight_usd'].isna()))
        elif missing_type == "قيمة الشحن النهائي ناقصة": cond = (df_filtered['final_freight_usd'] == 0) | (df_filtered['final_freight_usd'].isna())
        elif missing_type == "قيمة أمر التسليم ناقصة": cond = (df_filtered['do_value_lyd'] == 0) | (df_filtered['do_value_lyd'].isna())
        df_incomplete = df_filtered[cond].copy()
        if df_incomplete.empty: st.success("🎉 كل البيانات مكتملة ولا يوجد نواقص.")
        else: render_enterprise_html_grid(df_incomplete, show_internal_profit=False)

elif menu == "💰 إيصالات القبض والمالية":
    st.title("💰 إدارة المدفوعات وإيصالات قبض الزبائن")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    if customers_df.empty: st.warning("يرجى إضافة زبائن أولاً لتتمكن من تسجيل إيصالات قبض لهم.")
    else:
        st.subheader("➕ تسجيل إيصال قبض جديد في الخزينة")
        with st.form("receipt_form", clear_on_submit=True):
            rc1, rc2, rc3 = st.columns(3)
            with rc1: r_cust = st.selectbox("قبض من الزبون:", customers_df['name'])
            with rc2: r_amount = st.number_input("المبلغ المدفوع:", min_value=0.0, step=50.0)
            with rc3: r_curr = st.selectbox("العملة:", ["دينار ليبي LYD", "دولار أمريكي USD"])
            rc4, rc5 = st.columns([1, 2])
            with rc4: r_date = st.date_input("تاريخ القبض:", datetime.now())
            with rc5: r_notes = st.text_input("ملاحظات / رقم الإيصال أو الشيك:")
            submit_receipt = st.form_submit_button("💾 حفظ وإدراج الإيصال في الحساب المالي")
            if submit_receipt and r_amount > 0:
                cursor.execute('INSERT INTO receipts (customer_name, amount, currency, receipt_date, notes) VALUES (%s, %s, %s, %s, %s)', 
                               (r_cust, r_amount, r_curr, r_date.strftime('%Y-%m-%d'), r_notes))
                conn.commit(); st.success(f"🎉 تم تسجيل وإدراج المدفوعات بنجاح!")
    cursor.close(); conn.close()

elif menu == "✏️ تعديل وحذف الإيصالات":
    st.title("✏️ التحكم في إيصالات القبض (تعديل / حذف)")
    conn = get_db_connection()
    cursor = conn.cursor()
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    if receipts_all.empty: st.info("لا توجد إيصالات قبض مسجلة حالياً.")
    else:
        search_receipt = st.text_input("🔍 صندوق البحث عن إيصالات القبض:")
        filtered_r = receipts_all.copy()
        if search_receipt.strip():
            sr = search_receipt.strip().lower()
            filtered_r = receipts_all[receipts_all['customer_name'].str.lower().str.contains(sr, na=False) | receipts_all['notes'].str.lower().str.contains(sr, na=False)]
        if filtered_r.empty: st.warning("لم يتم العثور على نتائج.")
        else:
            filtered_r['selector_text'] = filtered_r['customer_name'] + " | مبلغ: " + filtered_r['amount'].astype(str) + " (" + filtered_r['currency'] + ") | ملاحظة: " + filtered_r['notes']
            selected_receipt_opt = st.selectbox("اختر الإيصال الدقيق للتعديل/الحذف:", filtered_r['selector_text'])
            selected_r_row = filtered_r[filtered_r['selector_text'] == selected_receipt_opt].iloc[0]
            receipt_id = int(selected_r_row['id'])
            st.write("---")
            rec_c1, rec_c2, rec_c3 = st.columns(3)
            with rec_c1: edit_r_cust = st.text_input("اسم الزبون", value=selected_r_row['customer_name'], disabled=True)
            with rec_c2: edit_r_amount = st.number_input("المبلغ المعدل", value=float(selected_r_row['amount']))
            with rec_c3: edit_r_curr = st.selectbox("العملة", ["دينار ليبي LYD", "دولار أمريكي USD"], index=0 if "دينار" in selected_r_row['currency'] else 1)
            rec_c4, rec_c5 = st.columns(2)
            with rec_c4: edit_r_date = st.text_input("التاريخ (YYYY-MM-DD)", value=selected_r_row['receipt_date'])
            with rec_c5: edit_r_notes = st.text_input("ملاحظات / رقم الشيك", value=selected_r_row['notes'])
            btn_r1, btn_r2 = st.columns(2)
            with btn_r1:
                if st.button("💾 حفظ تعديلات الإيصال"):
                    cursor.execute('UPDATE receipts SET amount=%s, currency=%s, receipt_date=%s, notes=%s WHERE id=%s', (edit_r_amount, edit_r_curr, edit_r_date, edit_r_notes, receipt_id))
                    conn.commit(); st.success("تم تحديث بيانات الإيصال بنجاح!"); st.rerun()
            with btn_r2:
                if st.button("🗑️ حذف هذا الإيصال نهائياً"):
                    cursor.execute("DELETE FROM receipts WHERE id=%s", (receipt_id,))
                    conn.commit(); st.success("تم حذف إيصال القبض."); st.rerun()
    cursor.close(); conn.close()

elif menu == "➕ إضافة شحنة جديدة (يدوي/LCL)":
    st.title("➕ إضافة حاوية / شحنة جديدة يدوياً")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    if customers_df.empty: st.warning("يجب إضافة زبائن أولاً قبل تسجيل شحنات جديدة.")
    else:
        with st.form("manual_shipment_form", clear_on_submit=True):
            sc1, sc2, sc3 = st.columns(3)
            with sc1: s_cust = st.selectbox("اختر اسم الزبون:", customers_df['name'])
            with sc2: s_container = st.text_input("رقم الحاوية:")
            with sc3: s_bl = st.text_input("رقم البوليصة (أساسي للربط):")
            sc4, sc5, sc6 = st.columns(3)
            with sc4: s_date = st.date_input("تاريخ الاستلام:", datetime.now())
            with sc5: s_do_num = st.text_input("رقم أمر التسليم:")
            with sc6: s_do_val = st.number_input("قيمة أمر التسليم (بالدينار LYD):", min_value=0.0, step=100.0)
            sc7, sc8 = st.columns(2)
            with sc7: s_agency = st.number_input("قيمة شحن الوكالة (بالدولار USD):", min_value=0.0, step=50.0)
            with sc8: s_final = st.number_input("قيمة الشحن النهائي للزبون (بالدولار USD):", min_value=0.0, step=50.0)
            submit_shipment = st.form_submit_button("🚀 إضافة الشحنة وتحديث الحسابات السحابية")
            if submit_shipment and s_container.strip() != "":
                cursor.execute('''
                    INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ''', (s_cust, s_container.strip(), s_bl.strip(), s_date.strftime('%Y-%m-%d'), s_do_num.strip(), s_do_val, s_agency, s_final))
                conn.commit(); st.success(f"🎉 تم حفظ وإضافة الحاوية بنجاح!")
    cursor.close(); conn.close()

elif menu == "📥 رفع ملف إكسل":
    st.title("📥 رفع البيانات مباشرة من ملف Excel")
    uploaded_file = st.file_uploader("اختر ملف الإكسل وارسم أعمدتك:", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("تم تحميل الملف بنجاح!")
            all_cols = list(df.columns)
            c1, c2, c3, c4 = st.columns(4)
            with c1: col_cust = st.selectbox("عمود اسم الزبون", all_cols, index=0)
            with c2: col_cont = st.selectbox("عمود رقم الحاوية", all_cols, index=min(1, len(all_cols)-1))
            with c3: col_bl = st.selectbox("عمود رقم البوليصة", all_cols, index=min(2, len(all_cols)-1))
            with c4: col_date = st.selectbox("عمود التاريخ", all_cols, index=min(3, len(all_cols)-1))
            c5, c6, c7, c8 = st.columns(4)
            with c5: col_donum = st.selectbox("عمود رقم أمر التسليم", all_cols, index=min(4, len(all_cols)-1))
            with c6: col_dovald = st.selectbox("عمود قيمة أمر التسليم (LYD)", all_cols, index=min(5, len(all_cols)-1))
            with c7: col_agency = st.selectbox("عمود شحن الوكالة (USD)", all_cols, index=min(6, len(all_cols)-1))
            with c8: col_final = st.selectbox("عمود الشحن النهائي (USD)", all_cols, index=min(7, len(all_cols)-1))
            
            if st.button("🚀 بدء المعالجة والدمج الذكي بقاعدة البيانات السحابية"):
                conn = get_db_connection()
                cursor = conn.cursor()
                insert_count, update_count = 0, 0
                for index, row in df.iterrows():
                    cust_name = str(row[col_cust]).strip()
                    if cust_name == "" or pd.isnull(row[col_cust]): continue
                    
                    cursor.execute("INSERT INTO customers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (cust_name,))
                    container, bl = str(row[col_cont]).strip(), str(row[col_bl]).strip()
                    raw_date = row[col_date]
                    date_str = raw_date.strftime('%Y-%m-%d') if isinstance(raw_date, (datetime, pd.Timestamp)) else str(raw_date)
                    new_do_num = str(row[col_donum]).strip()
                    new_do_val, new_agency, new_final = safe_float(row[col_dovald]), safe_float(row[col_agency]), safe_float(row[col_final])
                    cursor.execute("SELECT * FROM shipments WHERE customer_name = %s AND container_number = %s AND bl_number = %s", (cust_name, container, bl))
                    existing = cursor.fetchone()
                    if existing:
                        shipment_id = existing['id']
                        updates, params = [], []
                        if (not existing['do_number'] or existing['do_number'] in ["", "None", "nan"]) and new_do_num: updates.append("do_number = %s"); params.append(new_do_num)
                        if (existing['do_value_lyd'] == 0 or pd.isnull(existing['do_value_lyd'])) and new_do_val > 0: updates.append("do_value_lyd = %s"); params.append(new_do_val)
                        if (existing['agency_freight_usd'] == 0 or pd.isnull(existing['agency_freight_usd'])) and new_agency > 0: updates.append("agency_freight_usd = %s"); params.append(new_agency)
                        if (existing['final_freight_usd'] == 0 or pd.isnull(existing['final_freight_usd'])) and new_final > 0: updates.append("final_freight_usd = %s"); params.append(new_final)
                        if updates:
                            params.append(shipment_id)
                            cursor.execute(f"UPDATE shipments SET {', '.join(updates)} WHERE id = %s", params)
                            update_count += 1
                    else:
                        cursor.execute('INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', 
                                       (cust_name, container, bl, date_str, new_do_num, new_do_val, new_agency, new_final))
                        insert_count += 1
                conn.commit(); cursor.close(); conn.close()
                st.success(f"🎉 تمت العملية بنجاح! | 📥 حاويات مضافة: {insert_count} | 🔄 حاويات تم استكمال بياناتها: {update_count}")
        except Exception as e: st.error(f"حدث خطأ أثناء معالجة الملف: {e}")

elif menu == "👥 إدارة الزبائن":
    st.title("👥 التحكم الكامل في قائمة الزبائن")
    conn = get_db_connection()
    cursor = conn.cursor()
    tab1, tab2, tab3 = st.tabs(["➕ إضافة زبون جديد", "✏️ تعديل اسم زبون", "❌ حذف زبون"])
    with tab1:
        new_cust = st.text_input("اسم الزبون الجديد بالكامل:")
        if st.button("إضافة الآن"):
            if new_cust.strip():
                try:
                    cursor.execute("INSERT INTO customers (name) VALUES (%s)", (new_cust.strip(),))
                    conn.commit(); st.success("تم الإضافة بنجاح!"); st.rerun()
                except: st.error("هذا الزبون مسجل بالفعل!")
    with tab2:
        customers = pd.read_sql_query("SELECT * FROM customers", conn)
        if not customers.empty:
            cust_to_edit = st.selectbox("اختر الزبون لتعديل اسمه:", customers['name'])
            new_name = st.text_input("الاسم الجديد المعدل:")
            if st.button("تأكيد تعديل الاسم"):
                if new_name.strip():
                    cursor.execute("UPDATE customers SET name = %s WHERE name = %s", (new_name.strip(), cust_to_edit))
                    cursor.execute("UPDATE shipments SET customer_name = %s WHERE customer_name = %s", (new_name.strip(), cust_to_edit))
                    conn.commit(); st.success("تم التعديل بنجاح!"); st.rerun()
    with tab3:
        if not customers.empty:
            cust_to_del = st.selectbox("اختر الزبون المراد مسحه تماماً:", customers['name'])
            if st.button("موافق، حذف نهائي"):
                cursor.execute("DELETE FROM customers WHERE name = %s", (cust_to_del,))
                cursor.execute("DELETE FROM shipments WHERE customer_name = %s", (cust_to_del,))
                conn.commit(); st.success("تم الحذف."); st.rerun()
    cursor.close(); conn.close()

elif menu == "📝 تعديل وحذف الشحنات":
    st.title("📝 محرك البحث المتقدم وتعديل الحاويات يدوياً")
    conn = get_db_connection()
    cursor = conn.cursor()
    shipments = pd.read_sql_query("SELECT * FROM shipments", conn)
    if shipments.empty: st.info("لا توجد حاويات مسجلة.")
    else:
        search_query = st.text_input("🔍 صندوق البحث الذكي (رقم الحاوية, رقم البوليصة, أو اسم الزبون):")
        filtered_df = shipments.copy()
        if search_query.strip():
            q = search_query.strip().lower()
            filtered_df = shipments[shipments['container_number'].astype(str).str.lower().str.contains(q, na=False) | shipments['customer_name'].astype(str).str.lower().str.contains(q, na=False)]
        if filtered_df.empty: st.warning("لم يتم العثور على أي نتائج.")
        else:
            filtered_df['selector_text'] = filtered_df['customer_name'] + " | حاوية: " + filtered_df['container_number'] + " | بوليصة: " + filtered_df['bl_number']
            selected_option = st.selectbox("اختر الحاوية الدقيقة لبدء التعديل:", filtered_df['selector_text'])
            selected_row = filtered_df[filtered_df['selector_text'] == selected_option].iloc[0]
            shipment_id = int(selected_row['id'])
            st.write("---")
            ec1, ec2, ec3 = st.columns(3)
            with ec1: edit_cust = st.text_input("اسم الزبون", value=selected_row['customer_name'])
            with ec2: edit_cont = st.text_input("رقم الحاوية", value=selected_row['container_number'])
            with ec3: edit_bl = st.text_input("رقم البوليصة", value=selected_row['bl_number'])
            ec4, ec5, ec6 = st.columns(3)
            with ec4: edit_date = st.text_input("التاريخ", value=selected_row['shipment_date'])
            with ec5: edit_do_num = st.text_input("رقم أمر التسليم", value=selected_row['do_number'])
            with ec6: edit_do_val = st.number_input("قيمة أمر التسليم (LYD)", value=float(selected_row['do_value_lyd']))
            ec7, ec8 = st.columns(2)
            with ec7: edit_agency = st.number_input("شحن الوكالة (USD)", value=float(selected_row['agency_freight_usd']))
            with ec8: edit_final = st.number_input("الشحن النهائي للزبون (USD)", value=float(selected_row['final_freight_usd']))
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("💾 حفظ التغييرات السحابية"):
                    cursor.execute('UPDATE shipments SET customer_name=%s, container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                   (edit_cust, edit_cont, edit_bl, edit_date, edit_do_num, edit_do_val, edit_agency, edit_final, shipment_id))
                    conn.commit(); st.success("تم التحديث بنجاح!"); st.rerun()
            with btn_col2:
                if st.button("🗑️ حذف هذه الحاوية تماماً"):
                    cursor.execute("DELETE FROM shipments WHERE id=%s", (shipment_id,))
                    conn.commit(); st.success("تم الحذف."); st.rerun()
    cursor.close(); conn.close()

elif menu == "🗑️ مسح البيانات دفعة واحدة":
    st.title("🗑️ الحذف الانتقائي والذكي للحاويات")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    tab1, tab2 = st.tabs(["👤 حذف حاويات مخصصة لزبون معين", "💥 تصفير ومسح كافة الحاويات بالنظام"])
    with tab1:
        if customers_df.empty: st.info("لا يوجد زبائن.")
        else:
            target_cust = st.selectbox("اختر الزبون لتحديد شحناته وحذفها:", customers_df['name'], key="bulk_del_select")
            cursor.execute("SELECT id, container_number, bl_number, do_number FROM shipments WHERE customer_name = %s", (target_cust,))
            cust_shipments = cursor.fetchall()
            if not cust_shipments: st.info(f"لا توجد حاويات للزبون حالياً.")
            else:
                shipment_options = {f"📦 حاوية: {r['container_number']} | بوليصة: {r['bl_number']}": r['id'] for r in cust_shipments}
                select_all = st.checkbox("🔄 تحديد جميع الحاويات الحالية لـ الزبون المختار")
                default_selection = list(shipment_options.keys()) if select_all else []
                selected_labels = st.multiselect("اختر الحاويات المراد حذفها:", options=list(shipment_options.keys()), default=default_selection)
                if selected_labels:
                    confirm_word = st.text_input("أكتب كلمة 'حذف' لتأكيد الشطب:")
                    if st.button("🗑️ تنفيذ حذف الحاويات المحددة"):
                        if confirm_word == "حذف":
                            ids_to_delete = [shipment_options[lbl] for lbl in selected_labels]
                            placeholders = ', '.join(['%s'] * len(ids_to_delete))
                            cursor.execute(f"DELETE FROM shipments WHERE id IN ({placeholders})", ids_to_delete)
                            conn.commit(); st.success("تم المسح بنجاح!"); st.rerun()
    with tab2:
        clear_financials = st.checkbox("مسح إيصالات القبض وقائمة أسماء الزبائن أيضاً (تصفير شامل للبرنامج)")
        confirm_all = st.text_input("لتأكيد التصفير، اكتب عبارة 'Core-Reset' في الفراغ أدناه:")
        if st.button("💥 بدء التصفير الشامل والنهائي"):
            if confirm_all == "Core-Reset":
                cursor.execute("TRUNCATE TABLE shipments RESTART IDENTITY")
                if clear_financials:
                    cursor.execute("TRUNCATE TABLE receipts RESTART IDENTITY")
                    cursor.execute("TRUNCATE TABLE customers RESTART IDENTITY")
                conn.commit(); st.success("تم تصفير المنظومة بنجاح!"); st.rerun()
    cursor.close(); conn.close()
