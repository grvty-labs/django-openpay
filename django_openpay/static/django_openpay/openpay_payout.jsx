var React = require('react');

//Forma de pago
var FormOpenPay = React.createClass({

  render: function () {
    return (
      <div className='page'>
        <div className='container'>
          <form action='#' method='POST' id='payment-form' className='form-horizontal' role='form'>
            <input type='hidden' name='token_id' id='token_id'></input>
            <fieldset>

              <legend>Forma de Pago</legend>

              <div className='form-group'>
                <label className='name-label' htmlFor='card-holder-name'
                  >Nombre en la tarjeta</label>
                <input className='form-control' name='card-holder-name' type='text'
                  id='card-holder-name' placeholder='Propietario' data-openpay-card='holder_name'
                  autoComplete='off'
                />
              </div>

              <div className='form-group'>
                <label className='number-label' htmlFor='card-number'>Número de Tarjeta</label>
                <input className='form-control' type='text' name='card-number'
                  id='card-number' placeholder='Número de la tarjeta de debito/credito'
                  data-openpay-card='card_number'
                  autoComplete='off'
                />
              </div>


              <div className='form-group'>
                <label className='date-label' htmlFor='expiry-month'>Fecha de Expiracion</label>
                <select
                  className='form-control col-sm-2'
                  name='expiry-month'
                  id='expiry-month'
                  data-openpay-card='expiration_month'
                >
                  <option value='01'>Jan (01)</option>
                  <option value='02'>Feb (02)</option>
                  <option value='03'>Mar (03)</option>
                  <option value='04'>Apr (04)</option>
                  <option value='05'>May (05)</option>
                  <option value='06'>June (06)</option>
                  <option value='07'>July (07)</option>
                  <option value='08'>Aug (08)</option>
                  <option value='09'>Sep (09)</option>
                  <option value='10'>Oct (10)</option>
                  <option value='11'>Nov (11)</option>
                  <option value='12'>Dec (12)</option>
                </select>
                <select
                  className='form-control'
                  name='expiry-year'
                  data-openpay-card='expiration_year'
                >
                  <option value='13'>2013</option>
                  <option value='14'>2014</option>
                  <option value='15'>2015</option>
                  <option value='16'>2016</option>
                  <option value='17'>2017</option>
                  <option value='18'>2018</option>
                  <option value='19'>2019</option>
                  <option value='20'>2020</option>
                  <option value='21'>2021</option>
                  <option value='22'>2022</option>
                  <option value='23'>2023</option>
                </select>
              </div>

              <div className='form-group'>
                <label className='col-sm-3 cvv-label' htmlFor='cvv'
                  >Codigo de Seguridad (CVV)</label>
                <input
                  type='text'
                  className='form-control'
                  name='cvv' id='cvv'
                  placeholder='Codigo de Seguridad'
                  data-openpay-card='cvv2'>
                </input>

              </div>


              <div className='form-group'>
                <div className='row'>
                  <button id='pay-button' type='button' className='btn btn-success'>Pagar</button>
                  <button type='button' className='btn btn-danger'>Cancelar</button>
                </div>
              </div>

            </fieldset>
          </form>
        </div>
      </div>
    );
  },
});
