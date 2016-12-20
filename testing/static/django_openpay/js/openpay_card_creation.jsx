var React = require('react');
var jQuery = require('jquery');
var openpay = require('openpay');
var Csrf = require('./tools/csrf');

var OpenPayCardCreate = React.createClass({
  propTypes: {
    merchantID: React.PropTypes.string.isRequired,
    publicKey: React.PropTypes.string.isRequired,
    customerID: React.PropTypes.string.isRequired,
    url: React.PropTypes.string.isRequired,
    sandboxActive: React.PropTypes.bool.isRequired,
  },

  getInitialState: function () {
    return {
      deviceId: null,
      cardSaved: false,
      sending: false,
      validations: {
        number: true,
        cvv: true,
        expiration: true,
      },
      card: {
        holderName: '',
        number: '',
        bank: '',
        month: '01',
        year: new Date().getFullYear().toString().substr(2, 2),
        cvv: '',
      },
      address: {
        line1: '',
        line2: '',
        line3: '',
        city: '',
        state: '',
        countryCode: '',
        postalCode: '',
      },
    };
  },

  componentWillMount: function () {
    openpay.setId(this.props.merchantID);
    openpay.setApiKey(this.props.publicKey);
    openpay.setSandboxMode(this.props.sandboxActive);
    this.setState({ deviceId: openpay.deviceData.setup() });
  },

  componentWillUnmount: function () {
    if (this.serverRequest) {
      this.serverRequest.abort();
    }
  },

  handleCardChange: function (name, event) {
    var card = this.state.card;
    card[name] = event.target.value;
    this.setState({
      card: card,
    });
  },

  handleAddressChange: function (name, event) {
    var address = this.state.address;
    address[name] = event.target.value;
    this.setState({
      address: address,
    });
  },

  clearForm: function () {
    this.setState({
      cardSaved: false,
      validations: {
        number: true,
        cvv: true,
        expiration: true,
      },
      card: {
        holderName: '',
        number: '',
        bank: '',
        month: '01',
        year: new Date().getFullYear().toString().substr(2, 2),
        cvv: '',
      },
      address: {
        line1: '',
        line2: '',
        line3: '',
        city: '',
        state: '',
        countryCode: '',
        postalCode: '',
      }, });
  },

  handleCardBlur: function (name) {
    var validations = this.state.validations;
    var card = this.state.card;
    switch (name){
      case 'number':
        card.bank = openpay.card.cardType(card.number);
        validations.number = openpay.card.validateCardNumber(card.number);
        this.setState({ validations: validations, card: card });
        break;
      case 'cvv':
        validations.cvv = openpay.card.validateCVC(card.cvv);
        this.setState({ validations: validations });
        break;
      case 'month':
      case 'year':
        validations.expiration = openpay.card.validateExpiry(
          card.month, '20' + card.year
        );
        this.setState({ validations: validations });
        break;
    };
  },

  submitRegister: function (event) {
    event.preventDefault();
    var card = this.state.card;
    var address = this.state.address;
    var deviceId = this.state.deviceId;
    this.setState({ sending: true, cardSaved: false });

    openpay.token.create({
        card_number: card.number,
        holder_name: card.holderName,
        expiration_year: card.year,
        expiration_month: card.month,
        cvv2: card.cvv,
        address: {
          line1: address.line1,
          line2: address.line2,
          line3: address.line3,
          city: address.city,
          state: address.state,
          country_code: address.countryCode,
          postal_code: address.postalCode,
        },
      },
      function (response) {
        var csrftoken = Csrf.getCookie('csrftoken');
        this.serverRequest = jQuery.ajax({
          beforeSend: function (xhr, settings) {
            if (!Csrf.csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
          }.bind(this),

          type: 'POST',
          url: this.props.url,
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify({
            token: response.data.id,
            deviceId: deviceId,
            customerId: this.props.customerID,
          }),

          success: function (result) {
            this.setState({ cardSaved: true, });
            alert('Successful');
            console.log('Success');
          }.bind(this),

          error: function (xhr, status, err) {
            console.log('URL: ' + this.props.url + ' / ' + status +
              ' / ' + err.toString());
            this.setState({ cardSaved: false, });
            console.log('Error');
            alert('Error from django');
          }.bind(this),

          complete: function (xhr, status) {
            this.setState({ sending: false, });
            console.log('Completed');
          }.bind(this),
        });
      }.bind(this),

      function (response) {
        var content = 'Estatus del error: ' + response.data.status;
        content += ' |> Error: ' + response.message;
        content += ' |> Descripción: ' + response.data.description;
        content += ' |> ID de la petición: ' + response.data.request_id;
        console.log(content);
        alert('OPENPAY: Incomplete');
        this.setState({ sending: false, });
      }.bind(this)
    );

  },

  render: function () {
    var year = new Date().getFullYear();
    var yearOptions = [];
    for (var i = year; i < year + 10; i++) {
      yearOptions.push(
        <option value={ i.toString().substr(2, 2) } key={ i }>{ i }</option>
      );
    }

    return (
      <div className='openpay payout'>
        <form id='formId' onSubmit={ this.submitRegister }>

          <div className='card-information'>
            <div className='field'>
              <label htmlFor='card_holder_name'>Nombre en la tarjeta</label>
              <input type='text' id='card_holder_name' placeholder='Propietario'
                autoComplete='off' value={ this.state.card.holderName }
                onChange={ this.handleCardChange.bind(this, 'holderName') }
              />
            </div>

            <div className='field'>
              <label htmlFor='card_number'>Número de Tarjeta</label>
              <input type='number' id='card_number'
                placeholder='Número de la tarjeta de debito/credito'
                autoComplete='off' value={ this.state.card.number }
                onChange={ this.handleCardChange.bind(this, 'number') }
                onBlur={ this.handleCardBlur.bind(null, 'number') }
              />
            </div>


            <div className='field'>
              <label htmlFor='card_expiration_month'>Fecha de Expiracion</label>
              <select id='card_expiration_month' value={ this.state.card.month }
                onChange={ this.handleCardChange.bind(this, 'month') }
                onBlur={ this.handleCardBlur.bind(null, 'month') }>
                <option value='01' key={ 1 }>Jan (01)</option>
                <option value='02' key={ 2 }>Feb (02)</option>
                <option value='03' key={ 3 }>Mar (03)</option>
                <option value='04' key={ 4 }>Apr (04)</option>
                <option value='05' key={ 5 }>May (05)</option>
                <option value='06' key={ 6 }>June (06)</option>
                <option value='07' key={ 7 }>July (07)</option>
                <option value='08' key={ 8 }>Aug (08)</option>
                <option value='09' key={ 9 }>Sep (09)</option>
                <option value='10' key={ 10 }>Oct (10)</option>
                <option value='11' key={ 11 }>Nov (11)</option>
                <option value='12' key={ 12 }>Dec (12)</option>
              </select>

              <select id='card_expiration_year' value={ this.state.card.year }
                onChange={ this.handleCardChange.bind(this, 'year') }
                onBlur={ this.handleCardBlur.bind(null, 'year') }>
                { yearOptions }
              </select>
            </div>

            <div className='field'>
              <label htmlFor='card_cvv'>Codigo de Seguridad (CVV)</label>
              <input type='number' id='card_cvv' placeholder='Codigo de Seguridad'
                autoComplete='off' value={ this.state.card.cvv }
                onChange={ this.handleCardChange.bind(this, 'cvv') }
                onBlur={ this.handleCardBlur.bind(null, 'cvv') }
              />
            </div>
          </div>

          <div className='card-address'>
            <div className='field'>
              <label htmlFor='address_line_1'>Línea 1</label>
              <input type='text' id='address_line_1'
                value={ this.state.address.line1 }
                onChange={ this.handleAddressChange.bind(this, 'line1') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_line_2'>Línea 2</label>
              <input type='text' id='address_line_2'
                value={ this.state.address.line2 }
                onChange={ this.handleAddressChange.bind(this, 'line2') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_line_3'>Línea 3</label>
              <input type='text' id='address_line_3'
                value={ this.state.address.line3 }
                onChange={ this.handleAddressChange.bind(this, 'line3') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_city'>Ciudad</label>
              <input type='text' id='address_city' placeholder='Ciudad'
                value={ this.state.address.city }
                onChange={ this.handleAddressChange.bind(this, 'city') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_state'>Estado</label>
              <input type='text' id='address_state' placeholder='Estado'
                value={ this.state.address.state }
                onChange={ this.handleAddressChange.bind(this, 'state') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_country_code'>País</label>
              <input type='text' id='address_country_code' placeholder='Código del País'
                value={ this.state.address.countryCode }
                onChange={ this.handleAddressChange.bind(this, 'countryCode') }
              />
            </div>

            <div className='field'>
              <label htmlFor='address_postal_code'>Código Postal</label>
              <input type='text' id='address_postal_code' placeholder='Código Postal'
                value={ this.state.address.postalCode }
                onChange={ this.handleAddressChange.bind(this, 'postalCode') }
              />
            </div>
          </div>

          <div className='buttons'>
            <button type='submit' className='register'
              disabled={ this.state.sending }>Registrar</button>
            <button type='button' className='cancel'
              onClick={ this.clearForm }>Cancelar</button>
          </div>
        </form>
      </div>
    );
  },
});

module.exports = OpenPayCardCreate;
