import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import base64

# 1. إعداد الصفحة بنسق عريض
st.set_page_config(page_title="إستبرق للوجستيات | نظام الـ ERP", layout="wide", initial_sidebar_state="expanded")

# 2. حزمة CSS أساسية نظيفة لواجهة المستخدم فقط (الطباعة أصبحت معزولة تماماً)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
html, body, [data-testid="stSidebar"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #f5f6fa; }
.stHeading, .stMarkdown, p, div, label, span { text-align: right; direction: rtl; }
div.stButton > button:first-child { background-color: #1e4620; color:white; font-weight: 600; width: 100%; border-radius: 8px; height: 48px; border: none; transition: 0.3s; }
div.stButton > button:hover { background-color: #2e7d32; }
.kpi-card { background: #fff; padding: 20px; border-radius: 10px; border-top: 5px solid #1e4620; box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 20px; }
.kpi-card h5 { color: #555; font-size: 15px; margin-bottom: 10px; }
.kpi-card h2 { color: #1e4620; font-size: 24px; margin: 0; }
table.ui-table { width: 100%; border-collapse: collapse; direction: rtl; background: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
table.ui-table th { background-color: #1e4620; color: white; padding: 12px; font-size: 14px; border: 1px solid #ddd; white-space: nowrap; }
table.ui-table td { padding: 10px; font-size: 14px; border: 1px solid #ddd; color: #222; }
table.ui-table tr:nth-child(even) { background-color: #f9f9f9; }
</style>
""", unsafe_allow_html=True)

# 3. الاتصال بقاعدة البيانات
def get_db_connection():
    try:
        db_url = st.secrets["postgres"]["url"]
        return psycopg2.connect(db_url, cursor_factory=DictCursor)
    except Exception as e:
        st.error(f"🔴 خطأ في الاتصال بقاعدة البيانات: {e}")
        st.stop()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS customers (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS shipments (id SERIAL PRIMARY KEY, customer_name TEXT, container_number TEXT, bl_number TEXT, shipment_date TEXT, do_number TEXT, do_value_lyd DOUBLE PRECISION, agency_freight_usd DOUBLE PRECISION, final_freight_usd DOUBLE PRECISION)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receipts (id SERIAL PRIMARY KEY, customer_name TEXT, amount DOUBLE PRECISION, currency TEXT, receipt_date TEXT, notes TEXT)''')
    conn.commit()
    cursor.close(); conn.close()

init_db()

# 4. دوال التصدير والطباعة المعزولة
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Report')
    return output.getvalue()

def generate_isolated_print_html(df, report_type, customer_name, total_lyd, total_usd, show_profit=False):
    """هذا المحرك يولد صفحة HTML نقية معزولة تطبع أوتوماتيكياً بنظام A4 المتعدد الصفحات"""
    # بناء صفوف الجدول
    rows_html = ""
    if report_type == "summary":
        th_html = "<th>اسم الزبون</th><th>عدد الحاويات</th><th>المطلوب (د.ل)</th><th>المدفوع (د.ل)</th><th>المتبقي (د.ل)</th><th>الشحن ($)</th><th>المدفوع ($)</th><th>المتبقي ($)</th>"
        for _, r in df.iterrows():
            rows_html += f"<tr><td>{r['اسم الزبون']}</td><td>{r['عدد الحاويات']}</td><td>{r['المطلوب (د.ل)']:,.2f}</td><td>{r['المدفوع (د.ل)']:,.2f}</td><td>{r['المتبقي (د.ل)']:,.2f}</td><td>${r['الشحن ($)']:,.2f}</td><td>${r['المدفوع ($)']:,.2f}</td><td>${r['المتبقي ($)']:,.2f}</td></tr>"
    else:
        th_html = "<th>اسم الزبون</th><th>رقم البوليصة</th><th>رقم الحاوية</th><th>التاريخ</th><th>أمر التسليم</th><th>قيمة أ.ت (د.ل)</th><th>الشحن النهائي ($)</th>"
        if show_profit: th_html += "<th>شحن الوكالة</th><th>الربح</th>"
        for _, r in df.iterrows():
            rows_html += f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f}</td><td>${r['final_freight_usd']:,.2f}</td>"
            if show_profit: rows_html += f"<td>${r['agency_freight_usd']:,.2f}</td><td>${r['profit_usd']:,.2f}</td>"
            rows_html += "</tr>"

    doc_title = "كشف أرصاد مالي إجمالي" if report_type == "summary" else "كشف سجل حاويات تفصيلي"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>طباعة تقرير - إستبرق</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
            body {{ font-family: 'Cairo', sans-serif; background-color: white; color: black; padding: 20px; font-size: 14px; margin: 0; }}
            .header {{ text-align: center; border-bottom: 3px double #1e4620; padding-bottom: 10px; margin-bottom: 20px; }}
            .header h1 {{ color: #1e4620; margin: 0; font-size: 24px; }}
            .header p {{ margin: 5px 0 0 0; color: #555; }}
            .info-table {{ width: 100%; margin-bottom: 20px; }}
            .info-table td {{ border: none; padding: 5px; }}
            table.data-table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
            table.data-table th, table.data-table td {{ border: 1px solid #000; padding: 8px; text-align: right; }}
            table.data-table th {{ background-color: #f2f2f2; -webkit-print-color-adjust: exact; }}
            .totals {{ border: 2px solid #000; padding: 15px; background-color: #fafafa; -webkit-print-color-adjust: exact; page-break-inside: avoid; }}
            .sigs {{ display: flex; justify-content: space-between; margin-top: 50px; font-weight: bold; page-break-inside: avoid; }}
            @media print {{
                @page {{ size: A4 portrait; margin: 15mm; }}
                table.data-table {{ page-break-inside: auto; }}
                tr {{ page-break-inside: avoid; page-break-after: auto; }}
                thead {{ display: table-header-group; }}
            }}
        </style>
    </head>
    <body onload="window.print()">
        <div class="header">
            <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية</h1>
            <p>مصراتة - ليبيا | الحسابات المركزية</p>
        </div>
        <table class="info-table">
            <tr>
                <td><b>الحساب الجاري:</b> {customer_name}</td>
                <td style="text-align: left;"><b>تاريخ الاستخراج:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
            </tr>
            <tr>
                <td><b>نوع المستند:</b> {doc_title}</td>
                <td style="text-align: left;"><b>عدد السجلات المدرجة:</b> {len(df)} سجل</td>
            </tr>
        </table>
        <table class="data-table">
            <thead><tr>{th_html}</tr></thead>
            <tbody>{rows_html}</tbody>
        </table>
        <div class="totals">
            <div style="margin-bottom: 8px;"><b>إجمالي قيمة أوامر التسليم المستحقة:</b> {total_lyd:,.2f} دينار ليبي</div>
            <div><b>إجمالي قيمة نولون الشحن المستحقة:</b> ${total_usd:,.2f} دولار أمريكي</div>
        </div>
        <div class="sigs">
            <div>توقيع الحسابات: ........................</div>
            <div>ختم الشركة: ........................</div>
        </div>
    </body>
    </html>
    """
    return html_content

def create_print_button(html_content):
    """تحويل الـ HTML إلى رابط Base64 يفتح في نافذة جديدة للطباعة النظيفة"""
    b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
    href = f'''
    <a href="data:text/html;charset=utf-8;base64,{b64}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #d32f2f; color: white; padding: 12px; border-radius: 8px; text-align: center; font-family: 'Cairo', sans-serif; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;">
            🖨️ طباعة التقرير (نافذة PDF رسمية A4)
        </div>
    </a><br>
    '''
    return href

# ----------------- القائمة الجانبية -----------------
st.sidebar.markdown("<h2 style='text-align: center; color: #1e4620; font-weight:700;'>🚢 إستبرق الدولية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4caf50;'>🌐 نظام الإدارة والرقابة المالية</p>", unsafe_allow_html=True)
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

# ==================== 📊 1. لوحة التحكم والتقارير (مبنية من الصفر للمثالية) ====================
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 مركز التقارير وإدارة الحسابات")
    
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers ORDER BY name ASC", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments ORDER BY id DESC", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty:
        st.warning("لا توجد بيانات مسجلة.")
    else:
        # 1. لوحة الفلاتر السريعة (تصفية بالزبون وتحديد نوع التقرير)
        with st.container():
            st.markdown("### ⚙️ محرك استخراج الكشوفات:")
            c1, c2, c3 = st.columns(3)
            with c1: filter_scope = st.radio("نطاق الكشف:", ["كل الزبائن", "زبون محدد"])
            with c2: filter_type = st.radio("نوع الكشف:", ["إجمالي (أرصاد)", "تفصيلي (حاويات)"])
            with c3: show_profit = st.checkbox("عرض أرباح الوكالة (في التفصيلي)")
            
            target_customer = "كافة عملاء المنظومة"
            if filter_scope == "زبون محدد":
                target_customer = st.selectbox("🎯 حدد الزبون:", customers_df['name'].tolist())

        st.write("---")
        
        df_display = pd.DataFrame()
        html_report_table = ""
        total_lyd = 0.0
        total_usd = 0.0
        report_mode = "summary"
        
        # 2. معالجة البيانات حسب اختيار المستخدم
        if filter_scope == "كل الزبائن":
            if filter_type == "إجمالي (أرصاد)":
                report_mode = "summary"
                st.subheader("📋 كشف ملخص الأرصاد لجميع الزبائن")
                sum_data = []
                for cust in customers_df['name']:
                    cs = shipments_all[shipments_all['customer_name'] == cust]
                    cr = receipts_all[receipts_all['customer_name'] == cust]
                    r_l = cs['do_value_lyd'].sum() if not cs.empty else 0.0
                    r_u = cs['final_freight_usd'].sum() if not cs.empty else 0.0
                    p_l = cr[cr['currency'] == 'دينار ليبي LYD']['amount'].sum() if not cr.empty else 0.0
                    p_u = cr[cr['currency'] == 'دولار أمريكي USD']['amount'].sum() if not cr.empty else 0.0
                    sum_data.append({
                        "اسم الزبون": cust, "عدد الحاويات": len(cs), "المطلوب (د.ل)": r_l, "المدفوع (د.ل)": p_l, "المتبقي (د.ل)": r_l - p_l, "الشحن ($)": r_u, "المدفوع ($)": p_u, "المتبقي ($)": r_u - p_u
                    })
                df_display = pd.DataFrame(sum_data)
                total_lyd = df_display['المطلوب (د.ل)'].sum()
                total_usd = df_display['الشحن ($)'].sum()
                
                # بناء جدول واجهة العرض
                th = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                tr = "".join(f"<tr><td>{r['اسم الزبون']}</td><td>{r['عدد الحاويات']}</td><td>{r['المطلوب (د.ل)']:,.2f}</td><td>{r['المدفوع (د.ل)']:,.2f}</td><td style='color:red;'>{r['المتبقي (د.ل)']:,.2f}</td><td>${r['الشحن ($)']:,.2f}</td><td>${r['المدفوع ($)']:,.2f}</td><td style='color:red;'>${r['المتبقي ($)']:,.2f}</td></tr>" for _, r in df_display.iterrows())
                html_report_table = f"<div style='overflow-x:auto;'><table class='ui-table'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>"

            else:
                report_mode = "detailed"
                st.subheader("📋 كشف الحاويات التفصيلي الشامل لكافة الزبائن")
                df_display = shipments_all.copy()
                df_display['profit_usd'] = df_display['final_freight_usd'] - df_display['agency_freight_usd']
                total_lyd = df_display['do_value_lyd'].sum()
                total_usd = df_display['final_freight_usd'].sum()
                
                h_list = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "أمر التسليم", "قيمة أ.ت", "الشحن النهائي"]
                if show_profit: h_list.extend(["شحن الوكالة", "صافي الربح"])
                th = "".join(f"<th>{h}</th>" for h in h_list)
                tr = ""
                for _, r in df_display.iterrows():
                    tr += f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f}</td><td>${r['final_freight_usd']:,.2f}</td>"
                    if show_profit: tr += f"<td>${r['agency_freight_usd']:,.2f}</td><td>${r['profit_usd']:,.2f}</td>"
                    tr += "</tr>"
                html_report_table = f"<div style='overflow-x:auto;'><table class='ui-table'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>"

        else:
            # تصفية زبون محدد
            dfs = shipments_all[shipments_all['customer_name'] == target_customer].copy()
            dfr = receipts_all[receipts_all['customer_name'] == target_customer]
            r_l = dfs['do_value_lyd'].sum() if not dfs.empty else 0.0
            r_u = dfs['final_freight_usd'].sum() if not dfs.empty else 0.0
            p_l = dfr[dfr['currency'] == 'دينار ليبي LYD']['amount'].sum() if not dfr.empty else 0.0
            p_u = dfr[dfr['currency'] == 'دولار أمريكي USD']['amount'].sum() if not dfr.empty else 0.0
            
            # كروت داشبورد الزبون
            st.markdown(f"""
            <div style="display:flex; gap:20px; direction:rtl;">
                <div class="kpi-card" style="flex:1;"><h5>ذمم أوامر التسليم المستحقة</h5><h2>{r_l - p_l:,.2f} د.ل</h2><p style="font-size:12px; color:#666;">المطلوب: {r_l:,.2f} | المدفوع: {p_l:,.2f}</p></div>
                <div class="kpi-card" style="flex:1;"><h5>نولون الشحن الدولي المستحق</h5><h2>${r_u - p_u:,.2f}</h2><p style="font-size:12px; color:#666;">المطلوب: ${r_u:,.2f} | المدفوع: ${p_u:,.2f}</p></div>
            </div>
            """, unsafe_allow_html=True)

            if filter_type == "إجمالي (أرصاد)":
                report_mode = "summary"
                st.subheader(f"📋 الموقف المالي لحساب: {target_customer}")
                df_display = pd.DataFrame([{"اسم الزبون": target_customer, "عدد الحاويات": len(dfs), "المطلوب (د.ل)": r_l, "المدفوع (د.ل)": p_l, "المتبقي (د.ل)": r_l-p_l, "الشحن ($)": r_u, "المدفوع ($)": p_u, "المتبقي ($)": r_u-p_u}])
                total_lyd = r_l
                total_usd = r_u
                
                th = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
                tr = "".join(f"<tr><td>{r['اسم الزبون']}</td><td>{r['عدد الحاويات']}</td><td>{r['المطلوب (د.ل)']:,.2f}</td><td>{r['المدفوع (د.ل)']:,.2f}</td><td style='color:red;'>{r['المتبقي (د.ل)']:,.2f}</td><td>${r['الشحن ($)']:,.2f}</td><td>${r['المدفوع ($)']:,.2f}</td><td style='color:red;'>${r['المتبقي ($)']:,.2f}</td></tr>" for _, r in df_display.iterrows())
                html_report_table = f"<div style='overflow-x:auto;'><table class='ui-table'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>"
            else:
                report_mode = "detailed"
                st.subheader(f"📋 سجل حاويات الزبون: {target_customer}")
                dfs['profit_usd'] = dfs['final_freight_usd'] - dfs['agency_freight_usd']
                df_display = dfs.copy()
                total_lyd = r_l
                total_usd = r_u
                
                h_list = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "أمر التسليم", "قيمة أ.ت", "الشحن النهائي"]
                if show_profit: h_list.extend(["شحن الوكالة", "صافي الربح"])
                th = "".join(f"<th>{h}</th>" for h in h_list)
                tr = ""
                for _, r in df_display.iterrows():
                    tr += f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f}</td><td>${r['final_freight_usd']:,.2f}</td>"
                    if show_profit: tr += f"<td>${r['agency_freight_usd']:,.2f}</td><td>${r['profit_usd']:,.2f}</td>"
                    tr += "</tr>"
                html_report_table = f"<div style='overflow-x:auto;'><table class='ui-table'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>"

        # 3. عرض الجدول على الشاشة
        st.markdown(html_report_table, unsafe_allow_html=True)
        
        # 4. أزرار الأكشن (إكسل + طباعة معزولة)
        if not df_display.empty:
            st.write("---")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                st.download_button(label="📥 تحميل التقرير المعروض بصيغة Excel", data=to_excel(df_display), file_name=f"istabraq_report_{datetime.now().strftime('%Y%m%d')}.xlsx")
            with col_btn2:
                # توليد صفحة الطباعة المعزولة وعرض الرابط كزرار
                print_html = generate_isolated_print_html(df_display, report_mode, target_customer, total_lyd, total_usd, show_profit)
                st.markdown(create_print_button(print_html), unsafe_allow_html=True)
                st.markdown("<p style='text-align:center; font-size:13px; color:#666;'>اضغط على الزر الأحمر لفتح الفاتورة في نافذة جديدة نظيفة وجاهزة للطباعة (Ctrl+P) بدون أي قص أو خلل.</p>", unsafe_allow_html=True)

        # 5. لوحة تعديل الحاويات السريعة للزبون المختار (عشان متلغيش الميزة كلياً لكن تنظمها)
        if filter_scope == "زبون محدد" and not dfs.empty:
            st.write("---")
            with st.expander("🛠️ لوحة المعالجة السريعة (تحديث بيانات حاوية ناقصة)"):
                dfs['edit_label'] = "معرف [" + dfs['id'].astype(str) + "] | بوليصة: " + dfs['bl_number'].astype(str) + " | حاوية: " + dfs['container_number'].astype(str)
                selected_edit = st.selectbox("اختر الشحنة المراد إكمال بياناتها:", dfs['edit_label'].tolist())
                if selected_edit:
                    c_row = dfs[dfs['edit_label'] == selected_edit].iloc[0]
                    with st.form("quick_edit_form_clean"):
                        m1, m2, m3 = st.columns(3)
                        with m1: u_cust = st.text_input("اسم الزبون", value=str(c_row['customer_name']), disabled=True)
                        with m2: u_cont = st.text_input("الحاوية", value=str(c_row['container_number']))
                        with m3: u_bl = st.text_input("البوليصة", value=str(c_row['bl_number']))
                        m4, m5, m6 = st.columns(3)
                        with m4: u_date = st.text_input("التاريخ", value=str(c_row['shipment_date']))
                        with m5: u_do_num = st.text_input("أمر التسليم", value=str(c_row['do_number']))
                        with m6: u_do_val = st.number_input("قيمة أمر التسليم (LYD)", value=float(c_row['do_value_lyd']))
                        m7, m8 = st.columns(2)
                        with m7: u_agency = st.number_input("شحن الوكالة (USD)", value=float(c_row['agency_freight_usd']))
                        with m8: u_final = st.number_input("الشحن النهائي (USD)", value=float(c_row['final_freight_usd']))
                        if st.form_submit_button("💾 حفظ التعديلات السحابية"):
                            u_conn = get_db_connection()
                            u_cursor = u_conn.cursor()
                            u_cursor.execute('UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s', 
                                             (u_cont.strip(), u_bl.strip(), u_date.strip(), u_do_num.strip(), u_do_val, u_agency, u_final, int(c_row['id'])))
                            u_conn.commit(); u_cursor.close(); u_conn.close()
                            st.success("تم تحديث البيانات بنجاح!")
                            st.rerun()

# ----------------- باقي الأقسام اللوجستية والمالية (محدثة وجاهزة) -----------------
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
        else:
            th = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم أمر التسليم", "قيمة أمر التسليم", "الشحن النهائي"])
            tr = "".join(f"<tr><td>{r['customer_name']}</td><td>{r['bl_number']}</td><td>{r['container_number']}</td><td>{r['shipment_date']}</td><td>{r['do_number']}</td><td>{r['do_value_lyd']:,.2f}</td><td>${r['final_freight_usd']:,.2f}</td></tr>" for _, r in df_incomplete.iterrows())
            st.markdown(f"<div style='overflow-x:auto;'><table class='ui-table'><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>", unsafe_allow_html=True)

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
