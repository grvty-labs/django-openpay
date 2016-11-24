var React = require('react');
var ReactDOM = require('react-dom');
var OpenPayCardCreate = require('./js/openpay_card_creation');

ReactDOM.render(
  <OpenPayCardCreate
    merchantID={ CONST_OPENPAY_MERCHANT_ID }
    publicKey={ CONST_OPENPAY_PUBLIC_API_KEY }
    customerID={ CONST_OPENPAY_CUSTOMER_ID }
    sandboxActive={ CONST_OPENPAY_SANDBOX }
    />,
  document.getElementById('test_me')
);

//
