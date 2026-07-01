import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import plotly.graph_objects as go

# 1. إعداد الصفحة الأساسي وتثبيت العناوين الرسمية
st.set_page_config(page_title="منظومة إستبرق لإدارة الشحنات والمالية", layout="wide", initial_sidebar_state="expanded")

# 2. حزمة الـ CSS الاحترافية لضبط الجداول على الشاشة وتنسيق الطباعة العمودية الفاخرة A4
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
html, body, [data-testid="stSidebar"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #fcfcfc; }
.stHeading, .stMarkdown, p, div, label, span { text-align: right; direction: rtl; }

/* تصميم أزرار المنظومة */
div.stButton > button:first-child { background-color: #1e4620; color:white; font-weight: 600; width: 100%; border-radius: 10px; height: 48px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.06); transition: all 0.2s; }
div.stButton > button:hover { background-color: #2e7d32; transform: translateY(-1px); }
.metric-card { background-color: #ffffff; padding: 22px; border-radius: 14px; border-right: 6px solid #1e4620; box-shadow: 0 4px 15px rgba(0,0,0,0.03); margin-bottom: 20px; }

/* 📊 جداول ويب حقيقية RTL فائقة الاتساع والوضوح (حل نهائي ومستقر لمشكلة تداخل الحروف) */
.table-responsive-wrapper { width: 100%; overflow-x: auto; direction: rtl; margin: 20px 0; border-radius: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); background: white; }
table.enterprise-html-table { width: 100%; border-collapse: collapse; direction: rtl; text-align: right; }
table.enterprise-html-table th { background-color: #1e4620; color: white; padding: 15px 18px; font-weight: 600; font-size: 14px; border-bottom: 2px solid #143316; white-space: nowrap; }
table.enterprise-html-table td { padding: 13px 18px; text-align: right; border-bottom: 1px solid #f0f4ee; color: #222222; font-size: 14px; font-weight: 500; white-space: nowrap; }
table.enterprise-html-table tr:nth-child(even) { background-color: #fbfdfb; }
table.enterprise-html-table tr:hover { background-color: #f3f7f3; }

/* 📜 تصميم كشف الحساب الرسمي الملوكي المقاوم للتشوه عند الطباعة */
.printable-invoice-container { background-color: white !important; padding: 40px; border: 1px solid #000000; border-radius: 6px; direction: rtl; text-align: right; margin-top: 30px; color: #000000 !important; }
.invoice-header { text-align: center; border-bottom: 4px double #1e4620; padding-bottom: 15px; margin-bottom: 25px; }
.invoice-header h2 { color: #1e4620 !important; font-weight: 700; margin: 0; font-size: 24px; text-align: center; }
.invoice-meta-table { width: 100%; margin-bottom: 20px; font-size: 14px; color: #000000 !important; }
.invoice-meta-table td { padding: 5px; border: none !important; }

table.invoice-items-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 13px; color: #000000 !important; }
table.invoice-items-table th { background-color: #f2f2f2 !important; color: #1e4620 !important; border: 1px solid #000000 !important; padding: 10px; font-weight: bold; text-align: right; }
table.invoice-items-table td { border: 1px solid #000000 !important; padding: 10px; text-align: right; color: #000000 !important; font-weight: 500; }

.invoice-summary-zone { margin-top: 25px; padding: 15px; background-color: #fcfcf9; border: 1px solid #000000; border-radius: 6px; color: #000000 !important; }
.invoice-signatures-zone { margin-top: 50px; width: 100%; display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; color: #000000 !important; }

/* 🖨️ محرك الطباعة العمودي الصارم المطور A4 Portrait */
@media print {
    @page { size: A4 portrait; margin: 15mm; }
    html, body { background-color: white !important; color: black !important; }
    [data-testid="stSidebar"], 
    [data-testid="stHeader"], 
    [data-testid="stElementToolbar"],
    div.stButton, 
    div.stSelectbox, 
    div.stMultiSelect, 
    div.stRadio, 
    .stExpander,
    .print-instruction,
    .table-responsive-wrapper,
    .table-responsive-container,
    .dashboard-kpi-container,
    .no-print {
        display: none !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    [data-testid="stAppViewContainer"] { padding: 0 !important; margin: 0 !important; background-color: white !important; }
    .printable-invoice-container { border: none !important; padding: 0 !important; margin: 0 !important; }
}
</style>
""", unsafe_allow_html=True)

# 3. الاتصال بقاعدة البيانات السحابية
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
        df.to_excel(writer, index=False, sheet_name='كشف المنظومة')
    return output.getvalue()

# 4. دالة رندرة جداول الـ HTML المستقرة RTL على الشاشة (تمنع تماماً كود الماركدوان الرمادي المشوه)
def render_html_rtl_grid(df, show_financials=False):
    headers = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)"]
    if show_financials:
        headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
        
    th_string = "".join(f"<th>{h}</th>" for h in headers)
    tr_string = ""
    for _, r in df.iterrows():
        tr_string += "<tr>"
        tr_string += f"<td>{r['customer_name']}</td>"
        tr_string += f"<td>{r['bl_number']}</td>"
        tr_string += f"<td>{r['container_number']}</td>"
        tr_string += f"<td>{r['shipment_date']}</td>"
        tr_string += f"<td>{r['do_number']}</td>"
        tr_string += f"<td>{r['do_value_lyd']:,.2f} د.ل</td>"
        tr_string += f"<td>${r['final_freight_usd']:,.2f}</td>"
        if show_financials:
            tr_string += f"<td>${r['agency_freight_usd']:,.2f}</td>"
            tr_string += f"<td>${r['profit_usd']:,.2f}</td>"
        tr_string += "</tr>"
        
    grid_html = f"<div class='table-responsive-wrapper'><table class='enterprise-html-table'><thead><tr>{th_string}</tr></thead><tbody>{tr_string}</tbody></table></div>"
    st.markdown(grid_html, unsafe_allow_html=True)

# ----------------- القائمة الجانبية للمنظومة -----------------
st.sidebar.markdown("<h2 style='text-align: center; color: #1e4620; font-weight:700;'>🚢 إستبرق الدولية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4caf50;'>🌐 لوحة التخليص والوجستيات</p>", unsafe_allow_html=True)
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

# ==================== 📊 5. بناء لوحة التحكم والتقارير الاحترافية الشاملة ====================
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 شاشة الرقابة المالية وحصر كشوفات الحساب")
    
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty:
        st.warning("لا توجد بيانات مسجلة في قاعدة البيانات حالياً.")
    else:
        # لوحة الفلاتر المتطورة (تلبية للميزة رقم 4 ورقم 1 و 2)
        with st.expander("⚙️ محرك التحكم وتحديد نوع كشف الحساب المطلوب", expanded=True):
            f1, f2, f3 = st.columns(3)
            with f1: f_scope = st.radio("1. نطاق البحث المالي:", ["كل الزبائن", "زبون محدد"], horizontal=True)
            with f2: f_type = st.radio("2. نوع هيكل الكشف:", ["كشف إجمالي عام", "كشف تفصيلي"], horizontal=True)
            with f3: f_profit = st.checkbox("إظهار قيم شحن الوكالة وصافي الأرباح", value=False)
            
            st.write("---")
            if f_scope == "زبون محدد":
                f_customer = st.selectbox("🎯 اختر اسم الزبون لفرز وحصر بياناته (تصفية بالزبون):", customers_df['name'].tolist())
            else:
                f_customer = "الكل"

        st.write("---")

        # 🟢 تنفيذ التقارير الأربعة وتحميل الإكسل (الميزات 1 و 2 و 4)
        df_active_report = pd.DataFrame()
        
        if f_scope == "كل الزبائن":
            if f_type == "كشف إجمالي عام":
                st.subheader("📋 كشف الأرصاد الإجمالي لكافة زبائن الشركة (كل زبون في صف)")
                all_summary = []
                for cust in customers_df['name']:
                    c_ship = shipments_all[shipments_all['customer_name'] == cust]
                    c_rec = receipts_all[receipts_all['customer_name'] == cust]
                    req_l = c_ship['do_value_lyd'].sum() if not c_ship.empty else 0.0
                    req_u = c_ship['final_freight_usd'].sum() if not c_ship.empty else 0.0
                    paid_l = c_rec[c_rec['currency'] == 'دينار ليبي LYD']['amount'].sum() if not c_rec.empty else 0.0
                    paid_u = c_rec[c_rec['currency'] == 'دولار أمريكي USD']['amount'].sum() if not c_rec.empty else 0.0
                    all_summary.append({
                        "اسم الزبون": cust, "عدد الحاويات": len(c_ship), "المطلوب (د.ل)": req_l, "المدفوع (د.ل)": paid_l, "المتبقي (د.ل)": req_l - paid_l, "الشحن ($)": req_u, "المدفوع ($)": paid_u, "المتبقي ($)": req_u - paid_u
                    })
                df_active_report = pd.DataFrame(all_summary)
                
                # رندرة جدول الإجمالي العام لجميع الزبائن
                th_sum = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "عدد الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                tr_sum = ""
                for _, r in df_active_report.iterrows():
                    tr_sum += f"<tr><td>{r['اسم الزبون']}</td><td>{r['عدد الحاويات']}</td><td>{r['المطلوب (د.ل)']:,.2f} د.ل</td><td>{r['المدفوع (د.ل)']:,.2f} د.ل</td><td style='color:red; font-weight:bold;'>{r['المتبقي (د.ل)']:,.2f} د.ل</td><td>${r['الشحن ($)']:,.2f}</td><td>${r['المدفوع ($)']:,.2f}</td><td style='color:red; font-weight:bold;'>${r['المتبقي ($)']:,.2f}</td></tr>"
                st.markdown(f"<div class='table-responsive-wrapper'><table class='enterprise-html-table'><thead><tr>{th_sum}</tr></thead><tbody>{tr_sum}</tbody></table></div>", unsafe_allow_html=True)
            else:
                st.subheader("📋 سجل الحساب التفصيلي الشامل لكافة حاويات المنظومة")
                df_active_report = shipments_all.copy()
                df_active_report['profit_usd'] = df_active_report['final_freight_usd'] - df_active_report['agency_freight_usd']
                render_html_rtl_grid(df_active_report, show_financials=f_profit)
        else:
            # تصفية لزبون محدد
            df_cust_ship = shipments_all[shipments_all['customer_name'] == f_customer].copy()
            df_cust_rec = receipts_all[receipts_all['customer_name'] == f_customer]
            req_l = df_cust_ship['do_value_lyd'].sum() if not df_cust_ship.empty else 0.0
            req_u = df_cust_ship['final_freight_usd'].sum() if not df_cust_ship.empty else 0.0
            paid_l = df_cust_rec[df_cust_rec['currency'] == 'دينار ليبي LYD']['amount'].sum() if not df_cust_rec.empty else 0.0
            paid_u = df_cust_rec[df_cust_rec['currency'] == 'دولار أمريكي USD']['amount'].sum() if not df_cust_rec.empty else 0.0
            
            if f_type == "كشف إجمالي عام":
                st.subheader(f"📋 كروت الموقف المالي الإجمالي لحساب: {f_customer}")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"""<div class='metric-card' style='border-right-color: #2196f3;'>
                        <h5>💵 ذمم أوامر التسليم بالدينار الليبي:</h5>
                        <p>إجمالي المطلوب: <b>{req_l:,.2f} د.ل</b> | المدفوع: <b style='color:green;'>{paid_l:,.2f} د.ل</b></p>
                        <p>المتبقي بذمته جاري: <b style='color:red;'>{req_l - paid_l:,.2f} د.ل</b></p>
                    </div>""", unsafe_allow_html=True)
                with c2:
                    st.markdown(f"""<div class='metric-card' style='border-right-color: #4caf50;'>
                        <h5>💵 مطلوب نولون الشحن بالدولار الأمريكي:</h5>
                        <p>إجمالي المطلوب: <b>${req_u:,.2f}</b> | المدفوع: <b style='color:green;'>${paid_u:,.2f}</b></p>
                        <p>المتبقي بذمته جاري: <b style='color:red;'>${req_u - paid_u:,.2f}</b></p>
                    </div>""", unsafe_allow_html=True)
                df_active_report = pd.DataFrame([{"اسم الزبون": f_customer, "المطلوب (د.ل)": req_l, "المدفوع (د.ل)": paid_l, "المتبقي (د.ل)": req_l-paid_l, "الشحن ($)": req_u, "المدفوع ($)": paid_u, "المتبقي ($)": req_u-paid_u}])
            else:
                st.subheader(f"📋 كشف السجل التفصيلي لكافة حاويات الزبون: {f_customer}")
                df_cust_ship['profit_usd'] = df_cust_ship['final_freight_usd'] - df_cust_ship['agency_freight_usd']
                df_active_report = df_cust_ship.copy()
                render_html_rtl_grid(df_active_report, show_financials=f_profit)

        # زر تحميل الإكسل الذكي الموحد للأربع كشوفات
        if not df_active_report.empty:
            st.download_button(label="📥 تحميل كشف الحساب المعروض حالياً بصيغة Excel", data=to_excel(df_active_report), file_name=f"istabraq_report_{datetime.now().strftime('%Y%m%d')}.xlsx")

        # ==================== 🖨️ [الميزة 5]: محرك الطباعة العمودية الفاخر المضمون A4 Portrait ====================
        st.write("---")
        st.markdown("### 🖨️ محرك توليد وفصل كشوفات الحساب الرسمية للطباعة العمودية:")
        st.markdown("<p style='font-size:14px; color:#555;'>💡 حدد حاويات منتقاة من القائمة المنسدلة (مثلاً 5 من أصل 50) ثم اضغط توليد وافتح خيار طباعة المتصفح للحفظ كـ PDF رسمي منسق عمودياً.</p>", unsafe_allow_html=True)
        
        # فرز قائمة الحاويات المتاحة حسب نطاق الفلترة لسهولة الاختيار
        df_print_source = shipments_all[shipments_all['customer_name'] == f_customer].copy() if f_scope == "زبون محدد" else shipments_all.copy()
        df_print_source['print_label'] = "زبون: " + df_print_source['customer_name'] + " | بوليصة: " + df_print_source['bl_number'] + " | حاوية: " + df_print_source['container_number']
        
        chosen_containers = st.multiselect(
            "اختر الشحنات الدقيقة المراد إدراجها في وثيقة الفاتورة والطباعة (اتركها فارغة لطباعة كل المعروض):",
            options=df_print_source['print_label'].tolist()
        )
        
        df_print_final = df_print_source[df_print_source['print_label'].isin(chosen_containers)] if chosen_containers else df_print_source.copy()
        
        if st.button("🖨️ توليد واعتماد وثيقة كشف الحساب الجاهزة للطباعة"):
            st.success("🎉 تم توليد الوثيقة الرسمية بنجاح! اضغط الآن على Ctrl + P من لوحة مفاتيح جهازك لبدء الطباعة العمودية المنسقة فوراً.")
            
            p_total_lyd = df_print_final['do_value_lyd'].sum()
            p_total_usd = df_print_final['final_freight_usd'].sum()
            
            rows_html_string = ""
            for _, row in df_print_final.iterrows():
                agency_td_p = f"<td>${row['agency_freight_usd']:,.2f}</td>" if f_profit else ""
                profit_td_p = f"<td>${(row['final_freight_usd'] - row['agency_freight_usd']):,.2f}</td>" if f_profit else ""
                rows_html_string += "<tr>"
                rows_html_string += f"<td>{row['customer_name']}</td>"
                rows_html_string += f"<td>{row['bl_number']}</td>"
                rows_html_string += f"<td>{row['container_number']}</td>"
                rows_html_string += f"<td>{row['shipment_date']}</td>"
                rows_html_string += f"<td>{row['do_number']}</td>"
                rows_html_string += f"<td>{row['do_value_lyd']:,.2f} د.ل</td>"
                rows_html_string += f"<td>${row['final_freight_usd']:,.2f}</td>"
                if f_profit:
                    rows_html_string += agency_td_p + profit_td_p
                rows_html_string += "</tr>"
                
            th_agency_p = "<th>شحن الوكالة</th>" if f_profit else ""
            th_profit_p = "<th>صافي الربح</th>" if f_profit else ""
            
            # بناء الهيكل الملوكي للطباعة العمودية الصارمة بدون أي مسافات بادئة تسبب التشويه النصي
            invoice_html_template = "<div class='printable-invoice-container'>"
            invoice_html_template += "<div class='invoice-header'><h2>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h2><p style='margin:5px 0 0 0; font-size:14px; color:#555;'>مصراتة - ليبيا | هاتف الإدارة المالية المركزية</p></div>"
            invoice_html_template += "<table class='invoice-meta-table'>"
            invoice_html_template += f"<tr><td><b>كشف حساب جاري جمركي للعميل:</b> {f_customer if f_scope == 'زبون محدد' else 'كافة عملاء الشركة'}</td><td style='text-align: left;'><b>تاريخ استخراج الوثيقة:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td></tr>"
            invoice_html_template += f"<tr><td><b>نوع البيان المشهود:</b> كشف حاويات تفصيلي معتمد A4</td><td style='text-align: left;'><b>عدد الحاويات المدرجة:</b> {len(df_print_final)} حاوية جارية</td></tr>"
            invoice_html_template += "</table>"
            invoice_html_template += f"<table class='invoice-items-table'><thead><tr><th>اسم الزبون</th><th>رقم البوليصة</th><th>رقم الحاوية</th><th>التاريخ</th><th>رقم أمر التسليم</th><th>قيمة أمر التسليم</th><th>الشحن النهائي</th>{th_agency_p}{th_profit_p}</tr></thead><tbody>{rows_html_string}</tbody></table>"
            invoice_html_template += "<div class='invoice-summary-zone'>"
            invoice_html_template += f"<div style='width:100%; text-align:left; font-size:15px; margin-bottom:8px; color:#000;'><b>إجمالي صافي ذمم أوامر التسليم المستحقة:</b> <span style='border-bottom: 2px double #000;'>{p_total_lyd:,.2f} دينار ليبي</span></div>"
            invoice_html_template += f"<div style='width:100%; text-align:left; font-size:15px; color:#000;'><b>إجمالي صافي مطلوب نولون الشحن الدولي:</b> <span style='border-bottom: 2px double #000;'>${p_total_usd:,.2f} دولار أمريكي</span></div>"
            invoice_html_template += "</div>"
            invoice_html_template += "<div class='invoice-signatures-zone'><div>ختم شركة إستبرق للتصديق: .........................</div><div>توقيع واعتماد الحسابات: .........................</div></div>"
            invoice_html_template += "</div>"
            
            st.markdown(invoice_html_template, unsafe_allow_html=True)


        # ==================== 🛠️ [الميزة 3]: محرك التعديل وإكمال حقول الحاويات الناقصة ====================
        st.write("---")
        with st.expander("🛠️ لوحة التعديل السريع وإكمال بيانات الحاويات الناقصة", expanded=False):
            st.markdown("💡 **طريقة المعالجة السريعة:** اختر معرّف الشحنة من القائمة، ستظهر تفاصيلها الحالية في استمارة الإدخال، عدّل الحقل الناقص واضغط حفظ للتحديث الفوري أونلاين.")
            
            df_edit_src = shipments_all[shipments_all['customer_name'] == f_customer].copy() if f_scope == "زبون محدد" else shipments_all.copy()
            
            if df_edit_src.empty:
                st.info("لا توجد حاويات متوفرة للتعديل.")
            else:
                df_edit_src['edit_label'] = "معرف [" + df_edit_src['id'].astype(str) + "] | بوليصة: " + df_edit_src['bl_number'].astype(str) + " | حاوية: " + df_edit_src['container_number'].astype(str)
                selected_edit_label = st.selectbox("اختر المعرف الدقيق للشحنة المراد تحديثها:", df_edit_src['edit_label'].tolist())
                
                # سحب بيانات السطر الحالي للحاوية المستهدفة
                current_edit_row = df_edit_src[df_edit_src['edit_label'] == selected_edit_label].iloc[0]
                active_shipment_id = int(current_edit_row['id'])
                
                st.write("")
                with st.form("quick_edit_enterprise_form", clear_on_submit=False):
                    m1, m2, m3 = st.columns(3)
                    with m1: u_cust = st.text_input("اسم حساب الزبون", value=str(current_edit_row['customer_name']), disabled=True)
                    with m2: u_cont = st.text_input("رقم الحاوية الحالي", value=str(current_edit_row['container_number']))
                    with m3: u_bl = st.text_input("رقم البوليصة الحالي", value=str(current_edit_row['bl_number']))
                        
                    m4, m5, m6 = st.columns(3)
                    with m4: u_date = st.text_input("التاريخ (YYYY-MM-DD)", value=str(current_edit_row['shipment_date']))
                    with m5: u_do_num = st.text_input("رقم أمر التسليم", value=str(current_edit_row['do_number']))
                    with m6: u_do_val = st.number_input("قيمة أمر التسليم (LYD)", value=float(current_edit_row['do_value_lyd']))
                        
                    m7, m8 = st.columns(2)
                    with m7: u_agency = st.number_input("شحن الوكالة (USD)", value=float(current_edit_row['agency_freight_usd']))
                    with m8: u_final = st.number_input("الشحن النهائي للعميل (USD)", value=float(current_edit_row['final_freight_usd']))
                    
                    st.write("")
                    save_trigger = st.form_submit_button("💾 حفظ وإرسال البيانات المعدلة إلى السيرفر السحابي أونلاين")
                    if save_trigger:
                        u_conn = get_db_connection()
                        u_cursor = u_conn.cursor()
                        u_cursor.execute('''
                            UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s
                        ''', (u_cont.strip(), u_bl.strip(), u_date.strip(), u_do_num.strip(), u_do_val, u_agency, u_final, active_shipment_id))
                        u_conn.commit()
                        u_cursor.close(); u_conn.close()
                        st.success("🎉 تم تحديث بيانات الحاوية ومزامنتها بنجاح أونلاين!")
                        st.rerun()

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
        if df_incomplete.empty: st.success("🎉 ممتاز! لا توجد أي حاويات ينطبق عليها هذا النقص.")
        else: render_custom_html_grid(df_incomplete, show_profit=False)

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
            submit_receipt = st.form_submit_button("💾 حفظ وإدراج الإيصال في الحساب")
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
