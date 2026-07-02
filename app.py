import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import re

st.set_page_config(
    page_title="إستبرق الدولية - منظومة إدارة الشحنات والرقابة المالية",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stSidebar"], .stApp {
    font-family: 'Cairo', sans-serif;
    direction: rtl !important;
    text-align: right !important;
    background-color: #f4f6f9;
    color: #2c3e50;
}

.stHeading, .stMarkdown, p, div, label, span, h1, h2, h3, h4, h5, h6 {
    text-align: right !important;
    direction: rtl !important;
}

.kpi-container {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-bottom: 25px;
    direction: rtl !important;
}
.kpi-card {
    flex: 1;
    min-width: 260px;
    background: #ffffff;
    padding: 24px;
    border-radius: 8px;
    border-top: 4px solid #1e4620;
    box-shadow: 0 4px 12px rgba(0,0,0,0.02);
}
.kpi-card h5 { margin: 0 0 10px 0 !important; color: #7f8c8d !important; font-size: 14px !important; font-weight: 600 !important; }
.kpi-card h2 { margin: 0 !important; font-size: 24px !important; font-weight: 700 !important; color: #1e4620 !important; }
.kpi-card p { margin: 5px 0 0 0 !important; font-size: 12px !important; color: #95a5a6 !important; }

.enterprise-table-container {
    width: 100%;
    overflow-x: auto;
    direction: rtl !important;
    margin: 20px 0;
    border-radius: 8px;
    border: 1px solid #e2e8f0;
    background: #ffffff;
}
table.corporate-data-table {
    width: 100%;
    border-collapse: collapse;
    direction: rtl !important;
    text-align: right !important;
}
table.corporate-data-table th {
    background-color: #1e4620 !important;
    color: #ffffff !important;
    padding: 14px 18px;
    font-weight: 600;
    font-size: 14px;
    border-bottom: 2px solid #143316;
    white-space: nowrap;
    text-align: right !important;
}
table.corporate-data-table td {
    padding: 12px 18px;
    text-align: right !important;
    border-bottom: 1px solid #edf2f7;
    color: #2d3748;
    font-size: 14px;
    font-weight: 500;
    white-space: nowrap;
}
table.corporate-data-table tr:nth-child(even) { background-color: #f7fafc; }
table.corporate-data-table tr:hover { background-color: #f0f4f1; }

div.stButton > button:first-child {
    background-color: #1e4620 !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    width: 100% !important;
    border-radius: 8px !important;
    height: 46px !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
}
div.stButton > button:hover { background-color: #2e7d32 !important; }

.status-badge { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; }
.status-green { background-color: #e8f5e9; color: #2e7d32; }
.status-red { background-color: #ffebee; color: #c62828; }
.status-orange { background-color: #fff3e0; color: #ef6c00; }

/* 📜 حزمة العزل الكلي للطباعة */
.official-print-document { display: none; }

@media print {
    header, footer, [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stElementToolbar"],
    div.stButton, div.stForm, div.stSelectbox, div.stMultiSelect, div.stRadio, .stExpander, .print-instruction,
    .enterprise-table-container, .analytics-container, .no-print, [data-testid="stSidebarUserContent"],
    .kpi-container, iframe, .stTabs, div[data-testid="stMarkdownContainer"] {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stVerticalBlock"] > div { display: none !important; }
    div[data-testid="stVerticalBlock"] > div:has(.official-print-document) { display: block !important; }

    [data-testid="stAppViewContainer"], .main, .block-container, [data-testid="stVerticalBlock"] {
        padding: 0 !important;
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        display: block !important;
        overflow: visible !important;
        height: auto !important;
        background-color: #ffffff !important;
    }

    .official-print-document {
        display: block !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        padding: 15mm 12mm !important;
        direction: rtl !important;
        text-align: right !important;
    }

    @page { size: A4 portrait; margin: 0; }
    table.print-invoice-table { width: 100% !important; border-collapse: collapse !important; margin-top: 25px !important; font-size: 13px !important; }
    table.print-invoice-table th { background-color: #f2f2f2 !important; color: #000000 !important; border: 1px solid #000000 !important; padding: 10px !important; font-weight: bold !important; text-align: right !important; -webkit-print-color-adjust: exact; }
    table.print-invoice-table td { border: 1px solid #000000 !important; padding: 10px !important; text-align: right !important; color: #000000 !important; }
    table.print-invoice-table tr { page-break-inside: avoid !important; page-break-after: auto !important; }
    thead { display: table-header-group !important; }
    
    table.print-totals-table { width: 100% !important; border-collapse: collapse !important; margin-top: 30px !important; page-break-inside: avoid !important; }
    table.print-totals-table th { background-color: #eaeaea !important; border: 1px solid #000000 !important; padding: 12px !important; font-weight: bold !important; text-align: center !important; -webkit-print-color-adjust: exact; }
    table.print-totals-table td { border: 1px solid #000000 !important; padding: 12px !important; text-align: center !important; font-weight: 600 !important; }
    .print-signatures-block { margin-top: 50px !important; width: 100% !important; display: flex !important; justify-content: space-between !important; font-weight: bold !important; page-break-inside: avoid !important; color: #000000 !important; }
}
</style>
""", unsafe_allow_html=True)

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
    cursor.execute("CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id SERIAL PRIMARY KEY, customer_name TEXT, container_number TEXT, bl_number TEXT,
            shipment_date TEXT, do_number TEXT, do_value_lyd DOUBLE PRECISION DEFAULT 0.0,
            agency_freight_usd DOUBLE PRECISION DEFAULT 0.0, final_freight_usd DOUBLE PRECISION DEFAULT 0.0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS receipts (
            id SERIAL PRIMARY KEY, customer_name TEXT, amount DOUBLE PRECISION DEFAULT 0.0,
            currency TEXT, receipt_date TEXT, notes TEXT
        )
    """)
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
        df.to_excel(writer, index=False, sheet_name='كشف الحساب')
    return output.getvalue()

def render_premium_html_grid(df, show_internal_profit=False):
    headers = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)", "مؤشر الربحية"]
    if show_internal_profit: headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    tr_html = ""
    for _, row in df.iterrows():
        profit_indicator = "<span class='status-badge status-green'>مربح</span>"
        if row['final_freight_usd'] < row['agency_freight_usd']: profit_indicator = "<span class='status-badge status-red'>🚨 خسارة</span>"
        elif row['final_freight_usd'] == 0: profit_indicator = "<span class='status-badge status-orange'>غير مسعر</span>"
        tr_html += f"<tr><td>{row['customer_name']}</td><td>{row['bl_number']}</td><td>{row['container_number']}</td><td>{row['shipment_date']}</td><td>{row['do_number']}</td><td>{row['do_value_lyd']:,.2f} د.ل</td><td>${row['final_freight_usd']:,.2f}</td><td>{profit_indicator}</td>"
        if show_internal_profit: tr_html += f"<td>${row['agency_freight_usd']:,.2f}</td><td>${row['profit_usd']:,.2f}</td>"
        tr_html += "</tr>"
    st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align: center; color: #1e4620; font-weight:700;'>🚢 إستبرق الدولية</h2>", unsafe_allow_html=True)
menu = st.sidebar.radio("قائمة تحكم المنظومة:", ["📊 لوحة التحكم والتقارير", "⚠️ الشحنات متأخرة السداد", "💰 إيصالات القبض والمالية", "✏️ تعديل وحذف الإيصالات", "➕ إضافة شحنة جديدة (يدوي/LCL)", "📥 رفع ملف إكسل", "👥 إدارة الزبائن", "📝 تعديل وحذف الشحنات", "🗑️ مسح البيانات دفعة واحدة"])

if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 مركز التقارير والرقابة المالية والموازنات الجارية")
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty: st.warning("لا توجد بيانات مسجلة حالياً.")
    else:
        t_cont, t_lyd, t_usd = len(shipments_all), shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0, shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
        st.markdown(f'<div class="kpi-container"><div class="kpi-card"><h5>📦 حجم الحاويات المعالجة</h5><h2>{t_cont} شحنة جارية</h2></div><div class="kpi-card"><h5>💵 ذمم أوامر التسليم الكلية</h5><h2>{t_lyd:,.2f} د.ل</h2></div><div class="kpi-card"><h5>💵 نولون الشحن الكلي</h5><h2>${t_usd:,.2f}</h2></div></div>', unsafe_allow_html=True)
        
        with st.expander("⚙️ محرك تحديد هيكلية التقارير وعمليات الفرز", expanded=True):
            c_filter1, c_filter2, c_filter3 = st.columns(3)
            with c_filter1: report_scope = st.radio("1. نطاق كشف الحساب:", ["كل زبائن المنظومة", "زبون محدد فردي"])
            with c_filter2: report_structure = st.radio("2. نوع وثيقة الكشف:", ["كشف مالي إجمالي عام", "كشف حساب تفصيلي"])
            with c_filter3: display_profit = st.checkbox("إظهار قيم شحن الوكالة وصافي الأرباح")
            if report_scope == "زبون محدد فردي": target_customer = st.selectbox("🎯 اختر اسم حساب الزبون المستهدف بالفرز المالي:", customers_df['name'].tolist())
            else: target_customer = "الكل"

        df_export_target = pd.DataFrame()
        req_l, paid_l, req_u, paid_u = 0.0, 0.0, 0.0, 0.0
        
        if report_scope == "كل زبائن المنظومة":
            if report_structure == "كشف مالي إجمالي عام":
                st.subheader("📋 كشف ملخص أرصاد الحسابات لجميع الزبائن")
                global_summary = []
                for cust in customers_df['name']:
                    cust_s = shipments_all[shipments_all['customer_name'] == cust]
                    cust_r = receipts_all[receipts_all['customer_name'] == cust]
                    r_lyd_c = cust_s['do_value_lyd'].sum() if not cust_s.empty else 0.0
                    r_usd_c = cust_s['final_freight_usd'].sum() if not cust_s.empty else 0.0
                    p_lyd_c = cust_r[cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not cust_r.empty else 0.0
                    p_usd_c = cust_r[cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not cust_r.empty else 0.0
                    global_summary.append({"customer_name": cust, "total_containers": len(cust_s), "required_lyd": r_lyd_c, "paid_lyd": p_lyd_c, "remaining_lyd": r_lyd_c - p_lyd_c, "required_usd": r_usd_c, "paid_usd": p_usd_c, "remaining_usd": r_usd_c - p_usd_c})
                df_export_target = pd.DataFrame(global_summary)
                th_html = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                tr_html = "".join(f"<tr><td>{r['customer_name']}</td><td>{r['total_containers']}</td><td>{r['required_lyd']:,.2f} د.ل</td><td>{r['paid_lyd']:,.2f} د.ل</td><td style='color:red; font-weight:bold;'>{r['remaining_lyd']:,.2f} د.ل</td><td>${r['required_usd']:,.2f}</td><td>${r['paid_usd']:,.2f}</td><td style='color:red; font-weight:bold;'>${r['remaining_usd']:,.2f}</td></tr>" for _, r in df_export_target.iterrows())
                st.markdown(f'<div class="enterprise-table-container"><table class="corporate-data-table"><thead><tr>{th_html}</tr></thead><tbody>{tr_html}</tbody></table></div>', unsafe_allow_html=True)
                req_l, req_u = shipments_all['do_value_lyd'].sum(), shipments_all['final_freight_usd'].sum()
                paid_l = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD']['amount'].sum()
                paid_u = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD']['amount'].sum()
            else:
                st.subheader("📋 كشف السجل التفصيلي الشامل")
                df_export_target = shipments_all.copy()
                df_export_target['profit_usd'] = df_export_target['final_freight_usd'] - df_export_target['agency_freight_usd']
                render_premium_html_grid(df_export_target, show_internal_profit=display_profit)
                req_l, req_u = df_export_target['do_value_lyd'].sum(), df_export_target['final_freight_usd'].sum()
                paid_l = receipts_all[receipts_all['currency'] == 'دينار ليبي LYD']['amount'].sum()
                paid_u = receipts_all[receipts_all['currency'] == 'دولار أمريكي USD']['amount'].sum()
        else:
            df_cust_s = shipments_all[shipments_all['customer_name'] == target_customer].copy()
            df_cust_r = receipts_all[receipts_all['customer_name'] == target_customer]
            req_l = df_cust_s['do_value_lyd'].sum() if not df_cust_s.empty else 0.0
            req_u = df_cust_s['final_freight_usd'].sum() if not df_cust_s.empty else 0.0
            paid_l = df_cust_r[df_cust_r['currency'] == 'دينار ليبي LYD']['amount'].sum() if not df_cust_r.empty else 0.0
            paid_u = df_cust_r[df_cust_r['currency'] == 'دولار أمريكي USD']['amount'].sum() if not df_cust_r.empty else 0.0
            
            if report_structure == "كشف مالي إجمالي عام":
                st.subheader(f"📋 الموقف المالي لحساب: {target_customer}")
                df_export_target = df_cust_s.copy()
            else:
                st.subheader(f"📋 كشف سجل الحاويات التفصيلي لحساب: {target_customer}")
                df_cust_s['profit_usd'] = df_cust_s['final_freight_usd'] - df_cust_s['agency_freight_usd']
                df_export_target = df_cust_s.copy()
                render_premium_html_grid(df_export_target, show_internal_profit=display_profit)

        if not df_export_target.empty:
            st.download_button(label="📥 تحميل كشف الحساب النشط حالياً بصيغة Excel معتمد", data=to_excel(df_export_target), file_name="istabraq_statement.xlsx")

        st.write("---")
        st.markdown("### 🖨️ وثيقة تصديق ومطابقة كشوفات الحساب الرسمية للطباعة:")
        if st.button("🖨️ تأكيد معالجة وتوليد وثيقة كشف الحساب للطباعة الفورية"):
            rows_html_p = ""
            if report_structure == "كشف مالي إجمالي عام" and report_scope == "كل زبائن المنظومة":
                for _, r in df_export_target.iterrows():
                    rows_html_p += f"<tr><td>{r['customer_name']}</td><td>{r['total_containers']}</td><td>{r['required_lyd']:,.2f} د.ل</td><td>{r['paid_lyd']:,.2f} د.ل</td><td>{r['remaining_lyd']:,.2f} د.ل</td><td>${r['required_usd']:,.2f}</td><td>${r['paid_usd']:,.2f}</td><td>${r['remaining_usd']:,.2f}</td></tr>"
                table_headers = "<th>اسم الزبون</th><th>الحاويات</th><th>المطلوب (د.ل)</th><th>المدفوع (د.ل)</th><th>المتبقي (د.ل)</th><th>الشحن ($)</th><th>المدفوع ($)</th><th>المتبقي ($)</th>"
                doc_type_text = "كشف الأرصاد والموقف المالي الإجمالي المجمع لعملاء الشركة"
            else:
                for _, r in df_export_target.iterrows():
                    agency_td_p = f"<td>${r['agency_freight_usd']:,.2f}</td>" if display_profit else ""
                    profit_td_p = f"<td>${(r['final_freight_usd'] - r['agency_freight_usd']):,.2f}</td>" if display_profit else ""
                    rows_html_p += f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f} د.ل</td><td>${r['final_freight_usd']:,.2f}</td>{agency_td_p}{profit_td_p}</tr>"
                th_agency_print = "<th>شحن الوكالة</th>" if display_profit else ""
                th_profit_print = "<th>صافي الربح</th>" if display_profit else ""
                table_headers = f"<th>اسم الزبون</th><th>رقم البوليصة</th><th>رقم الحاوية</th><th>التاريخ</th><th>رقم أمر التسليم</th><th>قيمة أمر التسليم</th><th>الشحن النهائي</th>{th_agency_print}{th_profit_print}"
                doc_type_text = "كشف سجل الحاويات التفصيلي الجمركي المعتمد والمصفى"

            summary_table_html = f"""
            <table class="print-totals-table">
                <thead><tr><th>العملة والبيان الحسابي للتحصيل الرسمي</th><th>إجمالي القيمة المطلوبة بذمته</th><th>إجمالي القيمة المدفوعة والمستلمة</th><th>صافي الرصيد المتبقي (الجاري)</th></tr></thead>
                <tbody>
                    <tr><td><b>حساب أوامر التسليم والتخليص الجمركي (LYD)</b></td><td>{req_l:,.2f} د.ل</td><td style="color:green;">{paid_l:,.2f} د.ل</td><td style="color:red; font-weight:bold;">{req_l - paid_l:,.2f} د.ل</td></tr>
                    <tr><td><b>حساب نولون وأرصاد الشحن الدولي (USD)</b></td><td>${req_u:,.2f}</td><td style="color:green;">${paid_u:,.2f}</td><td style="color:red; font-weight:bold;">${req_u - paid_u:,.2f}</td></tr>
                </tbody>
            </table>"""

            html_document_payload = f"""
            <div class='official-print-document'>
                <div class='document-corporate-header'><h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1><p>مصراتة - ليبيا | الحسابات المركزية المعتمدة</p></div>
                <table class='document-meta-table'>
                    <tr><td><b>كشف حساب مالي جاري للعميل:</b> {target_customer if report_scope == 'زبون محدد فردي' else 'كافة عملاء المنظومة'}</td><td style='text-align: left;'><b>تاريخ استخراج الوثيقة:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td></tr>
                    <tr><td><b>نوع المستند الجمركي:</b> {doc_type_text}</td><td style='text-align: left;'><b>حصر السجلات المدرجة:</b> {len(df_export_target)} سجل جاري</td></tr>
                </table>
                <table class='print-invoice-table'><thead><tr>{table_headers}</tr></thead><tbody>{rows_html_p}</tbody></table>
                {summary_table_html}
                <div class='print-signatures-block'><div>توقيع واعتماد الحسابات المركزية: .........................</div><div>خِتم وتصديق الشركة الرسمي: .........................</div></div>
            </div>"""
            st.markdown(html_document_payload, unsafe_allow_html=True)
            st.success("🎉 تم توليد الوثيقة الملوكية بنجاح! اضغط الآن من لوحة المفاتيح على Ctrl + P لبدء الطباعة المعزولة تماماً.")

elif menu == "⚠️ الشحنات متأخرة السداد":
    st.title("⚠️ محرك رصد أعمار الديون والشحنات المتأخرة (Aging Balances)")
    conn = get_db_connection()
    shipments_all = pd.read_sql_query("SELECT * FROM shipments", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if shipments_all.empty: st.success("لا توجد حاويات مسجلة حالياً.")
    else:
        overdue_records = []
        current_date = datetime.now()
        for index, row in shipments_all.iterrows():
            cust = row['customer_name']
            c_ship = shipments_all[shipments_all['customer_name'] == cust]
            c_rec = receipts_all[receipts_all['customer_name'] == cust]
            r_l, r_u = c_ship['do_value_lyd'].sum(), c_ship['final_freight_usd'].sum()
            p_l = c_rec[c_rec['currency'] == 'دينار ليبي LYD']['amount'].sum()
            p_u = c_rec[c_rec['currency'] == 'دولار أمريكي USD']['amount'].sum()
            try:
                ship_dt = datetime.strptime(row['shipment_date'], "%Y-%m-%d")
                days_passed = (current_date - ship_dt).days
            except: days_passed = 0
            if days_passed > 30 and ((r_l - p_l) > 0 or (r_u - p_u) > 0):
                overdue_records.append({"customer_name": cust, "bl_number": row['bl_number'], "container_number": row['container_number'], "shipment_date": row['shipment_date'], "days_aged": f"{days_passed} يوم", "remaining_lyd": f"{r_l - p_l:,.2f} د.ل", "remaining_usd": f"${r_u - p_u:,.2f}"})
        if not overdue_records: st.success("🎉 لا توجد أي شحنات متأخرة السداد فوق 30 يوماً.")
        else:
            df_overdue = pd.DataFrame(overdue_records)
            th = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "تاريخ الاستلام", "عمر الدين جاري", "رصيد العميل المعلق (د.ل)", "رصيد العميل المعلق ($)"])
            tr = "".join(f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td style='color:orange; font-weight:bold;'>{r['days_aged']}</td><td style='color:red;'>{r['remaining_lyd']}</td><td style='color:red;'>{r['remaining_usd']}</td></tr>" for _, r in df_overdue.iterrows())
            st.markdown(f'<div class="premium-table-wrapper"><table class="premium-enterprise-table"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>', unsafe_allow_html=True)

elif menu == "💰 إيصالات القبض والمالية":
    st.title("💰 إدارة المدفوعات وإيصالات قبض الزبائن")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    if customers_df.empty: st.warning("يرجى إضافة زبائن أولاً.")
    else:
        st.subheader("➕ تسجيل إيصال قبض جديد")
        with st.form("receipt_form", clear_on_submit=True):
            rc1, rc2, rc3 = st.columns(3)
            with rc1: r_cust = st.selectbox("قبض من الزبون:", customers_df['name'])
            with rc2: r_amount = st.number_input("المبلغ المدفوع:", min_value=0.0, step=50.0)
            with rc3: r_curr = st.selectbox("العملة:", ["دينار ليبي LYD", "دولار أمريكي USD"])
            rc4, rc5 = st.columns([1, 2])
            with rc4: r_date = st.date_input("تاريخ القبض:", datetime.now())
            with rc5: r_notes = st.text_input("ملاحظات / رقم الإيصال:")
            if st.form_submit_button("💾 حفظ وإدراج الإيصال") and r_amount > 0:
                cursor.execute('INSERT INTO receipts (customer_name, amount, currency, receipt_date, notes) VALUES (%s, %s, %s, %s, %s)', (r_cust, r_amount, r_curr, r_date.strftime('%Y-%m-%d'), r_notes))
                conn.commit(); st.success("🎉 تم تسجيل وإدراج المدفوعات بنجاح!")
    cursor.close(); conn.close()

elif menu == "✏️ تعديل وحذف الإيصالات":
    st.title("✏️ التحكم في إيصالات القبض (تعديل / حذف)")
    conn = get_db_connection()
    cursor = conn.cursor()
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    if receipts_all.empty: st.info("لا توجد إيصالات.")
    else:
        search_receipt = st.text_input("🔍 ابحث:")
        filtered_r = receipts_all.copy()
        if search_receipt.strip():
            sr = search_receipt.strip().lower()
            filtered_r = receipts_all[receipts_all['customer_name'].str.lower().str.contains(sr, na=False) | receipts_all['notes'].str.lower().str.contains(sr, na=False)]
        if filtered_r.empty: st.warning("لا توجد نتائج.")
        else:
            filtered_r['selector_text'] = filtered_r['customer_name'] + " | مبلغ: " + filtered_r['amount'].astype(str) + " (" + filtered_r['currency'] + ") | ملاحظة: " + filtered_r['notes']
            selected_receipt_opt = st.selectbox("اختر الإيصال:", filtered_r['selector_text'])
            selected_r_row = filtered_r[filtered_r['selector_text'] == selected_receipt_opt].iloc[0]
            receipt_id = int(selected_r_row['id'])
            with st.form("edit_r_form"):
                rec_c1, rec_c2, rec_c3 = st.columns(3)
                with rec_c1: edit_r_cust = st.text_input("اسم الزبون", value=selected_r_row['customer_name'], disabled=True)
                with rec_c2: edit_r_amount = st.number_input("المبلغ المعدل", value=float(selected_r_row['amount']))
                with rec_c3: edit_r_curr = st.selectbox("العملة", ["دينار ليبي LYD", "دولار أمريكي USD"], index=0 if "دينار" in selected_r_row['currency'] else 1)
                rec_c4, rec_c5 = st.columns(2)
                with rec_c4: edit_r_date = st.text_input("التاريخ (YYYY-MM-DD)", value=selected_r_row['receipt_date'])
                with rec_c5: edit_r_notes = st.text_input("ملاحظات", value=selected_r_row['notes'])
                b1, b2 = st.columns(2)
                with b1:
                    if st.form_submit_button("💾 حفظ التعديل"):
                        cursor.execute('UPDATE receipts SET amount=%s, currency=%s, receipt_date=%s, notes=%s WHERE id=%s', (edit_r_amount, edit_r_curr, edit_r_date, edit_r_notes, receipt_id))
                        conn.commit(); st.success("تم تحديث بيانات الإيصال!"); st.sidebar.markdown("🔄 يرجى إعادة تحديث الصفحة"); st.rerun()
                with b2:
                    if st.form_submit_button("🗑️ حذف نهائي"):
                        cursor.execute("DELETE FROM receipts WHERE id=%s", (receipt_id,))
                        conn.commit(); st.success("تم حذف الإيصال."); st.rerun()
    cursor.close(); conn.close()

elif menu == "➕ إضافة شحنة جديدة (يدوي/LCL)":
    st.title("➕ إضافة بوليصة / شحنة جديدة يدوياً بدعم الحاويات المتعددة")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    if customers_df.empty: st.warning("يجب إضافة زبائن أولاً.")
    else:
        num_containers = st.number_input("حدد كم حاوية تابعة لهذه البوليصة المستهدفة:", min_value=1, max_value=20, value=1, step=1)
        with st.form("manual_shipment_form_v2", clear_on_submit=True):
            sc1, sc2 = st.columns(2)
            with sc1: s_cust = st.selectbox("اختر اسم الزبون المسجل:", customers_df['name'])
            with sc2: s_bl = st.text_input("رقم البوليصة الجمركي الرئيسي:")
            container_inputs = []
            c_cols = st.columns(min(num_containers, 4))
            for i in range(num_containers):
                col_idx = i % 4
                with c_cols[col_idx]: container_inputs.append(st.text_input(f"رقم الحاوية {i+1}:", key=f"manual_container_input_{i}"))
            sc4, sc5, sc6 = st.columns(3)
            with sc4: s_date = st.date_input("تاريخ الاستلام الفعلي:", datetime.now())
            with sc5: s_do_num = st.text_input("رقم أمر التسليم (D.O):")
            with sc6: s_do_val = st.number_input("قيمة أمر التسليم الإجمالية (بالدينار LYD):", min_value=0.0, step=100.0)
            sc7, sc8 = st.columns(2)
            with sc7: s_agency = st.number_input("قيمة شحن الوكالة الكلية (بالدولار USD):", min_value=0.0, step=50.0)
            with sc8: s_final = st.number_input("قيمة الشحن النهائي للزبون (بالدولار USD):", min_value=0.0, step=50.0)
            if st.form_submit_button("🚀 إضافة الشحنة"):
                valid_containers = [c.strip() for c in container_inputs if c.strip()]
                if not valid_containers: st.error("❌ خطأ: يجب كتابة رقم حاوية واحد على الأقل.")
                elif s_bl.strip() == "": st.error("❌ خطأ: يرجى كتابة رقم البوليصة.")
                else:
                    combined_containers_string = " , ".join(valid_containers)
                    cursor.execute('INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (s_cust, combined_containers_string, s_bl.strip(), s_date.strftime('%Y-%m-%d'), s_do_num.strip(), s_do_val, s_agency, s_final))
                    conn.commit(); st.success("🎉 تم حفظ البوليصة بنجاح!"); st.rerun()
    cursor.close(); conn.close()

elif menu == "📥 رفع ملف إكسل":
    st.title("📥 رفع البيانات مباشرة وتلقائياً من ملف Excel")
    uploaded_file = st.file_uploader("اختر ملف الإكسل لتحديث ودمج السجلات الجارية:", type=["xlsx", "xls"])
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.success("تم تحميل الملف بنجاح!")
            all_cols = list(df.columns)
            c1, c2, c3, c4 = st.columns(4)
            with c1: col_cust = st.selectbox("عمود اسم الزبون", all_cols, index=0)
            with c2: col_cont = st.selectbox("عمود رقم الحاوية (يدعم حاويات مدمجة بالخلية)", all_cols, index=min(1, len(all_cols)-1))
            with c3: col_bl = st.selectbox("عمود رقم البوليصة", all_cols, index=min(2, len(all_cols)-1))
            with c4: col_date = st.selectbox("عمود التاريخ", all_cols, index=min(3, len(all_cols)-1))
            c5, c6, c7, c8 = st.columns(4)
            with c5: col_donum = st.selectbox("عمود رقم أمر التسليم", all_cols, index=min(4, len(all_cols)-1))
            with c6: col_dovald = st.selectbox("عمود قيمة أمر التسليم (LYD)", all_cols, index=min(5, len(all_cols)-1))
            with c7: col_agency = st.selectbox("عمود شحن الوكالة (USD)", all_cols, index=min(6, len(all_cols)-1))
            with c8: col_final = st.selectbox("عمود الشحن النهائي (USD)", all_cols, index=min(7, len(all_cols)-1))
            
            if st.button("🚀 بدء دمج البيانات والمطابقة الذكية بقاعدة البيانات أونلاين"):
                conn = get_db_connection()
                cursor = conn.cursor()
                insert_count, update_count = 0, 0
                for index, row in df.iterrows():
                    cust_name = str(row[col_cust]).strip()
                    if cust_name == "" or pd.isnull(row[col_cust]): continue
                    cursor.execute("INSERT INTO customers (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (cust_name,))
                    bl = str(row[col_bl]).strip()
                    raw_date = row[col_date]
                    date_str = raw_date.strftime('%Y-%m-%d') if isinstance(raw_date, (datetime, pd.Timestamp)) else str(raw_date)
                    new_do_num = str(row[col_donum]).strip()
                    new_do_val, new_agency, new_final = safe_float(row[col_dovald]), safe_float(row[col_agency]), safe_float(row[col_final])
                    raw_containers = str(row[col_cont]).strip()
                    container_list = re.split(r'[,/؛;\s
]+', raw_containers)
                    container_list = [c.strip() for c in container_list if c.strip()]
                    if not container_list: container_list = [""]
                    for container in container_list:
                        cursor.execute("SELECT id FROM shipments WHERE container_number = %s AND bl_number = %s", (container, bl))
                        existing = cursor.fetchone()
                        if existing:
                            cursor.execute('UPDATE shipments SET customer_name=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', (cust_name, date_str, new_do_num, new_do_val, new_agency, new_final, existing['id']))
                            update_count += 1
                        else:
                            cursor.execute('INSERT INTO shipments (customer_name, container_number, bl_number, shipment_date, do_number, do_value_lyd, agency_freight_usd, final_freight_usd) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (cust_name, container, bl, date_str, new_do_num, new_do_val, new_agency, new_final))
                            insert_count += 1
                conn.commit(); cursor.close(); conn.close()
                st.success(f"🎉 تكللت العملية بالنجاح!")
        except Exception as e: st.error(f"حدث خطأ أثناء معالجة ملف الإكسل: {e}")

elif menu == "👥 إدارة الزبائن":
    st.title("👥 التحكم الكامل في أسماء قائمة العملاء")
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
                except: st.error("هذا العميل مسجل بالسيستم بالفعل!")
    with tab2:
        customers = pd.read_sql_query("SELECT * FROM customers", conn)
        if not customers.empty:
            cust_to_edit = st.selectbox("اختر الزبون لتعديل اسمه:", customers['name'])
            new_name = st.text_input("الاسم الجديد المعدل الصريح:")
            if st.button("تأكيد تعديل الاسم"):
                if new_name.strip():
                    cursor.execute("UPDATE customers SET name = %s WHERE name = %s", (new_name.strip(), cust_to_edit))
                    cursor.execute("UPDATE shipments SET customer_name = %s WHERE customer_name = %s", (new_name.strip(), cust_to_edit))
                    conn.commit(); st.success("تم التعديل ومزامنة حساب العميل بنجاح!"); st.rerun()
    with tab3:
        if not customers.empty:
            cust_to_del = st.selectbox("اختر الزبون المراد مسحه تماماً بكل سجلاته الحالية:", customers['name'])
            if st.button("موافق، حذف نهائي"):
                cursor.execute("DELETE FROM customers WHERE name = %s", (cust_to_del,))
                cursor.execute("DELETE FROM shipments WHERE customer_name = %s", (cust_to_del,))
                conn.commit(); st.success("تم الحذف."); st.rerun()
    cursor.close(); conn.close()

elif menu == "📝 تعديل وحذف الشحنات":
    st.title("📝 محرك البحث المتقدم والتحكم الفردي الصارم بالشحنات")
    conn = get_db_connection()
    cursor = conn.cursor()
    shipments = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    if shipments.empty: st.info("لا يوجد شحنات جارية مسجلة بالمنظومة حالياً.")
    else:
        search_query = st.text_input("🔍 صندوق البحث الذكي:")
        filtered_df = shipments.copy()
        if search_query.strip():
            q = search_query.strip().lower()
            filtered_df = shipments[shipments['container_number'].astype(str).str.lower().str.contains(q, na=False) | shipments['bl_number'].astype(str).str.lower().str.contains(q, na=False) | shipments['customer_name'].astype(str).str.lower().str.contains(q, na=False)]
        if filtered_df.empty: st.warning("لم يتم العثور على أي نتائج.")
        else:
            filtered_df['selector_text'] = "بوليصة: " + filtered_df['bl_number'].astype(str) + " | حاوية: " + filtered_df['container_number'].astype(str) + " (" + filtered_df['customer_name'] + ")"
            selected_option = st.selectbox("اختر السجل الدقيق المعني بإجراء المعالجة والتحديث السحابي:", filtered_df['selector_text'].tolist())
            selected_row = filtered_df[filtered_df['selector_text'] == selected_option].iloc[0]
            shipment_id = int(selected_row['id'])
            with st.form("edit_ship_form_v2"):
                ec1, ec2, ec3 = st.columns(3)
                with ec1: edit_cust = st.text_input("اسم حساب العميل", value=selected_row['customer_name'], disabled=True)
                with ec2: edit_cont = st.text_input("رقم الحاوية / الحاويات", value=selected_row['container_number'])
                with ec3: edit_bl = st.text_input("رقم البوليصة الرئيسي", value=selected_row['bl_number'])
                ec4, ec5, ec6 = st.columns(3)
                with ec4: edit_date = st.text_input("التاريخ (YYYY-MM-DD)", value=selected_row['shipment_date'])
                with ec5: edit_do_num = st.text_input("رقم أمر التسليم (D.O)", value=selected_row['do_number'])
                with ec6: edit_do_val = st.number_input("قيمة أمر التسليم الفعالة (LYD)", value=float(selected_row['do_value_lyd']))
                ec7, ec8 = st.columns(2)
                with ec7: edit_agency = st.number_input("تكلفة شحن الوكالة (USD)", value=float(selected_row['agency_freight_usd']))
                with ec8: edit_final = st.number_input("قيمة الشحن النهائي للزبون (USD)", value=float(selected_row['final_freight_usd']))
                b1, b2 = st.columns(2)
                with b1:
                    if st.form_submit_button("💾 حفظ وتأكيد مزامنة البيانات المعدلة"):
                        cursor.execute('UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', (edit_cont.strip(), edit_bl.strip(), edit_date.strip(), edit_do_num.strip(), edit_do_val, edit_agency, edit_final, shipment_id))
                        conn.commit(); st.success("🎉 تم التعديل السحابي!"); st.rerun()
                with b2:
                    if st.form_submit_button("🗑️ حذف وإلغاء هذه الشحنة تماماً"):
                        cursor.execute("DELETE FROM shipments WHERE id=%s", (shipment_id,))
                        conn.commit(); st.success("تم مسح السجل الفردي بنجاح."); st.rerun()
    cursor.close(); conn.close()

elif menu == "🗑️ مسح البيانات دفعة واحدة":
    st.title("🗑️ محرك التصفير والشطب الكلي لسجلات قاعدة البيانات")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    tab1, tab2 = st.tabs(["👤 حذف شحنات مخصصة لزبون معين", "💥 تصفير ومسح كافة البيانات بالنظام"])
    with tab1:
        if customers_df.empty: st.info("لا يوجد زبائن مسجلين حالياً.")
        else:
            target_cust = st.selectbox("اختر اسم الحساب المراد إزالة حاوياته بالكامل:", customers_df['name'], key="bulk_del_select")
            cursor.execute("SELECT id, container_number, bl_number, do_number FROM shipments WHERE customer_name = %s", (target_cust,))
            cust_shipments = cursor.fetchall()
            if not cust_shipments: st.info(f"لا توجد أي شحنات جارية معلقة لحساب هذا الزبون حالياً.")
            else:
                shipment_options = {f"📦 حاوية: {r['container_number']} | بوليصة: {r['bl_number']}": r['id'] for r in cust_shipments}
                select_all = st.checkbox("🔄 تحديد وتظليل كافة حاويات هذا الحساب المسجلة")
                default_selection = list(shipment_options.keys()) if select_all else []
                selected_labels = st.multiselect("اختر الشحنات المستهدفة بالإزالة الفورية:", options=list(shipment_options.keys()), default=default_selection)
                if selected_labels:
                    confirm_word = st.text_input("لتنفيذ الشطب، اكتب كلمة 'حذف' صراحة في الفراغ:")
                    if st.button("🗑️ تنفيذ حذف الحاويات المحددة"):
                        if confirm_word == "حذف":
                            ids_to_delete = [shipment_options[lbl] for lbl in selected_labels]
                            placeholders = ', '.join(['%s'] * len(ids_to_delete))
                            cursor.execute(f"DELETE FROM shipments WHERE id IN ({placeholders})", ids_to_delete)
                            conn.commit(); st.success("تم مسح الشحنات المحددة بنجاح!"); st.rerun()
    with tab2:
        clear_financials = st.checkbox("مسح وتصفير كافة إيصالات الخزينة وقوائم أسماء الزبائن أيضاً")
        confirm_all = st.text_input("لتأكيد التصفير السحابي الشامل، اكتب العبارة 'Core-Reset' في الفراغ:")
        if st.button("💥 بدء التصفير الشامل والنهائي للنظام"):
            if confirm_all == "Core-Reset":
                cursor.execute("TRUNCATE TABLE shipments RESTART IDENTITY")
                if clear_financials:
                    cursor.execute("TRUNCATE TABLE receipts RESTART IDENTITY")
                    cursor.execute("TRUNCATE TABLE customers RESTART IDENTITY")
                conn.commit(); st.success("تم تصفير قاعدة البيانات السحابية بالكامل وعودتها لنقطة البداية!"); st.rerun()
    cursor.close(); conn.close()
