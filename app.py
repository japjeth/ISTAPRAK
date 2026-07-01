import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import plotly.graph_objects as go

# ----------------- إعدادات الصفحة والـ UI -----------------
st.set_page_config(page_title="منظومة إستبرق لإدارة الشحنات والمالية", layout="wide", initial_sidebar_state="expanded")

# حزمة الـ CSS السحابية الفاخرة لضبط هندسة الجداول الحقيقية والطباعة النظيفة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    html, body, [data-testid="stSidebar"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #f8f9fa; }
    .stHeading, .stMarkdown, p, div, label, span { text-align: right; direction: rtl; }
    
    /* استايل الأزرار والفورم */
    div.stButton > button:first-child { background-color: #1e4620; color:white; font-weight: 600; width: 100%; border-radius: 10px; height: 50px; border: none; box-shadow: 0 4px 10px rgba(30,70,32,0.2); transition: all 0.3s; }
    div.stButton > button:hover { background-color: #2e7d32; transform: translateY(-2px); box-shadow: 0 6px 15px rgba(30,70,32,0.3); }
    
    /* تصميم بطاقات الـ KPI المالية التفاعلية */
    .dashboard-kpi-container { display: flex; gap: 20px; flex-wrap: wrap; margin-bottom: 25px; direction: rtl; }
    .kpi-box { flex: 1; min-width: 220px; background: white; padding: 20px; border-radius: 12px; border-right: 6px solid #1e4620; box-shadow: 0 4px 12px rgba(0,0,0,0.03); }
    .kpi-box h4 { margin: 0 0 8px 0; color: #666; font-size: 14px; font-weight: 600; }
    .kpi-box p { margin: 0; font-size: 20px; font-weight: 700; color: #1e4620; }
    
    /* 📊 هندسة الجداول الحقيقية المستقرة RTL (حل نهائي وقاطع لمشكلة التداخل والانكماش الظاهر في image_0b07d4) */
    .table-responsive-container { width: 100%; overflow-x: auto; direction: rtl; margin: 20px 0; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); background: white; border: 1px solid #eef2e6; }
    table.enterprise-rtl-table { width: 100%; border-collapse: collapse; direction: rtl; text-align: right; }
    table.enterprise-rtl-table th { background-color: #1e4620; color: white; padding: 16px 20px; font-weight: 600; font-size: 14px; border-bottom: 2px solid #143316; white-space: nowrap; }
    table.enterprise-rtl-table td { padding: 14px 20px; text-align: right; border-bottom: 1px solid #f0f4ee; color: #333333; font-size: 14px; font-weight: 500; white-space: nowrap; }
    table.enterprise-rtl-table tr:nth-child(even) { background-color: #fcfdfe; }
    table.enterprise-rtl-table tr:hover { background-color: #f4f8f4; }

    /* 📜 تصميم كشف الحساب الملوكي الفخم المخصص للطباعة والحفظ الفوري */
    .printable-report { background-color: white !important; padding: 50px; border: 2px solid #000000; border-radius: 8px; direction: rtl; text-align: right; margin-top: 35px; color: #000000 !important; box-shadow: 0 4px 20px rgba(0,0,0,0.02); }
    .report-header { text-align: center; border-bottom: 4px double #1e4620; padding-bottom: 20px; margin-bottom: 30px; }
    .report-header h1 { color: #1e4620 !important; font-weight: 700; margin: 0; font-size: 26px; }
    .report-info-table { width: 100%; margin-bottom: 25px; font-size: 15px; color: #000000 !important; }
    .report-info-table td { padding: 6px; border: none !important; }
    
    table.print-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; color: #000000 !important; }
    table.print-table th { background-color: #f2f2f2 !important; color: #1e4620 !important; border: 1px solid #000000 !important; padding: 12px; font-weight: bold; text-align: right; }
    table.print-table td { border: 1px solid #000000 !important; padding: 12px; text-align: right; color: #000000 !important; }
    
    .print-totals-zone { margin-top: 35px; padding: 20px; background-color: #fcfcf9; border: 1px solid #000000; border-radius: 6px; color: #000000 !important; }
    .print-signatures { margin-top: 60px; width: 100%; display: flex; justify-content: space-between; font-weight: bold; font-size: 15px; color: #000000 !important; }
    
    /* 🖨️ السحر الفولاذي الحاسم للطباعة: يخفي كل شائبة في السيستم ويترك فقط الفاتورة الملوكية النظيفة */
    @media print {
        body * { visibility: hidden !important; }
        .printable-report, .printable-report * { visibility: visible !important; }
        .printable-report { position: absolute !important; left: 0 !important; top: 0 !important; width: 100% !important; border: none !important; padding: 0 !important; margin: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- 🌐 الاتصال بقاعدة البيانات السحابية -----------------
def get_db_connection():
    try:
        db_url = st.secrets["postgres"]["url"]
        conn = psycopg2.connect(db_url, cursor_factory=DictCursor)
        return conn
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
    cursor.close()
    conn.close()

init_db()

def safe_float(val):
    if pd.isnull(val): return 0.0
    try:
        if isinstance(val, (datetime, pd.Timestamp)): return 0.0
        return float(val)
    except: return 0.0

# ----------------- دالة بناء ورندرة جداول الـ HTML المستقرة RTL -----------------
def render_custom_html_grid(df, show_profit=False):
    """رندرة جدول HTML حقيقي يدعم الترتيب الصارم المطلوب من اليمين لليسار"""
    # ترتيب الأعمدة من اليمين لليسار بدقة متناهية وبدون تداخل
    headers = ["اسم الزبون", "رقم البوليصة", "رقم الحاوية", "التاريخ", "رقم أمر التسليم", "قيمة أمر التسليم (د.ل)", "الشحن النهائي ($)"]
    if show_profit:
        headers.extend(["شحن الوكالة ($)", "صافي الربح ($)"])
        
    # بناء هيدر الجدول
    th_html = "".join(f"<th>{h}</th>" for h in headers)
    
    # بناء صفوف الجدول ببيانات منسقة ومقروءة
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
        if show_profit:
            tr_html += f"<td>${row['agency_freight_usd']:,.2f}</td>"
            tr_html += f"<td>${row['profit_usd']:,.2f}</td>"
        tr_html += "</tr>"
        
    html_grid = f"""
    <div class="table-responsive-container">
        <table class="enterprise-rtl-table">
            <thead><tr>{th_html}</tr></thead>
            <tbody>{tr_html}</tbody>
        </table>
    </div>
    """
    st.markdown(html_grid, unsafe_allow_html=True)

# ----------------- 📝 نافذة التعديل المنبثقة التفاعلية السحابية -----------------
@st.dialog("📝 تعديل وإكمال بيانات الحاوية سحابياً")
def edit_container_modal(shipment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM shipments WHERE id = %s", (shipment_id,))
    row = cursor.fetchone()
    if row:
        st.write(f"⚙️ تحديث بيانات الحاوية التابعة لحساب: **{row['customer_name']}**")
        ec1, ec2 = st.columns(2)
        with ec1: u_container = st.text_input("رقم الحاوية", value=str(row['container_number']))
        with ec2: u_bl = st.text_input("رقم البوليصة", value=str(row['bl_number']))
        ec3, ec4, ec5 = st.columns(3)
        with ec3: u_date = st.text_input("التاريخ (YYYY-MM-DD)", value=str(row['shipment_date']))
        with ec4: u_do_num = st.text_input("رقم أمر التسليم", value=str(row['do_number']))
        with ec5: u_do_val = st.number_input("قيمة أمر التسليم (LYD)", value=float(row['do_value_lyd']))
        ec6, ec7 = st.columns(2)
        with ec6: u_agency = st.number_input("شحن الوكالة (USD)", value=float(row['agency_freight_usd']))
        with ec7: u_final = st.number_input("الشحن النهائي للزبون (USD)", value=float(row['final_freight_usd']))
        st.write("---")
        if st.button("💾 حفظ التحديث ومزامنة البيانات أونلاين"):
            cursor.execute('''
                UPDATE shipments SET container_number=%s, bl_number=%s, shipment_date=%s, do_number=%s, do_value_lyd=%s, agency_freight_usd=%s, final_freight_usd=%s WHERE id=%s
            ''', (u_container, u_bl, u_date, u_do_num, u_do_val, u_agency, u_final, shipment_id))
            conn.commit()
            cursor.close(); conn.close()
            st.success("🎉 تم تحديث بيانات الحاوية بنجاح!")
            st.rerun()
    else:
        cursor.close(); conn.close()

# ----------------- القائمة الجانبية -----------------
st.sidebar.markdown("<h2 style='text-align: center; color: #1e4620; font-weight:700;'>🚢 إستبرق للوجستيات</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #4caf50;'>🌐 المنظومة السحابية المركزية</p>", unsafe_allow_html=True)
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

# ----------------- 1. لوحة التحكم والتقارير المطورة كلياً -----------------
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 لوحة تحكم ومراقبة الأداء المالي اللوجستي")
    
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty:
        st.warning("لا يوجد بيانات مسجلة حالياً أونلاين.")
    else:
        # حساب المؤشرات الكلية للمنظومة (Dashboard KPIs)
        total_cont = len(shipments_all)
        req_lyd_total = shipments_all['do_value_lyd'].sum() if not shipments_all.empty else 0.0
        req_usd_total = shipments_all['final_freight_usd'].sum() if not shipments_all.empty else 0.0
        
        st.markdown(f"""
        <div class="dashboard-kpi-container">
            <div class="kpi-box"><h4>📦 إجمالي الحاويات المشغولة</h4><p>{total_cont} حاوية</p></div>
            <div class="kpi-box"><h4>💵 إجمالي ذمم أوامر التسليم</h4><p>{req_lyd_total:,.2f} د.ل</p></div>
            <div class="kpi-box"><h4>💵 إجمالي شحن دولار مطلوب</h4><p>${req_usd_total:,.2f}</p></div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("⚙️ محرك الفلترة الذكي وتحديد هيكلة كشوفات الحساب", expanded=True):
            rc1, rc2 = st.columns(2)
            with rc1: report_scope = st.radio("نطاق البحث المالي:", ["كل الزبائن (تقرير إجمالي عام)", "زبون محدد (تقرير تفصيلي)"], horizontal=True)
            with rc2: show_agency_price = st.checkbox("إظهار شحن الوكالة وحساب صافي أرباح الشركة في الجداول", value=False)
            st.write("---")
            if report_scope == "زبون محدد (تقرير تفصيلي)":
                selected_customer = st.selectbox("اختر اسم حساب الزبون المستهدف:", list(customers_df['name']))
                
        st.write("---")
        
        # 🟢 الحالة الأولى: التقرير الإجمالي العام لجميع الزبائن (كل زبون في صف)
        if report_scope == "كل الزبائن (تقرير إجمالي عام)":
            st.subheader("📋 كشف ملخص أرصاد الحسابات لجميع الزبائن")
            summary_data = []
            for cust in customers_df['name']:
                cust_shipments = shipments_all[shipments_all['customer_name'] == cust]
                cust_receipts = receipts_all[receipts_all['customer_name'] == cust]
                
                req_lyd = cust_shipments['do_value_lyd'].sum() if not cust_shipments.empty else 0.0
                req_usd = cust_shipments['final_freight_usd'].sum() if not cust_shipments.empty else 0.0
                agency_usd = cust_shipments['agency_freight_usd'].sum() if not cust_shipments.empty else 0.0
                
                paid_lyd = cust_receipts[cust_receipts['currency'] == 'دينار ليبي LYD']['amount'].sum() if not cust_receipts.empty else 0.0
                paid_usd = cust_receipts[cust_receipts['currency'] == 'دولار أمريكي USD']['amount'].sum() if not cust_receipts.empty else 0.0
                
                row_dict = {
                    "اسم الزبون": cust, "عدد الحاويات": len(cust_shipments),
                    "أوامر التسليم (د.ل)": req_lyd, "المدفوع (د.ل)": paid_lyd, "المتبقي (د.ل)": req_lyd - paid_lyd,
                    "الشحن النهائي ($)": req_usd, "المدفوع ($)": paid_usd, "المتبقي ($)": req_usd - paid_usd
                }
                summary_data.append(row_dict)
            
            df_sum = pd.DataFrame(summary_data)
            # رندرة جدول HTML نقي RTL للملخص الإجمالي
            th_sum = "".join(f"<th>{h}</th>" for h in ["اسم الزبون", "الحاويات", "المطلوب (د.ل)", "المدفوع (د.ل)", "المتبقي (د.ل)", "الشحن ($)", "المدفوع ($)", "المتبقي ($)"])
            tr_sum = ""
            for _, r in df_sum.iterrows():
                tr_sum += f"<tr><td>{r['اسم الزبون']}</td><td>{r['عدد الحاويات']}</td><td>{r['أوامر التسليم (د.ل)']:,.2f} د.ل</td><td>{r['المدفوع (د.ل)']:,.2f} د.ل</td><td style='color:red; font-weight:bold;'>{r['المتبقي (د.ل)']:,.2f} د.ل</td><td>${r['الشحن النهائي ($)']:,.2f}</td><td>${r['المدفوع ($)']:,.2f}</td><td style='color:red; font-weight:bold;'>${r['المتبقي ($)']:,.2f}</td></tr>"
            st.markdown(f'<div class="table-responsive-container"><table class="enterprise-rtl-table"><thead><tr>{th_sum}</tr></thead><tbody>{tr_sum}</tbody></table></div>', unsafe_allow_html=True)

        # 🟢 الحالة الثانية: التقرير التفصيلي لزبون محدد (هنا الابتكار الفولاذي)
        else:
            df_cust = shipments_all[shipments_all['customer_name'] == selected_customer].copy()
            cust_receipts = receipts_all[receipts_all['customer_name'] == selected_customer]
            
            req_lyd = df_cust['do_value_lyd'].sum() if not df_cust.empty else 0.0
            req_usd = df_cust['final_freight_usd'].sum() if not df_cust.empty else 0.0
            paid_lyd = cust_receipts[cust_receipts['currency'] == 'دينار ليبي LYD']['amount'].sum() if not cust_receipts.empty else 0.0
            paid_usd = cust_receipts[cust_receipts['currency'] == 'دولار أمريكي USD']['amount'].sum() if not cust_receipts.empty else 0.0
            
            # كروت مالية خاصة بالزبون المختار
            st.write(f"### 📊 الموقف المالي الحالي لحساب: {selected_customer}")
            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown(f"""<div class='metric-card' style='border-right-color: #2196f3;'>
                    <h5>💵 حساب أوامر التسليم بالدينار الليبي:</h5>
                    <p>إجمالي المطلوب: <b>{req_lyd:,.2f} د.ل</b> | المدفوع: <b style='color:green;'>{paid_lyd:,.2f} د.ل</b></p>
                    <p>المتبقي بذمته صافي: <b style='color:red;'>{req_lyd - paid_lyd:,.2f} د.ل</b></p>
                </div>""", unsafe_allow_html=True)
            with mc2:
                st.markdown(f"""<div class='metric-card' style='border-right-color: #4caf50;'>
                    <h5>💵 حساب نولون الشحن بالدولار الأمريكي:</h5>
                    <p>إجمالي المطلوب: <b>${req_usd:,.2f}</b> | المدفوع: <b style='color:green;'>${paid_usd:,.2f}</b></p>
                    <p>المتبقي بذمته صافي: <b style='color:red;'>${req_usd - paid_usd:,.2f}</b></p>
                </div>""", unsafe_allow_html=True)
                
            if df_cust.empty:
                st.info("لا توجد حاويات مسجلة لهذا الزبون.")
            else:
                df_cust['profit_usd'] = df_cust['final_freight_usd'] - df_cust['agency_freight_usd']
                
                # 1. عرض جدول الـ HTML الاحترافي الثابت RTL على الشاشة (مستحيل يتشوه)
                st.write("#### 📦 سجل الحاويات المفتوحة أونلاين (عرض فقط):")
                render_custom_html_grid(df_cust, show_profit=show_agency_price)
                
                # 2. لوحة التحكم والتحضير للعمليات (تعديل / طباعة تفصيلية منتقاة)
                st.write("---")
                st.markdown("### ⚙️ لوحة المعالجة الذكية والتحكم في كشوفات الحساب:")
                
                # تجهيز قائمة الاختيارات النصية السلسة والواضحة لربط العمليات بالـ ID الفعلي
                df_cust['process_label'] = "معرف [" + df_cust['id'].astype(str) + "] | بوليصة: " + df_cust['bl_number'].astype(str) + " | حاوية: " + df_cust['container_number'].astype(str)
                
                # صندوق الاختيار المتعدد السلس والآمن (اختر 5 من أصل 50 براحتك وبدون حساسية نقر)
                selected_shipments = st.multiselect(
                    "اضغط هنا وانقر على أرقام الحاويات/البوالص المراد تعديلها أو طباعتها فقط (اتركها فارغة لتحديد الكل تلقائياً):",
                    options=df_cust['process_label'].tolist()
                )
                
                # تصفية البيانات لحظياً بناءً على اختيار المستخدم
                if selected_shipments:
                    df_chosen_units = df_cust[df_cust['process_label'].isin(selected_shipments)]
                else:
                    df_chosen_units = df_cust.copy() # لو سابها فاضية يحسب الكل تلقائياً
                    
                st.write("")
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    # زر التعديل الصريح يفتح فقط في حالة تظليل حاوية واحدة منعاً للتداخل
                    if len(selected_shipments) == 1:
                        target_db_id = int(df_chosen_units.iloc[0]['id'])
                        if st.button("📝 تعديل وإكمال بيانات الحاوية المختارة"):
                            edit_container_modal(target_db_id)
                    else:
                        st.info("💡 لتعديل بيانات شحنة، يرجى اختيار حاوية واحدة فقط من القائمة أعلاه.")
                        
                with btn_col2:
                    # زر توليد الفاتورة وكشف الحساب الملوكي المخصص للطباعة
                    generate_invoice = st.button("🖨️ توليد كشف الحساب الفاخر الجاهز للطباعة والـ PDF")
                    
                if generate_invoice:
                    st.success("🎉 تم توليد كشف الحساب بنجاح! اضغط الآن على Ctrl + P من لوحة المفاتيح لبدء الطباعة الفورية.")
                    
                    total_lyd_print = df_chosen_units['do_value_lyd'].sum()
                    total_usd_print = df_chosen_units['final_freight_usd'].sum()
                    
                    # بناء صفوف جدول الطباعة الجمركي الأسود الصارم
                    print_rows_html = ""
                    for _, r in df_chosen_units.iterrows():
                        agency_td_p = f"<td>${r['agency_freight_usd']:,.2f}</td>" if show_agency_price else ""
                        profit_td_p = f"<td>${r['profit_usd']:,.2f}</td>" if show_agency_price else ""
                        print_rows_html += f"""
                        <tr>
                            <td>{r['customer_name']}</td>
                            <td>{r['bl_number']}</td>
                            <td>{r['container_number']}</td>
                            <td>{r['shipment_date']}</td>
                            <td>{r['do_number']}</td>
                            <td>{r['do_value_lyd']:,.2f} د.ل</td>
                            <td>${r['final_freight_usd']:,.2f}</td>
                            {agency_td_p}
                            {profit_td_p}
                        </tr>
                        """
                        
                    th_agency_p = "<th>شحن الوكالة</th>" if show_agency_price else ""
                    th_profit_p = "<th>صافي الربح</th>" if show_agency_price else ""
                    
                    # 👑 الفاتورة الملوكية المطورة للطباعة الرسمية (مستحيل تتشوه ومحمية ضد الحجب الجانبي)
                    st.markdown(f"""
                    <div class="printable-report">
                        <div class="report-header">
                            <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1>
                            <p style="margin:6px 0 0 0; color:#444; font-size:14px;">المركز الرئيسي: مصراتة - ليبيا | هاتف: الحسابات المركزية</p>
                        </div>
                        <table class="report-info-table">
                            <tr>
                                <td><b>كشف حساب جاري للعميل:</b> {selected_customer}</td>
                                <td style="text-align: left;"><b>تاريخ الاستخراج:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                            </tr>
                            <tr>
                                <td><b>نوع الوثيقة:</b> كشف حاويات تفصيلي منتقى ومصفى</td>
                                <td style="text-align: left;"><b>عدد الشحنات المدرجة:</b> {len(df_chosen_units)} حاوية</td>
                            </tr>
                        </table>
                        <table class="print-table">
                            <thead>
                                <tr>
                                    <th>اسم الزبون</th>
                                    <th>رقم البوليصة</th>
                                    <th>رقم الحاوية</th>
                                    <th>التاريخ</th>
                                    <th>رقم أمر التسليم</th>
                                    <th>قيمة أمر التسليم</th>
                                    <th>الشحن النهائي</th>
                                    {th_agency_p}
                                    {th_profit_p}
                                </tr>
                            </thead>
                            <tbody>
                                {print_rows_html}
                            </tbody>
                        </table>
                        <div class="print-totals-zone">
                            <div style="width:100%; text-align:left; font-size:16px; margin-bottom:8px; color:#000;">
                                <b>إجمالي قيمة أوامر التسليم المذكورة:</b> <span style="border-bottom: 2px double #000; padding-bottom:2px;">{total_lyd_print:,.2f} دينار ليبي</span>
                            </div>
                            <div style="width:100%; text-align:left; font-size:16px; color:#000;">
                                <b>إجمالي مطلوب نولون الشحن الدولي:</b> <span style="border-bottom: 2px double #000; padding-bottom:2px;">${total_usd_print:,.2f} دولار أمريكي</span>
                            </div>
                        </div>
                        <div class="print-signatures">
                            <div>الختم الرسمي للشركة: .........................</div>
                            <div>توقيع وتصديق قسم الحسابات: .........................</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- باقي الأقسام (محدثة بالكامل ومتوافقة مع PostgreSQL %s) -----------------
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
            cond = ((df_filtered['container_number'].isna()) | (df_filtered['container_number'] == "") | (df_filtered['bl_number'].isna()) | (df_filtered['bl_number'] == "") | (df_filtered['do_value_lyd'] == 0) | (df_filtered['final_freight_usd'] == 0))
        elif missing_type == "قيمة الشحن النهائي ناقصة": cond = (df_filtered['final_freight_usd'] == 0) | (df_filtered['final_freight_usd'].isna())
        elif missing_type == "قيمة أمر التسليم ناقصة": cond = (df_filtered['do_value_lyd'] == 0) | (df_filtered['do_value_lyd'].isna())
        df_incomplete = df_filtered[cond].copy()
        if df_incomplete.empty: st.success("🎉 كل البيانات مكتملة ولا يوجد نواقص.")
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
            submit_receipt = st.form_submit_button("💾 حفظ وإدراج الإيصال في الحساب المالي السحابي")
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
                select_all = st.checkbox(f"🔄 تحديد جميع الحاويات الحالية لـ {target_cust}")
                default_selection = list(shipment_options.keys()) if select_all else []
                selected_labels = st.multiselect("اختر الحاويات المراد حذفها:", options=list(shipment_options.keys()), default=default_selection)
                if selected_labels:
                    confirm_word = st.text_input("أكتب كلمة 'حذف' لتأكيد الشطب:")
                    if st.button("🗑️ تنفيذ حذف الحاويات المحددة"):
                        if confirm_word == "حذف":
                            ids_to_delete = [shipment_options[lbl] for lbl in selected_labels]
                            cursor.execute("DELETE FROM shipments WHERE id = ANY(%s)", (ids_to_delete,))
                            conn.commit(); st.success("تم المسح بنجاح!"); st.rerun()
    with tab2:
        clear_financials = st.checkbox("مسح إيصالات القبض وقائمة أسماء الزبائن أيضاً")
        confirm_all = st.text_input("لتأكيد التصفير، اكتب عبارة 'Core-Reset' في الفراغ أدناه:")
        if st.button("💥 بدء التصفير الشامل والنهائي"):
            if confirm_all == "Core-Reset":
                cursor.execute("TRUNCATE TABLE shipments RESTART IDENTITY")
                if clear_financials:
                    cursor.execute("TRUNCATE TABLE receipts RESTART IDENTITY")
                    cursor.execute("TRUNCATE TABLE customers RESTART IDENTITY")
                conn.commit(); st.success("تم تصفير المنظومة بنجاح!"); st.rerun()
    cursor.close(); conn.close()
