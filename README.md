# ERP System (MVP) - Django + DRF

هذا مشروع **نواة ERP** (قابل للتوسّع) مبني على Django و DRF:

- تعدد الشركات/المؤسسات (Organization) عبر **Row-Level Multi-Tenancy**
- JWT Authentication
- وحدات أساسية: المخزون + المبيعات + المشتريات
- توثيق API عبر Swagger (OpenAPI)

## التشغيل محلياً

```bash
python3 -m pip install -r requirements.txt
python3 erp_backend/manage.py migrate
python3 erp_backend/manage.py createsuperuser
python3 erp_backend/manage.py runserver 0.0.0.0:8000
```

## الروابط

- Admin: `http://localhost:8000/admin/`
- Swagger: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## استخدام سريع (API)

1) احصل على JWT:
- POST ` /api/auth/token/ ` مع `username` و `password`

2) أنشئ مؤسسة:
- POST ` /api/orgs/ ` { "name": "My Company" }

3) استخدم مسارات المؤسسة (org_id):
- ` /api/orgs/<org_id>/items/ `
- ` /api/orgs/<org_id>/warehouses/ `
- ` /api/orgs/<org_id>/customers/ `
- ` /api/orgs/<org_id>/sales-invoices/ ` ثم POST `.../<invoice_id>/post_invoice/`
- ` /api/orgs/<org_id>/vendors/ `
- ` /api/orgs/<org_id>/purchase-bills/ ` ثم POST `.../<bill_id>/post_bill/`

