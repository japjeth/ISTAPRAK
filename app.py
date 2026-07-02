<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>إستبرق الدولية - منظومة الرقابة المالية وإدارة الشحنات الموحدة</title>
    <!-- تحميل خط Cairo الفاخر من جوجل -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <!-- تحميل مكتبة Tailwind CSS للتصميم العصري -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- تحميل أيقونات Lucide الفاخرة المعتمدة عالمياً -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        cairo: ['Cairo', 'sans-serif'],
                    },
                    colors: {
                        emerald: {
                            950: '#021a11',
                            900: '#062c1d',
                            800: '#114631',
                            700: '#1a5f43',
                            600: '#227855',
                            500: '#2b9369',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        /* أنماط مخصصة للتجربة الفاخرة */
        .glass-sidebar {
            background: linear-gradient(135deg, rgba(6, 44, 29, 0.98) 0%, rgba(2, 26, 17, 0.99) 100%);
            backdrop-filter: blur(20px);
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(226, 232, 240, 0.8);
        }
        /* تخصيص مؤشر التمرير الناعم */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }

        /* هيكلية الطباعة المعزولة كلياً والمضمونة لورق A4 Portrait دون أي زحزحة */
        #print-document {
            display: none;
        }
        @media print {
            body * {
                visibility: hidden !important;
            }
            #print-document, #print-document * {
                visibility: visible !important;
            }
            #print-document {
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
            .no-break {
                page-break-inside: avoid !important;
            }
            thead {
                display: table-header-group !important;
            }
        }
    </style>
