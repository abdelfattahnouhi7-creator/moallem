import streamlit as st
import streamlit.components.v1 as components
import urllib.parse

st.set_page_config(page_title="المعلم v6.1 - بالصوت", page_icon="🎤", layout="wide")
st.title("🧠 المعلم v6.1 - بالصوت 🎤")
st.caption("14 شجرة | هضر والمعلم يفهمك | Samsung + iPhone 2024-2026")

EXPERT = {
"ما كيشعلش - NO POWER": {"desc":"ميت تماما.","steps":["1- قيس البطارية 3.7-4.4V. إلا 0V جرب بطارية اخرى.","2- باور سبلاي 4.2V. سحب 0.00A = قطع VBAT. قيس كونكتور + فيوز.","3- سحب ثابت 0.20-0.35A = شورت. حقن 1.8V في VPH + كاميرا حرارية.","4- سحب 0.50A+ = شورت صريح في VDD_MAIN.","5- PWRKEY خاص يكون 1.8V. إلا 0V = زر باور.","6- سحب 0.08A ثابت = IC Power او UFS.","7- فك كل الفلاتات وجرب. 30% فلاتة.","8- طاح في الماء: نقي البوردة قبل اي قياس.","9- بعد سوفت: جرب EDL / DFU.","10- احتمال اخير: المعالج - بدل بوردة."],"samsung_note":"A15/A25/A35: الفيوز كيقطع بعد شاحن غير اصلي.","iphone_note":"15/16/17: سحب 0.22A ثابت = Tristar."},
"ما كيشارجيش - NO CHARGE": {"desc":"كيشعل ولكن ما كيطلعش الشحن.","steps":["1- جرب كابل + شاحن اصلي. 40% غير كابل.","2- نقي كونكتور الشحن. قيس 5V.","3- VBUS=5V؟ إلا لا = كونكتور او فلاتة سفلية.","4- VBAT اثناء الشحن خاص يطلع لـ 4.2V.","5- كيقول حرارة مرتفعة = NTC حدا البطارية.","6- كيشارجي ببطء = مقاومة في فلاتة الشحن.","7- كيشارجي غير في جهة = Tristar.","8- بعد الماء = نقي بوردة الشحن السفلية.","9- كيطلع علامة وكيطفى = بطارية ميتة.","10- احتمال اخير: IC Power."],"samsung_note":"A55/A56: IC شحن كيسخن مع 45W.","iphone_note":"15/16: Tristar. 17: Hydra."},
"الشاشة كحلة / ما كتبانش": {"desc":"كيهتز ولكن الشاشة كحلة.","steps":["1- وصل بالشاحن. إلا دار فيبرور = البوردة خدامة.","2- جرب شاشة اخرى. 70% كيتحل هكا.","3- قيس LED_A = 20-30V. إلا 0V = IC اضاءة.","4- قيس كونكتور الشاشة.","5- بعد طيحة = فلاتة الشاشة مقطوعة.","6- بعد الماء = نقي كونكتور.","7- الصورة خدامة والتاتش لا = فلاتة التاتش.","8- خطوط / الوان = الشاشة نفسها.","9- بعد تبديل شاشة = غير متوافقة.","10- احتمال اخير: المعالج / MIPI."],"samsung_note":"S24/S25: 80% الشاشة نفسها بعد طيحة.","iphone_note":"15 Pro Max: فلاتة الشاشة كتقطع."},
"ما فيهش ريزو - NO SERVICE": {"desc":"ما كيلقاش الريزو.","steps":["1- جرب SIM اخرى. *#06# واش IMEI كاين.","2- IMEI=0 = سوفت / EFS.","3- وضع طيران 10 ثواني وحيدو.","4- IMEI سليم = قيس PA.","5- كونكتور الانتين / كابل مقطوع؟","6- طاح في الماء = نقي خطوط الشبكة.","7- بعد سوفت = Baseband ضايع.","8- كيلقى وكيمشي = الانتين / PA ضعيف.","9- Dual SIM وحدة خدامة = قارئ SIM.","10- احتمال اخير: IC شبكة."],"samsung_note":"A15/A16: كابل الانتين كيتقطع.","iphone_note":"بعد تبديل شاشة = كابل الانتين اللي فوق."},
"كيسخن بزاف / كيخوى الشارج": {"desc":"كيسخن حتى وهو طافي.","steps":["1- باور سبلاي وهو طافي. سحب 0.10-0.30A = تسريب.","2- فك فلاتة الكاميرا.","3- فك فلاتة الشحن.","4- فك فلاتة الشاشة.","5- حقن 4.2V + كاميرا حرارية.","6- غالبا مكثف او IC شحن.","7- بعد تحديث = سوفت.","8- بعد الماء = تآكل.","9- بطارية منفوخة = بدلها فورا.","10- احتمال اخير: المعالج."],"samsung_note":"A55 بعد الماء.","iphone_note":"15 Pro Max: بعد تحديث = سوفت."},
"واقف على اللوغو / كيعاود يشعل": {"desc":"Bootloop.","steps":["1- ريكفري. Wipe Cache.","2- سوفت كامل.","3- سحب طالع نازل = UFS / NAND.","4- Samsung: شبلنة UFS 80%.","5- iPhone: DFU Update قبل Restore.","6- قيس البطارية.","7- قيس زر الباور.","8- فك فلاتة الكاميرا.","9- بعد طيحة = UFS مفصول.","10- احتمال اخير: المعالج."],"samsung_note":"A12/A15: Bootloop من البطارية.","iphone_note":"واقف على التفاحة = NAND."},
"الكاميرا كحلة / ما كتفتحش": {"desc":"كاميرا كتخرج او كحلة.","steps":["1- جرب الامامية والخلفية بوحدهم.","2- نقي كونكتور الكاميرا.","3- جرب كاميرا اخرى.","4- قيس VCAM=2.8V.","5- كترجف = OIS. بدل الكاميرا.","6- كتفتح وتخرج = شورت في الكاميرا.","7- بعد سوفت = Reset.","8- بعد طيحة = كونكتور مرخي.","9- بعد الماء = تآكل.","10- احتمال اخير: IC تغذية."],"samsung_note":"S24 Ultra: إلا كتخرج = سوفت قبل تبديل.","iphone_note":"15 Pro: الكاميرا الامامية مربوطة مع Face ID."},
"الصوت - ما كيتسمعش / الميكرو": {"desc":"صوت / ميكرو.","steps":["1- حدد: مكالمة؟ فيديو؟ سبيكر؟","2- مكالمة لا وسبيكر ايه = سماعة داخلية.","3- ميكرو مكالمة لا وفيديو ايه = ميكرو سفلي.","4- كيوشوش = نقي شبكة السماعة.","5- جرب سماعة / ميكرو اخر.","6- قيس SPK_P / SPK_N.","7- بعد الماء = IC صوت.","8- ما كاين والو صوت = واش البلوتوث مشبوك؟","9- كيقطع = سماعة ضعيفة.","10- احتمال اخير: Audio Codec."],"samsung_note":"A15/A25: السماعة كتوسخ.","iphone_note":"15/16: الميكرو في فلاتة السماعة."},
"البصمة / Face ID ما خدامش": {"desc":"بصمة او Face ID.","steps":["1- مسح البصمة وعاود سجلها.","2- نقي بلاصة البصمة.","3- بعد تبديل شاشة = مربوطة مع الاصلية.","4- Samsung: Calibration.","5- iPhone Face ID: بعد تبديل شاشة = خاص نقل القطع.","6- بعد طيحة = فلاتة مقطوعة.","7- بعد الماء = مصدي.","8- كيقول حاول من بعد = Reset Face ID.","9- قيس كونكتور.","10- احتمال اخير: IC البصمة."],"samsung_note":"A35/A55: البصمة في الشاشة.","iphone_note":"Face ID: Dot Projector كيتكسر مع طيحة."},
"الواي فاي / البلوتوث ما خدامش": {"desc":"واي فاي ما كيلقاش.","steps":["1- وضع طيران 10 ثواني وحيدو.","2- نسي الشبكة وعاود دخل الكود.","3- جرب واي فاي اخر.","4- كيطفى بوحدو = IC كيسخن.","5- بلوتوث ما كيلقاش = جرب جهاز اخر.","6- بعد طيحة = كابل الانتين.","7- بعد الماء = نقي IC.","8- واي فاي رمادي = IC مضروب.","9- بعد سوفت = Reset Network.","10- احتمال اخير: IC واي فاي."],"samsung_note":"A15: IC واي فاي بعد طيحة.","iphone_note":"15/16: واي فاي + بلوتوث في نفس IC."},
"التاتش ما خدامش": {"desc":"الشاشة كتبان ولكن التاتش لا.","steps":["1- رستارتي.","2- حيد الجراب / الزجاج.","3- نقي الشاشة.","4- جرب شاشة اخرى.","5- خدام في بلاصة ولا = الشاشة مكسورة.","6- بعد تبديل شاشة = غير متوافقة.","7- بعد الماء = نقي كونكتور.","8- قيس كونكتور.","9- كيتحرك بوحدو = شاشة / شاحن غير اصلي.","10- احتمال اخير: IC التاتش."],"samsung_note":"A35: التاتش مع شاحن غير اصلي.","iphone_note":"15: التاتش مربوط مع الشاشة."},
"البطارية كتنفخ / كتخوى بسرعة": {"desc":"بطارية.","steps":["1- منفوخة = بدلها فورا. خطر.","2- صحة البطارية تحت 80% = بدلها.","3- شوف التطبيقات اللي كتاكل.","4- كتخوى وهو طافي = تسريب.","5- كتشارجي وتخوى = IC شحن.","6- كتسخن = بطارية او IC.","7- جرب بطارية اخرى.","8- بعد الماء = مضروبة.","9- بعد طيحة = كونكتور.","10- احتمال اخير: المعالج."],"samsung_note":"A15: كتنفخ مع شاحن غير اصلي.","iphone_note":"15/16: صحة البطارية في الاعدادات."},
"السيم ما كتقراش / No SIM": {"desc":"SIM.","steps":["1- جرب SIM اخرى.","2- نقي بلاصة SIM.","3- Dual SIM: جرب بوحدهم.","4- No SIM = قارئ مصدي.","5- بعد طيحة = مفصول.","6- بعد الماء = نقي.","7- IMEI=0 = سوفت.","8- كيقرا وكيقطع = قارئ ضعيف.","9- وضع طيران وحيدو.","10- احتمال اخير: IC SIM."],"samsung_note":"A15: قارئ كيتكسر.","iphone_note":"US: eSIM فقط."},
"السنسور / التقريب / الدوران": {"desc":"سنسور.","steps":["1- الشاشة ما كتطفاش في المكالمة = سنسور التقريب موسخ.","2- بعد تبديل شاشة = ما تركبش مزيان.","3- الدوران لا = جيروسكوب. رستارتي.","4- البوصلة غالطة = Calibration.","5- السطوع التلقائي لا = سنسور الضوء.","6- بعد الماء = مصدي.","7- بعد طيحة = مفصول.","8- سوفت. Reset.","9- قيس كونكتور.","10- احتمال اخير: IC سنسور."],"samsung_note":"A35: سنسور التقريب كيتوسخ.","iphone_note":"15/16: سنسور في فلاتة السماعة."},
}

