# ==========================================
#  المعلم - Moallem v3.0
#  تشخيص + زبناء + فلوس + WhatsApp
# ==========================================

import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import datetime

st.set_page_config(page_title="المعلم v3.0 - WhatsApp", page_icon="🔧")

F_MEMOIRE = "memoire_moallem.csv"
F_CLIENTS = "clients_moallem.csv"

def charger_memoire():
    if os.path.exists(F_MEMOIRE):
        return pd.read_csv(F_MEMOIRE)
    data = [[0.07,1,4.2,1.8,"khadama","J710"],[0.00,0,0.0,0.0,"VBAT","J710"],[0.00,0,4.2,0.0,"PWRKEY","J710"]]
    df = pd.DataFrame(data, columns=["sahb","vibration","vbat","pwrkey","resultat","model"])
    df.to_csv(F_MEMOIRE, index=False)
    return df

def charger_clients():
    if os.path.exists(F_CLIENTS):
        return pd.read_csv(F_CLIENTS)
    df = pd.DataFrame(columns=["date","nom","telephone","model","panne","diagnostic","prix","paye","reste","statut"])
    df.to_csv(F_CLIENTS, index=False)
    return df

df = charger_memoire()
df_clients = charger_clients()

def diagnostiquer(sahb, vibration, vbat, pwrkey):
    if vbat <= 2.0: return "VBAT", "قلب court-circuit"
    if pwrkey <= 0.9: return "PWRKEY", "الزر ما واصلش"
    if vibration == 0 and sahb <= 0.05: return "PMIC", "البوردة ما كتفيقش"
    if vibration == 0 and sahb > 0.05: return "moteur", "moteur خاسر"
    if vibration == 1 and vbat <= 3.6: return "khadama-batterie-naqsa", "batterie naqsa"
    if vibration == 1: return "khadama", "البوردة خدامة"
    return "غير معروف", "زيد قياسات"

# --- دالة WhatsApp - هادي هي القيمة ---
def lien_whatsapp(telephone, nom, model, diagnostic, reste, statut):
    # نقي النمرة: نحيدو + و الفراغات
    tel = str(telephone).replace("+","").replace(" ","").replace("-","")
    # إلا كانت النمرة مغربية وبدات بـ 06، نزيدو 212
    if tel.startswith("06") or tel.startswith("07"):
        tel = "212" + tel[1:]
    if statut == "تصلح":
        msg = f"سلام {nom}، معاك المعلم من محل التصليح. البوردة ديالك {model} واجدة، المشكل كان {diagnostic}. أجي خودها. باقي ليك {reste} درهم. شكرا 🙏"
    elif statut == "قيد التصليح":
        msg = f"سلام {nom}، البوردة ديالك {model} مازالا كنصلحوها، المشكل هو {diagnostic}. غادي نعيطو ليك ملي توجد. المعلم 🔧"
    elif statut == "ما تصلحش":
        msg = f"سلام {nom}، قلبنا البوردة ديالك {model}، المشكل هو {diagnostic} وما كتصلحش، أجي خودها بلا ما تخلص. المعلم"
    else:
        msg = f"سلام {nom}، شكرا جيتي عندنا، البوردة ديالك {model} تسلمات. إلا كان شي مشكل، رجع عندنا. المعلم 🔧"
    msg_encoded = urllib.parse.quote(msg)
    return f"https://wa.me/{tel}?text={msg_encoded}", msg

st.title("🔧 المعلم - Moallem v3.0")
st.write("تشخيص + زبناء + فلوس + WhatsApp أوتوماتيك")

# --- لوحة الفلوس ---
total_paye = df_clients["paye"].sum() if len(df_clients)>0 else 0
total_reste = df_clients["reste"].sum() if len(df_clients)>0 else 0
c1,c2,c3,c4 = st.columns(4)
c1.metric("بوردة تعلمنا", len(df))
c2.metric("زبون", len(df_clients))
c3.metric("دخلنا DH", f"{total_paye:.0f}")
c4.metric("باقي DH", f"{total_reste:.0f}")
st.divider()

