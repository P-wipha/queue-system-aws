<div align="center">

# ระบบจองคิวออนไลน์บน AWS
### Cloud Queue Booking System

![AWS](https://img.shields.io/badge/AWS-Serverless-f9c6d0?style=flat-square&logo=amazonaws&logoColor=c47a85)
![Python](https://img.shields.io/badge/Python-Lambda-c9e4ca?style=flat-square&logo=python&logoColor=5a8a5e)
![HTML](https://img.shields.io/badge/HTML-Frontend-fde8c8?style=flat-square&logo=html5&logoColor=c4834a)
![DynamoDB](https://img.shields.io/badge/DynamoDB-Database-c8d8f5?style=flat-square&logo=amazondynamodb&logoColor=4a6ab5)
![S3](https://img.shields.io/badge/S3-Hosting-e8d5f5?style=flat-square&logo=amazons3&logoColor=8a5ab5)
![API Gateway](https://img.shields.io/badge/API_Gateway-REST-fdf5c8?style=flat-square&logo=amazonapigateway&logoColor=a09040)

<br/>

**วิชา ICT24467** — การพัฒนาซอฟต์แวร์ระบบประมวลผลคลาวด์และความปลอดภัยของข้อมูล

มหาวิทยาลัยศรีปทุม ภาคการศึกษาที่ 2 ปีการศึกษา 2568

</div>

---

## 🌸 สมาชิกกลุ่ม

| ชื่อ | รหัสนักศึกษา |
|:-----|:------------:|
| นางสาว วิภาภรณ์ ปลอดสันเทียะ | 67094859 |
| นางสาว ณัฐชา แล้วกระโทก | 67126501 |
| นางสาว ทิวารัตน์ อัมฤทธิ์ | 67167139 |
| นางสาว พลอยลดา สุขภักดีธนพงศ์ | 67171448 |

---

## 🏗️ สถาปัตยกรรมระบบ
```mermaid
flowchart TD
    A[👤 ผู้ใช้งาน Browser] --> B[🪣 Amazon S3\nindex.html / admin.html]
    B --> C[🔗 Amazon API Gateway]
    C --> D[⚡ AWS Lambda\n7 Functions Python]
    D --> E[🗄️ Amazon DynamoDB\nqueue_db]

    style A fill:#fde8f0,stroke:#f4a7c3,color:#333
    style B fill:#fdf5c8,stroke:#f0d060,color:#333
    style C fill:#e8d5f5,stroke:#c4a0e8,color:#333
    style D fill:#c9e4ca,stroke:#90c490,color:#333
    style E fill:#c8d8f5,stroke:#90b0e8,color:#333
```

---

## ☁️ เทคโนโลยีที่ใช้

| บริการ | หน้าที่ |
|:-------|:--------|
| 🗄️ Amazon DynamoDB | จัดเก็บข้อมูลคิวทั้งหมด |
| ⚡ AWS Lambda | ประมวลผล Backend (Python) |
| 🔗 Amazon API Gateway | เปิด HTTP API ให้หน้าเว็บเรียกใช้ |
| 🪣 Amazon S3 | Host หน้าเว็บไซต์แบบ Static |

---

## ⚡ Lambda Functions ทั้ง 7 ฟังก์ชัน

| ฟังก์ชัน | Method | Path | หน้าที่ |
|:---------|:------:|:-----|:--------|
| `createQueue` | POST | `/queue` | สร้างคิวใหม่ |
| `getQueues` | GET | `/queues` | ดูคิวทั้งหมด (แอดมิน) |
| `getQueueByPhone` | GET | `/queue-by-phone` | ค้นหาคิวด้วยเบอร์โทร |
| `getCurrentQueue` | GET | `/current-queue` | ดูคิวปัจจุบัน |
| `nextQueue` | POST | `/next-queue` | เรียกคิวถัดไป |
| `updateQueueStatus` | POST | `/update-status` | อัปเดตสถานะคิว |
| `clearAllQueues` | POST | `/clear-queues` | ล้างคิวทั้งหมด |

---

## 📁 โครงสร้างโปรเจกต์

```
queue-system-aws/
├── README.md
├── frontend/
│   ├── index.html
│   └── admin.html
└── lambda/
    ├── createQueue.py
    ├── getQueues.py
    ├── getQueueByPhone.py
    ├── getCurrentQueue.py
    ├── nextQueue.py
    ├── updateQueueStatus.py
    └── clearAllQueues.py
---

## 🌐 ลิงก์เว็บไซต์จริง

<div align="center">

| หน้า | ลิงก์ |
|:----:|:------|
| 👤 หน้าลูกค้า | [index.html](https://queue-web-2026.s3.ap-southeast-1.amazonaws.com/index.html) |
| 🔧 หน้าแอดมิน | [admin.html](https://queue-web-2026.s3.ap-southeast-1.amazonaws.com/admin.html) |

</div>

---

## 🔄 การทำงานของระบบ

**🧍 ฝั่งลูกค้า**
1. 📝 กรอกชื่อและเบอร์โทร → ยืนยัน PDPA → จองคิว
2. 🔍 ตรวจสอบสถานะคิวด้วยเบอร์โทร
3. ❌ ยกเลิกคิวด้วยตนเอง

**🛠️ ฝั่งแอดมิน**
1. 📋 ดูรายการคิวทั้งหมดแบบ real-time
2. ➡️ เรียกคิวถัดไป
3. 🗑️ ยกเลิกหรือรีเซ็ตคิวทั้งหมด

---

<div align="center">
  <sub>🌷 เสนอ อาจารย์ อำนาจ คงเจริญถิ่น &nbsp;|&nbsp; มหาวิทยาลัยศรีปทุม 2568 🌷</sub>
</div>