# ===== محرك الفهم بالدارجة - يفهم اي كلمة =====
def find_symptom(text):
    if not text: return None
    t = text.lower().strip()
    mapping = {
        "الكاميرا كحلة / ما كتفتحش": ["كاميرا", "camera", "cam", "تصوير", "كحلة كاميرا"],
        "الصوت - ما كيتسمعش / الميكرو": ["صوت", "ميكرو", "mic", "سماعة", "ماكيتسمعش", "مكيتسمعش", "صوت"],
        "الشاشة كحلة / ما كتبانش": ["شاشة", "كحلة", "ecran", "شاشة كحلة", "ماكتبانش"],
        "ما كيشعلش - NO POWER": ["ماكيشعلش", "ما كيشعلش", "ميت", "طافي", "مايشعلش", "power"],
        "ما كيشارجيش - NO CHARGE": ["ماكيشارجيش", "ما كيشارجيش", "شحن", "charge", "شارج", "كيشارجي"],
        "ما فيهش ريزو - NO SERVICE": ["ريزو", "شبكة", "reseau", "service", "signal"],
        "كيسخن بزاف / كيخوى الشارج": ["كيسخن", "سخونية", "كيخوى", "حرارة", "سخون"],
        "واقف على اللوغو / كيعاود يشعل": ["لوغو", "كيعاود", "boot", "واقف", "تفاحة", "logo"],
        "البصمة / Face ID ما خدامش": ["بصمة", "face", "فيس", "empreinte", "بصمه"],
        "الواي فاي / البلوتوث ما خدامش": ["واي فاي", "wifi", "بلوتوث", "bluetooth", "ويفي"],
        "التاتش ما خدامش": ["تاتش", "touch", "لمس", "ماكيتحركش"],
        "البطارية كتنفخ / كتخوى بسرعة": ["بطارية", "batterie", "منفوخة", "كتخوى", "battery"],
        "السيم ما كتقراش / No SIM": ["سيم", "sim", "كارت", "puce"],
        "السنسور / التقريب / الدوران": ["سنسور", "تقريب", "دوران", "capteur", "sensor"],
    }
    for key, words in mapping.items():
        for w in words:
            if w in t:
                return key
    return None