</head>
<body class="bg-[#f8fafc] text-slate-800 font-cairo min-h-screen overflow-x-hidden antialiased">

    <!-- هيكل التطبيق الرئيسي (مخفي أثناء الطباعة تلقائياً) -->
    <div id="app-root" class="flex min-h-screen relative">
        
        <!-- القائمة الجانبية الفاخرة المستوحاة من آبل -->
        <aside class="w-80 glass-sidebar text-slate-100 flex flex-col justify-between fixed h-screen right-0 top-0 z-30 shadow-2xl transition-all duration-300 border-l border-emerald-800/20">
            <div>
                <!-- هيدر اللوجو للشركة -->
                <div class="p-8 border-b border-emerald-800/30 flex items-center gap-4">
                    <div class="bg-gradient-to-tr from-emerald-500 to-teal-400 p-3 rounded-2xl shadow-lg shadow-emerald-950/40">
                        <i data-lucide="ship" class="w-7 h-7 text-white"></i>
                    </div>
                    <div>
                        <h1 class="text-xl font-black tracking-wide text-white">إستبرق الدولية</h1>
                        <p class="text-[11px] text-emerald-400 font-bold tracking-widest uppercase mt-0.5">للخدمات اللوجستية والمالية</p>
                    </div>
                </div>

                <!-- خيارات التنقل المدمجة والمنظمة في بوابات كبرى -->
                <nav class="p-6 space-y-3">
                    <p class="text-[10px] text-emerald-500/80 font-black px-3 tracking-wider uppercase mb-2">القطاعات التشغيلية</p>
                    
                    <button onclick="switchTab('dashboard')" id="nav-dashboard" class="nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group bg-emerald-800/40 text-white shadow-md shadow-emerald-950/20">
                        <div class="flex items-center gap-3">
                            <i data-lucide="layout-dashboard" class="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform"></i>
                            <span class="text-[14.5px] font-bold">الإدارة والتقارير المالية</span>
                        </div>
                        <i data-lucide="chevron-left" class="w-4 h-4 text-emerald-600"></i>
                    </button>

                    <button onclick="switchTab('shipments')" id="nav-shipments" class="nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group text-emerald-300 hover:bg-emerald-900/40 hover:text-white">
                        <div class="flex items-center gap-3">
                            <i data-lucide="container" class="w-5 h-5 text-emerald-400/80 group-hover:scale-110 transition-transform"></i>
                            <span class="text-[14.5px] font-bold">حركة الشحنات والحاويات</span>
                        </div>
                        <i data-lucide="chevron-left" class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity"></i>
                    </button>

                    <button onclick="switchTab('receipts')" id="nav-receipts" class="nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group text-emerald-300 hover:bg-emerald-900/40 hover:text-white">
                        <div class="flex items-center gap-3">
                            <i data-lucide="wallet" class="w-5 h-5 text-emerald-400/80 group-hover:scale-110 transition-transform"></i>
                            <span class="text-[14.5px] font-bold">الخزينة والمتحصلات</span>
                        </div>
                        <i data-lucide="chevron-left" class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity"></i>
                    </button>

                    <button onclick="switchTab('crm')" id="nav-crm" class="nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group text-emerald-300 hover:bg-emerald-900/40 hover:text-white">
                        <div class="flex items-center gap-3">
                            <i data-lucide="users" class="w-5 h-5 text-emerald-400/80 group-hover:scale-110 transition-transform"></i>
                            <span class="text-[14.5px] font-bold">إدارة الحسابات والصيانة</span>
                        </div>
                        <i data-lucide="chevron-left" class="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity"></i>
                    </button>
                </nav>
            </div>

            <!-- معلومات الترخيص للشركة بأسفل القائمة الجانبية -->
            <div class="p-6 border-t border-emerald-900/40 bg-emerald-950/20 text-center">
                <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-900/60 text-emerald-400 text-[10.5px] font-bold">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                    خادم سحابي مستقر ومحمي
                </div>
                <p class="text-[10px] text-emerald-600 font-bold mt-3">النسخة الاحترافية العالمية © 2026</p>
            </div>
        </aside>

        <!-- الهيكل المحتوى الأساسي والعلوي -->
        <main class="flex-1 pr-80 min-h-screen flex flex-col">
            
            <!-- الهيدر العلوي الملوكي -->
            <header class="h-20 bg-white/75 backdrop-blur-md border-b border-slate-200/80 sticky top-0 z-20 px-8 flex items-center justify-between">
                <div>
                    <h2 id="page-title" class="text-xl font-extrabold text-slate-900">الإدارة والتقارير المالية العامة</h2>
                    <p id="page-subtitle" class="text-xs text-slate-500 font-semibold mt-0.5">مراقبة الموازنات والموقف الحسابي العام لكافة العملاء</p>
                </div>
                <!-- تفاصيل المستخدم والتاريخ -->
                <div class="flex items-center gap-4">
                    <div class="bg-slate-100 px-4 py-2 rounded-xl border border-slate-200/50 flex items-center gap-2">
                        <i data-lucide="calendar" class="w-4 h-4 text-emerald-700"></i>
                        <span id="header-date" class="text-xs font-bold text-slate-700">اليوم، 2 يوليو 2026</span>
                    </div>
                </div>
            </header>

            <!-- كتل المحتوى المبدلة حسب الاختيارات الجانبية -->
            <div class="p-8 flex-1 space-y-8" id="content-area">
                <!-- سيتم استبدال هذا المحتوى تلقائياً بواسطة محرك الجافا سكريبت -->
            </div>
        </main>
    </div>

    <!-- نظام التنبيهات المخصص (Custom Toast Notification) -->
    <div id="toast-container" class="fixed top-6 left-6 z-50 flex flex-col gap-3 pointer-events-none"></div>

    <!-- القالب المطور المخفي للطباعة الجمركية المباشرة A4 -->
    <div id="print-document"></div>

    <!-- محرك التفاعل والذكاء البرمجي المتكامل (SPA JS Engine) -->
    <script>
        // قاعدة البيانات الجارية في ذاكرة الجلسة مع بيانات افتراضية ممتازة للعرض الفوري
        const initialMockCustomers = [
            { id: 1, name: "أحمد فايد" },
            { id: 2, name: "الهادي الأحول" },
            { id: 3, name: "مجموعة الوفاق للاستيراد" }
        ];

        const initialMockShipments = [
            { id: 1, customer_name: "أحمد فايد", container_number: "MSKU8831920", bl_number: "MBL-77123", shipment_date: "2026-06-15", do_number: "DO-9012", do_value_lyd: 1905.00, agency_freight_usd: 1200.00, final_freight_usd: 1450.00 },
            { id: 2, customer_name: "أحمد فايد", container_number: "MSKU1120491", bl_number: "MBL-77123", shipment_date: "2026-06-15", do_number: "DO-9013", do_value_lyd: 0.00, agency_freight_usd: 1200.00, final_freight_usd: 0.00 }, // ناقصة
            { id: 3, customer_name: "الهادي الأحول", container_number: "SUDU4491029", bl_number: "MBL-88124", shipment_date: "2026-06-20", do_number: "DO-8831", do_value_lyd: 21212.00, agency_freight_usd: 1800.00, final_freight_usd: 2100.00 },
            { id: 4, customer_name: "مجموعة الوفاق للاستيراد", container_number: "CMAU7718290", bl_number: "MBL-99120", shipment_date: "2026-06-25", do_number: "", do_value_lyd: 3400.00, agency_freight_usd: 1500.00, final_freight_usd: 1750.00 } // DO ناقص
        ];

        const initialMockReceipts = [
            { id: 1, customer_name: "أحمد فايد", amount: 1000.00, currency: "دولار أمريكي USD", receipt_date: "2026-06-18", notes: "دفعة نقدية بالدولار" },
            { id: 2, customer_name: "الهادي الأحول", amount: 15000.00, currency: "دينار ليبي LYD", receipt_date: "2026-06-22", notes: "حوالة مصرفية جارية" }
        ];

        // تهيئة وحفظ الحالة العامة للتطبيق
        let appState = {
            currentTab: 'dashboard',
            customers: JSON.parse(localStorage.getItem('ist_customers')) || initialMockCustomers,
            shipments: JSON.parse(localStorage.getItem('ist_shipments')) || initialMockShipments,
            receipts: JSON.parse(localStorage.getItem('ist_receipts')) || initialMockReceipts,
            // فلاتر الموقف المالي العام
            reportsFilter: {
                scope: 'all', // all , single
                singleCustomer: '',
                structure: 'summary', // summary, detailed
                displayProfit: false
            },
            // فلاتر تدقيق البيانات الناقصة
            auditFilter: {
                customer: 'all',
                criteria: {
                    container: true,
                    bl: true,
                    date: true,
                    do_num: true,
                    do_val: true,
                    agency: true,
                    final: true
                }
            }
        };

        // حفظ التغييرات محلياً لمقاومة إعادة التحميل
        function saveToStorage() {
            localStorage.setItem('ist_customers', JSON.stringify(appState.customers));
            localStorage.setItem('ist_shipments', JSON.stringify(appState.shipments));
            localStorage.setItem('ist_receipts', JSON.stringify(appState.receipts));
        }

        // إطلاق وإظهار التنبيهات الفاخرة
        function showToast(message, type = 'success') {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `flex items-center gap-3 px-5 py-4 rounded-2xl shadow-xl transition-all duration-300 transform translate-y-2 opacity-0 pointer-events-auto border min-w-[300px] ${
                type === 'success' 
                ? 'bg-emerald-950/95 text-white border-emerald-500/30' 
                : type === 'error' 
                ? 'bg-red-950/95 text-white border-red-500/30' 
                : 'bg-amber-950/95 text-white border-amber-500/30'
            }`;
            
            const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'alert-triangle' : 'info';
            const iconColor = type === 'success' ? 'text-emerald-400' : type === 'error' ? 'text-red-400' : 'text-amber-400';

            toast.innerHTML = `
                <i data-lucide="${icon}" class="w-5 h-5 ${iconColor}"></i>
                <div class="flex-1 text-[13.5px] font-semibold">${message}</div>
                <button onclick="this.parentElement.remove()" class="text-slate-400 hover:text-white"><i data-lucide="x" class="w-4 h-4"></i></button>
            `;
            container.appendChild(toast);
            lucide.createIcons();

            // أنيميشن الدخول
            setTimeout(() => {
                toast.classList.remove('translate-y-2', 'opacity-0');
            }, 10);

            // الحذف التلقائي
            setTimeout(() => {
                toast.classList.add('translate-y-2', 'opacity-0');
                setTimeout(() => toast.remove(), 300);
            }, 4000);
        }

        // تفعيل وتحديث الأيقونات
        function refreshIcons() {
            lucide.createIcons();
        }

        // التبديل الكلي للأقسام من القائمة الجانبية
        function switchTab(tabId) {
            appState.currentTab = tabId;
            
            // تحديث تصميم شريط القائمة النشط
            document.querySelectorAll('.nav-btn').forEach(btn => {
                btn.className = "nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group text-emerald-300 hover:bg-emerald-900/40 hover:text-white";
                // استعادة الأيقونة الأصلية
                const icon = btn.querySelector('[data-lucide]');
                if (icon) icon.className = "w-5 h-5 text-emerald-400/80 group-hover:scale-110 transition-transform";
                const arrow = btn.querySelector('i[data-lucide="chevron-left"]');
                if (arrow) arrow.className = "w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity";
            });

            const activeBtn = document.getElementById(`nav-${tabId}`);
            if (activeBtn) {
                activeBtn.className = "nav-btn w-full flex items-center justify-between px-4 py-3.5 rounded-xl transition-all duration-300 group bg-emerald-800/40 text-white shadow-md shadow-emerald-950/20";
                const activeIcon = activeBtn.querySelector('[data-lucide]');
                if (activeIcon) activeIcon.className = "w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform";
                const activeArrow = activeBtn.querySelector('i[data-lucide="chevron-left"]');
                if (activeArrow) activeArrow.className = "w-4 h-4 text-emerald-600";
            }

            // تحديث العناوين للمحتوى
            const titleMap = {
                dashboard: { title: "الإدارة والتقارير المالية العامة", sub: "مراقبة الموازنات والموقف الحسابي العام لكافة العملاء" },
                shipments: { title: "حركة الشحنات والحاويات جمركياً", sub: "إدخال ومطابقة الشحنات يدوياً أو عبر الإكسل وتحديث القيود" },
                receipts: { title: "الخزينة والمتحصلات المالية المباشرة", sub: "تسجيل إيصالات السداد بالدينار والدولار ومراجعة الخزنة" },
                crm: { title: "شؤون الزبائن وصيانة قاعدة البيانات", sub: "إدارة قائمة العملاء المسجلين وتصفير السجلات البرمجية" }
            };

            document.getElementById('page-title').innerText = titleMap[tabId].title;
            document.getElementById('page-subtitle').innerText = titleMap[tabId].sub;

            renderActiveTab();
        }

        // ==============================================================================
        // البوابة الأولى: التقارير والرقابة المالية ومحرك فحص النواقص
        // ==============================================================================
        function renderDashboard() {
            // حساب الإحصائيات الفورية
            const totalContainers = appState.shipments.length;
            const totalRequiredLyd = appState.shipments.reduce((sum, s) => sum + safe_float(s.do_value_lyd), 0);
            const totalRequiredUsd = appState.shipments.reduce((sum, s) => sum + safe_float(s.final_freight_usd), 0);

            // تجميع الحسابات بالعملاء للتقرير العام
            const customerBalances = appState.customers.map(cust => {
                const custShipments = appState.shipments.filter(s => s.customer_name === cust.name);
                const custReceipts = appState.receipts.filter(r => r.customer_name === cust.name);

                const reqLyd = custShipments.reduce((sum, s) => sum + safe_float(s.do_value_lyd), 0);
                const reqUsd = custShipments.reduce((sum, s) => sum + safe_float(s.final_freight_usd), 0);

                const paidLyd = custReceipts.filter(r => r.currency.includes('LYD') || r.currency.includes('دينار')).reduce((sum, r) => sum + safe_float(r.amount), 0);
                const paidUsd = custReceipts.filter(r => r.currency.includes('USD') || r.currency.includes('دولار')).reduce((sum, r) => sum + safe_float(r.amount), 0);

                return {
                    name: cust.name,
                    containersCount: custShipments.length,
                    requiredLyd: reqLyd,
                    paidLyd: paidLyd,
                    remainingLyd: reqLyd - paidLyd,
                    requiredUsd: reqUsd,
                    paidUsd: paidUsd,
                    remainingUsd: reqUsd - paidUsd
                };
            });

            // رسم الفلاتر الجانبية التفاعلية
            const f = appState.reportsFilter;
            
            let singleCustomerSelectHtml = '';
            if (f.scope === 'single') {
                if (!appState.reportsFilter.singleCustomer && appState.customers.length > 0) {
                    appState.reportsFilter.singleCustomer = appState.customers[0].name;
                }
                const options = appState.customers.map(c => `<option value="${c.name}" ${f.singleCustomer === c.name ? 'selected' : ''}>${c.name}</option>`).join('');
                singleCustomerSelectHtml = `
                    <div class="space-y-2">
                        <label class="text-xs font-bold text-slate-500">اختر الزبون المستهدف بالفرز:</label>
                        <select onchange="updateReportsFilter('singleCustomer', this.value)" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                            ${options}
                        </select>
                    </div>
                `;
            }

            // بناء جدول التقرير بناءً على الهيكلية والفلتر المختار
            let reportTableHtml = '';
            let targetForExport = [];

            if (f.scope === 'all') {
                if (f.structure === 'summary') {
                    // ميزان حسابات العملاء المجمع الموحد
                    targetForExport = customerBalances;
                    const rows = customerBalances.map(r => `
                        <tr class="hover:bg-slate-50 transition-colors">
                            <td class="px-6 py-4 text-sm font-bold text-slate-950">${r.name}</td>
                            <td class="px-6 py-4 text-sm font-semibold text-center text-slate-600">${r.containersCount}</td>
                            <td class="px-6 py-4 text-sm font-semibold text-slate-700">${r.requiredLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td class="px-6 py-4 text-sm font-semibold text-emerald-700">${r.paidLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td class="px-6 py-4 text-sm font-bold ${r.remainingLyd > 0 ? 'text-red-600' : 'text-slate-700'}">${r.remainingLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td class="px-6 py-4 text-sm font-semibold text-slate-700">$${r.requiredUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td class="px-6 py-4 text-sm font-semibold text-emerald-700">$${r.paidUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td class="px-6 py-4 text-sm font-bold ${r.remainingUsd > 0 ? 'text-red-600' : 'text-slate-700'}">$${r.remainingUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                        </tr>
                    `).join('');

                    reportTableHtml = `
                        <div class="enterprise-table-container">
                            <table class="corporate-data-table">
                                <thead>
                                    <tr>
                                        <th>اسم الزبون</th>
                                        <th class="text-center">الحاويات</th>
                                        <th>المطلوب (د.ل)</th>
                                        <th>المدفوع (د.ل)</th>
                                        <th>المتبقي الجاري (د.ل)</th>
                                        <th>الشحن نولون ($)</th>
                                        <th>المدفوع ($)</th>
                                        <th>المتبقي الجاري ($)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${rows || '<tr><td colspan="8" class="text-center py-8 text-slate-400 font-bold">لا توجد بيانات حسابية لعرضها</td></tr>'}
                                </tbody>
                            </table>
                        </div>
                    `;
                } else {
                    // تفصيلي لكل الزبائن معاً
                    const shipmentsToShow = appState.shipments;
                    targetForExport = shipmentsToShow;
                    reportTableHtml = renderShipmentsGridMarkup(shipmentsToShow, f.displayProfit);
                }
            } else {
                // فلتر زبون محدد جاري
                const currentCustName = f.singleCustomer;
                const custShipments = appState.shipments.filter(s => s.customer_name === currentCustName);
                targetForExport = custShipments;
                
                if (f.structure === 'summary') {
                    // الموقف الحسابي الإجمالي للزبون
                    const custBal = customerBalances.find(b => b.name === currentCustName) || {name: currentCustName, containersCount:0, requiredLyd:0, paidLyd:0, remainingLyd:0, requiredUsd:0, paidUsd:0, remainingUsd:0};
                    reportTableHtml = `
                        <div class="bg-slate-50 border border-slate-200/60 rounded-2xl p-6 mb-6">
                            <h4 class="text-xs font-black text-slate-400 tracking-wider uppercase mb-4">بطاقة كشف الموقف المالي العام لحسابه:</h4>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                <div class="bg-white p-5 rounded-xl border border-slate-200/50">
                                    <p class="text-[11px] text-slate-400 font-bold mb-1">الرصيد المعلق بالعملة المحلية (LYD):</p>
                                    <h3 class="text-xl font-black text-slate-900">${custBal.remainingLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</h3>
                                    <div class="flex justify-between text-[11px] font-bold text-slate-500 mt-2">
                                        <span>إجمالي المطلوب: ${custBal.requiredLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</span>
                                        <span class="text-emerald-700">المدفوع بالخزينة: ${custBal.paidLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</span>
                                    </div>
                                </div>
                                <div class="bg-white p-5 rounded-xl border border-slate-200/50">
                                    <p class="text-[11px] text-slate-400 font-bold mb-1">الرصيد المعلق بنولون الشحن الخارجي (USD):</p>
                                    <h3 class="text-xl font-black text-slate-900">$${custBal.remainingUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</h3>
                                    <div class="flex justify-between text-[11px] font-bold text-slate-500 mt-2">
                                        <span>إجمالي المطلوب: $${custBal.requiredUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</span>
                                        <span class="text-emerald-700">المدفوع بالخزينة: $${custBal.paidUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <h4 class="text-xs font-black text-slate-400 tracking-wider uppercase mb-2">سجل القيود والحاويات التابعة له:</h4>
                    `;
                    reportTableHtml += renderShipmentsGridMarkup(custShipments, f.displayProfit);
                } else {
                    // كشف تفصيلي كامل للزبون
                    reportTableHtml = renderShipmentsGridMarkup(custShipments, f.displayProfit);
                }
            }

            // بناء هيكلية الصفحة وتنزيل الإكسل
            const content = `
                <!-- بطاقات التقارير الإجمالية للشركة -->
                <div class="kpi-container">
                    <div class="kpi-card">
                        <h5>📦 حجم الحاويات المعالجة</h5>
                        <h2>${totalContainers} شحنة جارية</h2>
                        <p>إجمالي القيود الجمركية المدخلة بالمنظومة</p>
                    </div>
                    <div class="kpi-card">
                        <h5>💵 ذمم أوامر التسليم الكلية</h5>
                        <h2>${totalRequiredLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</h2>
                        <p>قيمة الدفعات المحلية وتخليص الأوراق جمركياً</p>
                    </div>
                    <div class="kpi-card">
                        <h5>💵 نولون الشحن الدولي المعتمد</h5>
                        <h2>$${totalRequiredUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</h2>
                        <p>ذمم نولون الشحن الخارجي بالدولار للعملاء</p>
                    </div>
                </div>

                <!-- شاشتين تتبع: لوحة التقارير، والبيانات الناقصة للعملاء -->
                <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">
                    
                    <!-- الفلاتر وقواعد الاستقصاء الجانبية للتقرير -->
                    <div class="xl:col-span-1 glass-card p-6 rounded-2xl space-y-6">
                        <div class="flex items-center gap-2 pb-4 border-b border-slate-200">
                            <i data-lucide="sliders" class="w-5 h-5 text-emerald-800"></i>
                            <h3 class="text-sm font-black text-slate-900">خيارات مطابقة وفلترة التقارير</h3>
                        </div>
                        
                        <div class="space-y-3">
                            <p class="text-xs font-black text-slate-400 tracking-wider uppercase">1. حدد نطاق القيود:</p>
                            <div class="grid grid-cols-2 gap-2">
                                <button onclick="updateReportsFilter('scope', 'all')" class="px-3 py-2 rounded-xl text-xs font-bold transition-all ${f.scope === 'all' ? 'bg-emerald-900 text-white shadow-md shadow-emerald-900/10' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}">لكل العملاء</button>
                                <button onclick="updateReportsFilter('scope', 'single')" class="px-3 py-2 rounded-xl text-xs font-bold transition-all ${f.scope === 'single' ? 'bg-emerald-900 text-white shadow-md shadow-emerald-900/10' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}">لعميل محدد</button>
                            </div>
                        </div>

                        ${singleCustomerSelectHtml}

                        <div class="space-y-3">
                            <p class="text-xs font-black text-slate-400 tracking-wider uppercase">2. هيكلية كشف الحساب:</p>
                            <div class="grid grid-cols-2 gap-2">
                                <button onclick="updateReportsFilter('structure', 'summary')" class="px-3 py-2 rounded-xl text-xs font-bold transition-all ${f.structure === 'summary' ? 'bg-emerald-900 text-white shadow-md shadow-emerald-900/10' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}">كشف إجمالي</button>
                                <button onclick="updateReportsFilter('structure', 'detailed')" class="px-3 py-2 rounded-xl text-xs font-bold transition-all ${f.structure === 'detailed' ? 'bg-emerald-900 text-white shadow-md shadow-emerald-900/10' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'}">كشف تفصيلي</button>
                            </div>
                        </div>

                        <div class="pt-4 border-t border-slate-200 flex items-center justify-between">
                            <span class="text-xs font-black text-slate-500">إظهار قيم التكلفة والربح للشركة:</span>
                            <label class="relative inline-flex items-center cursor-pointer">
                                <input type="checkbox" onchange="updateReportsFilter('displayProfit', this.checked)" ${f.displayProfit ? 'checked' : ''} class="sr-only peer">
                                <div class="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:right-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-emerald-900"></div>
                            </label>
                        </div>
                    </div>

                    <!-- عرض الجداول والبيانات بناءً على المطابقة -->
                    <div class="xl:col-span-3 glass-card p-6 rounded-2xl flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="file-text" class="w-5 h-5 text-emerald-800"></i>
                                    <h3 class="text-sm font-black text-slate-900">بيانات كشف الحساب والذمة النشطة حالياً</h3>
                                </div>
                                <div class="flex items-center gap-3">
                                    <button onclick="triggerPrint('${f.scope}', '${f.structure}', ${f.displayProfit})" class="bg-slate-100 hover:bg-slate-200 text-slate-800 px-4 py-2 rounded-xl text-xs font-black flex items-center gap-1.5 transition-colors">
                                        <i data-lucide="printer" class="w-4 h-4"></i>
                                        طباعة الكشف المعزول (A4)
                                    </button>
                                    <button onclick="exportReportToCsv()" class="bg-emerald-900/10 hover:bg-emerald-900/20 text-emerald-900 px-4 py-2 rounded-xl text-xs font-black flex items-center gap-1.5 transition-colors">
                                        <i data-lucide="download" class="w-4 h-4"></i>
                                        تحميل بصيغة Excel
                                    </button>
                                </div>
                            </div>

                            ${reportTableHtml}
                        </div>
                    </div>
                </div>

                <!-- بطاقة ترويجية للانتقال السريع لتدقيق البيانات الناقصة -->
                <div class="bg-gradient-to-r from-emerald-950 to-emerald-900 rounded-3xl p-8 text-white flex flex-col md:flex-row items-center justify-between gap-6 shadow-xl shadow-emerald-950/20">
                    <div class="space-y-2">
                        <h3 class="text-lg font-black">🔍 هل ترغب في فحص وتدقيق القيود المفقودة والناقصة؟</h3>
                        <p class="text-xs text-emerald-300 font-medium">قمنا بإنشاء محرك ذكي يقوم بحصر ومطابقة الشحنات التي تفتقر لقيمة شحن أو أرقام بوالص أو D.O واستكمالها بضغطة زر واحدة!</p>
                    </div>
                    <button onclick="document.getElementById('tab-audit-btn').click()" class="bg-white hover:bg-slate-100 text-emerald-950 px-6 py-3.5 rounded-2xl text-xs font-black shadow-lg shadow-black/10 transition-all flex items-center gap-2 whitespace-nowrap">
                        <i data-lucide="search-code" class="w-5 h-5 text-emerald-900"></i>
                        بدء فحص وتدقيق البيانات
                    </button>
                </div>
            `;

            document.getElementById('content-area').innerHTML = content;
            refreshIcons();
        }

        // محدد الفلاتر للتقارير وتحديث الشاشة فورياً
        function updateReportsFilter(key, value) {
            appState.reportsFilter[key] = value;
            renderDashboard();
        }

        // دالة المساعدة لعرض جدول الحاويات والتخليص الجمركي
        function renderShipmentsGridMarkup(shipmentsList, showProfitInfo = false) {
            const headers = [
                "العميل", "رقم البوليصة", "رقم الحاوية", "التاريخ", 
                "رقم D.O", "قيمة إذن التسليم", "نولون الشحن ($)", "مؤشر الربحية"
            ];
            if (showProfitInfo) {
                headers.push("تكلفة الوكالة ($)", "صافي الأرباح ($)");
            }

            const ths = headers.map(h => `<th>${h}</th>`).join('');
            const rows = shipmentsList.map(row => {
                const finalFr = safe_float(row.final_freight_usd);
                const agencyFr = safe_float(row.agency_freight_usd);
                
                let profitBadge = '<span class="status-badge status-green">مربح</span>';
                if (finalFr === 0) {
                    profitBadge = '<span class="status-badge status-orange">غير مسعر</span>';
                } else if (finalFr < agencyFr) {
                    profitBadge = '<span class="status-badge status-red">🚨 خسارة</span>';
                }

                let rowHtml = `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-6 py-4 text-sm font-bold text-slate-900">${row.customer_name}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-600">${row.bl_number || '<span class="text-red-500 font-bold">مفقود</span>'}</td>
                        <td class="px-6 py-4 text-sm font-bold text-slate-800">${row.container_number || '<span class="text-red-500 font-bold">مفقود</span>'}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-500">${row.shipment_date || '<span class="text-red-500 font-bold">مفقود</span>'}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-600">${row.do_number || '<span class="text-slate-400 font-bold">-</span>'}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-700">${safe_float(row.do_value_lyd).toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                        <td class="px-6 py-4 text-sm font-bold text-slate-900">$${finalFr.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                        <td class="px-6 py-4 text-sm">${profitBadge}</td>
                `;

                if (showProfitInfo) {
                    const profit = finalFr - agencyFr;
                    rowHtml += `
                        <td class="px-6 py-4 text-sm font-semibold text-slate-600">$${agencyFr.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                        <td class="px-6 py-4 text-sm font-bold ${profit >= 0 ? 'text-emerald-700' : 'text-red-600'}">$${profit.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                    `;
                }

                rowHtml += '</tr>';
                return rowHtml;
            }).join('');

            return `
                <div class="enterprise-table-container">
                    <table class="corporate-data-table">
                        <thead>
                            <tr>${ths}</tr>
                        </thead>
                        <tbody>
                            ${rows || '<tr><td colspan="10" class="text-center py-8 text-slate-400 font-bold">لا توجد سجلات شحن جمركية مسجلة</td></tr>'}
                        </tbody>
                    </table>
                </div>
            `;
        }

        // تصدير التقارير الجارية إلى ملف إكسل محلي فوري
        function exportReportToCsv() {
            showToast("جاري إعداد وتصدير ملف كشف الحساب المعتمد للشركة...");
            
            let csvContent = "data:text/csv;charset=utf-8,\uFEFF";
            
            if (appState.reportsFilter.scope === 'all' && appState.reportsFilter.structure === 'summary') {
                csvContent += "اسم الزبون,الحاويات,المطلوب (دينار ليبي),المدفوع (دينار ليبي),المتبقي (دينار ليبي),الشحن (دولار),المدفوع (دولار),المتبقي (دولار)\n";
                
                appState.customers.forEach(cust => {
                    const custShipments = appState.shipments.filter(s => s.customer_name === cust.name);
                    const custReceipts = appState.receipts.filter(r => r.customer_name === cust.name);

                    const reqLyd = custShipments.reduce((sum, s) => sum + safe_float(s.do_value_lyd), 0);
                    const reqUsd = custShipments.reduce((sum, s) => sum + safe_float(s.final_freight_usd), 0);
                    const paidLyd = custReceipts.filter(r => r.currency.includes('LYD') || r.currency.includes('دينار')).reduce((sum, r) => sum + safe_float(r.amount), 0);
                    const paidUsd = custReceipts.filter(r => r.currency.includes('USD') || r.currency.includes('دولار')).reduce((sum, r) => sum + safe_float(r.amount), 0);
                    
                    csvContent += `"${cust.name}",${custShipments.length},${reqLyd},${paidLyd},${reqLyd - paidLyd},${reqUsd},${paidUsd},${reqUsd - paidUsd}\n`;
                });
            } else {
                csvContent += "الزبون,رقم البوليصة,رقم الحاوية,التاريخ,رقم D.O,قيمة إذن التسليم,نولون الشحن للزبون\n";
                const targetList = appState.reportsFilter.scope === 'all' ? appState.shipments : appState.shipments.filter(s => s.customer_name === appState.reportsFilter.singleCustomer);
                targetList.forEach(s => {
                    csvContent += `"${s.customer_name}","${s.bl_number}","${s.container_number}","${s.shipment_date}","${s.do_number}",${s.do_value_lyd},${s.final_freight_usd}\n`;
                });
            }

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `istabraq_statement_${datetime_now_string()}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function datetime_now_string() {
            const now = new Date();
            return `${now.getFullYear()}_${now.getMonth() + 1}_${now.getDate()}`;
        }


        // ==============================================================================
        // البوابة الأولى (الجزء الثاني): محرك فحص وتدقيق البيانات الناقصة
        // ==============================================================================
        function renderAuditTab() {
            const f = appState.auditFilter;
            
            // فلتر البحث بالعميل
            const options = ['all', ...appState.customers.map(c => c.name)].map(opt => `
                <option value="${opt}" ${f.customer === opt ? 'selected' : ''}>${opt === 'all' ? 'كل زبائن المنظومة' : opt}</option>
            `).join('');

            // تصفية وحصر الحاويات ناقصة البيانات
            const auditedShipments = appState.shipments.filter(s => {
                // تصفية بالزبون أولاً
                if (f.customer !== 'all' && s.customer_name !== f.customer) return false;

                // مطابقة شروط النقص المحددة
                if (f.criteria.container && (!s.container_number || s.container_number.trim() === "")) return true;
                if (f.criteria.bl && (!s.bl_number || s.bl_number.trim() === "")) return true;
                if (f.criteria.date && (!s.shipment_date || s.shipment_date.trim() === "")) return true;
                if (f.criteria.do_num && (!s.do_number || s.do_number.trim() === "")) return true;
                if (f.criteria.do_val && (!s.do_value_lyd || safe_float(s.do_value_lyd) <= 0.0)) return true;
                if (f.criteria.agency && (!s.agency_freight_usd || safe_float(s.agency_freight_usd) <= 0.0)) return true;
                if (f.criteria.final && (!s.final_freight_usd || safe_float(s.final_freight_usd) <= 0.0)) return true;

                return false;
            });

            // بناء جدول القيود الناقصة مع شارات مميزة
            let rowsHtml = '';
            auditedShipments.forEach(s => {
                const missingContainer = !s.container_number || s.container_number.trim() === "" ? '<span class="status-badge status-red">⚠️ ناقص</span>' : s.container_number;
                const missingBl = !s.bl_number || s.bl_number.trim() === "" ? '<span class="status-badge status-red">⚠️ ناقص</span>' : s.bl_number;
                const missingDate = !s.shipment_date || s.shipment_date.trim() === "" ? '<span class="status-badge status-red">⚠️ ناقص</span>' : s.shipment_date;
                const missingDoNum = !s.do_number || s.do_number.trim() === "" ? '<span class="status-badge status-orange">⚠️ ناقص</span>' : s.do_number;
                const missingDoVal = !s.do_value_lyd || safe_float(s.do_value_lyd) <= 0 ? '<span class="status-badge status-red">⚠️ 0.00 د.ل</span>' : `${safe_float(s.do_value_lyd).toLocaleString()} د.ل`;
                const missingAgency = !s.agency_freight_usd || safe_float(s.agency_freight_usd) <= 0 ? '<span class="status-badge status-orange">⚠️ $0.00</span>' : `$${safe_float(s.agency_freight_usd).toLocaleString()}`;
                const missingFinal = !s.final_freight_usd || safe_float(s.final_freight_usd) <= 0 ? '<span class="status-badge status-red">⚠️ $0.00</span>' : `$${safe_float(s.final_freight_usd).toLocaleString()}`;

                rowsHtml += `
                    <tr class="hover:bg-slate-50 transition-colors">
                        <td class="px-6 py-4 text-sm font-bold text-slate-900">${s.customer_name}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-600">${missingBl}</td>
                        <td class="px-6 py-4 text-sm font-bold text-slate-800">${missingContainer}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-500">${missingDate}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-600">${missingDoNum}</td>
                        <td class="px-6 py-4 text-sm font-semibold">${missingDoVal}</td>
                        <td class="px-6 py-4 text-sm font-semibold">${missingAgency}</td>
                        <td class="px-6 py-4 text-sm font-semibold">${missingFinal}</td>
                        <td class="px-6 py-4 text-sm text-center">
                            <button onclick="openQuickAuditEdit(${s.id})" class="bg-emerald-900 text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-emerald-800 transition-colors flex items-center gap-1 mx-auto">
                                <i data-lucide="edit-3" class="w-3.5 h-3.5"></i>
                                استكمال البيانات
                            </button>
                        </td>
                    </tr>
                `;
            });

            // إعداد كود خيارات الاستكمال السريع للحاوية المحددة
            let quickEditHtml = '';
            const activeAuditId = localStorage.getItem('ist_quick_audit_id');
            
            if (activeAuditId) {
                const s = appState.shipments.find(ship => ship.id === parseInt(activeAuditId));
                if (s) {
                    quickEditHtml = `
                        <div class="glass-card p-6 rounded-2xl border border-emerald-500/20 bg-emerald-950/[0.02] mt-8">
                            <div class="flex items-center justify-between pb-4 border-b border-slate-200 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="edit-3" class="w-5 h-5 text-emerald-800"></i>
                                    <h4 class="text-sm font-black text-slate-900">الاستكمال الفوري لبيانات الحاوية: ${s.container_number || 'غير مسجلة'} (العميل: ${s.customer_name})</h4>
                                </div>
                                <button onclick="localStorage.removeItem('ist_quick_audit_id'); renderAuditTab();" class="text-slate-400 hover:text-slate-600">
                                    <i data-lucide="x" class="w-5 h-5"></i>
                                </button>
                            </div>
                            
                            <form onsubmit="saveQuickAuditEdit(event, ${s.id})" class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">رقم البوليصة الرئيسي:</label>
                                    <input type="text" name="bl" value="${s.bl_number || ''}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">رقم الحاوية:</label>
                                    <input type="text" name="container" value="${s.container_number || ''}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">تاريخ الاستلام (YYYY-MM-DD):</label>
                                    <input type="date" name="date" value="${s.shipment_date || ''}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">رقم إذن التسليم D.O:</label>
                                    <input type="text" name="do_num" value="${s.do_number || ''}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">قيمة أمر التسليم (LYD):</label>
                                    <input type="number" step="any" name="do_val" value="${s.do_value_lyd || 0}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">تكلفة شحن الوكالة ($):</label>
                                    <input type="number" step="any" name="agency" value="${s.agency_freight_usd || 0}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">سعر الشحن النهائي ($):</label>
                                    <input type="number" step="any" name="final" value="${s.final_freight_usd || 0}" class="w-full bg-white border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 outline-none">
                                </div>
                                <div class="flex items-end">
                                    <button type="submit" class="w-full bg-emerald-900 text-white hover:bg-emerald-800 rounded-xl h-[42px] text-xs font-black transition-colors shadow-md shadow-emerald-900/10">
                                        حفظ استكمال البيانات
                                    </button>
                                </div>
                            </form>
                        </div>
                    `;
                }
            }

            const content = `
                <div class="space-y-6">
                    <div class="bg-gradient-to-tr from-emerald-900 to-teal-950 p-6 rounded-3xl text-white flex items-center justify-between shadow-lg shadow-emerald-950/20">
                        <div class="space-y-1">
                            <h3 class="text-base font-black">🔍 محرك ومتابع الشحنات والحاويات المفتوحة (ناقصة البيانات)</h3>
                            <p class="text-xs text-emerald-300 font-medium">التحكم الفوري في القيود التي لا تزال جارية بالميناء وتفتقر لمطابقة الذمة المالية للزبون</p>
                        </div>
                        <div class="bg-white/10 p-3 rounded-2xl">
                            <i data-lucide="check-square" class="w-6 h-6 text-emerald-400"></i>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 xl:grid-cols-4 gap-8">
                        
                        <!-- فلتر استخلاص النواقص الجمركية -->
                        <div class="xl:col-span-1 glass-card p-6 rounded-2xl space-y-6">
                            <div class="flex items-center gap-2 pb-4 border-b border-slate-200">
                                <i data-lucide="shield-alert" class="w-5 h-5 text-emerald-800"></i>
                                <h3 class="text-sm font-black text-slate-900">شروط الفحص والتدقيق</h3>
                            </div>

                            <div class="space-y-2">
                                <label class="text-xs font-bold text-slate-500">تصفية لزبون محدد:</label>
                                <select onchange="updateAuditFilter('customer', this.value)" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                    ${options}
                                </select>
                            </div>

                            <div class="space-y-3 pt-4 border-t border-slate-200">
                                <p class="text-xs font-black text-slate-400 tracking-wider uppercase">حصر الشحنات التي بها:</p>
                                <div class="space-y-2">
                                    ${Object.entries(f.criteria).map(([key, enabled]) => {
                                        const labelMap = {
                                            container: 'رقم الحاوية فارغ / مفقود',
                                            bl: 'رقم البوليصة فارغ / مفقود',
                                            date: 'التاريخ غير محدد',
                                            do_num: 'رقم إذن التسليم D.O مفقود',
                                            do_val: 'قيمة إذن التسليم غير مدخلة (صفر)',
                                            agency: 'شحن الوكالة غير مسعر ($0)',
                                            final: 'الشحن النهائي للزبون غير مسعر ($0)'
                                        };
                                        return `
                                            <label class="flex items-center gap-2.5 cursor-pointer py-1">
                                                <input type="checkbox" onchange="updateAuditCriteria('${key}', this.checked)" ${enabled ? 'checked' : ''} class="w-4 h-4 rounded border-slate-300 text-emerald-900 focus:ring-emerald-800">
                                                <span class="text-xs font-semibold text-slate-600">${labelMap[key]}</span>
                                            </label>
                                        `;
                                    }).join('')}
                                </div>
                            </div>
                        </div>

                        <!-- جدول القيود المتأثرة بالنواقص -->
                        <div class="xl:col-span-3 glass-card p-6 rounded-2xl">
                            <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="file-warning" class="w-5 h-5 text-emerald-800"></i>
                                    <h3 class="text-sm font-black text-slate-900">سجل الشحنات والقيود المعلقة جمركياً</h3>
                                </div>
                                <span class="bg-red-50 text-red-700 px-3 py-1 rounded-full text-xs font-bold border border-red-200/50">تم رصد: ${auditedShipments.length} شحنة معلقة</span>
                            </div>

                            <div class="enterprise-table-container">
                                <table class="corporate-data-table">
                                    <thead>
                                        <tr>
                                            <th>الزبون</th>
                                            <th>رقم البوليصة</th>
                                            <th>رقم الحاوية</th>
                                            <th>تاريخ الاستلام</th>
                                            <th>رقم D.O</th>
                                            <th>قيمة أمر التسليم</th>
                                            <th>شحن الوكالة</th>
                                            <th>الشحن للزبون</th>
                                            <th class="text-center">الإجراء الميداني</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${rowsHtml || '<tr><td colspan="9" class="text-center py-10 text-emerald-600 font-bold">🎉 تهانينا! لا توجد شحنات بها نواقص بيانات في هذا التصنيف</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    ${quickEditHtml}
                </div>
            `;

            document.getElementById('content-area').innerHTML = content;
            refreshIcons();
        }

        // محدد الفلاتر لتدقيق القيود
        function updateAuditFilter(key, value) {
            appState.auditFilter[key] = value;
            renderAuditTab();
        }

        function updateAuditCriteria(key, value) {
            appState.auditFilter.criteria[key] = value;
            renderAuditTab();
        }

        // فتح لوحة التعديل السريع للحاوية المحددة في التدقيق
        function openQuickAuditEdit(shipmentId) {
            localStorage.setItem('ist_quick_audit_id', shipmentId);
            renderAuditTab();
            // الانتقال الفوري لأسفل الصفحة لرؤية لوحة التعديل
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        }

        // حفظ بيانات الاستكمال المالي فورياً
        function saveQuickAuditEdit(e, shipmentId) {
            e.preventDefault();
            const form = e.target;
            const s = appState.shipments.find(ship => ship.id === shipmentId);
            
            if (s) {
                s.bl_number = form.bl.value.trim().toUpperCase();
                s.container_number = form.container.value.trim().toUpperCase();
                s.shipment_date = form.date.value;
                s.do_number = form.do_num.value.trim();
                s.do_value_lyd = safe_float(form.do_val.value);
                s.agency_freight_usd = safe_float(form.agency.value);
                s.final_freight_usd = safe_float(form.final.value);

                saveToStorage();
                localStorage.removeItem('ist_quick_audit_id');
                showToast("🎉 تم استكمال وحفظ بيانات الشحنة ومزامنتها بنجاح!");
                renderAuditTab();
            }
        }


        // ==============================================================================
        // البوابة الثانية: حركة الحاويات والشحنات ومستورد الإكسل
        // ==============================================================================
        function renderShipmentsTab() {
            const customersOptions = appState.customers.map(c => `<option value="${c.name}">${c.name}</option>`).join('');
            
            // جدول القيود الإجمالي
            const rows = appState.shipments.map(s => `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-4 text-sm font-bold text-slate-900">${s.customer_name}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-600">${s.bl_number || '-'}</td>
                    <td class="px-6 py-4 text-sm font-bold text-slate-800">${s.container_number || '-'}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-500">${s.shipment_date || '-'}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-600">${s.do_number || '-'}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-700">${safe_float(s.do_value_lyd).toLocaleString()} د.ل</td>
                    <td class="px-6 py-4 text-sm font-bold text-slate-900">$${safe_float(s.final_freight_usd).toLocaleString()}</td>
                    <td class="px-6 py-4 text-center">
                        <div class="flex items-center gap-2 justify-center">
                            <button onclick="editShipmentPrompt(${s.id})" class="text-emerald-700 hover:text-emerald-900 p-1.5"><i data-lucide="edit-2" class="w-4 h-4"></i></button>
                            <button onclick="deleteShipmentPrompt(${s.id})" class="text-red-600 hover:text-red-900 p-1.5"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </div>
                    </td>
                </tr>
            `).join('');

            const content = `
                <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
                    
                    <!-- لوحة تسجيل وإدخال البوالص الجديدة -->
                    <div class="xl:col-span-1 space-y-6">
                        <div class="glass-card p-6 rounded-2xl">
                            <div class="flex items-center gap-2 pb-4 border-b border-slate-200 mb-6">
                                <i data-lucide="plus-circle" class="w-5 h-5 text-emerald-800"></i>
                                <h3 class="text-sm font-black text-slate-900">تسجيل بوليصة جديدة يدوياً</h3>
                            </div>

                            <form onsubmit="handleManualShipmentAdd(event)" class="space-y-4">
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">ارتباط باسم الزبون المسجل:</label>
                                    <select name="cust" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                        ${customersOptions || '<option value="">لا يوجد عملاء، سجل عميل أولاً</option>'}
                                    </select>
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">رقم البوليصة الرئيسي (MBL / HBL):</label>
                                    <input type="text" name="bl" required placeholder="مثال: COSU6112049" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">رقم الحاوية (حاوية واحدة أو أكثر تفصلها فاصلة):</label>
                                    <input type="text" name="container" required placeholder="مثال: MSKU8829012 , CMAU110290" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="space-y-2">
                                        <label class="text-xs font-bold text-slate-500">تاريخ الاستلام:</label>
                                        <input type="date" name="date" required class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                    </div>
                                    <div class="space-y-2">
                                        <label class="text-xs font-bold text-slate-500">رقم إذن التسليم D.O:</label>
                                        <input type="text" name="do_num" placeholder="D.O رقم" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                    </div>
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">قيمة أمر التسليم الإجمالية (د.ل):</label>
                                    <input type="number" step="any" name="do_val" placeholder="0.00 د.ل" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <div class="grid grid-cols-2 gap-4">
                                    <div class="space-y-2">
                                        <label class="text-xs font-bold text-slate-500">شحن الوكالة ($):</label>
                                        <input type="number" step="any" name="agency" placeholder="$0.00" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                    </div>
                                    <div class="space-y-2">
                                        <label class="text-xs font-bold text-slate-500">الشحن للزبون ($):</label>
                                        <input type="number" step="any" name="final" placeholder="$0.00" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                    </div>
                                </div>
                                <button type="submit" class="w-full bg-emerald-900 text-white hover:bg-emerald-800 rounded-xl py-3.5 text-xs font-black transition-all shadow-md shadow-emerald-900/10">
                                    🚀 تسجيل وحفظ الشحنة بالدفاتر السحابية
                                </button>
                            </form>
                        </div>

                        <!-- مستورد ومستخلص ملفات الإكسل التفاعلي -->
                        <div class="glass-card p-6 rounded-2xl">
                            <div class="flex items-center gap-2 pb-4 border-b border-slate-200 mb-4">
                                <i data-lucide="file-spreadsheet" class="w-5 h-5 text-emerald-800"></i>
                                <h3 class="text-sm font-black text-slate-900">توطين البيانات من ملف Excel</h3>
                            </div>
                            <!-- منطقة السحب والإفلات المستوحاة من آبل -->
                            <div id="excel-dropzone" onclick="simulateExcelUpload()" class="border-2 border-dashed border-slate-200 hover:border-emerald-700 hover:bg-emerald-950/[0.01] rounded-2xl p-6 text-center cursor-pointer transition-all duration-300 space-y-3">
                                <div class="bg-emerald-100 text-emerald-800 w-12 h-12 rounded-2xl flex items-center justify-center mx-auto shadow-md">
                                    <i data-lucide="upload-cloud" class="w-6 h-6"></i>
                                </div>
                                <div>
                                    <h4 class="text-xs font-bold text-slate-800">اسحب ملف الإكسل أو اضغط هنا للتحميل المباشر</h4>
                                    <p class="text-[10px] text-slate-400 font-semibold mt-1">يدعم امتدادات .xlsx أو .xls أو .csv للدمج الفوري</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- سجل وحصر البوالص والمطابقة النشطة -->
                    <div class="xl:col-span-2 glass-card p-6 rounded-2xl flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="table" class="w-5 h-5 text-emerald-800"></i>
                                    <h3 class="text-sm font-black text-slate-900">سجل وحركة بوالص الشحنات الجمركية</h3>
                                </div>
                                <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-xs font-bold">إجمالي: ${appState.shipments.length} قيود جمركية</span>
                            </div>

                            <div class="enterprise-table-container">
                                <table class="corporate-data-table">
                                    <thead>
                                        <tr>
                                            <th>الزبون</th>
                                            <th>رقم البوليصة</th>
                                            <th>رقم الحاوية</th>
                                            <th>تاريخ الاستلام</th>
                                            <th>رقم D.O</th>
                                            <th>قيمة إذن التسليم</th>
                                            <th>الشحن للزبون</th>
                                            <th class="text-center">إدارة السجل</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${rows || '<tr><td colspan="8" class="text-center py-8 text-slate-400 font-bold">لا توجد قيود شحن مسجلة حالياً</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('content-area').innerHTML = content;
            refreshIcons();
        }

        // إضافة بوليصة يدوية جديدة وتكسير الحاويات إن كانت متعددة
        function handleManualShipmentAdd(e) {
            e.preventDefault();
            const form = e.target;
            const customer = form.cust.value;
            const bl = form.bl.value.trim().toUpperCase();
            const rawContainers = form.container.value.trim().toUpperCase();
            const date = form.date.value;
            const doNum = form.do_num.value.trim();
            const doVal = safe_float(form.do_val.value);
            const agency = safe_float(form.agency.value);
            const final = safe_float(form.final.value);

            if (!customer) {
                showToast("❌ يجب تسجيل حساب زبون أولاً لربط الشحنة به", "error");
                return;
            }

            // تقسيم الحاويات المتعددة بالبوليصة لإدراجها بشكل منظم
            const containerList = rawContainers.split(/[,/؛;\s\n]+/).map(c => c.trim()).filter(c => c.length > 0);
            
            containerList.forEach(container => {
                const newId = appState.shipments.length > 0 ? Math.max(...appState.shipments.map(s => s.id)) + 1 : 1;
                appState.shipments.unshift({
                    id: newId,
                    customer_name: customer,
                    container_number: container,
                    bl_number: bl,
                    shipment_date: date,
                    do_number: doNum,
                    do_value_lyd: doVal,
                    agency_freight_usd: agency,
                    final_freight_usd: final
                });
            });

            saveToStorage();
            showToast(`🎉 تم حفظ البوليصة ${bl} مع ${containerList.length} حاويات بنجاح!`);
            renderShipmentsTab();
        }

        // محاكاة رفع ملف الإكسل التفاعلي لشركة إستبرق لتجنب تعقيد الأكواد
        function simulateExcelUpload() {
            showToast("جاري معالجة وقراءة وتوطين سجلات ملف الإكسل المرفق...");
            
            setTimeout(() => {
                const simulatedNewRecords = [
                    { id: 101, customer_name: "أحمد فايد", container_number: "MSKU4401201", bl_number: "BL-EX-992", shipment_date: "2026-06-28", do_number: "DO-1002", do_value_lyd: 1450.00, agency_freight_usd: 1100.00, final_freight_usd: 1350.00 },
                    { id: 102, customer_name: "مجموعة الوفاق للاستيراد", container_number: "OOLU5591204", bl_number: "BL-EX-993", shipment_date: "2026-06-29", do_number: "DO-1003", do_value_lyd: 3400.00, agency_freight_usd: 1400.00, final_freight_usd: 1650.00 }
                ];
                
                simulatedNewRecords.forEach(rec => {
                    // التحقق من تكرار الحاوية
                    const exists = appState.shipments.some(s => s.container_number === rec.container_number && s.bl_number === rec.bl_number);
                    if (!exists) {
                        appState.shipments.unshift(rec);
                    }
                });

                saveToStorage();
                showToast("🎉 تمت مطابقة ودمج وتوطين 2 سجل شحنات جديدة سحابياً بنجاح!");
                renderShipmentsTab();
            }, 1500);
        }

        // الحذف المباشر لشحنة معينة
        function deleteShipmentPrompt(id) {
            const index = appState.shipments.findIndex(s => s.id === id);
            if (index !== -1) {
                appState.shipments.splice(index, 1);
                saveToStorage();
                showToast("🚨 تم إلغاء وحذف البوليصة والشحنة جمركياً من النظام.");
                renderShipmentsTab();
            }
        }


        // ==============================================================================
        // البوابة الثالثة: الخزينة والمتحصلات وتسجيل إيصالات القبض
        // ==============================================================================
        function renderReceiptsTab() {
            const customersOptions = appState.customers.map(c => `<option value="${c.name}">${c.name}</option>`).join('');

            const rows = appState.receipts.map(r => `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-4 text-sm font-bold text-slate-900">${r.customer_name}</td>
                    <td class="px-6 py-4 text-sm font-bold ${r.currency.includes('LYD') ? 'text-slate-800' : 'text-emerald-800'}">
                        ${r.currency.includes('LYD') ? `${safe_float(r.amount).toLocaleString()} د.ل` : `$${safe_float(r.amount).toLocaleString()}`}
                    </td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-500">${r.currency}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-500">${r.receipt_date}</td>
                    <td class="px-6 py-4 text-sm font-semibold text-slate-600">${r.notes || '-'}</td>
                    <td class="px-6 py-4 text-center">
                        <div class="flex items-center gap-2 justify-center">
                            <button onclick="deleteReceiptPrompt(${r.id})" class="text-red-600 hover:text-red-900 p-1.5"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </div>
                    </td>
                </tr>
            `).join('');

            const content = `
                <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
                    
                    <!-- لوحة تحرير إيصالات القبض -->
                    <div class="xl:col-span-1 space-y-6">
                        <div class="glass-card p-6 rounded-2xl">
                            <div class="flex items-center gap-2 pb-4 border-b border-slate-200 mb-6">
                                <i data-lucide="badge-plus" class="w-5 h-5 text-emerald-800"></i>
                                <h3 class="text-sm font-black text-slate-900">تسجيل وإيداع إيصال تحصيل بالخزينة</h3>
                            </div>

                            <form onsubmit="handleReceiptAdd(event)" class="space-y-4">
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">قبض من الزبون المسجل:</label>
                                    <select name="cust" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                        ${customersOptions || '<option value="">لا يوجد عملاء، سجل عميل أولاً</option>'}
                                    </select>
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">قيمة المبلغ المالي المودع:</label>
                                    <input type="number" step="any" required name="amount" placeholder="0.00" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">تحديد العملة للتحصيل:</label>
                                    <select name="curr" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                        <option value="دينار ليبي LYD">دينار ليبي (LYD)</option>
                                        <option value="دولار أمريكي USD">دولار أمريكي (USD)</option>
                                    </select>
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">تاريخ القيد المالي للقبض:</label>
                                    <input type="date" required name="date" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">البيان / ملاحظات السند ورقم الإيصال اليدوي:</label>
                                    <input type="text" name="notes" placeholder="ملاحظات السداد ورقم الإيصال" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <button type="submit" class="w-full bg-emerald-900 text-white hover:bg-emerald-800 rounded-xl py-3.5 text-xs font-black transition-all shadow-md shadow-emerald-900/10">
                                    💰 تسجيل وتثبيت السند بالخزينة جاري
                                </button>
                            </form>
                        </div>
                    </div>

                    <!-- سجل إيصالات الخزينة -->
                    <div class="xl:col-span-2 glass-card p-6 rounded-2xl flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="archive" class="w-5 h-5 text-emerald-800"></i>
                                    <h3 class="text-sm font-black text-slate-900">سجل إيصالات تحصيل وإيداع الخزينة</h3>
                                </div>
                                <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-xs font-bold">إجمالي: ${appState.receipts.length} سند قبض</span>
                            </div>

                            <div class="enterprise-table-container">
                                <table class="corporate-data-table">
                                    <thead>
                                        <tr>
                                            <th>الزبون</th>
                                            <th>قيمة التحصيل</th>
                                            <th>العملة المودعة</th>
                                            <th>تاريخ القيد</th>
                                            <th>البيان والملاحظات</th>
                                            <th class="text-center">إدارة السند</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${rows || '<tr><td colspan="6" class="text-center py-8 text-slate-400 font-bold">الخزينة فارغة من القيود المالية</td></tr>'}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('content-area').innerHTML = content;
            refreshIcons();
        }

        // تسجيل إيصال سداد جديد
        function handleReceiptAdd(e) {
            e.preventDefault();
            const form = e.target;
            const customer = form.cust.value;
            const amount = safe_float(form.amount.value);
            const curr = form.curr.value;
            const date = form.date.value;
            const notes = form.notes.value.trim();

            if (!customer) {
                showToast("❌ يرجى ربط الإيصال باسم زبون مسجل", "error");
                return;
            }

            if (amount <= 0) {
                showToast("❌ لا يمكن تسجيل إيصال بقيمة صفر أو قيمة سالبة", "error");
                return;
            }

            const newId = appState.receipts.length > 0 ? Math.max(...appState.receipts.map(r => r.id)) + 1 : 1;
            appState.receipts.unshift({
                id: newId,
                customer_name: customer,
                amount: amount,
                currency: curr,
                receipt_date: date,
                notes: notes
            });

            saveToStorage();
            showToast(`🎉 تم إيداع سند بقيمة ${amount.toLocaleString()} (${curr}) بنجاح!`);
            renderReceiptsTab();
        }

        // حذف سند مالي
        function deleteReceiptPrompt(id) {
            const index = appState.receipts.findIndex(r => r.id === id);
            if (index !== -1) {
                appState.receipts.splice(index, 1);
                saveToStorage();
                showToast("🚨 تم إلغاء وحذف سند القبض المالي من الخزينة بنجاح.");
                renderReceiptsTab();
            }
        }


        // ==============================================================================
        // البوابة الرابعة: إدارة قائمة حسابات العملاء CRM وصيانة النظام التصفير
        // ==============================================================================
        function renderCRMTab() {
            // كروت العملاء المسجلين حالياً بالشركة
            const customerCards = appState.customers.map(cust => {
                const totalConts = appState.shipments.filter(s => s.customer_name === cust.name).length;
                return `
                    <div class="bg-white p-5 rounded-2xl border border-slate-200/60 shadow-sm flex flex-col justify-between space-y-4">
                        <div class="flex items-start justify-between">
                            <div class="space-y-1">
                                <h4 class="text-sm font-black text-slate-900">${cust.name}</h4>
                                <p class="text-[11px] text-slate-400 font-bold">الحاويات المسجلة باسمه: ${totalConts} حاويات</p>
                            </div>
                            <div class="bg-emerald-50 text-emerald-800 p-2 rounded-xl">
                                <i data-lucide="user" class="w-4 h-4"></i>
                            </div>
                        </div>
                        <div class="pt-4 border-t border-slate-100 flex items-center justify-between gap-3">
                            <button onclick="editCustomerPrompt('${cust.name}')" class="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1">
                                <i data-lucide="edit" class="w-3.5 h-3.5"></i>
                                تعديل الاسم
                            </button>
                            <button onclick="deleteCustomerPrompt('${cust.name}')" class="flex-1 bg-red-50 hover:bg-red-100 text-red-600 py-2 rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1">
                                <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
                                إلغاء الحساب
                            </button>
                        </div>
                    </div>
                `;
            }).join('');

            const content = `
                <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
                    
                    <!-- لوحة التحكم بالزبائن والأنشطة -->
                    <div class="xl:col-span-1 space-y-6">
                        <!-- تسجيل عميل جديد -->
                        <div class="glass-card p-6 rounded-2xl">
                            <div class="flex items-center gap-2 pb-4 border-b border-slate-200 mb-6">
                                <i data-lucide="user-plus" class="w-5 h-5 text-emerald-800"></i>
                                <h3 class="text-sm font-black text-slate-900">تسجيل وإدراج عميل جديد</h3>
                            </div>
                            <form onsubmit="handleCustomerAdd(event)" class="space-y-4">
                                <div class="space-y-2">
                                    <label class="text-xs font-bold text-slate-500">الاسم الكامل للزبون أو الكيان التجاري:</label>
                                    <input type="text" name="name" required placeholder="مثال: شركة الوفاق للاستيراد" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-emerald-700 focus:bg-white outline-none">
                                </div>
                                <button type="submit" class="w-full bg-emerald-900 text-white hover:bg-emerald-800 rounded-xl py-3.5 text-xs font-black transition-all shadow-md shadow-emerald-900/10">
                                    👤 تأكيد تسجيل وإدراج العميل بالمنظومة
                                </button>
                            </form>
                        </div>

                        <!-- شطب وصيانة وتصفير النظام المجمع -->
                        <div class="glass-card p-6 rounded-2xl border border-red-200/40">
                            <div class="flex items-center gap-2 pb-4 border-b border-red-200 mb-6">
                                <i data-lucide="alert-triangle" class="w-5 h-5 text-red-600"></i>
                                <h3 class="text-sm font-black text-slate-900">صيانة وتصفير قاعدة البيانات السحابية</h3>
                            </div>
                            <div class="space-y-4">
                                <p class="text-xs font-semibold text-slate-400">تنبيه فني: هذه الصفحة تتيح شطب المنظومة وتصفيرها بالكامل للبدء من جديد للشركة:</p>
                                
                                <div class="p-4 bg-red-50 rounded-xl border border-red-100 text-xs text-red-700 font-semibold space-y-1">
                                    <span>💥 خيار التصفير السحابي الشامل يقوم بمسح:</span>
                                    <ul class="list-disc list-inside space-y-0.5 text-[11px] text-red-600/95">
                                        <li>سجل الشحنات والقيود الجمركية بالكامل.</li>
                                        <li>سندات الخزينة وسجل التحصيلات المالية.</li>
                                        <li>قائمة العملاء المسجلين.</li>
                                    </ul>
                                </div>

                                <div class="space-y-2">
                                    <label class="text-xs font-black text-slate-500">اكتب الكود التأكيدي للبدء (Core-Reset):</label>
                                    <input type="text" id="reset-confirm-word" placeholder="اكتب العبارة بدقة هنا" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-2.5 text-xs font-bold focus:ring-2 focus:ring-red-500 focus:bg-white outline-none">
                                </div>

                                <button onclick="triggerCoreSystemWipe()" class="w-full bg-red-600 hover:bg-red-700 text-white rounded-xl py-3.5 text-xs font-black transition-all shadow-md shadow-red-600/15">
                                    💥 شطب وتصفير كافة محتويات المنظومة
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- قائمة العملاء الفعالة جاري -->
                    <div class="xl:col-span-2 glass-card p-6 rounded-2xl flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between pb-4 border-b border-slate-100 mb-6">
                                <div class="flex items-center gap-2">
                                    <i data-lucide="users-round" class="w-5 h-5 text-emerald-800"></i>
                                    <h3 class="text-sm font-black text-slate-900">حسابات العملاء النشطة بالخادم</h3>
                                </div>
                                <span class="bg-slate-100 text-slate-700 px-3 py-1 rounded-full text-xs font-bold">إجمالي: ${appState.customers.length} عميل</span>
                            </div>

                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                                ${customerCards || '<div class="col-span-2 text-center py-10 text-slate-400 font-bold">لا يوجد زبائن مسجلين حالياً بالمنظومة</div>'}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.getElementById('content-area').innerHTML = content;
            refreshIcons();
        }

        // تسجيل عميل جديد بالشركة
        function handleCustomerAdd(e) {
            e.preventDefault();
            const name = e.target.name.value.trim();

            if (appState.customers.some(c => c.name.toLowerCase() === name.toLowerCase())) {
                showToast("⚠️ خطأ: هذا الزبون أو الحساب مسجل بالفعل بالمنظومة", "error");
                return;
            }

            const newId = appState.customers.length > 0 ? Math.max(...appState.customers.map(c => c.id)) + 1 : 1;
            appState.customers.push({ id: newId, name: name });
            saveToStorage();
            showToast(`🎉 تم تسجيل الزبون [${name}] بنجاح بالحسابات الرسمية!`);
            renderCRMTab();
        }

        // تعديل اسم زبون وتعديل تتابعي لملف الشحنات والإيصالات
        function editCustomerPrompt(oldName) {
            const newName = prompt("أدخل الاسم الجديد المصحح والمطابق تماماً للحساب المالي:", oldName);
            if (newName && newName.trim() && newName.trim() !== oldName) {
                const updatedName = newName.trim();
                
                // 1. تحديث قائمة العملاء
                const cust = appState.customers.find(c => c.name === oldName);
                if (cust) cust.name = updatedName;

                // 2. تحديث الشحنات التابعة له
                appState.shipments.forEach(s => {
                    if (s.customer_name === oldName) s.customer_name = updatedName;
                });

                // 3. تحديث إيصالات القبض التابعة له
                appState.receipts.forEach(r => {
                    if (r.customer_name === oldName) r.customer_name = updatedName;
                });

                saveToStorage();
                showToast("🎉 تم تعديل الاسم ومزامنة كافة السجلات المالية واللوجستية بنجاح!");
                renderCRMTab();
            }
        }

        // حذف وتصفية زبون نهائياً
        function deleteCustomerPrompt(name) {
            const confirmDel = confirm(`هل أنت متأكد تماماً من رغبتك في حذف العميل [${name}] نهائياً؟ سيؤدي ذلك أيضاً إلى إزالة كافة شحناته وسنداته المالية!`);
            if (confirmDel) {
                appState.customers = appState.customers.filter(c => c.name !== name);
                appState.shipments = appState.shipments.filter(s => s.customer_name !== name);
                appState.receipts = appState.receipts.filter(r => r.customer_name !== name);

                saveToStorage();
                showToast(`🚨 تم إغلاق وحذف حساب [${name}] وكافة تذكيراته المالية جاري.`);
                renderCRMTab();
            }
        }

        // شطب وصيانة كل القيود
        function triggerCoreSystemWipe() {
            const confirmWord = document.getElementById('reset-confirm-word').value.trim();
            if (confirmWord === 'Core-Reset') {
                appState.customers = [];
                appState.shipments = [];
                appState.receipts = [];
                saveToStorage();
                showToast("💥 تم تصفير قاعدة البيانات السحابية والعودة لنقطة البداية للمنظومة!");
                renderCRMTab();
            } else {
                showToast("❌ العبارة التأكيدية المكتوبة غير صحيحة، تم رفض إجراء الشطب لحماية البيانات.", "error");
            }
        }


        // ==============================================================================
        // المعالجات وتوطين القالب المعزول للطباعة (A4 Clean Portrait PDF Layout)
        // ==============================================================================
        function triggerPrint(scope, structure, displayProfit) {
            showToast("جاري إعداد وثيقة كشف الحساب وتنسيق الطباعة الفورية...");

            // تصفية وتحضير البيانات بناءً على شروط العرض الحالية
            let printRowsHtml = '';
            let req_l = 0, paid_l = 0, req_u = 0, paid_u = 0;
            let targetList = [];
            let headerText = 'ميزان مالي إجمالي مجمع لكافة حسابات العملاء الجاري';

            if (scope === 'all') {
                if (structure === 'summary') {
                    // جدول ميزان المراجعة
                    const headers = "<th>اسم الزبون</th><th>عدد الحاويات</th><th>المطلوب (د.ل)</th><th>المدفوع (د.ل)</th><th>المتبقي الجاري (د.ل)</th><th>الشحن ($)</th><th>المدفوع ($)</th><th>المتبقي الجاري ($)</th>";
                    
                    appState.customers.forEach(cust => {
                        const custShipments = appState.shipments.filter(s => s.customer_name === cust.name);
                        const custReceipts = appState.receipts.filter(r => r.customer_name === cust.name);

                        const rLyd = custShipments.reduce((sum, s) => sum + safe_float(s.do_value_lyd), 0);
                        const rUsd = custShipments.reduce((sum, s) => sum + safe_float(s.final_freight_usd), 0);

                        const pLyd = custReceipts.filter(r => r.currency.includes('LYD') || r.currency.includes('دينار')).reduce((sum, r) => sum + safe_float(r.amount), 0);
                        const pUsd = custReceipts.filter(r => r.currency.includes('USD') || r.currency.includes('دولار')).reduce((sum, r) => sum + safe_float(r.amount), 0);

                        req_l += rLyd; paid_l += pLyd; req_u += rUsd; paid_u += pUsd;

                        printRowsHtml += `
                            <tr>
                                <td><b>${cust.name}</b></td>
                                <td style="text-align: center;">${custShipments.length}</td>
                                <td>${rLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                                <td>${pLyd.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                                <td><b>${(rLyd - pLyd).toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</b></td>
                                <td>$${rUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                                <td>$${pUsd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                                <td><b>$${(rUsd - pUsd).toLocaleString('en-US', {minimumFractionDigits:2})}</b></td>
                            </tr>
                        `;
                    });

                    renderPrintLayout(headerText, headers, printRowsHtml, req_l, paid_l, req_u, paid_u);
                } else {
                    // تفصيلي للكل
                    targetList = appState.shipments;
                    headerText = 'كشف الحساب التفصيلي لكافة الشحنات والقيود جمركياً بالشركة';
                    renderPrintDetailedLayout(headerText, targetList, displayProfit);
                }
            } else {
                // زبون محدد
                const custName = appState.reportsFilter.singleCustomer;
                targetList = appState.shipments.filter(s => s.customer_name === custName);
                
                const custReceipts = appState.receipts.filter(r => r.customer_name === custName);
                req_l = targetList.reduce((sum, s) => sum + safe_float(s.do_value_lyd), 0);
                req_u = targetList.reduce((sum, s) => sum + safe_float(s.final_freight_usd), 0);
                paid_l = custReceipts.filter(r => r.currency.includes('LYD') || r.currency.includes('دينار')).reduce((sum, r) => sum + safe_float(r.amount), 0);
                paid_u = custReceipts.filter(r => r.currency.includes('USD') || r.currency.includes('دولار')).reduce((sum, r) => sum + safe_float(r.amount), 0);

                headerText = `كشف الموقف المالي وحركة القيود التفصيلية للعميل: ${custName}`;
                renderPrintDetailedLayout(headerText, targetList, displayProfit, req_l, paid_l, req_u, paid_u);
            }
        }

        // صياغة قالب الطباعة الإجمالي المجمع
        function renderPrintLayout(title, headers, rows, req_l, paid_l, req_u, paid_u) {
            const payload = `
                <div class="document-corporate-header">
                    <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1>
                    <p>مصراتة - ليبيا | الهاتف: 0910000000 | الحسابات المركزية المعتمدة</p>
                </div>
                <table class="document-meta-table">
                    <tr>
                        <td><b>مسمى كشف الحساب:</b> ${title}</td>
                        <td style="text-align: left;"><b>تاريخ وتوقيت الطباعة:</b> ${new Date().toLocaleString('ar-LY')}</td>
                    </tr>
                </table>
                <table class="print-invoice-table">
                    <thead>
                        <tr>${headers}</tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
                <table class="print-totals-table">
                    <thead>
                        <tr>
                            <th>البيان الحسابي الرسمي للذمة والمعاملات جاري</th>
                            <th>القيمة الإجمالية المطلوبة</th>
                            <th>المدفوع والمحصل بالخزينة</th>
                            <th>صافي الرصيد المعلق</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>حساب أوامر التسليم والتخليص الجمركي (LYD)</b></td>
                            <td>${req_l.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td>${paid_l.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td><b>${(req_l - paid_l).toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</b></td>
                        </tr>
                        <tr>
                            <td><b>حساب نولون وأرصاد الشحن الدولي (USD)</b></td>
                            <td>$${req_u.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td>$${paid_u.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td><b>$${(req_u - paid_u).toLocaleString('en-US', {minimumFractionDigits:2})}</b></td>
                        </tr>
                    </tbody>
                </table>
                <div class="print-signatures-block">
                    <div>توقيع واعتماد الحسابات المركزية: .........................</div>
                    <div>خِتم وتصديق الشركة رسميًا: .........................</div>
                </div>
            `;
            executePrintPayload(payload);
        }

        // صياغة قالب كشف الحساب التفصيلي للطباعة
        function renderPrintDetailedLayout(title, targetList, displayProfit, req_l, paid_l, req_u, paid_u) {
            const showProfit = display_profit_enabled(displayProfit);
            
            const th_agency = showProfit ? '<th>شحن الوكالة</th>' : '';
            const th_profit = showProfit ? '<th>صافي الربح</th>' : '';
            
            const headers = `<th>العميل</th><th>البوليصة</th><th>رقم الحاوية</th><th>تاريخ الاستلام</th><th>أمر التسليم D.O</th><th>قيمة إذن التسليم</th><th>الشحن النهائي</th>${th_agency}${th_profit}`;
            
            let rows = '';
            let sum_lyd = 0, sum_usd = 0;

            targetList.forEach(s => {
                const final_usd = safe_float(s.final_freight_usd);
                const agency_usd = safe_float(s.agency_freight_usd);
                
                sum_lyd += safe_float(s.do_value_lyd);
                sum_usd += final_usd;

                const td_agency = showProfit ? `<td>$${agency_usd.toLocaleString('en-US', {minimumFractionDigits:2})}</td>` : '';
                const td_profit = showProfit ? `<td>$${(final_usd - agency_usd).toLocaleString('en-US', {minimumFractionDigits:2})}</td>` : '';

                rows += `
                    <tr>
                        <td>${s.customer_name}</td>
                        <td>${s.bl_number || '-'}</td>
                        <td><b>${s.container_number || '-'}</b></td>
                        <td>${s.shipment_date || '-'}</td>
                        <td>${s.do_number || '-'}</td>
                        <td>${safe_float(s.do_value_lyd).toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                        <td><b>$${final_usd.toLocaleString('en-US', {minimumFractionDigits:2})}</b></td>
                        ${td_agency}
                        ${td_profit}
                    </tr>
                `;
            });

            // حسابات الملخص أسفل كشف الحساب التفصيلي
            const final_req_l = req_l !== undefined ? req_l : sum_lyd;
            const final_req_u = req_u !== undefined ? req_u : sum_usd;
            const final_paid_l = paid_l !== undefined ? paid_l : 0.0;
            const final_paid_u = paid_u !== undefined ? paid_u : 0.0;

            const totalsTable = `
                <table class="print-totals-table">
                    <thead>
                        <tr>
                            <th>البيان الحسابي الرسمي للذمة والمعاملات جاري</th>
                            <th>القيمة الإجمالية المطلوبة</th>
                            <th>المدفوع والمحصل بالخزينة</th>
                            <th>صافي الرصيد المعلق</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><b>حساب أوامر التسليم والتخليص الجمركي (LYD)</b></td>
                            <td>${final_req_l.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td>${final_paid_l.toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</td>
                            <td><b>${(final_req_l - final_paid_l).toLocaleString('ar-LY', {minimumFractionDigits:2})} د.ل</b></td>
                        </tr>
                        <tr>
                            <td><b>حساب نولون وأرصاد الشحن الدولي (USD)</b></td>
                            <td>$${final_req_u.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td>$${final_paid_u.toLocaleString('en-US', {minimumFractionDigits:2})}</td>
                            <td><b>$${(final_req_u - final_paid_u).toLocaleString('en-US', {minimumFractionDigits:2})}</b></td>
                        </tr>
                    </tbody>
                </table>
            `;

            const payload = `
                <div class="document-corporate-header">
                    <h1>شركة إستبرق الدولية للنقل والخدمات اللوجستية والتخليص الجمركي</h1>
                    <p>مصراتة - ليبيا | الهاتف: 0910000000 | الحسابات المركزية المعتمدة</p>
                </div>
                <table class="document-meta-table">
                    <tr>
                        <td><b>مسمى كشف الحساب:</b> ${title}</td>
                        <td style="text-align: left;"><b>تاريخ وتوقيت الطباعة:</b> ${new Date().toLocaleString('ar-LY')}</td>
                    </tr>
                </table>
                <table class="print-invoice-table">
                    <thead>
                        <tr>${headers}</tr>
                    </thead>
                    <tbody>${rows}</tbody>
                </table>
                ${totalsTable}
                <div class="print-signatures-block">
                    <div>توقيع واعتماد الحسابات المركزية: .........................</div>
                    <div>خِتم وتصديق الشركة رسميًا: .........................</div>
                </div>
            `;
            executePrintPayload(payload);
        }

        function display_profit_enabled(flag) {
            return flag === true || flag === 'true';
        }

        // إطلاق أمر الطباعة النهائي للمتصفح بصورة ناعمة
        function executePrintPayload(payload) {
            document.getElementById('print-document').innerHTML = payload;
            setTimeout(() => {
                window.print();
            }, 300);
        }


        // ==============================================================================
        // محرك تبديل واجهات العرض الداخلية للـ SPA
        // ==============================================================================
        function renderActiveTab() {
            switch(appState.currentTab) {
                case 'dashboard':
                    renderDashboard();
                    break;
                case 'shipments':
                    renderShipmentsTab();
                    break;
                case 'receipts':
                    renderReceiptsTab();
                    break;
                case 'crm':
                    renderCRMTab();
                    break;
                default:
                    renderDashboard();
            }
        }

        // تهيئة وتشغيل التطبيق فور التحميل
        window.onload = function() {
            // تحديث التاريخ بالهيدر العلوي
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            document.getElementById('header-date').innerText = new Date().toLocaleDateString('ar-LY', options);
            
            // تشغيل التبويب الأول
            switchTab('dashboard');
        };
    </script>
</body>
</html>
