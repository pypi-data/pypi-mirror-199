use pyo3::{prelude::*};
use pyo3::types::{PyDict, PyBytes};

mod pdf_builder;
use pdf_builder::create_payment_report;


#[pyclass]
pub struct PaymentOrder {
    #[pyo3(get, set)]
    creation_date: String,
    #[pyo3(get, set)]
    last_transaction_date: String,
    #[pyo3(get, set)]
    document_date: String,
    #[pyo3(get, set)]
    document_number: String,
    #[pyo3(get, set)]
    priority: String,
    #[pyo3(get, set)]
    transaction_type_code: String,
    #[pyo3(get, set)]
    purpose: String,

    #[pyo3(get, set)]
    payer_kpp: String,
    #[pyo3(get, set)]
    payer_inn: String,
    #[pyo3(get, set)]
    payer_name: String,
    #[pyo3(get, set)]
    payer_bank: String,
    #[pyo3(get, set)]
    payer_bank_address: String,

    #[pyo3(get, set)]
    side_recipient_inn: String,
    #[pyo3(get, set)]
    side_recipient_bank: String,
    #[pyo3(get, set)]
    side_recipient_bank_address: String,
    #[pyo3(get, set)]
    side_recipient_name: String,
    #[pyo3(get, set)]
    side_recipient_kpp: Option<String>,

    #[pyo3(get, set)]
    transaction_sum: String,
    #[pyo3(get, set)]
    payer_account: String,
    #[pyo3(get, set)]
    payer_bank_code: String,
    #[pyo3(get, set)]
    payer_cr_account: String,

    #[pyo3(get, set)]
    side_recipient_bank_code: String,
    #[pyo3(get, set)]
    side_recipient_account: String,
    #[pyo3(get, set)]
    side_recipient_cr_account: String,
    finance_administrator_name: String,
}


#[pymethods]
impl PaymentOrder {
    #[new] 
    #[pyo3(signature = (
        creation_date,
        last_transaction_date,
        document_date,
        document_number,
        priority,
        transaction_type_code,
        purpose,
        payer_kpp,
        payer_inn,
        payer_name,
        payer_bank,
        payer_bank_address,
        side_recipient_inn,
        side_recipient_bank,
        side_recipient_bank_address,
        side_recipient_name,
        side_recipient_kpp,
        transaction_sum,
        payer_account,
        payer_bank_code,
        payer_cr_account,
        side_recipient_bank_code,
        side_recipient_account,
        side_recipient_cr_account,
        finance_administrator_name,
    ))]
    fn new(
        creation_date: String,
        last_transaction_date: String,
        document_date: String,
        document_number: String,
        priority: String,
        transaction_type_code: String,
        purpose: String,

        payer_kpp: String,
        payer_inn: String,
        payer_name: String,
        payer_bank: String,
        payer_bank_address: String,

        side_recipient_inn: String,
        side_recipient_bank: String,
        side_recipient_bank_address: String,
        side_recipient_name: String,
        side_recipient_kpp: Option<String>,

        transaction_sum: String,
        payer_account: String,
        payer_bank_code: String,
        payer_cr_account: String,

        side_recipient_bank_code: String,
        side_recipient_account: String,
        side_recipient_cr_account: String,
        finance_administrator_name: String,
    ) -> Self {
        PaymentOrder {
            creation_date,
            last_transaction_date,
            document_date,
            document_number,
            priority,
            transaction_type_code,
            purpose,
            payer_kpp,
            payer_inn,
            payer_name,
            payer_bank,
            payer_bank_address,

            side_recipient_inn,
            side_recipient_bank,
            side_recipient_bank_address,
            side_recipient_name,
            side_recipient_kpp,

            transaction_sum,
            payer_account,
            payer_bank_code,
            payer_cr_account,

            side_recipient_bank_code,
            side_recipient_account,
            side_recipient_cr_account,
            finance_administrator_name,
        }
    }
}


impl PaymentOrder {
    fn reform_payment_ending(&mut self) {
        /*  Если число без остатка, то нужно возращать его  виде "12=",
            Если с остатком, то в виде "12-11"
        */
        let payment_integer = match self.transaction_sum.parse::<f64>() {
            Ok(payment) if payment == payment.trunc() || self.transaction_sum.ends_with(".00") => {
                format!("{}=", payment as i64)
            },
            Ok(payment) => {
                let payment_integer_part = payment.trunc() as i64;
                let payment_decimal_part = (payment.fract() * 100.0) as i64;
                format!("{}-{:02}", payment_integer_part, payment_decimal_part)
            },
            Err(_) => self.transaction_sum.clone(),
        };
        self.transaction_sum = payment_integer;
    }
}


