#!/usr/bin/env python3

import os
import json
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# โหลด environment variables จากไฟล์ .env
load_dotenv(".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def chatboot(question):
    system_prompt = """ 
        คุณคือระบบจำแนกผลไม้เพื่อวิเคราะห์ความสุกของเมล่อน จากข้อความบรรยาย
        โปรดวิเคราะห์คำบรรยายที่ได้รับ และจำแนกว่าเมลอนนั้นเป็น สุก หรือ ไม่สุก 
        แล้วตอบกลับไปเป็นภาษาไทยเท่านั้น
        
        วิเคราะห์ความสุกของเมล่อน
        พิจารณาจากข้อมูล 6 มิติ ได้แก่:
        1."ค่าพีเอช (pH) ที่แสดงระดับความเป็นกรด-ด่าง"
        2."ค่าองศาบริกซ์ (%Brix) ซึ่งเป็นค่าความหวาน"
        3."สีของเปลือก"
        4."ลักษณะผิวหรือเนื้อสัมผัส"
        5."ความแน่นของเนื้อ"
        6."กลิ่นหอมของเมล่อน"

        โดยเกณฑ์แนะนำที่ใช้ในการพิจารณาความสุกของเมล่อน
        ค่า Brix ≥ 12 = เริ่มถือว่าสุก
        ค่า pH 6.0 – 6.5 = กลาง ๆ ไม่เปรี้ยวเกินไป
        กลิ่นหอม, ผิวนุ่ม, สีเหลืองทอง, เสียงกลวง = บ่งบอกความสุก


        โปรดวิเคราะห์คำบรรยายที่ได้รับ และจำแนกว่าเมล่อนนั้นเป็น สุก หรือ ไม่สุก

        หากคำบรรยายไม่มีข้อมูลเพียงพอในการตัดสินใจ ให้ตอบว่า ไม่สามารถให้คำตอบที่แน่ชัดได้ ขอพิจารณาว่าไม่สุก

        คำอธิบาย: เมล่อนมีเปลือกสีเหลืองทอง ผิวเรียบแต่ยืดหยุ่น กลิ่นหอมแรง %Brix เท่ากับ 15 และค่า pH อยู่ที่ 6.2
        คำตอบ: สุก

        คำอธิบาย: เมล่อนมีสีเปลือกออกเหลืองนวล ผิวนุ่มเล็กน้อย กลิ่นหวานสดชื่น Brix 13.8 และ pH 6.0
        คำตอบ: สุก

        คำอธิบาย: ผิวเมล่อนเริ่มมีความยุบตัวเมื่อกด กลิ่นหอมออกมาชัดเจน สีเปลือกเขียวอมทอง ค่า Brix 14.5
        คำตอบ: สุก

        คำอธิบาย: สีเปลือกเป็นสีเขียวอ่อนค่อนไปทางเหลือง ผิวมีลายตาข่ายชัดเจน กลิ่นหอมฟุ้ง pH 6.3 และ Brix 16
        คำตอบ: สุก

        คำอธิบาย: เมล่อนมีเปลือกบาง กลิ่นหอมมาก ผิวสัมผัสยืดหยุ่น เสียงกลวงเมื่อเคาะ ค่า Brix 15.2
        คำตอบ: สุก

        คำอธิบาย: เมล่อนมีเปลือกสีเขียวเข้ม ผิวแข็ง ไม่มีเสียงเมื่อเคาะ กลิ่นไม่ชัดเจน ค่า Brix เท่ากับ 9.5
        คำตอบ: ไม่สุก

        คำอธิบาย: สีเปลือกเขียวสด ผิวยังแข็งแน่นมาก กลิ่นยังไม่มี ค่า pH 5.4 และ Brix 10
        คำตอบ: ไม่สุก

        คำอธิบาย: เปลือกเมล่อนยังแข็งมาก ไม่มีลายตาข่าย กลิ่นจาง ๆ pH 5.5 Brix 8.7
        คำตอบ: ไม่สุก

        คำอธิบาย: กลิ่นเมล่อนยังไม่ออก สีเขียวเข้มตลอดผล ผิวยังแน่นมาก Brix 9.3
        คำตอบ: ไม่สุก

        คำอธิบาย: เมล่อนมีผิวหยาบ เสียงทึบเมื่อเคาะ กลิ่นแทบไม่มี ค่า Brix ต่ำเพียง 8.9
        คำตอบ: ไม่สุก


        โปรดตอบกลับในรูปแบบ JSON ที่มีโครงสร้างดังนี้:
        "ให้ตอบคำถามความสุกของ เมล่อน เฉพาะข้อมูลที่อยู่ในเอกสารเท่านั้น"
        {
        "ripeness": "สุก" หรือ "ไม่สุก",
        "brix": (ค่าตัวเลข เช่น 13.2 หรือ null ถ้าไม่ระบุ),
        "ph": (ค่าตัวเลข เช่น 6.3 หรือ null ถ้าไม่ระบุ),
        "reason": "คำอธิบายเหตุผลที่ทำให้ตัดสินใจว่าเมล่อนสุกหรือไม่สุก"
        }

        หากไม่มีข้อมูล Brix หรือ pH ให้ใช้ค่า null แทน
        ตอบกลับเฉพาะ JSON เท่านั้น

        หากไม่สามารถตัดสินใจได้ ให้ใช้ "ripeness": "ข้อพิจารณาว่า ไม่สุก เพราะว่าข้อมูลอ้างอิงไม่เพียงพอ" """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0.2,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def main():
    # 🖼️ ตั้งค่าหน้าและธีมสี
    st.set_page_config(page_title="AI Melon Ripeness Bot", page_icon="🍈", layout="wide")
    st.markdown("""
        <style>
        body { background-color: #000000; }
        .stForm { background-color: #000000; padding: 2rem; border-radius: 12px; }
        </style>
    """, unsafe_allow_html=True)

    ##st.image("blue.jpg", use_column_width=True)
    st.title("🍈 แชตบอตเกษตรอัจฉริยะ")
    st.subheader("ช่วยวิเคราะห์ความสุกของเมลอน ด้วย AI ")

    # 🧾 เก็บข้อความสนทนา
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "สวัสดีค่ะ ฉันสามารถช่วยคุณวิเคราะห์ความสุกของเมล่อนได้จากคำบรรยาย 6 มิติค่ะ 🍈"}
        ]

    with st.form("chat_form"):
        query = st.text_input("🗣️ คุณ:", placeholder="พิมพ์ลักษณะของเมลอนที่ต้องการให้วิเคราะห์...").strip()
        submitted = st.form_submit_button("🚀 ส่งข้อความ")

        if submitted and query:
            answer = chatboot(query)
            st.session_state["messages"].append({"role": "user", "content": query})
            st.session_state["messages"].append({"role": "assistant", "content": answer})
        elif submitted and not query:
            st.warning("⚠️ กรุณาพิมพ์คำถามก่อนส่ง")

    # 🧠 แสดงผลแชตพร้อมจัดการ JSON
    for msg in st.session_state["messages"]:
        if msg["role"] == "user":
            st.markdown(f"**🧑‍🌾 คุณ:** {msg['content']}")
        else:
            try:
                data = json.loads(msg["content"])
                with st.container():
                    st.markdown("#### 🤖 ผลการวิเคราะห์เมลอน")
                    col1, col2 = st.columns(2)
                    col1.metric("ความสุก", data.get("ripeness", "ไม่ระบุ"))
                    col1.metric("ค่า Brix", data.get("brix", "ไม่ระบุ"))
                    col2.metric("ค่า pH", data.get("ph", "ไม่ระบุ"))
                    st.info(data.get("reason", ""))
            except Exception:
                st.markdown(f"**🤖 บอท:** {msg['content']}")

    st.markdown("---")
    st.caption("🌱 พัฒนาโดยทีม Sn.Guardian gen X เป็นส่วนหนึ่งของโครงการบ่มเพาะนวัตกรปัญญาประดิษฐ์ (AI Innovator) 🤖")

if __name__ == "__main__":
    main()
