import streamlit as st
import secrets
import string
import pandas as pd # Excel ve veri işlemleri için
from datetime import datetime

# --- 1. SAYFA VE TEMA AYARLARI ---
st.set_page_config(page_title="Eclit Pro Şifre Yönetimi", page_icon="🔐")

# Geçmişi hafızada tutmak için "Session State" kullanıyoruz
if 'sifre_gecmisi' not in st.session_state:
    st.session_state['sifre_gecmisi'] = []

# --- 2. FONKSİYONLAR ---
def generate_safe_password(length, use_digits, use_symbols, use_uppercase):
    chars = string.ascii_lowercase
    if use_uppercase: chars += string.ascii_uppercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation
    return ''.join(secrets.choice(chars) for _ in range(length))

# --- 3. ARAYÜZ (SIDEBAR) ---
st.sidebar.header("⚙️ Özelleştirme")
uzunluk = st.sidebar.slider("Karakter Uzunluğu", 8, 32, 16)
buyuk_harf = st.sidebar.checkbox("Büyük Harf", value=True)
rakamlar = st.sidebar.checkbox("Rakamlar", value=True)
semboller = st.sidebar.checkbox("Semboller", value=True)

# --- 4. ANA EKRAN ---
st.title("🛡️ Eclit Şifre Oluşturucu v2")
email = st.text_input("Kurumsal E-posta", placeholder="ad.soyad@eclit.com")

if st.button("🚀 Güvenli Şifre Üret"):
    if email.lower().endswith("@eclit.com"):
        yeni_sifre = generate_safe_password(uzunluk, rakamlar, semboller, buyuk_harf)
        zaman = datetime.now().strftime("%H:%M:%S")
        
        # Geçmişe ekle (En başa ekler)
        st.session_state['sifre_gecmisi'].insert(0, {
            "Saat": zaman,
            "Şifre": yeni_sifre,
            "Uzunluk": uzunluk
        })
        
        st.success("Yeni Şifre Oluşturuldu!")
        st.code(yeni_sifre) # Streamlit'te st.code zaten kopyalama butonu içerir!
        st.balloons() # Küçük bir kutlama efekti
    else:
        st.error("Lütfen geçerli bir @eclit.com adresi girin.")

st.divider()

# --- 5. GEÇMİŞ VE EXCEL ÇIKTISI ---
if st.session_state['sifre_gecmisi']:
    st.subheader("📜 Şifre Geçmişi")
    
    # Veriyi tabloya dönüştür
    df = pd.DataFrame(st.session_state['sifre_gecmisi'])
    st.table(df) # Geçmiş listesini gösterir

    # Excel Çıktısı Hazırlama
    # Not: Pandas sayesinde Excel (CSV) formatına çeviriyoruz
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Geçmişi Excel (CSV) Olarak İndir",
        data=csv,
        file_name=f"eclit_sifre_gecmisi_{datetime.now().strftime('%Y%m%d')}.csv",
        mime='text/csv',
    )
else:
    st.info("Henüz şifre üretilmedi. Geçmiş burada görünecek.")