# ===== 0. قسم الصوت =====
st.subheader("🎤 هضر دابا - بلا ما تكتب")
st.write("برك على الزر، وقول: `كاميرا كحلة`، `صوت ما كيتسمعش`، `شاشة كحلة`، `بصمة`...")

# زر الصوت - HTML + JS Speech Recognition
components.html("""
<div style="text-align:center; padding:10px;">
  <button id="micBtn" style="background:#FF4B4B; color:white; border:none; padding:15px 30px; border-radius:50px; font-size:18px; cursor:pointer; font-weight:bold;">🎤 هضر دابا - برك وقول العطل</button>
  <p id="result" style="color:white; margin-top:10px; font-size:16px;"></p>
  <p style="color:#888; font-size:12px;">كيخدم في Chrome / Brave / في التلفون. إلا ما خدمش، استعمل الميكرو ديال الكلافيي.</p>
</div>
<script>
const btn = document.getElementById('micBtn');
const res = document.getElementById('result');
btn.onclick = () => {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SR){ res.innerText = 'المتصفح ديالك ما كيدعمش الصوت. استعمل الميكرو ديال الكلافيي.'; return; }
  const rec = new SR();
  rec.lang = 'ar-MA';
  rec.interimResults = false;
  res.innerText = '🎧 كنسمعك... قول العطل دابا...';
  btn.innerText = '🎧 كنسمع...';
  rec.onresult = (e) => {
    const txt = e.results[0][0].transcript;
    res.innerText = 'سمعتك: ' + txt + ' - كنحولك للتشخيص...';
    // نرسل النص لـ Streamlit عن طريق الرابط
    const url = new URL(window.parent.location.href);
    url.searchParams.set('voice', txt);
    window.parent.location.href = url.toString();
  };
  rec.onerror = () => { res.innerText = 'ما سمعتكش مزيان. عاود برك وقول بصوت واضح.'; btn.innerText = '🎤 هضر دابا'; };
  rec.onend = () => { btn.innerText = '🎤 هضر دابا'; };
  rec.start();
};
</script>
""", height=140)

