"""Module for interacting with FreeAgent invoice data."""
from freeagent_api.base_object import BaseObject
from freeagent_api.invoice_item import InvoiceItem


class Invoice(BaseObject):
    """Representation of an invoice.

    See https://dev.freeagent.com/docs/invoices
    """

    API_FIELDS = [
        "url",
        "status",
        "long_status",
        "contact:id",
        "project:id",
        "property",
        "include_timeslips",
        "include_expenses",
        "include_estimates",
        "reference",
        "dated_on:date",
        "due_on:date",
        "payment_terms_in_days:integer",
        "currency",
        "cis_rate",
        "cis_deduction_rate:decimal",
        "cis_deduction:decimal",
        "cis_deduction_suffered:decimal",
        "comments",
        "send_new_invoice_emails:boolean",
        "send_reminder_emails:boolean",
        "send_thank_you_emails:boolean",
        "discount_percent:decimal",
        "client_contact_name",
        "payment_terms",
        "po_reference",
        "bank_account:id",
        "omit_header:boolean",
        "show_project_name:boolean",
        "always_show_bic_and_iban:boolean",
        "ec_status",
        "place_of_supply",
        "net_value:decimal",
        "exchange_rate:decimal",
        "involves_sales_tax:boolean",
        "sales_tax_value:decimal",
        "second_sales_tax_value:decimal",
        "total_value:decimal",
        "paid_value:decimal",
        "due_value:decimal",
        "is_interim_uk_vat:boolean",
        "paid_on:datetime",
        "written_off_date:date",
        "recurring_invoice",
        "payment_url",
        "payment_methods",
        "invoice_items", # Overridden
        "created_at:datetime",
        "updated_at:datetime",
    ]


    def as_dict(self) -> dict:
        """Overridden version of the base object's as_dict method.

        Generates a dictionary representation of the API object, also including
        any methods that can be called without requiring parameters.

        Returns:
            dict: Contents of object.
        """
        obj = super().as_dict()
        obj['invoice_items'] = []
        for item in self.invoice_items:
            obj['invoice_items'].append(item.as_dict())
        return obj


    @property
    def invoice_items(self) -> list[InvoiceItem]:
        """Get the items on this invoice as InvoiceItem objects.

        Parses the data returned by the API into objects.

        Returns:
            list: items on invoice
        """
        items = []
        for item_data in self._data['invoice_items']:
            items.append(InvoiceItem(item_data))
        return items
