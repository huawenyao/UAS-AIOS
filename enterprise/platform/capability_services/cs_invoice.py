"""
cs.invoice — 开票语义能力服务
覆盖：发票申请 / 开票 / 回款登记 / 账期管理
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List
import uuid


@dataclass
class Invoice:
    invoice_id: str
    order_id: str
    customer_id: str
    amount: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    status: str           # draft / submitted / issued / paid / overdue
    invoice_type: str     # vat_special / vat_normal / receipt
    due_date: str
    items: List[Dict]
    payment_records: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class PaymentRecord:
    payment_id: str
    invoice_id: str
    amount: float
    payment_method: str
    payment_date: str
    bank_flow_id: str
    confirmed: bool = False


class InvoiceService:
    """
    cs.invoice 开票与回款语义服务
    支持增值税专票/普票/收据，与财务系统集成
    """

    def __init__(self):
        self._invoices: Dict[str, Invoice] = {}
        self._payments: Dict[str, PaymentRecord] = {}

    def create_invoice_request(
        self,
        order_id: str,
        customer_id: str,
        amount: float,
        invoice_type: str,
        items: List[Dict],
        due_days: int = 30,
    ) -> Invoice:
        """创建开票申请"""
        tax_rate = 0.13 if invoice_type == "vat_special" else 0.06
        tax_amount = round(amount * tax_rate, 2)
        total = round(amount + tax_amount, 2)

        from datetime import timedelta
        due_date = (datetime.now(timezone.utc) + timedelta(days=due_days)).date().isoformat()

        invoice = Invoice(
            invoice_id=str(uuid.uuid4()),
            order_id=order_id,
            customer_id=customer_id,
            amount=amount,
            tax_rate=tax_rate,
            tax_amount=tax_amount,
            total_amount=total,
            status="draft",
            invoice_type=invoice_type,
            due_date=due_date,
            items=items,
        )
        self._invoices[invoice.invoice_id] = invoice
        return invoice

    def submit_invoice(self, invoice_id: str) -> Invoice:
        """提交开票（进入财务审核）"""
        inv = self._get_invoice(invoice_id)
        inv.status = "submitted"
        return inv

    def issue_invoice(self, invoice_id: str, invoice_number: str) -> Invoice:
        """完成开票（财务侧操作）"""
        inv = self._get_invoice(invoice_id)
        inv.status = "issued"
        inv.items[0]["invoice_number"] = invoice_number if inv.items else None
        return inv

    def record_payment(
        self,
        invoice_id: str,
        amount: float,
        method: str,
        bank_flow_id: str,
    ) -> PaymentRecord:
        """登记回款"""
        inv = self._get_invoice(invoice_id)
        payment = PaymentRecord(
            payment_id=str(uuid.uuid4()),
            invoice_id=invoice_id,
            amount=amount,
            payment_method=method,
            payment_date=datetime.now(timezone.utc).isoformat(),
            bank_flow_id=bank_flow_id,
        )
        self._payments[payment.payment_id] = payment
        inv.payment_records.append({"payment_id": payment.payment_id, "amount": amount})

        # 检查是否全款到账
        total_paid = sum(p.get("amount", 0) for p in inv.payment_records)
        if total_paid >= inv.total_amount:
            inv.status = "paid"
        return payment

    def check_overdue(self) -> List[Invoice]:
        """检查逾期发票"""
        today = datetime.now(timezone.utc).date().isoformat()
        overdue = []
        for inv in self._invoices.values():
            if inv.status == "issued" and inv.due_date < today:
                inv.status = "overdue"
                overdue.append(inv)
        return overdue

    def get_ar_summary(self, customer_id: str) -> Dict:
        """获取应收款汇总"""
        customer_invoices = [i for i in self._invoices.values() if i.customer_id == customer_id]
        return {
            "total_invoiced": sum(i.total_amount for i in customer_invoices),
            "total_paid": sum(
                sum(p.get("amount", 0) for p in i.payment_records)
                for i in customer_invoices
            ),
            "overdue_count": sum(1 for i in customer_invoices if i.status == "overdue"),
            "invoices": [i.invoice_id for i in customer_invoices],
        }

    def __call__(self, action: str, payload: Dict, context=None) -> Any:
        handlers = {
            "create": lambda p: vars(self.create_invoice_request(
                p["order_id"], p["customer_id"], p["amount"],
                p.get("invoice_type", "vat_normal"), p.get("items", [])
            )),
            "submit": lambda p: vars(self.submit_invoice(p["invoice_id"])),
            "issue": lambda p: vars(self.issue_invoice(p["invoice_id"], p["invoice_number"])),
            "record_payment": lambda p: vars(self.record_payment(
                p["invoice_id"], p["amount"], p["method"], p["bank_flow_id"]
            )),
            "ar_summary": lambda p: self.get_ar_summary(p["customer_id"]),
            "check_overdue": lambda p: [vars(i) for i in self.check_overdue()],
        }
        handler = handlers.get(action)
        if not handler:
            raise ValueError(f"cs.invoice: 未知 action={action}")
        return handler(payload)

    def _get_invoice(self, invoice_id: str) -> Invoice:
        if invoice_id not in self._invoices:
            raise ValueError(f"发票不存在: {invoice_id}")
        return self._invoices[invoice_id]