# قراءة الصوت من الرابط
voice_text = st.query_params.get("voice", "")
if voice_text:
    st.success(f"🎤 سمعتك قلتي: **{voice_text}**")
    found = find_symptom(voice_text)
    if found:
        st.info(f"فهمتك: **{found}** - هاهي الخطوات:")
        # غادي نختارو اوتوماتيكيا لتحت
        st.session_state["auto_symptom"] = found
    else:
        st.warning(f"ما فهمتش `{voice_text}` مزيان. جرب تقول: كاميرا، صوت، شاشة، بصمة، واي فاي...")
    if st.button("مسح الصوت"):
        st.query_params.clear()
        st.rerun()

# ===== 1. اختيار المشكل - كتابة او صوت =====
st.subheader("1. شنو هو المشكل؟")
# إلا كان الصوت خدام، نختارو اوتوماتيكيا
default_idx = 0
if "auto_symptom" in st.session_state and st.session_state["auto_symptom"] in EXPERT:
    default_idx = list(EXPERT.keys()).index(st.session_state["auto_symptom"])

# بحث سريع بالكتابة - حتى هو كيفهم الدارجة
search = st.text_input("🔎 ولا كتب هنا بالدارجة: كاميرا، صوت، شاشة، بصمة...", value=voice_text if voice_text else "")
if search:
    f = find_symptom(search)
    if f:
        default_idx = list(EXPERT.keys()).index(f)
        st.info(f"فهمتك: **{f}**")