tab1, tab2, tab3 = st.tabs(["🔍 تشخيص", "👤 زبون جديد", "💬 WhatsApp + الفلوس"])

with tab1:
    st.subheader("دخل القياسات")
    model = st.selectbox("الموديل", ["J710","A10s","A12","Redmi 9","أخر"], key="m1")
    sahb = st.number_input("السحب (A)", 0.0, 2.0, 0.07, 0.01)
    vibration = st.selectbox("فيبرور؟", [1,0], format_func=lambda x: "نعم" if x==1 else "لا")
    vbat = st.number_input("VBAT", 0.0, 5.0, 4.2, 0.1)
    pwrkey = st.number_input("PWRKEY", 0.0, 2.0, 1.8, 0.1)
    if st.button("شخص ليا", type="primary"):
        res, conseil = diagnostiquer(sahb, vibration, vbat, pwrkey)
        st.success(f"التشخيص: {res}")
        st.info(f"النصيحة: {conseil}")
        st.session_state["diag"] = res
        st.session_state["mesures"] = (sahb, vibration, vbat, pwrkey, model)

with tab2:
    st.subheader("زيد زبون جديد")
    nom = st.text_input("اسم الزبون")
    tel = st.text_input("النمرة - مثلا 0612345678")
    model2 = st.selectbox("الموديل", ["J710","A10s","A12","Redmi 9","أخر"], key="m2")
    panne = st.text_input("شنو قال ليك؟")
    diag = st.text_input("التشخيص", value=st.session_state.get("diag",""))
    prix = st.number_input("الثمن DH", 0, 2000, 150)
    paye = st.number_input("خلص دابا DH", 0, 2000, 100)
    reste = prix - paye
    st.write(f"باقي: **{reste} DH**")
    statut = st.selectbox("الحالة", ["قيد التصليح","تصلح","تسلم","ما تصلحش"])
    if st.button("سجل الزبون ✅"):
        if nom=="": st.error("دخل اسم الزبون")
        else:
            nouveau = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), nom, tel, model2, panne, diag, prix, paye, reste, statut]], columns=["date","nom","telephone","model","panne","diagnostic","prix","paye","reste","statut"])
            pd.concat([df_clients, nouveau], ignore_index=True).to_csv(F_CLIENTS, index=False)
            st.success(f"تسجل {nom} - {model2} - {prix} DH")
            st.balloons()

with tab3:
    st.subheader("💬 صيفط WhatsApp للزبون")
    if len(df_clients)>0:
        st.dataframe(df_clients)
        st.divider()
        # نختارو الزبون
        noms = df_clients["nom"].tolist()
        choix = st.selectbox("ختار الزبون", noms)
        row = df_clients[df_clients["nom"]==choix].iloc[0]
        st.write(f"**{row['nom']}** - {row['model']} - {row['diagnostic']} - باقي {row['reste']} DH - الحالة: {row['statut']}")
        # نبدلو الحالة إلا بغينا
        nouveau_statut = st.selectbox("بدل الحالة وصيفط مساج", ["تصلح","قيد التصليح","تسلم","ما تصلحش"], index=0)
        lien, msg = lien_whatsapp(row["telephone"], row["nom"], row["model"], row["diagnostic"], row["reste"], nouveau_statut)
        st.info(f"المساج اللي غادي يتصيفط:\n\n{msg}")
        st.link_button(f"📱 صيفط في WhatsApp لـ {row['nom']}", lien)
        st.write("ملي تبرك على الزر، غادي يتحل WhatsApp، والمساج واجد، غير برك Envoyer.")
        if st.button("بدل الحالة في الجدول"):
            df_clients.loc[df_clients["nom"]==choix, "statut"] = nouveau_statut
            df_clients.to_csv(F_CLIENTS, index=False)
            st.success(f"بدلنا الحالة ديال {choix} لـ {nouveau_statut}")
    else:
        st.write("مازال ما عندك حتى زبون.")

    st.divider()
    st.subheader("📚 الذاكرة")
    st.dataframe(df)
