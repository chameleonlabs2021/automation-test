const { Autofiller } = require('../lib/components/Autofiller.js');

function getDataAutofill(data) {
    console.log(`Autofill plugin - ${data?.policyLocator}`);
    console.log(JSON.stringify(data));
    
    const response = (new Autofiller(data)).getDataAutofill();
    console.log('Autofill Response: ', JSON.stringify(response));
    return response;
}

module.exports = {
    getDataAutofill
}