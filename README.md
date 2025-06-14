# ملف شرح مشروع موقع مواقيت الصلاة

## 1. نظرة عامة على المشروع

هذا المشروع عبارة عن موقع إلكتروني تفاعلي (Web Application) لعرض مواقيت الصلاة، تم تصميمه ليكون سهل الاستخدام وقابل للتخصيص بشكل كامل من قبل المستخدم. الهدف الأساسي هو توفير أداة دقيقة ومرنة لمتابعة أوقات الصلوات اليومية مع ميزات إضافية لتحسين تجربة المستخدم.

---

## 2. الميزات الرئيسية

* **عرض ديناميكي للمواقيت:** جلب وعرض مواقيت الصلاة لليوم الحالي بناءً على المدينة المختارة.
* **تخصيص الموقع:**
    * إمكانية اختيار أي مدينة رئيسية في السودان.
    * حفظ جميع إعدادات المستخدم تلقائياً في المتصفح (`localStorage`).
* **ساعة وتاريخ مباشر:** عرض الساعة الرقمية والتاريخ باللغة العربية.
* **تمييز الصلاة التالية:** تظليل بطاقة الصلاة القادمة تلقائياً لتسهيل المتابعة.
* **إعدادات متقدمة للأذان والإقامة:**
    * **تجاوز التوقيت التلقائي:** إمكانية إدخال وقت محدد يدوياً لكل صلاة.
    * **إعدادات الإقامة:** تفعيل عرض وقت الإقامة وتحديد مدة الانتظار بشكل منفصل لكل صلاة.
* **تنبيهات صوتية:**
    * تشغيل صوت الأذان عند حلول وقته.
    * تشغيل صوت تنبيه عند حلول وقت الإقامة.
    * طلب الإذن من المستخدم لتفعيل الصوت لضمان التوافق مع سياسات المتصفحات الحديثة.
* **تصميم عصري ومتجاوب:** واجهة أنيقة تعمل بكفاءة على جميع الأجهزة (كمبيوتر، تابلت، جوال).

---

## 3. التقنيات المستخدمة

* **HTML5:** لهيكلة المحتوى الأساسي للصفحة.
* **CSS3:** لتنسيق بعض العناصر الأساسية وإضافة انتقالات وحركات.
* **Tailwind CSS:** إطار عمل CSS حديث تم استخدامه لبناء معظم التصميم، مما يوفر سرعة في التطوير ومظهراً متناسقاً.
* **JavaScript (ES6+):** هي المحرك الأساسي للموقع، حيث تتم فيها معالجة كل المنطق البرمجي، بدءاً من جلب البيانات وحتى التفاعل مع المستخدم.

---

## 4. بنية الكود (`JavaScript`)

ينقسم الكود البرمجي إلى عدة أقسام منطقية لتسهيل القراءة والصيانة:

#### أ. المتغيرات العامة وعناصر DOM

في بداية الكود، يتم تعريف جميع الثوابت والمتغيرات التي يحتاجها التطبيق، مثل أسماء الصلوات، قائمة المدن، وربط عناصر HTML بمتغيرات JavaScript لتسهيل التعامل معها.

#### ب. إدارة الإعدادات (`loadSettings`, `saveSettings`)

* **`loadSettings()`:** عند تحميل الصفحة، تقوم هذه الدالة بالتحقق من وجود إعدادات محفوظة للمستخدم في `localStorage`. إذا وجدت، تقوم بتحميلها. إذا لم تجد، تستخدم الإعدادات الافتراضية. هذا يضمن تجربة مخصصة للمستخدم في كل زيارة.
* **`saveSettings()`:** بعد أي تغيير يقوم به المستخدم في نافذة الإعدادات، يتم استدعاء هذه الدالة لحفظ الكائن `settings` بالكامل في `localStorage` بصيغة JSON.

#### ج. جلب البيانات من الإنترنت (`updateUI`, `fetch`)

* **`updateUI()`:** هي الدالة المحورية التي تبدأ عملية تحديث الواجهة. تقوم ببناء رابط الـ API بناءً على المدينة المختارة.
* **`fetch(apiURL)`:** تستخدم لجلب البيانات من `api.aladhan.com`. تتعامل مع حالات النجاح (بتحليل بيانات JSON) وحالات الفشل (بإظهار رسالة خطأ للمستخدم).

#### د. عرض البيانات ومعالجتها (`processAndDisplayTimes`)

* بعد جلب المواقيت بنجاح، تقوم هذه الدالة بالمرور على كل صلاة.
* تتحقق أولاً إذا كان المستخدم قد أدخل وقتاً يدوياً لهذه الصلاة (`settings.overrides`). إذا كان كذلك، تستخدمه. وإلا، تستخدم الوقت القادم من الـ API.
* تحسب وقت الإقامة لكل صلاة بناءً على وقت الأذان والمدة المحددة في الإعدادات.
* تقوم بإنشاء بطاقات عرض الصلاة ديناميكياً وإضافتها إلى الصفحة.

#### هـ. منطق التنبيهات الصوتية والمؤقت (`timeCheckLoop`)

* تعمل هذه الدالة في الخلفية وتتحقق من الوقت كل 30 ثانية (لتحسين الأداء).
* تقارن الوقت الحالي بأوقات الأذان والإقامة المحفوظة.
* إذا تطابق الوقت وكان خيار الصوت مفعّلاً، تقوم بتشغيل الملف الصوتي المناسب (`adhanAudio` أو `iqamaAudio`).
* تسجل الصلوات التي تم تشغيل صوتها في كائن `playedToday` لمنع تكرار الصوت في نفس الدقيقة.

#### و. معالجة الأحداث (`initializeSettingsListeners`, `window.onload`)

* **`initializeSettingsListeners()`:** تربط جميع حقول الإدخال والأزرار داخل نافذة الإعدادات بوظائفها. أي تغيير في الإدخال يؤدي إلى تحديث كائن `settings` ثم استدعاء `updateUI()` لإعادة رسم الواجهة بالبيانات الجديدة.
* **`window.onload`:** عند اكتمال تحميل الصفحة بالكامل، تبدأ هذه الدالة في تشغيل كل شيء: تحميل الإعدادات، ملء النماذج، تشغيل الساعة، وبدء أول عملية جلب للمواقيت.
