class ERPConnector:
    def get_balance(self, name):
        # هنا سيتم الربط مستقبلاً بـ API العميل الحقيقي
        # حالياً سنعيد بيانات تجريبية (Mock Data) لإبهار العميل بالمنطق
        db_mock = {"فادي": 1500.50, "محمد": 2300.00, "أحمد": 450.00}
        balance = db_mock.get(name, 0.0)
        return {"status": "success", "balance": balance, "currency": "SAR"}
