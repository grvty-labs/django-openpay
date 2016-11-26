Webhook Endpoint Log
====================

This log was manually created using [RequestBin](https://requestb.in) and a
fake Openpay's Sandbox project. At the end of the testing, we will change all
the codes and delete that Sandbox project to prevent the reuse of the same.

All the webhook notifications arrive to the same URL (which needs to be
previously configured in the Openpay dashboard and verified in the same
place)

---
**Authentication of webhook endpoint**

```javascript
var body = {
  type: "verification",
  event_date: "2016-11-25T14:45:09-06:00",
  verification_code: "3vWQ1x6I",
  id: "w7evenqvf4a3crkdmkj6"
};
```
---
**Charges Refunded**

```javascript
var body = {
  type: "charge.refunded",
  event_date: "2016-11-25T19:19:49-06:00",
  transaction: {
    id: "try8qtuwamop489aiej8",
    authorization: "801585",
    method: "card",
    operation_type: "in",
    transaction_type: "charge",
    card: {
      id: "kl2ckjj7qyldd45icjtm",
      type: "debit",
      brand: "visa",
      address: {
        line1: "Av. Circ",
        line2: "",
        line3: "",
        state: "Q",
        city: "Q",
        postal_code: "76269",
        country_code: "MX"
      },
      card_number: "411111XXXXXX1111",
      holder_name: "D1",
      expiration_year: "25",
      expiration_month: "01",
      allows_charges: false,
      allows_payouts: true,
      creation_date: "2016-11-25T16:40:24-06:00",
      bank_name: "Banamex",
      customer_id: "ab9eovztudbzfvv5kuwe",
      bank_code: "002"
    },
    status: "completed",
    refund: {
      id: "trv2jntw5iq49o4jz9ny",
      authorization: "801585",
      method: "card",
      operation_type: "out",
      transaction_type: "refund",
      status: "completed",
      conciliated: false,
      creation_date: "2016-11-25T19:19:49-06:00",
      operation_date: "2016-11-25T19:19:49-06:00",
      description: null,
      error_message: null,
      order_id: null,
      customer_id: "ab9eovztudbzfvv5kuwe",
      amount: 10.00,
      currency: "MXN"
    },
    conciliated: false,
    creation_date: "2016-11-25T18:10:58-06:00",
    operation_date: "2016-11-25T18:10:58-06:00",
    description: "P2",
    error_message: null,
    order_id: null,
    customer_id: "ab9eovztudbzfvv5kuwe",
    amount: 10.00,
    currency: "MXN",
    fee: {
      amount: 2.7900,
      tax: 0.4464
    }
  }
};
```
---
**Charges Failed**

```javascript
//Not tested yet
var body = null;
```
---
**Charges Cancelled**

```javascript
var body = {
  type: "charge.cancelled",
  event_date: "2016-11-25T17:49:22-06:00",
  transaction: {
    id: "trjutinilzagantdyfpp",
    authorization: "801585",
    method: "card",
    operation_type: "in",
    transaction_type: "charge",
    card: {
      id: "kl2ckjj7qyldd45icjtm",
      type: "debit",
      brand: "visa",
      address: {
        line1: "Av. Circ",
        line2: "",
        line3: "",
        state: "Q",
        city: "Q",
        postal_code: "76269",
        country_code: "MX"
      },
      card_number: "411111XXXXXX1111",
      holder_name: "D1",
      expiration_year: "25",
      expiration_month: "01",
      allows_charges: false,
      allows_payouts: true,
      creation_date: "2016-11-25T16:40:24-06:00",
      bank_name: "Banamex",
      customer_id: "ab9eovztudbzfvv5kuwe",
      bank_code: "002"
    },
    status: "cancelled",
    conciliated: true,
    creation_date: "2016-11-25T16:57:49-06:00",
    operation_date: "2016-11-25T17:49:22-06:00",
    description: "P1",
    error_message: null,
    order_id: null,
    customer_id: "ab9eovztudbzfvv5kuwe",
    amount: 10.00,
    currency: "MXN"
  }
};
```
---
**Charges Created**

```javascript
var body = {
  type: "charge.created",
  event_date: "2016-11-25T16:58:19-06:00",
  transaction: {
    id: "tranj1s90igqweify1li",
    authorization: "801585",
    method: "card",
    operation_type: "in",
    transaction_type: "charge",
    card:{
      id: "kl2ckjj7qyldd45icjtm",
      type: "debit",
      brand: "visa",
      address: {
        line1: "Av. Circ",
        line2: "",
        line3: "",
        state: "Q",
        city: "Q",
        postal_code: "76269",
        country_code: "MX"
      },
      card_number: "411111XXXXXX1111",
      holder_name: "D1",
      expiration_year: "25",
      expiration_month: "01",
      allows_charges: false,
      allows_payouts: true,
      creation_date: "2016-11-25T16:40:24-06:00",
      bank_name: "Banamex",
      customer_id: "ab9eovztudbzfvv5kuwe",
      bank_code: "002"
    },
    status: "in_progress",
    conciliated: false,
    creation_date: "2016-11-25T16:58:18-06:00",
    operation_date: "2016-11-25T16:58:18-06:00",
    description: "P1",
    error_message: null,
    order_id: null,
    customer_id: "ab9eovztudbzfvv5kuwe",
    amount: 10.00,
    currency: "MXN"
  }
}
```
---
**Charges Succeeded (Capture after creation)**

```javascript
var body = {
  type: "charge.succeeded",
  event_date: "2016-11-25T18:25:05-06:00",
  transaction: {
    id: "tranj1s90igqweify1li",
    authorization: "801585",
    method: "card",
    operation_type: "in",
    transaction_type: "charge",
    card: {
      id: "kl2ckjj7qyldd45icjtm",
      type: "debit",
      brand: "visa",
      address: {
        line1: "Av. Circ",
        line2: "",
        line3: "",
        state: "Q",
        city: "Q",
        postal_code: "76269",
        country_code: "MX"
      },
      card_number: "411111XXXXXX1111",
      holder_name: "D1",
      expiration_year: "25",
      expiration_month: "01",
      allows_charges: false,
      allows_payouts: true,
      creation_date: "2016-11-25T16:40:24-06:00",
      bank_name: "Banamex",
      customer_id: "ab9eovztudbzfvv5kuwe",
      bank_code: "002"
    },
    status: "completed",
    conciliated: false,
    creation_date: "2016-11-25T16:58:18-06:00",
    operation_date: "2016-11-25T18:25:05-06:00",
    description: "P1",
    error_message: null,
    order_id: null,
    customer_id: "ab9eovztudbzfvv5kuwe",
    amount: 10.00,
    currency: "MXN",
    fee: {
        amount: 2.79,
        tax: 0.4464
    }
  }
};
```
---
**Charges Succeeded (Create with capture ON)**

```javascript
//Not tested yet
var url = null;
var body = {
  type: "charge.succeeded",
  event_date: "2016-11-25T18:10:59-06:00",
  transaction: {
    id: "try8qtuwamop489aiej8",
    authorization: "801585",
    method: "card",
    operation_type: "in",
    transaction_type: "charge",
    card: {
      id: "kl2ckjj7qyldd45icjtm",
      type: "debit",
      brand: "visa",
      address: {
        line1: "Av. Circ",
        line2: "",
        line3: "",
        state: "Q",
        city: "Q",
        postal_code: "76269",
        country_code: "MX"
      },
      card_number: "411111XXXXXX1111",
      holder_name: "D1",
      expiration_year: "25",
      expiration_month: "01",
      allows_charges: false,
      allows_payouts: true,
      creation_date: "2016-11-25T16:40:24-06:00",
      bank_name: "Banamex",
      customer_id: "ab9eovztudbzfvv5kuwe",
      bank_code: "002"
    },
    status: "completed",
    conciliated: false,
    creation_date: "2016-11-25T18:10:58-06:00",
    operation_date: "2016-11-25T18:10:58-06:00",
    description: "P2",
    error_message: null,
    order_id: null,
    customer_id: "ab9eovztudbzfvv5kuwe",
    amount: 10.00,
    currency: "MXN",
    fee:{
      amount: 2.79,
      tax: 0.4464
    }
  }
};
```
---
**Charges to subscriptions failed**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Payouts Created**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Payouts Completed**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Payouts Failed**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Transference Completed**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Fees Completed**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**SPEI Received**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Countercharge Created**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Countercharge Rejected**

```javascript
//Not tested yet
var url = null;
var body = null;
```
---
**Countercharge Accepted**

```javascript
//Not tested yet
var url = null;
var body = null;
```