symptom = st.selectbox("اختار العرض", list(EXPERT.keys()), index=default_idx)

col1, col2 = st.columns(2)
with col1:
    model = st.selectbox("الموديل", ["S24","S24 Ultra","S25","S25 Ultra","S26","S26 Ultra","A15","A25","A35","A55","A16","A26","A36","A56","Z Flip 6","Z Fold 6","iPhone 15","iPhone 15 Pro","iPhone 15 Pro Max","iPhone 16","iPhone 16 Pro","iPhone 16 Pro Max","iPhone 17","iPhone 17 Pro","iPhone 17 Pro Max","iPhone Air"])
    cur = st.number_input("السحب (A)", 0.0, 2.0, 0.08, 0.01)
with col2:
    vbat = st.number_input("VBAT (V)", 0.0, 5.0, 4.2, 0.1)
    pwr = st.number_input("PWRKEY (V)", 0.0, 3.0, 1.8, 0.1)
    water = st.checkbox("طاح في الماء؟")
    dropped = st.checkbox("طاح في الارض؟")

if st.button("عطيني كل الاحتمالات - 🧠", type="primary"):
    data = EXPERT[symptom]
    st.success(f"**التشخيص: {symptom}**")
    st.write(f"**الوصف:** {data['desc']}")
    st.warning("**🧠 تحليل المعلم:**")
    if cur == 0.0: st.write("- السحب 0.00A = قطع.")
    elif cur >= 0.50: st.write(f"- السحب {cur}A = شورت صريح!")
    elif cur >= 0.20: st.write(f"- السحب {cur}A = شورت او تسريب IC.")
    else: st.write(f"- السحب {cur}A = قريب من الطبيعي. المشكل غالبا سوفت، فلاتة، او قطعة.")
    if water: st.write("- طاح في الماء = نقي البوردة كاملة الاول.")
    if dropped: st.write("- طاح في الارض = قلب الفلاتات الاول. 70% فلاتة.")
    st.write("---")
    st.subheader("📋 كل الاحتمالات بالترتيب:")
    for step in data["steps"]:
        st.write(f"- {step}")
    st.write("---")
    if "iPhone" in model: st.info(f"**🍎 ملاحظة iPhone:** {data['iphone_note']}")
    else: st.info(f"**📱 ملاحظة Samsung:** {data['samsung_note']}")

st.divider()
st.subheader("👤 زبون جديد")
nom = st.text_input("اسم الزبون")
tel = st.text_input("النمرة")
prix = st.number_input("الثمن", value=150)
paye = st.number_input("خلص", value=100)
if st.button("سجل و صيفط WhatsApp"):
    rest = prix - paye
    msg = f"سلام {nom}، هاتفك {model} - المشكل: {symptom} - واجد. باقي {rest} درهم. المعلم 🔧"
    st.success(f"تم! باقي {rest} DH")
    st.text_area("المساج", msg)
    if tel: st.link_button("صيفط WhatsApp", f"https://wa.me/212{tel[1:]}?text={msg}")
st.caption("المعلم v6.1 | بالصوت 🎤 | 14 شجرة | Samsung + iPhone 2024-2026")
