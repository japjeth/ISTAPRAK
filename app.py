import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import DictCursor
from datetime import datetime
import io
import plotly.graph_objects as go

# ----------------- إعدادات الصفحة والـ UI -----------------
st.set_page_config(page_title="منظومة إستبرق لإدارة الشحنات والمالية", layout="wide", initial_sidebar_state="expanded")

# تصميم واجهة مستخدم فاخرة ومستقرة تدعم اللغة العربية والجداول الحقيقية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
    html, body, [data-testid="stSidebar"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #fcfcfc; }
    .stHeading, .stMarkdown, p, div, label, span { text-align: right; direction: rtl; }
    
    /* استايل الأزرار والفورم */
    div.stButton > button:first-child { background-color: #1e4620; color:white; font-weight: 600; width: 100%; border-radius: 10px; height: 48px; border: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    div.stButton > button:hover { background-color: #2e7d32; color: white; }
    .metric-card { background-color: #ffffff; padding: 22px; border-radius: 14px; border-right: 6px solid #1e4620; box-shadow: 0 4px 15px rgba(0,0,0,0.04); margin-bottom: 20px; }
    
    /* 📊 هندسة الجداول الحقيقية المستقرة RTL (حل مشكلة التداخل والانكماش تماماً) */
    .table-container { width: 100%; overflow-x: auto; direction: rtl; text-align: right; margin: 15px 0; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    table.excel-styled-table { width: 100%; border-collapse: collapse; font-family: 'Cairo', sans-serif; font-size: 14px; min-width: 100%; direction: rtl; }
    table.excel-styled-table th { background-color: #1e4620; color: white; padding: 14px 18px; text-align: right; border: 1px solid #dee2e6; font-weight: 600; white-space: nowrap; }
    table.excel-styled-table td { padding: 12px 18px; text-align: right; border: 1px solid #dee2e6; white-space: nowrap; color: #333; font-weight: 500; }
    table.excel-styled-table tr:nth-child(even) { background-color: #f9fbf9; }
    table.excel-styled-table tr:hover { background-color: #f1f5f1; }

    /* 📜 تصميم كشف الحساب الفاخر المخصص للطباعة الجمركية وللزبائن */
    .printable-report { background-color: white !important; padding: 40px; border: 2px solid #1e4620; border-radius: 8px; direction: rtl; text-align: right; margin-top: 30px; color: #000000 !important; }
    .report-header { text-align: center; border-bottom: 4px double #1e4620; padding-bottom: 20px; margin-bottom: 25px; }
    .report-header h1 { color: #1e4620 !important; font-weight: 700; margin: 0; font-size: 26px; }
    .report-info-table { width: 100%; margin-bottom: 25px; font-size: 15px; color: #000000 !important; }
    .report-info-table td { padding: 6px; border: none !important; }
    
    table.print-table { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; color: #000000 !important; }
    table.print-table th { background-color: #f5f5f2 !important; color: #1e4620 !important; border: 1px solid #000000 !important; padding: 12px; font-weight: bold; text-align: right; }
    table.print-table td { border: 1px solid #000000 !important; padding: 12px; text-align: right; color: #000000 !important; font-weight: 500; }
    
    .print-totals-box { margin-top: 30px; padding: 15px; background-color: #fafafa; border: 1px solid #000000; border-radius: 6px; color: #000000 !important; }
    .signature-area { margin-top: 50px; width: 100%; display: flex; justify-content: space-between; font-weight: bold; font-size: 14px; }
    
    /* 🖨️ حجب شامل متكامل لكافة عناصر النظام عند الضغط على زر الطباعة */
    @media print {
        body * { visibility: hidden !important; }
        .printable-report, .printable-report * { visibility: visible !important; }
        .printable-report { position: absolute !important; left: 0 !important; top: 0 !important; width: 100% !important; border: none !important; padding: 0 !important; margin: 0 !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# ----------------- الاتصال بقاعدة البيانات السحابية -----------------
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

# ----------------- دالة الرندرة الذكية للجداول RTL 100% -----------------
def render_html_rtl_table(df, show_agency=False):
    """بناء داتا فريم مخصصة وترتيب أعمدتها برمجياً من اليمين لليسار بدقة متناهية"""
    cols = ['اسم الزبون', 'رقم البوليصة', 'رقم الحاوية', 'التاريخ', 'رقم أمر التسليم', 'قيمة أمر التسليم (د.ل)', 'الشحن النهائي ($)']
    if show_agency:
        cols.extend(['شحن الوكالة ($)', 'صافي الربح ($)'])
        
    cols = [c for c in cols if c in df.columns]
    display_df = df[cols].copy()
    
    # تنسيق الأرقام والعملات لراحة العين
    if 'قيمة أمر التسليم (د.ل)' in display_df.columns:
        display_df['قيمة أمر التسليم (د.ل)'] = display_df['قيمة أمر التسليم (د.ل)'].map(lambda x: f"{x:,.2f} د.ل")
    if 'الشحن النهائي ($)' in display_df.columns:
        display_df['الشحن النهائي ($)'] = display_df['الشحن النهائي ($)'].map(lambda x: f"${x:,.2f}")
    if 'شحن الوكالة ($)' in display_df.columns:
        display_df['شحن الوكالة ($)'] = display_df['شحن الوكالة ($)'].map(lambda x: f"${x:,.2f}")
    if 'صافي الربح ($)' in display_df.columns:
        display_df['صافي الربح ($)'] = display_df['صافي الربح ($)'].map(lambda x: f"${x:,.2f}")
        
    html_table = display_df.to_html(classes='excel-styled-table', index=False, escape=False)
    st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)

# ----------------- 📝 نافذة التعديل المنبثقة التفاعلية -----------------
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

# ----------------- 1. لوحة التحكم والتقارير -----------------
if menu == "📊 لوحة التحكم والتقارير":
    st.title("📊 شاشة الموقف المالي والتقارير المتقدمة")
    
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments", conn)
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    conn.close()
    
    if customers_df.empty:
        st.warning("لا يوجد بيانات مسجلة حالياً أونلاين.")
    else:
        with st.expander("⚙️ محرك الفلترة وتحديد نوع التقرير المطلوب", expanded=True):
            rc1, rc2 = st.columns(2)
            with rc1: report_scope = st.radio("نطاق التقرير المستهدف:", ["كل الزبائن الممسكين", "زبون محدد فردي"], horizontal=True)
            with rc2: report_type = st.radio("نوع هيكل التقرير:", ["تقرير تفصيلي (سجل الحاويات وحصرها)", "تقرير إجمالي (الملخص والتحليل المالي)"], horizontal=True)
            st.write("---")
            cc1, cc2 = st.columns(2)
            with cc1:
                if report_scope == "زبون محدد فردي": selected_customer = st.selectbox("اختر اسم الزبون المعني:", list(customers_df['name']))
                else: selected_customer = "الكل"
            with cc2: show_agency_price = st.checkbox("إظهار قيمة شحن الوكالة وصافي الأرباح", value=False)

        st.write("---")
        
        # 1️⃣ تقرير إجمالي لكل الزبائن
        if report_scope == "كل الزبائن الممسكين" and report_type == "تقرير إجمالي (الملخص والتحليل المالي)":
            st.subheader("📋 تقرير الأرصاد والتحليل الإجمالي لجميع الزبائن")
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
                    "أوامر التسليم (د.ل)": f"{req_lyd:,.2f} د.ل", "المدفوع (د.ل)": f"{paid_lyd:,.2f} د.ل", "المتبقي (د.ل)": f"{req_lyd - paid_lyd:,.2f} د.ل",
                    "الشحن النهائي ($)": f"${req_usd:,.2f}", "المدفوع ($)": f"${paid_usd:,.2f}", "المتبقي ($)": f"${req_usd - paid_usd:,.2f}"
                }
                summary_data.append(row_dict)
            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

        # 2️⃣ تقرير تفصيلي لكل أو زبون محدد (تم دمج المنظومة الفولاذية الجديدة هنا)
        else:
            # تصفية البيانات حسب خيار المستخدم
            df_filtered = shipments_all.copy()
            if report_scope == "زبون محدد فردي":
                df_filtered = df_filtered[df_filtered['customer_name'] == selected_customer]
                st.subheader(f"📋 سجل الحاويات التفصيلي للزبون: {selected_customer}")
            else:
                st.subheader("📋 التقرير التفصيلي الشامل لكافة حاويات المنظومة")
                
            if df_filtered.empty:
                st.info("لا توجد حاويات مسجلة في نطاق البحث هذا.")
            else:
                df_filtered['profit_usd'] = df_filtered['final_freight_usd'] - df_filtered['agency_freight_usd']
                df_filtered = df_filtered.rename(columns={
                    'id': 'معرف', 'customer_name': 'اسم الزبون', 'bl_number': 'رقم البوليصة',
                    'container_number': 'رقم الحاوية', 'shipment_date': 'التاريخ', 'do_number': 'رقم أمر التسليم',
                    'do_value_lyd': 'قيمة أمر التسليم (د.ل)', 'agency_freight_usd': 'شحن الوكالة ($)', 'final_freight_usd': 'الشحن النهائي ($)', 'profit_usd': 'صافي الربح ($)'
                })
                
                # 💥 عرض الجدول الملوكي بتقنية الـ HTML النقي (RTL 100% مستحيل يتداخل أو ينكمش)
                render_html_rtl_table(df_filtered, show_agency=show_agency_price)
                
                st.write("---")
                st.markdown("### ⚙️ لوحة التحكم التفاعلية بالشحنات (تعديل / طباعة انتقائية):")
                
                # إنشاء نص ذكي داخل صندوق الاختيار ليسهل التعرف على الحاوية
                df_filtered['search_label'] = "معرف [" + df_filtered['معرف'].astype(str) + "] | بوليصة: " + df_filtered['رقم البوليصة'].astype(str) + " | حاوية: " + df_filtered['رقم الحاوية'].astype(str) + " (" + df_filtered['اسم الزبون'] + ")"
                
                # 🎯 صندوق الاختيار المتعدد الذكي لطباعة 5 من أصل 50 مثلاً
                selected_labels = st.multiselect(
                    "اضغط هنا واختر الحاوية / الحاويات المستهدفة لإجراء العملية:",
                    options=df_filtered['search_label'].tolist()
                )
                
                if selected_labels:
                    df_chosen_units = df_filtered[df_filtered['search_label'].isin(selected_labels)]
                    
                    st.write("")
                    btn_c1, btn_c2 = st.columns(2)
                    
                    with btn_c1:
                        # زر التعديل الصريح يفتح فقط في حالة اختيار حاوية واحدة
                        if len(selected_labels) == 1:
                            target_id = int(df_chosen_units.iloc[0]['معرف'])
                            if st.button("📝 تعديل بيانات الحاوية المختارة"):
                                edit_container_modal(target_id)
                        else:
                            st.info("💡 لتعديل شحنة، يرجى اختيار سطر واحد فقط من القائمة أعلاه.")
                            
                    with btn_c2:
                        # زر الطباعة الفورية الفاخرة
                        print_trigger = st.button("🖨️ توليد كشف الحساب الفاخر للطباعة")
                        
                    if print_trigger:
                        total_lyd_p = df_chosen_units['قيمة أمر التسليم (د.ل)'].sum()
                        total_usd_p = df_chosen_units['الشحن النهائي ($)'].sum()
                        
                        rows_html = ""
                        for _, r in df_chosen_units.iterrows():
                            agency_td = f"<td>${r['شحن الوكالة ($)']:,.2f}</td>" if show_agency_price else ""
                            profit_td = f"<td>${r['صافي الربح ($)']:,.2f}</td>" if show_agency_price else ""
                            rows_html += f"""
                            <tr>
                                <td>{r['اسم الزبون']}</td>
                                <td>{r['رقم البوليصة']}</td>
                                <td>{r['رقم الحاوية']}</td>
                                <td>{r['التاريخ']}</td>
                                <td>{r['رقم أمر التسليم']}</td>
                                <td>{r['قيمة أمر التسليم (د.ل)']:,.2f} د.ل</td>
                                <td>${r['الشحن النهائي ($)']:,.2f}</td>
                                {agency_td}
                                {profit_td}
                            </tr>
                            """
                        
                        agency_th = "<th>شحن الوكالة</th>" if show_agency_price else ""
                        profit_th = "<th>صافي الربح</th>" if show_agency_price else ""
                        
                        # 👑 قالب كشف الحساب الرسمي الملوكي للطباعة (مقاوم للتشوه تماماً)
                        st.markdown(f"""
                        <div class="printable-report">
                            <div class="report-header">
                                <h1>شركة إستبرق الدولية للشحن والخدمات اللوجستية</h1>
                                <p style="margin:5px 0 0 0; color:#555;">مصراتة - ليبيا | كشف حساب حاويات تفصيلي معتمد</p>
                            </div>
                            <table class="report-info-table">
                                <tr>
                                    <td><b>نوع الكشف:</b> كشف حساب حاويات منتقاة بدقة</td>
                                    <td style="text-align: left;"><b>تاريخ الاستخراج:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}</td>
                                </tr>
                                <tr>
                                    <td><b>الحالة المالية:</b> تحت المراجعة والتدقيق الجمركي</td>
                                    <td style="text-align: left;"><b>عدد شحنات الكشف:</b> {len(df_chosen_units)} حاوية مدرجة</td>
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
                                       {agency_th}
                                       {profit_th}
                                   </tr>
                               </thead>
                               <tbody>
                                   {rows_html}
                               </tbody>
                            </table>
                            <div class="print-totals-box">
                                <div style="width:100%; text-align:left; font-size:15px; margin-bottom:6px;">
                                    <b>إجمالي قيمة أوامر التسليم المستحقة:</b> {total_lyd_p:,.2f} دينار ليبي
                                </div>
                                <div style="width:100%; text-align:left; font-size:15px;">
                                    <b>إجمالي قيمة الشحن الدولي المستحقة:</b> ${total_usd_p:,.2f} دولار أمريكي
                                </div>
                            </div>
                            <div class="signature-area">
                                <div>ختم الشركة الرسمي: .........................</div>
                                <div>توقيع واعتماد الحسابات: .........................</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

# ----------------- الأقسام المتبقية (محدثة بالكامل سحابياً %s) -----------------
elif menu == "⚠️ الحاويات غير المكتملة":
    st.title("⚠️ محرك فحص وتحديد البيانات الناقصة في الحاويات")
    conn = get_db_connection()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    shipments_all = pd.read_sql_query("SELECT * FROM shipments", conn)
    conn.close()
    
    if shipments_all.empty: st.info("لا توجد شحنات.")
    else:
        with st.expander("🔍 خيارات تحديد نوع النقص المستهدف", expanded=True):
            fc1, fc2 = st.columns(2)
            with fc1: filter_cust = st.selectbox("تصفية لحساب زبون معين:", ["كل الزبائن"] + list(customers_df['name']))
            with fc2: missing_type = st.selectbox("نوع البيان المفقود المستهدف:", ["أي بيان ناقص بالكامل", "قيمة الشحن النهائي ناقصة", "قيمة أمر التسليم ناقصة", "رقم أمر التسليم ناقص"])
        
        df_filtered = shipments_all.copy()
        if filter_cust != "كل الزبائن": df_filtered = df_filtered[df_filtered['customer_name'] == filter_cust]
            
        if missing_type == "أي بيان ناقص بالكامل":
            cond = ((df_filtered['container_number'].isna()) | (df_filtered['container_number'] == "") |
                    (df_filtered['bl_number'].isna()) | (df_filtered['bl_number'] == "") |
                    (df_filtered['do_number'].isna()) | (df_filtered['do_number'] == "") |
                    (df_filtered['do_value_lyd'] == 0) | (df_filtered['do_value_lyd'].isna()) |
                    (df_filtered['final_freight_usd'] == 0) | (df_filtered['final_freight_usd'].isna()))
        elif missing_type == "قيمة الشحن النهائي ناقصة": cond = (df_filtered['final_freight_usd'] == 0) | (df_filtered['final_freight_usd'].isna())
        elif missing_type == "قيمة أمر التسليم ناقصة": cond = (df_filtered['do_value_lyd'] == 0) | (df_filtered['do_value_lyd'].isna())
        elif missing_type == "رقم أمر التسليم ناقص": cond = (df_filtered['do_number'].isna()) | (df_filtered['do_number'] == "")
            
        df_incomplete = df_filtered[cond].copy()
        st.write("---")
        if df_incomplete.empty: st.success("🎉 ممتاز! لا توجد أي حاويات ينطبق عليها هذا النقص.")
        else:
            df_incomplete = df_incomplete.rename(columns={
                'id': 'معرف الشحنة', 'customer_name': 'اسم الزبون', 'bl_number': 'رقم البوليصة', 
                'container_number': 'رقم الحاوية', 'shipment_date': 'التاريخ', 'do_number': 'رقم أمر التسليم',
                'do_value_lyd': 'قيمة أمر التسليم (د.ل)', 'agency_freight_usd': 'شحن الوكالة ($)', 'final_freight_usd': 'الشحن النهائي ($)'
            })
            render_html_rtl_table(df_incomplete, show_agency=False)

elif menu == "💰 إيصالات القبض والمالية":
    st.title("💰 إدارة المدفوعات وإيصالات قبض الزبائن")
    conn = get_db_connection()
    cursor = conn.cursor()
    customers_df = pd.read_sql_query("SELECT * FROM customers", conn)
    
    if customers_df.empty: st.warning("يرجى إضافة زبائن أولاً لتتمكن من تسجيل إيصالات قبض لهم.")
    else:
        st.subheader("➕ تسجيل إيصال قبض جديد")
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
                conn.commit()
                st.success(f"🎉 تم تسجيل الإيصال بنجاح!")
                    
        st.write("---")
        st.subheader("📋 سجل آخر 10 إيصالات مستلمة")
        receipts_df = pd.read_sql_query("SELECT * FROM receipts ORDER BY id DESC LIMIT 10", conn)
        if not receipts_df.empty:
            view_df = receipts_df.rename(columns={"customer_name": "اسم الزبون", "amount": "المبلغ", "currency": "العملة", "receipt_date": "التاريخ", "notes": "ملاحظات"})
            st.dataframe(view_df[["اسم الزبون", "المبلغ", "العملة", "التاريخ", "ملاحظات"]], use_container_width=True, hide_index=True)
    cursor.close(); conn.close()

elif menu == "✏️ تعديل وحذف الإيصالات":
    st.title("✏️ التحكم في إيصالات القبض (تعديل / حذف)")
    conn = get_db_connection()
    cursor = conn.cursor()
    receipts_all = pd.read_sql_query("SELECT * FROM receipts", conn)
    
    if receipts_all.empty: st.info("لا توجد إيصالات قبض مسجلة حالياً.")
    else:
        search_receipt = st.text_input("🔍 ابحث هنا لتصفية الإيصالات:")
        filtered_r = receipts_all.copy()
        if search_receipt.strip():
            sr = search_receipt.strip().lower()
            filtered_r = receipts_all[receipts_all['customer_name'].str.lower().str.contains(sr, na=False) | receipts_all['notes'].str.lower().str.contains(sr, na=False)]
            
        if filtered_r.empty: st.warning("لم يتم العثور على أي نتائج.")
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
            
            submit_shipment = st.form_submit_button("🚀 إضافة الشحنة وتحديث الحسابات")
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
        confirm_all = st.text_input("لتأكيد التصفير، اكتب عبارة 'Core-Reset' in الفراغ أدناه:")
        if st.button("💥 بدء التصفير الشامل والنهائي"):
            if confirm_all == "Core-Reset":
                cursor.execute("TRUNCATE TABLE shipments RESTART IDENTITY")
                if clear_financials:
                    cursor.execute("TRUNCATE TABLE receipts RESTART IDENTITY")
                    cursor.execute("TRUNCATE TABLE customers RESTART IDENTITY")
                conn.commit(); st.success("تم تصفير المنظومة بنجاح!"); st.rerun()
    cursor.close(); conn.close()