/// Функция ожидает словарь следующего вида:
/// Если КПП получателя отсутствует, просто передавайте None
/// 
/// 
/// from payment_order_renderer import create_pdf
/// 
/// 
/// payment_order_dict = {
///     'creation_date': '2021-07-21T00:00:00+05:00',
///     'last_transaction_date': '2021-07-21',
///     'document_date': '2021-07-21',
///     'document_number': '6000',
///     'priority': '5',
///     'transaction_type_code': '01',
///     'purpose': 'Оплата по договору (номер/дата) без НДС',
///     'payer_kpp': '773601001',
///     'payer_inn': '280267860010',
///     'payer_name': 'ООО "Рога и копыта"',
///     'payer_bank': 'БАНК ПЛАТЕЛЬЩИК',
///     'payer_bank_address': 'г. Москва',
///     'side_recipient_inn': '7839443197',
///     'side_recipient_bank': 'ПАО Сбербанк',
///     'side_recipient_bank_address': 'г. Екатернибург',
///     'side_recipient_name': 'Дядя Толик',
///     'side_recipient_kpp': None,
///     'transaction_sum': '1488.23',
///     'payer_account': '40702810401500014770',
///     'payer_bank_code': '044525989',
///     'payer_cr_account': '30101810845250000999',
///     'side_recipient_bank_code': '044525598',
///     'side_recipient_account': '42306810963160914857',
///     'side_recipient_cr_account': '30101810845250000999',
///     'finance_administrator_name': 'А.В. Прокопчук',
/// }

/// Путь до вашего png изображения печати
/// path = "../pythonProject/pics/stamp_with_signature-1.png"

/// Результат возвращается в байтах
/// result = create_pdf(payment_order_dict, path)
#[pyfunction]
fn create_pdf(py: Python, payment_order_dict: &PyDict, path: &str) -> PyResult<Py<PyBytes>> {
    let mut payment_order = PaymentOrder {
        creation_date: payment_order_dict.get_item("creation_date").unwrap().extract().unwrap(),
        last_transaction_date: payment_order_dict.get_item("last_transaction_date").unwrap().extract().unwrap(),
        document_date: payment_order_dict.get_item("document_date").unwrap().extract().unwrap(),
        document_number: payment_order_dict.get_item("document_number").unwrap().extract().unwrap(),
        priority: payment_order_dict.get_item("priority").unwrap().extract().unwrap(),
        transaction_type_code: payment_order_dict.get_item("transaction_type_code").unwrap().extract().unwrap(),
        purpose: payment_order_dict.get_item("purpose").unwrap().extract().unwrap(),
        payer_kpp: payment_order_dict.get_item("payer_kpp").unwrap().extract().unwrap(),
        payer_inn: payment_order_dict.get_item("payer_inn").unwrap().extract().unwrap(),
        payer_name: payment_order_dict.get_item("payer_name").unwrap().extract().unwrap(),
        payer_bank: payment_order_dict.get_item("payer_bank").unwrap().extract().unwrap(),
        payer_bank_address: payment_order_dict.get_item("payer_bank_address").unwrap().extract().unwrap(),
        side_recipient_inn: payment_order_dict.get_item("side_recipient_inn").unwrap().extract().unwrap(),
        side_recipient_bank: payment_order_dict.get_item("side_recipient_bank").unwrap().extract().unwrap(),
        side_recipient_bank_address: payment_order_dict.get_item("side_recipient_bank_address").unwrap().extract().unwrap(),
        side_recipient_name: payment_order_dict.get_item("side_recipient_name").unwrap().extract().unwrap(),
        side_recipient_kpp: payment_order_dict.get_item("side_recipient_kpp").unwrap().extract().unwrap(),
        transaction_sum: payment_order_dict.get_item("transaction_sum").unwrap().extract().unwrap(),
        payer_account: payment_order_dict.get_item("payer_account").unwrap().extract().unwrap(),
        payer_bank_code: payment_order_dict.get_item("payer_bank_code").unwrap().extract().unwrap(),
        payer_cr_account: payment_order_dict.get_item("payer_cr_account").unwrap().extract().unwrap(),
        side_recipient_bank_code: payment_order_dict.get_item("side_recipient_bank_code").unwrap().extract().unwrap(),
        side_recipient_account: payment_order_dict.get_item("side_recipient_account").unwrap().extract().unwrap(),
        side_recipient_cr_account: payment_order_dict.get_item("side_recipient_cr_account").unwrap().extract().unwrap(),
        finance_administrator_name: payment_order_dict.get_item("finance_administrator_name").unwrap().extract().unwrap(),
    };

    payment_order.reform_payment_ending();

    let bytes = create_payment_report(&payment_order, path);
    let py_bytes = PyBytes::new(py, &bytes.unwrap());

    Ok(py_bytes.into())
}


/// A Python module implemented in Rust.
#[pymodule]
fn payment_order_renderer(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PaymentOrder>()?;
    m.add_function(wrap_pyfunction!(create_pdf, m)?)?;
    Ok(())
}
